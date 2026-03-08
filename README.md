# Rho

Stack-based array programming language.

## Installation

```bash
uv venv .venv --seed --python 3.13
source .venv/bin/activate
pip install -e .
```

To run tests: `pytest`

For MLIR support (dialect, codegen, lowering tests), install the optional deps from the LLVM index:

```bash
pip install -e ".[mlir]" -f https://llvm.github.io/eudsl
```

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
