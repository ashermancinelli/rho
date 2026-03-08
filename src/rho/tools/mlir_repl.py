"""Interactive REPL that compiles Rho to MLIR and prints the IR."""

from rho.parser import parse
from rho.mlir.codegen import compile_program
from rho.repl import run_repl


def _handle(text: str) -> None:
    program = parse(text)
    module = compile_program(program)
    print(module)


def main() -> None:
    run_repl("rho mlir-repl  (Ctrl-D to exit)", _handle)


if __name__ == "__main__":
    main()
