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

    _extracted_fns = []

    def convert_fn(op, adaptor, converter, rewriter):
        global _fn_counter
        fn_name = f"rho_fn_{_fn_counter}"
        _fn_counter += 1
        _extracted_fns.append((fn_name, op))

        with rewriter.ip:
            fn_ptr = func.CallOp([ptr], f"rho_get_fn_ptr_{fn_name}", [])
            closure_val = func.CallOp([i64], "rho_make_closure", [fn_ptr.result, adaptor.stk])
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
    patterns.add_conversion(FnOp, convert_fn, type_converter)
    patterns.add_conversion(YieldOp, convert_yield, type_converter)
    patterns.add_conversion(MainOp, convert_main, type_converter)

    target = ConversionTarget()
    target.add_illegal_dialect(RhoDialect)

    config = ConversionConfig()
    config.build_materializations = False

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
        fn_body_type = FunctionType.get([ptr, ptr], [ptr])
        for fn_name, _ in _extracted_fns:
            func.FuncOp(fn_name, fn_body_type, visibility="private")
            func.FuncOp(f"rho_get_fn_ptr_{fn_name}", FunctionType.get([], [ptr]), visibility="private")
