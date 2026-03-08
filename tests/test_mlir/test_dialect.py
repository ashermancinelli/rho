"""Tests for the rho MLIR dialect: verify ops build and print correctly."""

import pytest

from mlir.ir import (
    Context, Location, Module, InsertionPoint,
    IntegerAttr, IntegerType, StringAttr, FloatAttr, F64Type,
)


@pytest.fixture(scope="module")
def ctx():
    """Single MLIR context for all tests in this module."""
    with Context() as c, Location.unknown():
        from rho.mlir.dialect import RhoDialect
        RhoDialect.load()
        yield c


def _m(ctx):
    """Helper: create a fresh module and return (module, ip inside rho.main)."""
    from rho.mlir.dialect import MainOp, YieldOp
    with Location.unknown(ctx):
        module = Module.create()
        with InsertionPoint(module.body):
            main = MainOp()
            main.body.blocks.append()
        return module, main.body.blocks[0]


def _i64(v):
    return IntegerAttr.get(IntegerType.get_signless(64), v)


def test_const_int(ctx):
    from rho.mlir.dialect import ConstIntOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstIntOp()
        c.operation.attributes["value"] = _i64(42)
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.const_int" in s
    assert "42" in s


def test_const_str(ctx):
    from rho.mlir.dialect import ConstStrOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstStrOp()
        c.operation.attributes["value"] = StringAttr.get("hello")
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.const_str" in s
    assert "hello" in s


def test_prim_add(ctx):
    from rho.mlir.dialect import ConstIntOp, PrimOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        a = ConstIntOp()
        a.operation.attributes["value"] = _i64(5)
        b = ConstIntOp()
        b.operation.attributes["value"] = _i64(3)
        p = PrimOp(a.out, b.out)
        p.operation.attributes["op"] = StringAttr.get("+")
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.prim" in s
    assert 'op = "+"' in s


def test_prim_mul(ctx):
    from rho.mlir.dialect import ConstIntOp, PrimOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        a = ConstIntOp()
        a.operation.attributes["value"] = _i64(7)
        b = ConstIntOp()
        b.operation.attributes["value"] = _i64(6)
        p = PrimOp(a.out, b.out)
        p.operation.attributes["op"] = StringAttr.get("*")
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert 'op = "*"' in s


def test_dup(ctx):
    from rho.mlir.dialect import ConstIntOp, DupOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstIntOp()
        c.operation.attributes["value"] = _i64(10)
        DupOp(c.out)
        YieldOp()
    assert module.operation.verify()
    assert "rho.dup" in str(module)


def test_swap(ctx):
    from rho.mlir.dialect import ConstIntOp, SwapOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        a = ConstIntOp()
        a.operation.attributes["value"] = _i64(1)
        b = ConstIntOp()
        b.operation.attributes["value"] = _i64(2)
        SwapOp(a.out, b.out)
        YieldOp()
    assert module.operation.verify()
    assert "rho.swap" in str(module)


def test_drop(ctx):
    from rho.mlir.dialect import ConstIntOp, DropOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstIntOp()
        c.operation.attributes["value"] = _i64(99)
        DropOp(c.out)
        YieldOp()
    assert module.operation.verify()
    assert "rho.drop" in str(module)


def test_def_and_load(ctx):
    from rho.mlir.dialect import ConstIntOp, DefOp, LoadOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstIntOp()
        c.operation.attributes["value"] = _i64(42)
        d = DefOp(c.out)
        d.operation.attributes["name"] = StringAttr.get("x")
        l = LoadOp()
        l.operation.attributes["name"] = StringAttr.get("x")
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.def" in s
    assert "rho.load" in s
    assert 'name = "x"' in s


def test_fn_with_params(ctx):
    from rho.mlir.dialect import ConstIntOp, FnOp, PrimOp, DefOp, YieldOp, ValueType
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        fn = FnOp()
        fn.body.blocks.append()
        fn_blk = fn.body.blocks[0]
        a = fn_blk.add_argument(ValueType.get(), Location.unknown())
        b = fn_blk.add_argument(ValueType.get(), Location.unknown())
        with InsertionPoint(fn_blk):
            r = PrimOp(a, b)
            r.operation.attributes["op"] = StringAttr.get("+")
            YieldOp()
        d = DefOp(fn.out)
        d.operation.attributes["name"] = StringAttr.get("add")
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.fn" in s
    assert 'name = "add"' in s


def test_fn_nested(ctx):
    """Nested fn: (x) (y) x + y (curried)."""
    from rho.mlir.dialect import FnOp, PrimOp, DefOp, YieldOp, ValueType
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        outer = FnOp()
        outer.body.blocks.append()
        o_blk = outer.body.blocks[0]
        x = o_blk.add_argument(ValueType.get(), Location.unknown())
        with InsertionPoint(o_blk):
            inner = FnOp()
            inner.body.blocks.append()
            i_blk = inner.body.blocks[0]
            y = i_blk.add_argument(ValueType.get(), Location.unknown())
            with InsertionPoint(i_blk):
                r = PrimOp(x, y)
                r.operation.attributes["op"] = StringAttr.get("+")
                YieldOp()
            YieldOp()
        d = DefOp(outer.out)
        d.operation.attributes["name"] = StringAttr.get("curry_add")
        YieldOp()
    assert module.operation.verify()
    assert str(module).count("rho.fn") == 2


def test_full_program_5_3_add(ctx):
    """Full program: 5 3 +."""
    from rho.mlir.dialect import ConstIntOp, PrimOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c5 = ConstIntOp()
        c5.operation.attributes["value"] = _i64(5)
        c3 = ConstIntOp()
        c3.operation.attributes["value"] = _i64(3)
        p = PrimOp(c5.out, c3.out)
        p.operation.attributes["op"] = StringAttr.get("+")
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.main" in s
    assert s.count("rho.const_int") == 2
    assert "rho.prim" in s
    assert "rho.yield" in s
