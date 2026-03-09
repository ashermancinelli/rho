"""End-to-end AST -> rho MLIR codegen tests."""

from rho.parser import parse
from rho.mlir.codegen import compile_program


def _mlir(src: str) -> str:
    return str(compile_program(parse(src)))


def test_codegen_simple_add():
    s = _mlir("5 3 +")
    assert "rho.init_stack" in s
    assert s.count("rho.const") == 2
    assert "rho.prim" in s
    assert 'op = "+"' in s


def test_codegen_tacit_double():
    s = _mlir("double <- dup +")
    assert "rho.eval" in s
    assert "rho.prim" in s
    assert 'name = "double"' in s


def test_codegen_quote_vs_eval():
    s = _mlir('f <- dup +; 5 f; &f')
    assert "rho.eval" in s
    assert "rho.load" in s
    assert s.count('name = "f"') >= 2


def test_codegen_array():
    s = _mlir('[1 2 3]')
    assert s.count('rho.const') == 3
    assert 'rho.make_array' in s
    assert 'count = 3 : i64' in s


def test_codegen_match():
    src = '(n) match { { dup 0 > } { "pos" } { true } { "other" } }'
    s = _mlir(src)
    assert 'rho.match' in s
    assert s.count('rho.match_case') == 2
    assert 'rho.eval' in s
    assert 'op = ">"' in s
    assert 'value = "pos"' in s
    assert 'value = "other"' in s


def test_codegen_match_in_function_definition():
    src = 'sign <- (n) match { { dup 0 > } { "pos" } { true } { "other" } }'
    s = _mlir(src)
    assert 'rho.fn' in s
    assert 'rho.def' in s
    assert 'name = "sign"' in s
    assert 'rho.match' in s
