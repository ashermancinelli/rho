"""Interactive REPL that parses Rho expressions and prints the AST."""

from rho.parser import parse
from rho.ast import ast_pprint
from rho.repl import run_repl


def _handle(text: str) -> None:
    program = parse(text)
    ast_pprint(program)


def main() -> None:
    run_repl("rho ast-repl  (Ctrl-D to exit)", _handle)


if __name__ == "__main__":
    main()
