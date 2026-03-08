# Rho Syntax

ANSI-only. No Unicode symbols.

## Tokens

- **Numbers**: `0`, `42`, `3.14`
- **Identifiers**: `[a-zA-Z_][a-zA-Z0-9_]*`
- **Primitives**: `+`, `-`, `*`, `/`
- **Symbols**: `<-`, `(`, `)`, `{`, `}`
- **Whitespace**: spaces/tabs separate tokens; newlines separate statements

## Programs

A program is a sequence of **statements** separated by newlines.

```
stmt
stmt
...
```

## Statements

A statement is either a **definition** or an **expression**.

### Definitions

```
name <- expr
```

Evaluate `expr`, bind the result to `name` in the current scope.

### Expressions

A sequence of terms evaluated left to right. Each term pushes value(s) onto the stack; primitives pop operands and push results.

```
5 3 +       -- pushes 5, pushes 3, pops two and pushes 8
```

Terms: number literals, identifiers (push their value), primitives, or function calls.

## Functions

`(params) expr` or `(params) { stmts }`.

Parenthesized identifiers are sugar for popping values off the stack and naming them in the scope of the following expression or block.

```
(a b) a + b         -- single-expression function
(a b) {             -- block function
  a + b
}
```

There is no `->`. The parenthesized names are always followed by either a single expression or a `{ }` block.

Calling a function pops its parameters from the stack and pushes the result(s).

```
add <- (a b) a + b
3 5 add             -- pushes 8
```

## Blocks

`{ stmt; stmt; ... }` introduces a scope. Each statement can push values onto the stack. All pushed values remain on the stack when the block exits.

```
f <- (x) {
  x x *
  x +
}
3 f   -- pushes 9, then pushes 3+9=12... depends on stack discipline
```

## Scope

Names are lexically scoped. A block `{ }` introduces a child scope; definitions inside are not visible outside.
