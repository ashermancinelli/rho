# Rho Semantics

## Values

Every value is a rank-polymorphic array. Scalars are rank-0 arrays. All primitives operate element-wise and broadcast, like APL/BQN/NumPy.

```
2 3 +         -- 5 (scalar + scalar)
[1 2 3] 10 *  -- [10 20 30] (array * scalar, broadcast)
```

## Stack

Rho is stack-based. Expressions push and pop values from an implicit operand stack.

- **Literal**: pushes one value.
- **Identifier**: pushes the value bound to that name.
- **Primitive** (`+`, `-`, `*`, `/`): pops two values, pushes the result (element-wise, rank-polymorphic).
- **Function call**: pops N values (one per parameter), executes body, pushes result(s).

## Functions

A function is a pair: a list of parameter names and a body (expression or block).

```
(a b) a + b
```

When called, the function:
1. Pops one value per parameter (rightmost param = top of stack).
2. Binds them in a new scope.
3. Evaluates the body.
4. All values left on the stack by the body are pushed back to the caller's stack.

## Blocks

`{ stmts }` is a scope. Each statement pushes its result(s) onto the stack. When the block ends, **all values remain** on the stack.

```
f <- (x) {
  x x *
  1 +
}
```

`x x *` pushes `x*x`; `1 +` pops `x*x` and `1`, pushes `x*x + 1`.

## Definitions

```
name <- expr
```

Evaluates `expr`, pops the top of the stack, binds it to `name` in the current scope. The value is **not** left on the stack.

## Machine Representation

OCaml-style tagged values. Every value is one 64-bit word:

- **Immediate** (low bit = 1): small integer `(n << 1) | 1`.
- **Pointer** (low bit = 0): points to a heap block.

Heap block: header word (tag byte + size) then payload words.

| Tag | Kind | Scannable |
|-----|------|-----------|
| 0 | tuple/record | yes |
| 1 | array | yes |
| 2 | closure | yes |
| 251 | float | no |
| 252 | string | no |

GC uses the tag to decide which payload words to trace.
