"""Interactive REPL that compiles Rho source, then lowers rho dialect to upstream MLIR."""

from rho.parser import parse
from rho.mlir.codegen import compile_program
from rho.mlir.context import get_rho_context
from rho.mlir.lower import convert_rho_to_runtime
from rho.repl import run_repl

from mlir.ir import Location
from mlir.passmanager import PassManager


def _handle(text: str) -> None:
    ctx = get_rho_context()
    with Location.unknown(ctx):
        module = compile_program(parse(text))
        print("=== rho dialect ===")
        print(module)

        pm = PassManager()
        pm.add(convert_rho_to_runtime)
        pm.run(module.operation)

        print("=== lowered ===")
        print(module)


def main() -> None:
    run_repl("rho lower-repl  (Ctrl-D to exit)", _handle)


if __name__ == "__main__":
    main()
