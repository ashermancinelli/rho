"""Snake-case convenience builders for rho dialect ops.

Each function constructs the op, sets attributes, and returns the result
(!rho.stack SSA value) directly. This mirrors the pattern used by upstream
MLIR Python dialect wrappers (e.g. gpu.wait, scf.for_).
"""

from typing import Union, Callable

from mlir.ir import (
    InsertionPoint,
    IntegerAttr,
    IntegerType,
    FloatAttr,
    F64Type,
    Location,
    StringAttr,
)

from rho.mlir.dialect import (
    StackType,
    InitStackOp,
    ConstOp,
    MakeArrayOp,
    PrimOp,
    DupOp,
    SwapOp,
    OverOp,
    DropOp,
    DefOp,
    LoadOp,
    EvalOp,
    FnOp,
    CallOp,
    YieldOp,
    MatchOp,
    MatchCaseOp,
    MainOp,
)


def init_stack() -> "OpResult":
    return InitStackOp().out


def const(stk, value: Union[int, float, str]) -> "OpResult":
    c = ConstOp(stk)
    if isinstance(value, str):
        c.operation.attributes["value"] = StringAttr.get(value)
    elif isinstance(value, float):
        c.operation.attributes["value"] = FloatAttr.get(F64Type.get(), value)
    else:
        c.operation.attributes["value"] = IntegerAttr.get(
            IntegerType.get_signless(64), value
        )
    return c.out


def make_array(stk, count: int) -> "OpResult":
    m = MakeArrayOp(stk)
    m.operation.attributes["count"] = IntegerAttr.get(
        IntegerType.get_signless(64), count
    )
    return m.out


def prim(stk, op: str) -> "OpResult":
    p = PrimOp(stk)
    p.operation.attributes["op"] = StringAttr.get(op)
    return p.out


def dup(stk) -> "OpResult":
    return DupOp(stk).out


def swap(stk) -> "OpResult":
    return SwapOp(stk).out


def over(stk) -> "OpResult":
    return OverOp(stk).out


def drop(stk) -> "OpResult":
    return DropOp(stk).out


def def_(stk, name: str) -> "OpResult":
    d = DefOp(stk)
    d.operation.attributes["name"] = StringAttr.get(name)
    return d.out


def load(stk, name: str) -> "OpResult":
    l = LoadOp(stk)
    l.operation.attributes["name"] = StringAttr.get(name)
    return l.out


def eval_(stk, name: str) -> "OpResult":
    e = EvalOp(stk)
    e.operation.attributes["name"] = StringAttr.get(name)
    return e.out


def call(stk) -> "OpResult":
    return CallOp(stk).out


def yield_(stk) -> None:
    YieldOp(stk)


def fn(stk, body_builder: Callable[["OpResult"], "OpResult"]) -> "OpResult":
    """Build a rho.fn op. body_builder(stk) should emit ops and return the final stack."""
    f = FnOp(stk)
    f.body.blocks.append()
    blk = f.body.blocks[0]
    fn_stk = blk.add_argument(StackType.get(), Location.unknown())
    with InsertionPoint(blk):
        result_stk = body_builder(fn_stk)
        yield_(result_stk)
    return f.out


def match(stk, cases_builder: Callable[[], None]) -> "OpResult":
    """Build a rho.match op. cases_builder() should emit match_case ops."""
    m = MatchOp(stk)
    m.cases.blocks.append()
    with InsertionPoint(m.cases.blocks[0]):
        cases_builder()
    return m.out


def match_case(
    guard_builder: Callable[["OpResult"], "OpResult"],
    body_builder: Callable[["OpResult"], "OpResult"],
) -> None:
    """Build a rho.match_case op inside a match's cases region."""
    case_op = MatchCaseOp()

    case_op.guard.blocks.append()
    gblk = case_op.guard.blocks[0]
    gstk = gblk.add_argument(StackType.get(), Location.unknown())
    with InsertionPoint(gblk):
        result = guard_builder(gstk)
        yield_(result)

    case_op.body.blocks.append()
    bblk = case_op.body.blocks[0]
    bstk = bblk.add_argument(StackType.get(), Location.unknown())
    with InsertionPoint(bblk):
        result = body_builder(bstk)
        yield_(result)


def main(body_builder: Callable[["OpResult"], "OpResult"]) -> MainOp:
    """Build a rho.main op. body_builder(stk) receives init_stack result."""
    m = MainOp()
    m.body.blocks.append()
    blk = m.body.blocks[0]
    with InsertionPoint(blk):
        stk = init_stack()
        result_stk = body_builder(stk)
        yield_(result_stk)
    return m
