"""Shared MLIR context for the rho dialect.

The ``mlir.dialects.ext`` API is sensitive to context/dialect lifetime, so we
keep one long-lived ``Context`` for rho operations in-process.

We also register an ``atexit`` cleanup to close the context while Python still
owns the GIL. Without this, the MLIR bindings can abort during interpreter
finalization.
"""

import atexit

from mlir.ir import Context, Location

_ctx: Context | None = None


def _close_rho_context() -> None:
    global _ctx
    if _ctx is not None:
        try:
            _ctx.__exit__(None, None, None)
        finally:
            _ctx = None


atexit.register(_close_rho_context)


def get_rho_context() -> Context:
    global _ctx
    if _ctx is None:
        _ctx = Context()
        _ctx.__enter__()
        from rho.mlir.dialect import RhoDialect
        with Location.unknown(_ctx):
            RhoDialect.load()
    return _ctx
