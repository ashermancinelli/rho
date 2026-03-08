# Rho

Stack-based array programming language.

## Installation

With uv (recommended — finds MLIR packages automatically via `[tool.uv]`):

```bash
uv venv .venv --seed --python 3.13
source .venv/bin/activate
uv pip install -e . -e src/tree-sitter-rho
```

With plain pip (need `-f` for the MLIR index):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e . -e src/tree-sitter-rho -f https://llvm.github.io/eudsl
```

To run tests: `pytest`

```
> f <- + +
> 5 5 5 f
15
> f <- (a b c) -> a + b + c
> 5 5 5 f
15
> f <- (a b c) {
    a + b + c
}
> 5 5 5 f
15
```
