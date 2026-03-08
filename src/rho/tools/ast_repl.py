"""Interactive REPL that parses Rho expressions and prints the AST.

Supports line history via readline (Ctrl-P / Ctrl-N to navigate).
"""

import sys

try:
    import readline  # noqa: F401 — enables line editing and history for input()
except ImportError:
    pass

from rho.parser import parse, ParseError
from rho.ast import ast_pprint


def main() -> None:
    print("rho ast-repl  (type expressions, Ctrl-P/Ctrl-N for history, Ctrl-D to exit)")
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        line = line.strip()
        if not line:
            continue
        try:
            program = parse(line)
            ast_pprint(program)
        except ParseError as e:
            print(f"parse error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
