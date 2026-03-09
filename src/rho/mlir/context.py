"""Shared MLIR context for the rho dialect.

The mlir.dialects.ext API is sensitive to context/dialect lifetime, so we keep
one long-lived Context for rho operations in-process.
"""

from mlir.ir import Context, Location

_ctx: Context | None = None


def get_rho_context() -> Context:
    global _ctx
    if _ctx is None:
        _ctx = Context()
        _ctx.__enter__()
        from rho.mlir.dialect import RhoDialect
        with Location.unknown(_ctx):
            RhoDialect.load()
    return _ctx
