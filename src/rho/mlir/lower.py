"""Rho dialect -> upstream MLIR conversion pass.

Converts rho ops to func/llvm dialect ops with calls to a C runtime.

Design:
- !rho.stack -> !llvm.ptr (opaque runtime stack+env object)
- The runtime stack carries an environment pointer internally.
- rho.const (int N) -> tag as immediate ((N << 1) | 1), then rho_push(stk, val)
- rho.prim -> call @rho_prim_{name}(stk)
- rho.fn -> extract body to func.func @rho_fn_N(stk, env) -> stk,
            then rho_make_closure(fn_ptr, stk) -> val, rho_push(stk, val)
            The closure captures the current env (embedded in stk).
- rho.def {name} -> rho_def(stk, name_hash) pops top and binds in env
- rho.load {name} -> rho_load(stk, name_hash) walks env chain, pushes
- rho.eval {name} -> rho_eval(stk, name_hash) load + auto-call if closure
- One generic rho_push for all value types.

Environment model:
- Each stack object has a current env pointer.
- Env is a linked list: { parent: *env, bindings: [...] }
- rho_def binds in the current env.
- rho_load walks the parent chain.
- On function entry, a child env is created from the closure's captured env.
"""

from functools import partial
import hashlib

from mlir.ir import (
    Block,
    FunctionType,
    InsertionPoint,
    IntegerAttr,
    IntegerType,
    Location,
    StringAttr,
    UnitAttr,
)
from mlir.rewrite import (
    RewritePatternSet,
    TypeConverter,
    ConversionTarget,
    ConversionConfig,
    apply_partial_conversion,
)
from mlir.dialects import llvm, func

from rho.mlir.dialect import (
    RhoDialect,
    StackType,
    InitStackOp,
    ConstOp,
    PrimOp,
    DropOp,
    DefOp,
    LoadOp,
    EvalOp,
    FnOp,
    FnDefOp,
    FnRefOp,
    YieldOp,
    MainOp,
)


PRIM_RUNTIME_NAMES = {
    "+": "rho_prim_add",
    "-": "rho_prim_sub",
    "*": "rho_prim_mul",
    "/": "rho_prim_div",
    ">": "rho_prim_gt",
    "<": "rho_prim_lt",
    "==": "rho_prim_eq",
    "!=": "rho_prim_ne",
    ">=": "rho_prim_ge",
    "<=": "rho_prim_le",
}

_fn_counter = 0


def _name_hash(name: str) -> int:
    """Deterministic i64 hash of a name for runtime env lookup."""
    h = int(hashlib.sha256(name.encode()).hexdigest()[:16], 16)
    return h & 0x7FFFFFFFFFFFFFFF


def _attr_string(attr) -> str:
    return str(attr).strip('"')


def _tagged_i64_constant(val_attr, i64):
    raw_int = val_attr.value
    tagged_int = (raw_int << 1) | 1
    return llvm.mlir_constant(IntegerAttr.get(i64, tagged_int))


def _lower_rho_block_to_func(old_block: Block, new_block: Block, ptr, i64):
    """Manually lower rho ops inside an outlined rho.fn_def body to func/llvm ops.

    This bypasses apply_partial_conversion for function bodies because the
    conversion framework does not recurse into newly-created func.func bodies.
    """
    value_map = {}
    # old block arg0 (!rho.stack) -> new block arg0 (!llvm.ptr)
    if len(old_block.arguments) >= 1:
        value_map[old_block.arguments[0]] = new_block.arguments[0]

    with InsertionPoint(new_block):
        for old_op in list(old_block.operations):
            name = old_op.name
            if name == "rho.const":
                stk = value_map[old_op.operands[0]]
                val_attr = old_op.attributes["value"]
                if isinstance(val_attr, IntegerAttr):
                    tagged = _tagged_i64_constant(val_attr, i64)
                else:
                    tagged = llvm.mlir_constant(IntegerAttr.get(i64, 0))
                result = func.CallOp([ptr], "rho_push", [stk, tagged]).result
                value_map[old_op.results[0]] = result
            elif name == "rho.prim":
                stk = value_map[old_op.operands[0]]
                op_name = _attr_string(old_op.attributes["op"])
                runtime_fn = PRIM_RUNTIME_NAMES.get(op_name, f"rho_prim_{op_name}")
                result = func.CallOp([ptr], runtime_fn, [stk]).result
                value_map[old_op.results[0]] = result
            elif name == "rho.drop":
                stk = value_map[old_op.operands[0]]
                result = func.CallOp([ptr], "rho_drop", [stk]).result
                value_map[old_op.results[0]] = result
            elif name == "rho.def":
                stk = value_map[old_op.operands[0]]
                name_h = llvm.mlir_constant(
                    IntegerAttr.get(i64, _name_hash(_attr_string(old_op.attributes["name"])))
                )
                result = func.CallOp([ptr], "rho_def", [stk, name_h]).result
                value_map[old_op.results[0]] = result
            elif name == "rho.load":
                stk = value_map[old_op.operands[0]]
                name_h = llvm.mlir_constant(
                    IntegerAttr.get(i64, _name_hash(_attr_string(old_op.attributes["name"])))
                )
                result = func.CallOp([ptr], "rho_load", [stk, name_h]).result
                value_map[old_op.results[0]] = result
            elif name == "rho.eval":
                stk = value_map[old_op.operands[0]]
                name_h = llvm.mlir_constant(
                    IntegerAttr.get(i64, _name_hash(_attr_string(old_op.attributes["name"])))
                )
                result = func.CallOp([ptr], "rho_eval", [stk, name_h]).result
                value_map[old_op.results[0]] = result
            elif name == "rho.fn_ref":
                stk = value_map[old_op.operands[0]]
                fn_name = _attr_string(old_op.attributes["sym_name"])
                fn_ptr = func.CallOp([ptr], f"rho_get_fn_ptr_{fn_name}", []).result
                closure_val = func.CallOp([i64], "rho_make_closure", [fn_ptr, stk]).result
                result = func.CallOp([ptr], "rho_push", [stk, closure_val]).result
                value_map[old_op.results[0]] = result
            elif name == "rho.yield":
                stk = value_map[old_op.operands[0]]
                func.ReturnOp([stk])
            else:
                raise RuntimeError(f"manual fn lowering does not yet handle op {name}")


def convert_rho_to_runtime(op, pass_):
    """PassManager-compatible pass that converts rho ops to runtime calls."""
    global _fn_counter
    ptr = llvm.PointerType.get()
    i64 = IntegerType.get_signless(64)

    type_converter = TypeConverter()

    def convert_stack(t):
        return ptr if isinstance(t, StackType) else None

    type_converter.add_conversion(convert_stack)

    patterns = RewritePatternSet()

    def convert_init_stack(op, adaptor, converter, rewriter):
        with rewriter.ip:
            result = func.CallOp([ptr], "rho_init_stack", [])
        rewriter.replace_op(op, result)

    def convert_const(op, adaptor, converter, rewriter):
        with rewriter.ip:
            val_attr = op.attributes["value"]
            if isinstance(val_attr, IntegerAttr):
                raw_int = val_attr.value
                tagged_int = (raw_int << 1) | 1
                tagged = llvm.mlir_constant(IntegerAttr.get(i64, tagged_int))
            else:
                tagged = llvm.mlir_constant(IntegerAttr.get(i64, 0))
            result = func.CallOp([ptr], "rho_push", [adaptor.stk, tagged])
        rewriter.replace_op(op, result)

    def convert_prim(op, adaptor, converter, rewriter):
        with rewriter.ip:
            op_name = str(op.attributes["op"]).strip('"')
            runtime_fn = PRIM_RUNTIME_NAMES.get(op_name, f"rho_prim_{op_name}")
            result = func.CallOp([ptr], runtime_fn, [adaptor.stk])
        rewriter.replace_op(op, result)

    def convert_drop(op, adaptor, converter, rewriter):
        with rewriter.ip:
            result = func.CallOp([ptr], "rho_drop", [adaptor.stk])
        rewriter.replace_op(op, result)

    def convert_def(op, adaptor, converter, rewriter):
        with rewriter.ip:
            name_str = str(op.attributes["name"]).strip('"')
            name_h = llvm.mlir_constant(IntegerAttr.get(i64, _name_hash(name_str)))
            result = func.CallOp([ptr], "rho_def", [adaptor.stk, name_h])
        rewriter.replace_op(op, result)

    def convert_load(op, adaptor, converter, rewriter):
        with rewriter.ip:
            name_str = str(op.attributes["name"]).strip('"')
            name_h = llvm.mlir_constant(IntegerAttr.get(i64, _name_hash(name_str)))
            result = func.CallOp([ptr], "rho_load", [adaptor.stk, name_h])
        rewriter.replace_op(op, result)

    def convert_eval(op, adaptor, converter, rewriter):
        with rewriter.ip:
            name_str = str(op.attributes["name"]).strip('"')
            name_h = llvm.mlir_constant(IntegerAttr.get(i64, _name_hash(name_str)))
            result = func.CallOp([ptr], "rho_eval", [adaptor.stk, name_h])
        rewriter.replace_op(op, result)

    def convert_fn_def(op, adaptor, converter, rewriter):
        rewriter.replace_op(op, [])

    def convert_fn_ref(op, adaptor, converter, rewriter):
        fn_name = str(op.attributes["sym_name"]).strip('"')
        with rewriter.ip:
            fn_ptr = llvm.mlir_zero(ptr)
            closure_val = func.CallOp([i64], "rho_make_closure", [fn_ptr, adaptor.stk])
            result = func.CallOp([ptr], "rho_push", [adaptor.stk, closure_val.result])
        rewriter.replace_op(op, result)

    def convert_fn(op, adaptor, converter, rewriter):
        with rewriter.ip:
            fn_ptr = llvm.mlir_zero(ptr)
            closure_val = func.CallOp([i64], "rho_make_closure", [fn_ptr, adaptor.stk])
            result = func.CallOp([ptr], "rho_push", [adaptor.stk, closure_val.result])
        rewriter.replace_op(op, result)

    def convert_yield(op, adaptor, converter, rewriter):
        with rewriter.ip:
            ret = func.ReturnOp([adaptor.stk])
        rewriter.replace_op(op, ret)

    def convert_main(op, adaptor, converter, rewriter):
        with rewriter.ip:
            fn = func.FuncOp("rho_main", FunctionType.get([], [ptr]))
            fn.attributes["llvm.emit_c_interface"] = UnitAttr.get()
            op.body.blocks[0].append_to(fn.body)
            rewriter.convert_region_types(fn.body, converter)
        rewriter.replace_op(op, fn)

    patterns.add_conversion(InitStackOp, convert_init_stack, type_converter)
    patterns.add_conversion(ConstOp, convert_const, type_converter)
    patterns.add_conversion(PrimOp, convert_prim, type_converter)
    patterns.add_conversion(DropOp, convert_drop, type_converter)
    patterns.add_conversion(DefOp, convert_def, type_converter)
    patterns.add_conversion(LoadOp, convert_load, type_converter)
    patterns.add_conversion(EvalOp, convert_eval, type_converter)
    patterns.add_conversion(FnDefOp, convert_fn_def, type_converter)
    patterns.add_conversion(FnRefOp, convert_fn_ref, type_converter)
    patterns.add_conversion(FnOp, convert_fn, type_converter)
    patterns.add_conversion(YieldOp, convert_yield, type_converter)
    patterns.add_conversion(MainOp, convert_main, type_converter)

    target = ConversionTarget()
    target.add_illegal_dialect(RhoDialect)

    config = ConversionConfig()
    config.build_materializations = False

    fn_defs = []
    for child in list(op.regions[0].blocks[0]):
        if child.name == "rho.fn_def":
            fn_name = str(child.attributes["sym_name"]).strip('"')
            fn_defs.append((fn_name, child))

    for fn_name, fn_def_op in fn_defs:
        fn_type = FunctionType.get([ptr, ptr], [ptr])
        with InsertionPoint(fn_def_op):
            fn_op = func.FuncOp(fn_name, fn_type, visibility="private")
        fn_op.body.blocks.append()
        blk = fn_op.body.blocks[0]
        blk.add_argument(ptr, Location.unknown())
        blk.add_argument(ptr, Location.unknown())
        old_block = fn_def_op.regions[0].blocks[0]
        _lower_rho_block_to_func(old_block, blk, ptr, i64)
        fn_def_op.erase()

    apply_partial_conversion(op, target, patterns.freeze(), config)

    with InsertionPoint(op.opview.body):
        func.FuncOp("rho_init_stack", FunctionType.get([], [ptr]), visibility="private")
        func.FuncOp("rho_push", FunctionType.get([ptr, i64], [ptr]), visibility="private")
        func.FuncOp("rho_make_closure", FunctionType.get([ptr, ptr], [i64]), visibility="private")
        for rt_name in PRIM_RUNTIME_NAMES.values():
            func.FuncOp(rt_name, FunctionType.get([ptr], [ptr]), visibility="private")
        func.FuncOp("rho_drop", FunctionType.get([ptr], [ptr]), visibility="private")
        func.FuncOp("rho_def", FunctionType.get([ptr, i64], [ptr]), visibility="private")
        func.FuncOp("rho_load", FunctionType.get([ptr, i64], [ptr]), visibility="private")
        func.FuncOp("rho_eval", FunctionType.get([ptr, i64], [ptr]), visibility="private")
