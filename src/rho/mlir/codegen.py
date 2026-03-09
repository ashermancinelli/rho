"""AST -> Rho MLIR dialect translation.

Walks the AST and emits rho dialect ops with a threaded ``!rho.stack``.
"""

from mlir.ir import Location, Module, InsertionPoint

from rho.mlir.context import get_rho_context
from rho.ast import (
    Apply, Array, Def, Drop, Expr, Fn, Lit, Match, Primitive, Program, Quote, Str, Word,
)

import rho.mlir.ops as rho


STACK_OPS = {"dup": rho.dup, "swap": rho.swap, "over": rho.over, "drop": rho.drop}
BINARY_PRIMITIVES = {"+", "-", "*", "/", ">", "<", "==", "!=", ">=", "<="}


def _emit_block(stmts, stk):
    for stmt in stmts:
        stk = emit_expr(stmt, stk)
    return stk


def emit_item(item, stk):
    if isinstance(item, Def):
        return rho.def_(emit_expr(item.body, stk), item.name)
    return emit_expr(item, stk)


def emit_expr(expr: Expr, stk):
    match expr:
        case Lit(value=v):
            return rho.const(stk, v)

        case Str(value=v):
            return rho.const(stk, v)

        case Array(elems=elems):
            for elem in elems:
                stk = emit_expr(elem, stk)
            return rho.make_array(stk, len(elems))

        case Word(name=name):
            return rho.eval_(stk, name)

        case Quote(name=name):
            return rho.load(stk, name)

        case Primitive(name=name) if name in STACK_OPS:
            return STACK_OPS[name](stk)

        case Primitive(name=name) if name in BINARY_PRIMITIVES:
            return rho.prim(stk, name)

        case Primitive(name=name):
            return rho.eval_(stk, name)

        case Apply(terms=terms):
            for term in terms:
                stk = emit_expr(term, stk)
            return stk

        case Fn(params=params, body=body):
            def fn_body(fn_stk):
                for param in params:
                    fn_stk = rho.def_(fn_stk, param)
                if isinstance(body, list):
                    for stmt in body:
                        fn_stk = emit_expr(stmt, fn_stk)
                else:
                    fn_stk = emit_expr(body, fn_stk)
                return fn_stk
            return rho.fn(stk, fn_body)

        case Match(cases=cases):
            def cases_builder():
                for case in cases:
                    rho.match_case(
                        guard_builder=lambda gs, c=case: _emit_block(c.guard, gs),
                        body_builder=lambda bs, c=case: _emit_block(c.body, bs),
                    )
            return rho.match(stk, cases_builder)

        case Drop():
            return rho.drop(stk)

    raise ValueError(f"unexpected AST node: {type(expr).__name__}")


def compile_program(program: Program) -> Module:
    """Compile a Program AST to an MLIR Module in the rho dialect."""
    ctx = get_rho_context()
    with Location.unknown(ctx):
        module = Module.create()
        with InsertionPoint(module.body):
            def body(stk):
                for item in program.items:
                    stk = emit_item(item, stk)
                return stk
            rho.main(body)
        assert module.operation.verify()
        return module
