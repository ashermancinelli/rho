"""Tests for rho dialect -> upstream MLIR lowering."""

from rho.parser import parse
from rho.mlir.codegen import compile_program
from rho.mlir.context import get_rho_context
from mlir.ir import Location
from mlir.passmanager import PassManager
from rho.mlir.lower import convert_rho_to_runtime


def _lower(src: str) -> str:
    ctx = get_rho_context()
    with Location.unknown(ctx):
        module = compile_program(parse(src))
        pm = PassManager()
        pm.add(convert_rho_to_runtime)
        pm.run(module.operation)
        return str(module)


def test_lower_simple_add():
    s = _lower("5 3 +")
    assert "func.func @rho_main" in s
    assert "call @rho_init_stack" in s
    assert "call @rho_push" in s
    assert "call @rho_prim_add" in s
    assert "return" in s
    # tagged int: (5 << 1) | 1 = 11, (3 << 1) | 1 = 7
    assert "llvm.shl" in s or "11" in s
    # no rho ops remain
    assert "rho.const" not in s
    assert "rho.prim" not in s


def test_lower_tagging():
    """Const ints should be tagged as immediates: (42 << 1) | 1 = 85."""
    s = _lower("42")
    assert "rho_push" in s
    assert "85" in s  # (42 << 1) | 1


def test_lower_dup_add():
    s = _lower("5 dup +")
    assert "call @rho_push" in s
    assert "call @rho_dup" in s
    assert "call @rho_prim_add" in s


def test_lower_swap():
    s = _lower("1 2 swap")
    assert "call @rho_swap" in s


def test_lower_multiple_prims():
    s = _lower("10 3 - 2 *")
    assert "call @rho_prim_sub" in s
    assert "call @rho_prim_mul" in s


def test_lower_comparison():
    s = _lower("5 3 >")
    assert "call @rho_prim_gt" in s


def test_lower_no_rho_ops_remain():
    """After lowering, no rho dialect ops should remain for flat programs."""
    s = _lower("1 2 + 3 * dup swap")
    for rho_op in ["rho.init_stack", "rho.const", "rho.prim", "rho.dup", "rho.swap", "rho.yield", "rho.main"]:
        assert rho_op not in s, f"{rho_op} should not remain after lowering"


def test_lower_generic_push():
    """All values go through rho_push, not type-specific push functions."""
    s = _lower("5 3 +")
    assert "rho_push_int" not in s
    assert "rho_push" in s
