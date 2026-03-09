# Rho Syntax

ANSI-only. No Unicode symbols.

## Tokens

- **Numbers**: `0`, `42`, `3.14`
- **Strings**: `"hello"`, `"hello\nworld"`
- **Identifiers**: `[a-zA-Z_][a-zA-Z0-9_]*`
- **Primitives**: `+`, `-`, `*`, `/`
- **Quote**: `&name` pushes a value without calling it
- **Drop**: `.`
- **Symbols**: `<-`, `(`, `)`, `[`, `]`, `{`, `}`, `;`
- **Whitespace**: spaces/tabs separate tokens; newlines or `;` separate statements

## Programs

A program is a sequence of **statements** separated by newlines or semicolons.

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
5 3 +
```

Terms: literals, arrays, quoted names, identifiers, primitives, functions, `match` expressions, or `.`.

## Functions

`(params) expr` or `(params) { stmts }`.

Parenthesized identifiers are sugar for popping values off the stack and naming them in the scope of the following expression or block.

```
(a b) a b +
(a b) {
  a b +
}
```

There is no `->`.

Calling a function pops its parameters from the stack and pushes the result(s).

```
add <- (a b) a b +
3 5 add
```

Use `&name` to push a function (or other value) without auto-calling it.

```
10 iota 0 &plus fold
```

Words like `iota` and `fold` are ordinary names, typically provided by the runtime or standard library, not special syntax.

## Arrays

Square brackets create array literals.

```
[1 2 3]
[[1 2] [3 4]]
```

## Blocks

`{ stmt; stmt; ... }` introduces a scope. Each statement can push values onto the stack. All pushed values remain on the stack when the block exits.

## Match

`match` evaluates guarded cases in order.

```
(n) match {
  { dup 0 > } { "greater than zero" printf }
  { true }    { "LE zero" printf }
}
```

Each case is `{ guard_expr } { body_expr }`.

The values named by the leading `( ... )` seed a fresh mini-stack for each case.
The guard runs first. If its top value is truthy, that truth value is removed and
its remaining mini-stack is passed to the body.

## Scope

Names are lexically scoped. A block `{ }` introduces a child scope; definitions inside are not visible outside.
