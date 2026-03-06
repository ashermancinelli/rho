"""Parser and AST tests: source -> parse -> ast_repr -> compare to expected."""

import pytest

from rho.ast import ast_repr
from rho.parser import parse


def test_parse_literal():
    program = parse("42")
    assert ast_repr(program) == "Program(Lit(42))"


def test_parse_apply_literals():
    program = parse("5 5 5")
    expected = "Program(Apply(Lit(5) Lit(5) Lit(5)))"
    assert ast_repr(program) == expected


def test_parse_definition():
    program = parse("f <- 1")
    assert ast_repr(program) == "Program(Def('f' <- Lit(1)))"


def test_parse_lambda():
    program = parse("f <- (a b) -> a + b")
    expected = "Program(Def('f' <- Lambda((a b) -> Apply(Word('a') Primitive('+') Word('b')))))"
    assert ast_repr(program) == expected


def test_parse_block():
    program = parse("f <- (a b c) { a + b + c }")
    # Block with params (a b c) and one stmt: a + b + c
    assert "Block((a b c)" in ast_repr(program)
    assert "Apply(Word('a') Primitive('+') Word('b') Primitive('+') Word('c'))" in ast_repr(program)


def test_parse_multiple_defs_and_expr():
    program = parse("f <- + +\n5 5 5 f")
    assert "Def('f'" in ast_repr(program)
    assert "Apply(Lit(5) Lit(5) Lit(5) Word('f'))" in ast_repr(program)


def test_parse_primitive():
    program = parse("dup")
    assert ast_repr(program) == "Program(Primitive('dup'))"
