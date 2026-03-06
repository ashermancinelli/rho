# Rho

Stack-based array programming language.

## Installation

Create a virtualenv and install the project editably (deps go into `.venv/`):

```bash
python3 -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
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

Has primitives from Forth.
Function syntax is sugar for popping arguments from the stack and pushing the result back.
