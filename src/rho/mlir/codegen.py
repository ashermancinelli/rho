"""Emit Rho dialect MLIR from AST."""

from mlir.ir import Context, InsertionPoint, Location, Module

from rho.ast import Apply, Block, Def, Expr, Lambda, Lit, Primitive, Program, Word
from rho.mlir.dialect import AddOp, ConstOp, MainOp, ValueType


def compile_program(program: Program) -> Module:
    """Build an MLIR Module in the rho dialect from a Program AST."""
    ctx = Context()
    with Location.unknown(ctx):
        from rho.mlir.dialect import RhoDialect
        RhoDialect.load()
        module = Module.create()
        with InsertionPoint(module.body):
            main = MainOp()
            main.body.blocks.append()
            ip = InsertionPoint(main.body.blocks[0])
            # Emit code for the last top-level expression if it's an expr (not a def)
            for item in program.items:
                if isinstance(item, Def):
                    continue
                _emit_expr(item, ip)
        return module


def _emit_expr(expr: Expr, ip: InsertionPoint) -> None:
    """Emit rho ops for an expression; result is left in the last op's result (not tracked for multi-term)."""
    if isinstance(expr, Lit):
        with ip:
            # Tagged immediate: (n << 1) | 1
            val = (int(expr.value) << 1) | 1 if isinstance(expr.value, int) else expr.value
            ConstOp(value=val)
        return
    if isinstance(expr, Word):
        # Lookup/call not implemented; would need symbol table
        return
    if isinstance(expr, Primitive):
        # Primitives are applied in context of Apply
        return
    if isinstance(expr, Apply):
        # Stack: push each term, then apply. For now only handle literals and +.
        stack: list = []
        for term in expr.terms:
            if isinstance(term, Lit):
                with ip:
                    v = (int(term.value) << 1) | 1 if isinstance(term.value, int) else term.value
                    op = ConstOp(value=v)
                    stack.append(op.out)
            elif isinstance(term, Primitive) and term.name == "+":
                if len(stack) >= 2:
                    rhs = stack.pop()
                    lhs = stack.pop()
                    with ip:
                        add_op = AddOp(lhs=lhs, rhs=rhs)
                    stack.append(add_op.result)
            elif isinstance(term, Word):
                # Placeholder: would look up and call
                pass
        return
    if isinstance(expr, (Lambda, Block)):
        # Closures not emitted in this minimal pass
        return
