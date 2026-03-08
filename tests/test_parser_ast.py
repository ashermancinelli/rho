"""Parser and AST tests: source -> parse -> ast_repr -> compare to expected."""

import pytest
from pprint import pformat

from rho.ast import ast_repr
from rho.parser import parse


def ast_pprint_str(program, indent: int = 2, width: int = 80) -> str:
    """Return pretty-printed tuple form of the AST (multi-line, for comparison)."""
    return pformat(program.to_tuple(), indent=indent, width=width)


def test_parse_literal():
    program = parse("42")
    assert ast_repr(program) == "Program(Lit(42))"


def test_parse_apply_literals():
    program = parse("5 5 5")
    assert ast_repr(program) == "Program(Apply(Lit(5) Lit(5) Lit(5)))"


def test_parse_definition():
    program = parse("f <- 1")
    assert ast_repr(program) == "Program(Def('f' <- Lit(1)))"


def test_parse_fn_inline():
    program = parse("f <- (a b) a + b")
    expected = "Program(Def('f' <- Fn((a b) Apply(Word('a') Primitive('+') Word('b')))))"
    assert ast_repr(program) == expected


def test_parse_fn_block():
    program = parse("f <- (a b c) { a + b + c }")
    r = ast_repr(program)
    assert "Fn((a b c)" in r
    assert "Apply(Word('a') Primitive('+') Word('b') Primitive('+') Word('c'))" in r


def test_parse_multiple_defs_and_expr():
    program = parse("f <- + +\n5 5 5 f")
    r = ast_repr(program)
    assert "Def('f'" in r
    assert "Apply(Lit(5) Lit(5) Lit(5) Word('f'))" in r


def test_parse_primitive():
    program = parse("dup")
    assert ast_repr(program) == "Program(Primitive('dup'))"


def test_parse_larger_program_pprint():
    source = "add <- (x y) x + y\ndouble <- (n) n n +\nadd 3 5\ndouble 10"
    program = parse(source)
    got = ast_pprint_str(program)
    assert "Fn" in got
    assert "add" in got and "double" in got
    assert "Lit" in got and "3" in got and "5" in got and "10" in got
    lines = got.strip().split("\n")
    assert len(lines) >= 5


def test_parse_larger_program_pprint_expected():
    source = "add <- (x y) x + y\ndouble <- (n) n n +\nadd 3 5\ndouble 10"
    program = parse(source)
    expected = """\
( 'Program',
  ( ( 'Def',
      'add',
      ( 'Fn',
        ('x', 'y'),
        ('Apply', (('Word', 'x'), ('Primitive', '+'), ('Word', 'y'))))),
    ( 'Def',
      'double',
      ( 'Fn',
        ('n',),
        ('Apply', (('Word', 'n'), ('Word', 'n'), ('Primitive', '+'))))),
    ('Apply', (('Word', 'add'), ('Lit', 3), ('Lit', 5))),
    ('Apply', (('Word', 'double'), ('Lit', 10)))))"""
    assert ast_pprint_str(program) == expected


def test_parse_nested_fn_pprint():
    source = "curry_add <- (x) (y) x + y"
    program = parse(source)
    got = ast_pprint_str(program)
    assert got.count("Fn") >= 2
    lines = got.strip().split("\n")
    assert len(lines) >= 4


def test_parse_def_with_block_pprint():
    source = "f <- (a b c) { a + b + c }"
    program = parse(source)
    got = ast_pprint_str(program)
    assert "Fn" in got
    assert "('a', 'b', 'c')" in got
    lines = got.strip().split("\n")
    assert len(lines) >= 3


def test_parse_mixed_defs_and_exprs_pprint():
    source = "id <- (x) x\none <- 1\ntwo <- 2\nid one\nid two\none two +"
    program = parse(source)
    got = ast_pprint_str(program)
    assert got.count("Def") == 3
    assert "id" in got and "one" in got and "two" in got
    assert got.count("Apply") >= 3
    lines = got.strip().split("\n")
    assert len(lines) >= 5


def test_parse_multiline_block():
    source = "f <- (a b c) {\na b\n*\nc\n+\n}"
    program = parse(source)
    r = ast_repr(program)
    assert "Fn((a b c)" in r


def test_parse_comment():
    source = "x <- 1 -- this is a comment\nx"
    program = parse(source)
    r = ast_repr(program)
    assert "Def('x'" in r
    assert "Word('x')" in r


def test_parse_tacit():
    source = "double <- dup +"
    program = parse(source)
    r = ast_repr(program)
    assert "Def('double'" in r
    assert "Primitive('dup')" in r
    assert "Primitive('+')" in r
