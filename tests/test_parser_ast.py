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


def test_parse_larger_program_pprint():
    """Larger program with multiple defs and exprs prints across multiple lines."""
    source = """
add <- (x y) -> x + y
double <- (n) -> n n +
add 3 5
double 10
"""
    program = parse(source.strip())
    got = ast_pprint_str(program)
    assert "Program" in got
    assert "Def" in got
    assert "add" in got
    assert "double" in got
    assert "Lambda" in got
    assert "Apply" in got
    assert "Lit" in got and "3" in got and "5" in got and "10" in got
    # Multi-line: output has newlines and indentation
    lines = got.strip().split("\n")
    assert len(lines) >= 5


def test_parse_larger_program_pprint_expected():
    """Larger program pformat matches expected multi-line structure."""
    source = "add <- (x y) -> x + y\ndouble <- (n) -> n n +\nadd 3 5\ndouble 10"
    program = parse(source)
    expected = """( 'Program',
  ( ( 'Def',
      'add',
      ( 'Lambda',
        ('x', 'y'),
        ('Apply', (('Word', 'x'), ('Primitive', '+'), ('Word', 'y'))))),
    ( 'Def',
      'double',
      ( 'Lambda',
        ('n',),
        ('Apply', (('Word', 'n'), ('Word', 'n'), ('Primitive', '+'))))),
    ('Apply', (('Word', 'add'), ('Lit', 3), ('Lit', 5))),
    ('Apply', (('Word', 'double'), ('Lit', 10)))))"""
    assert ast_pprint_str(program) == expected


def test_parse_nested_lambda_pprint():
    """Nested lambda (curried) prints across multiple lines."""
    source = "curry_add <- (x) -> (y) -> x + y"
    program = parse(source)
    got = ast_pprint_str(program)
    assert "Lambda" in got
    assert "curry_add" in got
    assert "Apply" in got
    # Nested: inner Lambda inside outer Lambda
    assert got.count("Lambda") >= 2
    lines = got.strip().split("\n")
    assert len(lines) >= 4


def test_parse_def_with_block_pprint():
    """Def with block body prints across multiple lines."""
    source = "f <- (a b c) { a + b + c }"
    program = parse(source)
    got = ast_pprint_str(program)
    assert "Block" in got
    assert "('a', 'b', 'c')" in got
    assert "Apply" in got
    assert "Primitive" in got
    lines = got.strip().split("\n")
    assert len(lines) >= 3


def test_parse_mixed_defs_and_exprs_pprint():
    """Several defs and trailing exprs produce a deep multi-line dump."""
    source = """
id <- (x) -> x
one <- 1
two <- 2
id one
id two
one two +
"""
    program = parse(source.strip())
    got = ast_pprint_str(program)
    assert got.count("Def") == 3
    assert "id" in got and "one" in got and "two" in got
    assert got.count("Apply") >= 3
    lines = got.strip().split("\n")
    assert len(lines) >= 5  # multi-line dump
