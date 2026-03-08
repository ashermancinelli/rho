"""Lexer for Rho: ANSI-only tokens."""

import re
from dataclasses import dataclass
from enum import Enum


class TokenKind(Enum):
    IDENT = "ident"
    NUMBER = "number"
    NEWLINE = "newline"
    ARROW_LEFT = "<-"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"


@dataclass
class Token:
    kind: TokenKind
    value: str
    line: int = 0
    col: int = 0

    def __str__(self) -> str:
        return f"{self.kind.value}({self.value!r})"


_IDENT_RE = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*|[+*/-]+")
_NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
_SPECIAL = {
    "<-": TokenKind.ARROW_LEFT,
    "(": TokenKind.LPAREN,
    ")": TokenKind.RPAREN,
    "{": TokenKind.LBRACE,
    "}": TokenKind.RBRACE,
}


def tokenize(source: str) -> list[Token]:
    """Tokenize Rho source; ANSI only."""
    tokens: list[Token] = []
    line, col = 1, 1
    i = 0
    n = len(source)

    while i < n:
        c = source[i]
        if c in " \t":
            i += 1
            col += 1
            continue
        if c == "\n":
            tokens.append(Token(TokenKind.NEWLINE, "\n", line, col))
            i += 1
            line += 1
            col = 1
            continue
        if c == "-" and i + 1 < n and source[i + 1] == "-":
            while i < n and source[i] != "\n":
                i += 1
            continue
        if i + 1 < n:
            two = source[i : i + 2]
            if two in _SPECIAL:
                tokens.append(Token(_SPECIAL[two], two, line, col))
                i += 2
                col += 2
                continue
        if c in _SPECIAL:
            tokens.append(Token(_SPECIAL[c], c, line, col))
            i += 1
            col += 1
            continue
        m = _NUMBER_RE.match(source, i)
        if m:
            raw = m.group(0)
            tokens.append(Token(TokenKind.NUMBER, raw, line, col))
            i += len(raw)
            col += len(raw)
            continue
        m = _IDENT_RE.match(source, i)
        if m:
            raw = m.group(0)
            tokens.append(Token(TokenKind.IDENT, raw, line, col))
            i += len(raw)
            col += len(raw)
            continue
        i += 1
        col += 1

    return tokens
