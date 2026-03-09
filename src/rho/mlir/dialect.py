"""Rho MLIR dialect: types and operations defined via mlir.dialects.ext.

The stack is threaded as an SSA value (!rho.stack). Every op takes the
current stack and produces a new one. Functions receive and return the
stack — no explicit arity.
"""

from mlir.ir import *
from mlir.dialects.ext import *


class RhoDialect(Dialect, name="rho"):
    pass


# -- Types --

class StackType(RhoDialect.Type, name="stack"):
    """Operand stack threaded through all ops."""
    pass


class ValueType(RhoDialect.Type, name="value"):
    """Single-word tagged value (OCaml-style: immediate int or heap pointer)."""
    pass


# -- Ops: stack creation --

class InitStackOp(RhoDialect.Operation, name="init_stack"):
    """Create an empty stack."""
    out: Result[StackType[()]]


# -- Ops: constants --

class ConstOp(RhoDialect.Operation, name="const"):
    """Push a constant onto the stack. Attribute "value" is IntegerAttr, FloatAttr, or StringAttr."""
    stk: Operand[StackType]
    out: Result[StackType[()]]


# -- Ops: arrays --

class MakeArrayOp(RhoDialect.Operation, name="make_array"):
    """Pop N elements from the stack, push an array. Attribute "count" is the number of elements."""
    stk: Operand[StackType]
    out: Result[StackType[()]]


# -- Ops: primitives --

class PrimOp(RhoDialect.Operation, name="prim"):
    """Pop operands, apply primitive, push result. Attribute "op" is the primitive name."""
    stk: Operand[StackType]
    out: Result[StackType[()]]


# -- Ops: drop --

class DropOp(RhoDialect.Operation, name="drop"):
    """Discard the top of the stack."""
    stk: Operand[StackType]
    out: Result[StackType[()]]


# -- Ops: names / scope --

class DefOp(RhoDialect.Operation, name="def"):
    """Pop the top of the stack, bind to a name. Attribute "name" is the identifier."""
    stk: Operand[StackType]
    out: Result[StackType[()]]


class LoadOp(RhoDialect.Operation, name="load"):
    """Push a named value onto the stack (no call). Attribute "name" is the identifier."""
    stk: Operand[StackType]
    out: Result[StackType[()]]


class EvalOp(RhoDialect.Operation, name="eval"):
    """Load a named value; if it's a function, call it. Attribute "name" is the identifier."""
    stk: Operand[StackType]
    out: Result[StackType[()]]


# -- Ops: functions --

class FnOp(RhoDialect.Operation, name="fn"):
    """Push a closure onto the stack. Body region takes and yields !rho.stack."""
    stk: Operand[StackType]
    body: Region
    out: Result[StackType[()]]


class CallOp(RhoDialect.Operation, name="call"):
    """Pop a function from the stack and call it. The function receives and returns the stack."""
    stk: Operand[StackType]
    out: Result[StackType[()]]


class YieldOp(RhoDialect.Operation, name="yield", traits=[IsTerminatorTrait]):
    """Terminate a function/main body, yielding the stack."""
    stk: Operand[StackType]


class MatchCaseOp(RhoDialect.Operation, name="match_case"):
    """A single guarded match case.

    The guard region receives a fresh mini-stack seeded from the match inputs and
    must yield a stack whose top is a truth value. If truthy, that top value is
    popped and the body region receives the remaining guard-produced mini-stack.
    The body yields a stack, of which only the top value escapes back to the
    outer stack.
    """
    guard: Region
    body: Region


class MatchOp(RhoDialect.Operation, name="match", traits=[NoTerminatorTrait]):
    """Evaluate guarded match cases against a mini-stack seeded from current inputs.

    Takes the outer stack, evaluates cases in order, and pushes one resulting
    value (the top of the selected body stack) back onto the outer stack.
    """
    stk: Operand[StackType]
    cases: Region
    out: Result[StackType[()]]


# -- Ops: entry point --

class MainOp(RhoDialect.Operation, name="main"):
    """Program entry point. Body region takes and yields !rho.stack."""
    body: Region
