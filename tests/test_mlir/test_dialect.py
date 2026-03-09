"""Tests for the rho MLIR dialect with threaded stack."""

import pytest

from mlir.ir import (
    Context, Location, Module, InsertionPoint,
    IntegerAttr, IntegerType, StringAttr, FloatAttr, F64Type,
)


@pytest.fixture(scope="module")
def ctx():
    with Context() as c, Location.unknown():
        from rho.mlir.dialect import RhoDialect
        RhoDialect.load()
        yield c


def _main(ctx):
    """Create module with rho.main, return (module, block, initial_stack)."""
    from rho.mlir.dialect import MainOp, StackType, InitStackOp
    with Location.unknown(ctx):
        module = Module.create()
        with InsertionPoint(module.body):
            main = MainOp()
            main.body.blocks.append()
            blk = main.body.blocks[0]
            with InsertionPoint(blk):
                init = InitStackOp()
        return module, blk, init.out


def _i64(v):
    return IntegerAttr.get(IntegerType.get_signless(64), v)


def test_init_stack(ctx):
    from rho.mlir.dialect import YieldOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        YieldOp(stk)
    assert module.operation.verify()
    s = str(module)
    assert "rho.init_stack" in s
    assert "!rho.stack" in s


def test_const_int(ctx):
    from rho.mlir.dialect import ConstOp, YieldOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        c = ConstOp(stk)
        c.operation.attributes["value"] = _i64(42)
        YieldOp(c.out)
    assert module.operation.verify()
    s = str(module)
    assert "rho.const" in s
    assert "42" in s


def test_const_float(ctx):
    from rho.mlir.dialect import ConstOp, YieldOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        c = ConstOp(stk)
        c.operation.attributes["value"] = FloatAttr.get(F64Type.get(), 3.14)
        YieldOp(c.out)
    assert module.operation.verify()
    s = str(module)
    assert "rho.const" in s
    assert "3.14" in s


def test_const_str(ctx):
    from rho.mlir.dialect import ConstOp, YieldOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        c = ConstOp(stk)
        c.operation.attributes["value"] = StringAttr.get("hello")
        YieldOp(c.out)
    assert module.operation.verify()
    s = str(module)
    assert "rho.const" in s
    assert "hello" in s


def test_prim_add(ctx):
    """5 3 + -> push 5, push 3, add."""
    from rho.mlir.dialect import ConstOp, PrimOp, YieldOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        s1 = ConstOp(stk)
        s1.operation.attributes["value"] = _i64(5)
        s2 = ConstOp(s1.out)
        s2.operation.attributes["value"] = _i64(3)
        s3 = PrimOp(s2.out)
        s3.operation.attributes["op"] = StringAttr.get("+")
        YieldOp(s3.out)
    assert module.operation.verify()
    s = str(module)
    assert "rho.prim" in s
    assert 'op = "+"' in s


def test_dup(ctx):
    from rho.mlir.dialect import ConstOp, DupOp, YieldOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        s1 = ConstOp(stk)
        s1.operation.attributes["value"] = _i64(10)
        s2 = DupOp(s1.out)
        YieldOp(s2.out)
    assert module.operation.verify()
    assert "rho.dup" in str(module)


def test_swap(ctx):
    from rho.mlir.dialect import ConstOp, SwapOp, YieldOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        s1 = ConstOp(stk)
        s1.operation.attributes["value"] = _i64(1)
        s2 = ConstOp(s1.out)
        s2.operation.attributes["value"] = _i64(2)
        s3 = SwapOp(s2.out)
        YieldOp(s3.out)
    assert module.operation.verify()
    assert "rho.swap" in str(module)


def test_drop(ctx):
    from rho.mlir.dialect import ConstOp, DropOp, YieldOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        s1 = ConstOp(stk)
        s1.operation.attributes["value"] = _i64(99)
        s2 = DropOp(s1.out)
        YieldOp(s2.out)
    assert module.operation.verify()
    assert "rho.drop" in str(module)


def test_def_and_load(ctx):
    from rho.mlir.dialect import ConstOp, DefOp, LoadOp, YieldOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        s1 = ConstOp(stk)
        s1.operation.attributes["value"] = _i64(42)
        s2 = DefOp(s1.out)
        s2.operation.attributes["name"] = StringAttr.get("x")
        s3 = LoadOp(s2.out)
        s3.operation.attributes["name"] = StringAttr.get("x")
        YieldOp(s3.out)
    assert module.operation.verify()
    s = str(module)
    assert "rho.def" in s
    assert "rho.load" in s
    assert 'name = "x"' in s


def test_fn_tacit(ctx):
    """Tacit function: double <- dup +"""
    from rho.mlir.dialect import ConstOp, FnOp, DupOp, PrimOp, DefOp, YieldOp, StackType
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        fn = FnOp(stk)
        fn.body.blocks.append()
        fn_blk = fn.body.blocks[0]
        fn_stk = fn_blk.add_argument(StackType.get(), Location.unknown())
        with InsertionPoint(fn_blk):
            s1 = DupOp(fn_stk)
            s2 = PrimOp(s1.out)
            s2.operation.attributes["op"] = StringAttr.get("+")
            YieldOp(s2.out)
        s_after = DefOp(fn.out)
        s_after.operation.attributes["name"] = StringAttr.get("double")
        YieldOp(s_after.out)
    assert module.operation.verify()
    s = str(module)
    assert "rho.fn" in s
    assert "rho.dup" in s
    assert 'name = "double"' in s


def test_fn_plus_plus(ctx):
    """Tacit: f <- + + (takes 3 values, produces 1)."""
    from rho.mlir.dialect import FnOp, PrimOp, DefOp, YieldOp, StackType
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        fn = FnOp(stk)
        fn.body.blocks.append()
        fn_blk = fn.body.blocks[0]
        fn_stk = fn_blk.add_argument(StackType.get(), Location.unknown())
        with InsertionPoint(fn_blk):
            s1 = PrimOp(fn_stk)
            s1.operation.attributes["op"] = StringAttr.get("+")
            s2 = PrimOp(s1.out)
            s2.operation.attributes["op"] = StringAttr.get("+")
            YieldOp(s2.out)
        s_after = DefOp(fn.out)
        s_after.operation.attributes["name"] = StringAttr.get("f")
        YieldOp(s_after.out)
    assert module.operation.verify()
    s = str(module)
    assert s.count("rho.prim") == 2


def test_full_program(ctx):
    """Full: 5 3 + (should produce 8 on the stack)."""
    from rho.mlir.dialect import ConstOp, PrimOp, YieldOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        s1 = ConstOp(stk)
        s1.operation.attributes["value"] = _i64(5)
        s2 = ConstOp(s1.out)
        s2.operation.attributes["value"] = _i64(3)
        s3 = PrimOp(s2.out)
        s3.operation.attributes["op"] = StringAttr.get("+")
        YieldOp(s3.out)
    assert module.operation.verify()
    s = str(module)
    assert "rho.main" in s
    assert "rho.init_stack" in s
    assert s.count("rho.const") == 2
    assert "rho.prim" in s


def test_call(ctx):
    """Define f <- dup +, then: 5 f (call)."""
    from rho.mlir.dialect import (
        ConstOp, FnOp, DupOp, PrimOp, DefOp, LoadOp, CallOp, YieldOp, StackType,
    )
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        fn = FnOp(stk)
        fn.body.blocks.append()
        fn_blk = fn.body.blocks[0]
        fn_stk = fn_blk.add_argument(StackType.get(), Location.unknown())
        with InsertionPoint(fn_blk):
            fs1 = DupOp(fn_stk)
            fs2 = PrimOp(fs1.out)
            fs2.operation.attributes["op"] = StringAttr.get("+")
            YieldOp(fs2.out)
        s1 = DefOp(fn.out)
        s1.operation.attributes["name"] = StringAttr.get("f")
        s2 = ConstOp(s1.out)
        s2.operation.attributes["value"] = _i64(5)
        s3 = LoadOp(s2.out)
        s3.operation.attributes["name"] = StringAttr.get("f")
        s4 = CallOp(s3.out)
        YieldOp(s4.out)
    assert module.operation.verify()
    s = str(module)
    assert "rho.call" in s
    assert "rho.fn" in s


def test_match_op(ctx):
    from rho.mlir.dialect import MatchOp, MatchCaseOp, YieldOp, StackType, PrimOp, ConstOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        m = MatchOp(stk)
        m.cases.blocks.append()
        cases_blk = m.cases.blocks[0]
        with InsertionPoint(cases_blk):
            case1 = MatchCaseOp()
            # guard region
            case1.guard.blocks.append()
            gblk = case1.guard.blocks[0]
            gstk = gblk.add_argument(StackType.get(), Location.unknown())
            with InsertionPoint(gblk):
                g1 = PrimOp(gstk)
                g1.operation.attributes["op"] = StringAttr.get(">")
                YieldOp(g1.out)
            # body region
            case1.body.blocks.append()
            bblk = case1.body.blocks[0]
            bstk = bblk.add_argument(StackType.get(), Location.unknown())
            with InsertionPoint(bblk):
                c = ConstOp(bstk)
                c.operation.attributes["value"] = StringAttr.get("pos")
                YieldOp(c.out)
        YieldOp(m.out)
    assert module.operation.verify()
    s = str(module)
    assert "rho.match" in s
    assert "rho.match_case" in s
    assert "rho.prim" in s


def test_match_two_cases(ctx):
    from rho.mlir.dialect import MatchOp, MatchCaseOp, YieldOp, StackType, PrimOp, ConstOp
    module, blk, stk = _main(ctx)
    with InsertionPoint(blk):
        m = MatchOp(stk)
        m.cases.blocks.append()
        cases_blk = m.cases.blocks[0]
        with InsertionPoint(cases_blk):
            for opname, result in [(">", "pos"), ("true", "other")]:
                case = MatchCaseOp()
                case.guard.blocks.append()
                gblk = case.guard.blocks[0]
                gstk = gblk.add_argument(StackType.get(), Location.unknown())
                with InsertionPoint(gblk):
                    if opname == "true":
                        c = ConstOp(gstk)
                        c.operation.attributes["value"] = IntegerAttr.get(IntegerType.get_signless(64), 1)
                        YieldOp(c.out)
                    else:
                        g = PrimOp(gstk)
                        g.operation.attributes["op"] = StringAttr.get(opname)
                        YieldOp(g.out)
                case.body.blocks.append()
                bblk = case.body.blocks[0]
                bstk = bblk.add_argument(StackType.get(), Location.unknown())
                with InsertionPoint(bblk):
                    c = ConstOp(bstk)
                    c.operation.attributes["value"] = StringAttr.get(result)
                    YieldOp(c.out)
        YieldOp(m.out)
    assert module.operation.verify()
    s = str(module)
    assert s.count("rho.match_case") == 2
