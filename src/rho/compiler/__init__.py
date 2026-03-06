"""Public API for the Rho compiler."""

from rho.ast import Program, ast_repr
from rho.parser import parse


def evaluate(source: str):
    """Evaluate Rho source (interpreter). Optional; not implemented initially."""
    _ = source
    raise NotImplementedError("evaluate not yet implemented")


def compile_to_mlir(ast: Program):
    """Compile a Rho Program AST to an MLIR module (rho dialect)."""
    from rho.mlir.codegen import compile_program
    return compile_program(ast)
