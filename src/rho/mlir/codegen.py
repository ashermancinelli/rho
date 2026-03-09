"""AST -> Rho MLIR dialect translation.

Walks the AST and emits rho dialect ops with a threaded ``!rho.stack``.
"""

from mlir.ir import (
    Location,
    Module,
    InsertionPoint,
    IntegerAttr,
    IntegerType,
    FloatAttr,
    F64Type,
    StringAttr,
)

from rho.mlir.context import get_rho_context
from rho.ast import (
    Apply,
    Array,
    Def,
    Drop,
    Expr,
    Fn,
    Lit,
    Match,
    Primitive,
    Program,
    Quote,
    Str,
    Word,
)


STACK_PRIMITIVES = {"dup", "swap", "over", "drop"}
BINARY_PRIMITIVES = {"+", "-", "*", "/", ">", "<", "==", "!=", ">=", "<="}


def compile_program(program: Program) -> Module:
    """Compile a Program AST to an MLIR Module in the rho dialect."""
    ctx = get_rho_context()
    with Location.unknown(ctx):
        from rho.mlir.dialect import (
            StackType,
            InitStackOp,
            ConstOp,
            MakeArrayOp,
            PrimOp,
            DupOp,
            SwapOp,
            OverOp,
            DropOp as RhoDropOp,
            DefOp,
            LoadOp,
            EvalOp,
            FnOp,
            YieldOp,
            MatchOp,
            MatchCaseOp,
            MainOp,
        )

        stack_op_map = {
            "dup": DupOp,
            "swap": SwapOp,
            "over": OverOp,
            "drop": RhoDropOp,
        }

        def emit_item(item, stk):
            if isinstance(item, Def):
                stk = emit_expr(item.body, stk)
                d = DefOp(stk)
                d.operation.attributes["name"] = StringAttr.get(item.name)
                return d.out
            return emit_expr(item, stk)

        def emit_expr(expr: Expr, stk):
            if isinstance(expr, Lit):
                c = ConstOp(stk)
                if isinstance(expr.value, float):
                    c.operation.attributes["value"] = FloatAttr.get(F64Type.get(), expr.value)
                else:
                    c.operation.attributes["value"] = IntegerAttr.get(
                        IntegerType.get_signless(64), expr.value
                    )
                return c.out

            if isinstance(expr, Str):
                c = ConstOp(stk)
                c.operation.attributes["value"] = StringAttr.get(expr.value)
                return c.out

            if isinstance(expr, Array):
                for elem in expr.elems:
                    stk = emit_expr(elem, stk)
                m = MakeArrayOp(stk)
                m.operation.attributes["count"] = IntegerAttr.get(
                    IntegerType.get_signless(64), len(expr.elems)
                )
                return m.out

            if isinstance(expr, Word):
                e = EvalOp(stk)
                e.operation.attributes["name"] = StringAttr.get(expr.name)
                return e.out

            if isinstance(expr, Quote):
                l = LoadOp(stk)
                l.operation.attributes["name"] = StringAttr.get(expr.name)
                return l.out

            if isinstance(expr, Primitive):
                if expr.name in STACK_PRIMITIVES:
                    op = stack_op_map[expr.name](stk)
                    return op.out
                if expr.name in BINARY_PRIMITIVES:
                    p = PrimOp(stk)
                    p.operation.attributes["op"] = StringAttr.get(expr.name)
                    return p.out
                e = EvalOp(stk)
                e.operation.attributes["name"] = StringAttr.get(expr.name)
                return e.out

            if isinstance(expr, Apply):
                for term in expr.terms:
                    stk = emit_expr(term, stk)
                return stk

            if isinstance(expr, Fn):
                fn = FnOp(stk)
                fn.body.blocks.append()
                fn_blk = fn.body.blocks[0]
                fn_stk_arg = fn_blk.add_argument(StackType.get(), Location.unknown())
                with InsertionPoint(fn_blk):
                    fn_stk = fn_stk_arg
                    for param in expr.params:
                        d = DefOp(fn_stk)
                        d.operation.attributes["name"] = StringAttr.get(param)
                        fn_stk = d.out
                    if isinstance(expr.body, list):
                        for stmt in expr.body:
                            fn_stk = emit_expr(stmt, fn_stk)
                    else:
                        fn_stk = emit_expr(expr.body, fn_stk)
                    YieldOp(fn_stk)
                return fn.out

            if isinstance(expr, Match):
                m = MatchOp(stk)
                m.cases.blocks.append()
                cases_blk = m.cases.blocks[0]
                with InsertionPoint(cases_blk):
                    for case in expr.cases:
                        case_op = MatchCaseOp()

                        case_op.guard.blocks.append()
                        gblk = case_op.guard.blocks[0]
                        gstk = gblk.add_argument(StackType.get(), Location.unknown())
                        with InsertionPoint(gblk):
                            cur = gstk
                            for guard_expr in case.guard:
                                cur = emit_expr(guard_expr, cur)
                            YieldOp(cur)

                        case_op.body.blocks.append()
                        bblk = case_op.body.blocks[0]
                        bstk = bblk.add_argument(StackType.get(), Location.unknown())
                        with InsertionPoint(bblk):
                            cur = bstk
                            for body_expr in case.body:
                                cur = emit_expr(body_expr, cur)
                            YieldOp(cur)
                return m.out

            if isinstance(expr, Drop):
                d = RhoDropOp(stk)
                return d.out

            raise ValueError(f"unexpected AST node: {type(expr).__name__}")

        module = Module.create()
        with InsertionPoint(module.body):
            main = MainOp()
            main.body.blocks.append()
            blk = main.body.blocks[0]
            with InsertionPoint(blk):
                stk = InitStackOp().out
                for item in program.items:
                    stk = emit_item(item, stk)
                YieldOp(stk)
        assert module.operation.verify()
        return module