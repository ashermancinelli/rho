"""Parser for Rho: builds AST from tokens."""

from typing import NoReturn

from rho.ast import Apply, Block, Def, Expr, Lambda, Lit, Primitive, Program, Word
from rho.lexer import Token, TokenKind, tokenize


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

    def parse_program(self) -> Program:
        items: list[Def | Expr] = []
        while True:
            self._skip_newlines()
            t = self._peek()
            if t is None:
                break
            # Definition: ident <- expr
            if t.kind == TokenKind.IDENT and self._is_def():
                items.append(self._parse_def())
                continue
            # Otherwise expression
            items.append(self._parse_expression())
        return Program(items)

    def _skip_newlines(self) -> None:
        while self._peek() and self._peek().kind == TokenKind.NEWLINE:
            self._advance()

    def _is_def(self) -> bool:
        """Check if we have ident <- ... (need to look ahead)."""
        if self.pos + 1 >= len(self.tokens):
            return False
        return self.tokens[self.pos + 1].kind == TokenKind.ARROW_LEFT

    def _parse_def(self) -> Def:
        name_t = self._expect(TokenKind.IDENT)
        self._expect(TokenKind.ARROW_LEFT)
        body = self._parse_expression()
        return Def(name=name_t.value, body=body)

    def _parse_expression(self) -> Expr:
        t = self._peek()
        if t is None:
            _fail("expected expression, got end of input")
        if t.kind == TokenKind.LPAREN:
            self._advance()
            return self._parse_paren_expr()
        # Stack expression: sequence of terms (lit, word, primitive) until we hit ) } or end
        terms: list[Expr] = []
        while True:
            t = self._peek()
            if t is None or t.kind in (TokenKind.NEWLINE, TokenKind.RPAREN, TokenKind.RBRACE):
                break
            if t.kind == TokenKind.LPAREN:
                terms.append(self._parse_expression())
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
                name = t.value
                if name in ("+", "-", "*", "/") or name in ("dup", "swap", "drop", "over"):
                    terms.append(Primitive(name))
                else:
                    terms.append(Word(name))
                continue
            _fail("expected term in expression", t)
        if not terms:
            _fail("expected at least one term in expression")
        if len(terms) == 1:
            return terms[0]
        return Apply(terms=terms)

    def _parse_paren_expr(self) -> Expr:
        """After consuming '(', parse ( id* ) -> expr  or  ( id* ) { stmts }."""
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
        if t is None:
            _fail("expected -> or { after )")
        if t.kind == TokenKind.ARROW:
            self._advance()
            body = self._parse_expression()
            return Lambda(params=params, body=body)
        if t.kind == TokenKind.LBRACE:
            self._advance()
            stmts = self._parse_block_stmts()
            return Block(params=params, stmts=stmts)
        _fail("expected -> or { after )", t)

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
