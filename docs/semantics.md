# Rho Semantics

## Values

Every value is a rank-polymorphic array. Scalars are rank-0 arrays. All primitives operate element-wise and broadcast, like APL/BQN/NumPy.

```
2 3 +
[1 2 3] 10 *
```

Strings are values. Arrays may contain scalars, arrays, strings, and functions.

## Stack

Rho is stack-based. Expressions push and pop values from an implicit operand stack.

- **Literal**: pushes one value.
- **Array literal**: pushes one array value.
- **Identifier**: loads a value; if it is a function, it is auto-called.
- **Quoted identifier** (`&name`): pushes the value without auto-calling it.
- **Primitive** (`+`, `-`, `*`, `/`): pops operands, pushes the result.
- **Drop** (`.`): pops and discards the top of the stack.
- **Function call**: implicit via identifier evaluation.

## Functions

A function is a list of parameter names and a body.

```
(a b) a b +
```

When called, the function:
1. Pops one value per parameter (rightmost param = top of stack).
2. Binds them in a new scope.
3. Evaluates the body.
4. Leaves the resulting stack for the caller.

Tacit functions work directly on the shared stack:

```
double <- dup +
sum3 <- + +
```

## Blocks

`{ stmts }` is a scope. Each statement pushes its result(s) onto the stack. When the block ends, all values remain on the stack.

## Definitions

```
name <- expr
```

Evaluates `expr`, pops the top of the stack, binds it to `name` in the current scope. The bound value is not left on the stack.

## Match

`match` evaluates guarded cases in order.

```
(n) match {
  { dup 0 > } { "greater than zero" printf }
  { true }    { "LE zero" printf }
}
```

Semantics:
- Each case is `{ guard_expr } { body_expr }`.
- The guard runs on the current stack.
- If the top of the resulting stack is truthy, that case matches.
- The body runs on the stack produced by the matching guard.
- The first truthy guard wins.
- If no guard matches, it is a runtime error.

A final `{ true } { ... }` case is the usual catch-all.

## Combinator Loops

Iteration is primarily expressed with array/range combinators.

```
10 iota 0 &plus fold
```

Here:
- `iota` pushes `[0, 1, ..., n-1]`
- `fold` requires an explicit initial accumulator
- `&plus` quotes the function value instead of calling it

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
