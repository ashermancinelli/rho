"""Rho MLIR dialect: types and operations defined via mlir.dialects.ext.

Values are SSA (!rho.value). The stack is resolved at AST->MLIR time:
each AST node that pushes produces a !rho.value result, and each node
that pops takes a !rho.value operand.
"""

from mlir.ir import *
from mlir.dialects.ext import *


class RhoDialect(Dialect, name="rho"):
    pass


# -- Types --

class ValueType(RhoDialect.Type, name="value"):
    """Single-word tagged value (OCaml-style: immediate int or heap pointer)."""
    pass


# -- Ops: constants --

class ConstOp(RhoDialect.Operation, name="const"):
    """Produce a constant value. Use one of: IntegerAttr, FloatAttr, StringAttr."""
    out: Result[ValueType[()]]


class MakeArrayOp(RhoDialect.Operation, name="make_array"):
    """Construct an array from N element values."""
    out: Result[ValueType[()]]


# -- Ops: primitives --

class PrimOp(RhoDialect.Operation, name="prim"):
    """Apply a binary primitive (+, -, *, /) element-wise with broadcast.

    Attribute "op" is the primitive name string.
    """
    lhs: Operand[ValueType]
    rhs: Operand[ValueType]
    out: Result[ValueType[()]]


# -- Ops: stack manipulation --

class DupOp(RhoDialect.Operation, name="dup"):
    """Duplicate a value (identity — both results alias the input)."""
    in_: Operand[ValueType]
    out1: Result[ValueType[()]]
    out2: Result[ValueType[()]]


class SwapOp(RhoDialect.Operation, name="swap"):
    """Swap two values (pass-through — reorder in SSA)."""
    a: Operand[ValueType]
    b: Operand[ValueType]
    out_b: Result[ValueType[()]]
    out_a: Result[ValueType[()]]


class OverOp(RhoDialect.Operation, name="over"):
    """Copy the second value over the top."""
    a: Operand[ValueType]
    b: Operand[ValueType]
    out_a: Result[ValueType[()]]
    out_b: Result[ValueType[()]]
    out_a2: Result[ValueType[()]]


class DropOp(RhoDialect.Operation, name="drop"):
    """Discard a value."""
    in_: Operand[ValueType]


# -- Ops: names / scope --

class DefOp(RhoDialect.Operation, name="def"):
    """Bind a value to a name in the current scope (consumed, not on stack)."""
    val: Operand[ValueType]


class LoadOp(RhoDialect.Operation, name="load"):
    """Load a named value from scope."""
    out: Result[ValueType[()]]


# -- Ops: functions --

class FnOp(RhoDialect.Operation, name="fn"):
    """Define a function (closure). Body region takes N params, yields results."""
    body: Region
    out: Result[ValueType[()]]


class CallOp(RhoDialect.Operation, name="call"):
    """Call a function value, passing N arguments, producing M results."""
    callee: Operand[ValueType]


class YieldOp(RhoDialect.Operation, name="yield", traits=[IsTerminatorTrait]):
    """Terminate a function body, yielding values back to caller."""
    pass


# -- Ops: entry point --

class MainOp(RhoDialect.Operation, name="main"):
    """Program entry point with a body region."""
    body: Region
