from mlir.ir import Context, Location, Module, InsertionPoint
from mlir.dialects.ext import Dialect
class DummyDialect(Dialect, name="repro"):
    pass
class MainOp(DummyDialect.Operation, name="main"):
    pass
def build_once() -> None:
    with Context(), Location.unknown():
        DummyDialect.load()
        module = Module.create()
        with InsertionPoint(module.body):
            MainOp()
        print(module)
        assert module.operation.verify()
build_once()
build_once()
'''
module {
  "repro.main"() : () -> ()
}
LLVM ERROR: repro.main created with unregistered dialect. If this is intended, please call allowUnregisteredDialects() on the MLIRContext, or use -allow-unregistered-dialect with the MLIR tool used.
[1]    372 abort      python repro.py
'''
