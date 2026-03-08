"""Shared REPL utilities: syntax highlighting, multiline input, session."""

import sys
from pathlib import Path
from typing import Callable

import tree_sitter_rho
from tree_sitter import Language, Parser as TSParser, Query, QueryCursor

from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.history import InMemoryHistory

_lang = Language(tree_sitter_rho.language())
_ts_parser = TSParser(_lang)

_HIGHLIGHTS_SCM = (
    Path(__file__).resolve().parent.parent
    / "tree-sitter-rho" / "queries" / "highlights.scm"
).read_text()
_query = Query(_lang, _HIGHLIGHTS_SCM)

_STYLES = {
    "number": "ansiyellow",
    "operator": "bold ansimagenta",
    "variable": "",
    "variable.definition": "bold ansicyan",
    "variable.parameter": "italic ansicyan",
    "keyword.operator": "bold ansired",
    "punctuation.bracket": "ansibrightblack",
    "comment": "ansigreen italic",
}

_PRIORITY = {
    "variable.definition": 3,
    "variable.parameter": 3,
    "keyword.operator": 2,
    "operator": 2,
    "number": 2,
    "comment": 2,
    "punctuation.bracket": 1,
    "variable": 0,
}


class RhoLexer(Lexer):
    """prompt_toolkit Lexer using tree-sitter for real-time highlighting."""

    def lex_document(self, document):
        text = document.text
        if not text:
            return lambda lineno: []

        src = text.encode("utf-8")

        try:
            tree = _ts_parser.parse(src)
            cursor = QueryCursor(_query)
            captures = cursor.captures(tree.root_node)
        except Exception:
            return lambda lineno: [("", text.split("\n")[lineno])] if lineno < text.count("\n") + 1 else []

        byte_styles: dict[int, tuple[int, str, int]] = {}
        for name, nodes in captures.items():
            prio = _PRIORITY.get(name, 0)
            style = _STYLES.get(name, "")
            for node in nodes:
                if node.end_byte <= node.start_byte:
                    continue
                existing = byte_styles.get(node.start_byte)
                if existing is None or prio > existing[0]:
                    byte_styles[node.start_byte] = (prio, style, node.end_byte)

        lines = text.split("\n")

        def get_line(lineno):
            if lineno >= len(lines):
                return []
            line_start = sum(len(lines[j].encode("utf-8")) + 1 for j in range(lineno))
            line_end = line_start + len(lines[lineno].encode("utf-8"))
            fragments = []
            i = line_start
            while i < line_end:
                if i in byte_styles:
                    _, style, end = byte_styles[i]
                    end = min(end, line_end)
                    if end <= i:
                        fragments.append(("", src[i:i+1].decode("utf-8", errors="replace")))
                        i += 1
                        continue
                    fragments.append((style, src[i:end].decode("utf-8", errors="replace")))
                    i = end
                else:
                    fragments.append(("", src[i:i+1].decode("utf-8", errors="replace")))
                    i += 1
            return fragments

        return get_line


def needs_continuation(text: str) -> tuple[bool, int]:
    """Return (needs_more, indent_level) for the input so far."""
    paren_depth = 0
    brace_depth = 0
    for ch in text:
        if ch == "(":
            paren_depth += 1
        elif ch == ")":
            paren_depth -= 1
        elif ch == "{":
            brace_depth += 1
        elif ch == "}":
            brace_depth -= 1
    if paren_depth > 0 or brace_depth > 0:
        return True, max(brace_depth, 0)
    if text.rstrip().endswith(")"):
        return True, 0
    return False, 0


def run_repl(banner: str, handler: Callable[[str], None]) -> None:
    """Run an interactive REPL with syntax highlighting and multiline support.

    handler(text) is called with each complete input. It should print output
    or raise an exception (which will be printed to stderr).
    """
    session = PromptSession(
        lexer=RhoLexer(),
        history=InMemoryHistory(),
        multiline=False,
    )

    print(banner)
    while True:
        try:
            line = session.prompt("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        lines = [line]
        needs_more, indent = needs_continuation("\n".join(lines))

        while needs_more:
            prefix = "  " * (indent + 1)
            try:
                cont = session.prompt(f". {prefix}", lexer=RhoLexer())
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if cont is None:
                break
            lines.append(cont)
            needs_more, indent = needs_continuation("\n".join(lines))

        text = "\n".join(lines).strip()
        if not text:
            continue

        try:
            handler(text)
        except Exception as e:
            print(f"error: {e}", file=sys.stderr)
