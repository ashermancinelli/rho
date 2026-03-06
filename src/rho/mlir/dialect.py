"""Rho MLIR dialect: types and operations defined via mlir.dialects.ext."""

from mlir.ir import *
from mlir.dialects.ext import *


class RhoDialect(Dialect, name="rho"):
    pass


class ValueType(RhoDialect.Type, name="value"):
    """Single-word value type (OCaml-style tagged value)."""
    pass


class ConstOp(RhoDialect.Operation, name="const"):
    """rho.const: integer constant -> value (tagged immediate)."""
    value: int  # attribute
    out: Result[ValueType[()]]


class AddOp(RhoDialect.Operation, name="add"):
    """rho.add: add two values (both must be immediates for now)."""
    lhs: Operand[ValueType]
    rhs: Operand[ValueType]
    result: Result[ValueType[()]]


class MainOp(RhoDialect.Operation, name="main"):
    """rho.main: entry point with a body region."""
    body: Region
