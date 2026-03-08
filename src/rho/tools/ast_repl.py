"""Interactive REPL that parses Rho expressions and prints the AST.

Supports line history via readline (Ctrl-P / Ctrl-N to navigate).
Supports multiline input: unclosed ( or { continues on the next line.
"""

import sys

try:
    import readline  # noqa: F401 — enables line editing and history for input()
except ImportError:
    pass

from rho.parser import parse, ParseError
from rho.ast import ast_pprint


def _bracket_depth(text: str) -> int:
    """Return the net open-bracket depth (parens + braces) in text."""
    depth = 0
    for ch in text:
        if ch in "({":
            depth += 1
        elif ch in ")}":
            depth -= 1
    return max(depth, 0)


def _read_input() -> str | None:
    """Read one (possibly multiline) expression from the user.

    Returns None on EOF/Ctrl-C.
    """
    try:
        line = input("> ")
    except (EOFError, KeyboardInterrupt):
        return None

    lines = [line]
    depth = _bracket_depth(line)

    while depth > 0:
        indent = "  " * depth
        try:
            cont = input(f"{'.' * depth} {indent}")
        except (EOFError, KeyboardInterrupt):
            return None
        lines.append(cont)
        depth = _bracket_depth("\n".join(lines))

    return "\n".join(lines)


def main() -> None:
    print("rho ast-repl  (type expressions, Ctrl-P/Ctrl-N for history, Ctrl-D to exit)")
    while True:
        text = _read_input()
        if text is None:
            print()
            break
        text = text.strip()
        if not text:
            continue
        try:
            program = parse(text)
            ast_pprint(program)
        except ParseError as e:
            print(f"parse error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
