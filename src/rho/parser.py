"""Parser for Rho: builds AST from tokens."""

from typing import NoReturn

from rho.ast import Apply, Fn, Def, Expr, Lit, Primitive, Program, Word
from rho.lexer import Token, TokenKind, tokenize


PRIMITIVES = {"+", "-", "*", "/", "dup", "swap", "drop", "over"}


class ParseError(Exception):
    def __init__(self, msg: str, token: Token | None = None):
        if token is not None:
            msg = f"{msg} at line {token.line} col {token.col}"
        super().__init__(msg)


def _fail(msg: str, token: Token | None = None) -> NoReturn:
    raise ParseError(msg, token)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> Token | None:
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def _advance(self) -> Token | None:
        if self.pos >= len(self.tokens):
            return None
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def _expect(self, kind: TokenKind) -> Token:
        t = self._peek()
        if t is None:
            _fail(f"expected {kind.value}, got end of input")
        if t.kind != kind:
            _fail(f"expected {kind.value}, got {t.kind.value}", t)
        self._advance()
        return t

    def _skip_newlines(self) -> None:
        while self._peek() and self._peek().kind == TokenKind.NEWLINE:
            self._advance()

    def parse_program(self) -> Program:
        items: list[Def | Expr] = []
        while True:
            self._skip_newlines()
            t = self._peek()
            if t is None:
                break
            if t.kind == TokenKind.IDENT and self._is_def():
                items.append(self._parse_def())
                continue
            items.append(self._parse_expression())
        return Program(items)

    def _is_def(self) -> bool:
        if self.pos + 1 >= len(self.tokens):
            return False
        return self.tokens[self.pos + 1].kind == TokenKind.ARROW_LEFT

    def _parse_def(self) -> Def:
        name_t = self._expect(TokenKind.IDENT)
        self._expect(TokenKind.ARROW_LEFT)
        body = self._parse_expression()
        return Def(name=name_t.value, body=body)

    def _parse_expression(self) -> Expr:
        """Parse a stack expression: sequence of terms until newline/)/}/end.

        ( always starts a param list (function), never grouping.
        """
        terms: list[Expr] = []
        while True:
            t = self._peek()
            if t is None or t.kind in (TokenKind.NEWLINE, TokenKind.RPAREN, TokenKind.RBRACE):
                break
            if t.kind == TokenKind.LPAREN:
                terms.append(self._parse_fn())
                continue
            if t.kind == TokenKind.NUMBER:
                self._advance()
                raw = t.value
                if "." in raw:
                    terms.append(Lit(float(raw)))
                else:
                    terms.append(Lit(int(raw)))
                continue
            if t.kind == TokenKind.IDENT:
                self._advance()
                if t.value in PRIMITIVES:
                    terms.append(Primitive(t.value))
                else:
                    terms.append(Word(t.value))
                continue
            _fail("expected term in expression", t)
        if not terms:
            _fail("expected at least one term in expression")
        if len(terms) == 1:
            return terms[0]
        return Apply(terms=terms)

    def _parse_fn(self) -> Fn:
        """Parse (params) expr  or  (params) { stmts }.

        Parens always mean: pop values and bind names.
        """
        self._expect(TokenKind.LPAREN)
        params: list[str] = []
        while True:
            t = self._peek()
            if t is None:
                _fail("unclosed (")
            if t.kind == TokenKind.RPAREN:
                self._advance()
                break
            if t.kind == TokenKind.IDENT:
                self._advance()
                params.append(t.value)
                continue
            _fail("expected identifier or ) in parameter list", t)

        t = self._peek()
        if t is not None and t.kind == TokenKind.LBRACE:
            self._advance()
            stmts = self._parse_block_stmts()
            return Fn(params=params, body=stmts)
        body = self._parse_expression()
        return Fn(params=params, body=body)

    def _parse_block_stmts(self) -> list[Expr]:
        stmts: list[Expr] = []
        while True:
            self._skip_newlines()
            t = self._peek()
            if t is None:
                _fail("unclosed {")
            if t.kind == TokenKind.RBRACE:
                self._advance()
                break
            stmts.append(self._parse_expression())
        return stmts


def parse(source: str) -> Program:
    """Parse Rho source into a Program AST."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse_program()
