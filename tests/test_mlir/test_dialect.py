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
    """Helper: create a fresh module and return (module, block inside rho.main)."""
    from rho.mlir.dialect import MainOp
    with Location.unknown(ctx):
        module = Module.create()
        with InsertionPoint(module.body):
            main = MainOp()
            main.body.blocks.append()
        return module, main.body.blocks[0]


def _i64(v):
    return IntegerAttr.get(IntegerType.get_signless(64), v)


def test_const_int(ctx):
    from rho.mlir.dialect import ConstOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstOp()
        c.operation.attributes["value"] = _i64(42)
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.const" in s
    assert "42" in s


def test_const_float(ctx):
    from rho.mlir.dialect import ConstOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstOp()
        c.operation.attributes["value"] = FloatAttr.get(F64Type.get(), 3.14)
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.const" in s
    assert "3.14" in s


def test_const_str(ctx):
    from rho.mlir.dialect import ConstOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstOp()
        c.operation.attributes["value"] = StringAttr.get("hello")
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.const" in s
    assert "hello" in s


def test_prim_add(ctx):
    from rho.mlir.dialect import ConstOp, PrimOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        a = ConstOp()
        a.operation.attributes["value"] = _i64(5)
        b = ConstOp()
        b.operation.attributes["value"] = _i64(3)
        p = PrimOp(a.out, b.out)
        p.operation.attributes["op"] = StringAttr.get("+")
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.prim" in s
    assert 'op = "+"' in s


def test_prim_mul(ctx):
    from rho.mlir.dialect import ConstOp, PrimOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        a = ConstOp()
        a.operation.attributes["value"] = _i64(7)
        b = ConstOp()
        b.operation.attributes["value"] = _i64(6)
        p = PrimOp(a.out, b.out)
        p.operation.attributes["op"] = StringAttr.get("*")
        YieldOp()
    assert module.operation.verify()
    assert 'op = "*"' in str(module)


def test_dup(ctx):
    from rho.mlir.dialect import ConstOp, DupOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstOp()
        c.operation.attributes["value"] = _i64(10)
        DupOp(c.out)
        YieldOp()
    assert module.operation.verify()
    assert "rho.dup" in str(module)


def test_swap(ctx):
    from rho.mlir.dialect import ConstOp, SwapOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        a = ConstOp()
        a.operation.attributes["value"] = _i64(1)
        b = ConstOp()
        b.operation.attributes["value"] = _i64(2)
        SwapOp(a.out, b.out)
        YieldOp()
    assert module.operation.verify()
    assert "rho.swap" in str(module)


def test_drop(ctx):
    from rho.mlir.dialect import ConstOp, DropOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstOp()
        c.operation.attributes["value"] = _i64(99)
        DropOp(c.out)
        YieldOp()
    assert module.operation.verify()
    assert "rho.drop" in str(module)


def test_def_and_load(ctx):
    from rho.mlir.dialect import ConstOp, DefOp, LoadOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c = ConstOp()
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
    from rho.mlir.dialect import FnOp, PrimOp, DefOp, YieldOp, ValueType
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
    from rho.mlir.dialect import ConstOp, PrimOp, YieldOp
    module, blk = _m(ctx)
    with InsertionPoint(blk):
        c5 = ConstOp()
        c5.operation.attributes["value"] = _i64(5)
        c3 = ConstOp()
        c3.operation.attributes["value"] = _i64(3)
        p = PrimOp(c5.out, c3.out)
        p.operation.attributes["op"] = StringAttr.get("+")
        YieldOp()
    assert module.operation.verify()
    s = str(module)
    assert "rho.main" in s
    assert s.count("rho.const") == 2
    assert "rho.prim" in s
    assert "rho.yield" in s
