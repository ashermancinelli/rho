"""AST nodes and string representation for Rho."""

from dataclasses import dataclass
from typing import Union


# Expression nodes
@dataclass
class Lit:
    """Numeric literal (int or float)."""
    value: Union[int, float]

    def __str__(self) -> str:
        if isinstance(self.value, float):
            return f"Lit({self.value})"
        return f"Lit({self.value})"


@dataclass
class Word:
    """Identifier (variable or function name)."""
    name: str

    def __str__(self) -> str:
        return f"Word({self.name!r})"


@dataclass
class Primitive:
    """Built-in primitive (e.g. +, dup, swap)."""
    name: str

    def __str__(self) -> str:
        return f"Primitive({self.name!r})"


@dataclass
class Apply:
    """Stack application: sequence of expressions (first pushed first, then applied)."""
    terms: list["Expr"]

    def __str__(self) -> str:
        inner = " ".join(str(t) for t in self.terms)
        return f"Apply({inner})"


@dataclass
class Lambda:
    """Lambda: (params) -> body."""
    params: list[str]
    body: "Expr"

    def __str__(self) -> str:
        params = " ".join(self.params)
        return f"Lambda(({params}) -> {self.body})"


@dataclass
class Block:
    """Block: (params) { stmts }."""
    params: list[str]
    stmts: list["Expr"]

    def __str__(self) -> str:
        params = " ".join(self.params)
        stmts = "; ".join(str(s) for s in self.stmts)
        return f"Block(({params}) {{ {stmts} }})"


Expr = Union[Lit, Word, Primitive, Apply, Lambda, Block]


@dataclass
class Def:
    """Definition: name <- expression."""
    name: str
    body: Expr

    def __str__(self) -> str:
        return f"Def({self.name!r} <- {self.body})"


@dataclass
class Program:
    """Top-level program: list of definitions and optional trailing expression."""
    items: list[Union[Def, Expr]]

    def __str__(self) -> str:
        parts = [str(x) for x in self.items]
        return "Program(" + ", ".join(parts) + ")"


def ast_repr(program: Program) -> str:
    """Deterministic string representation of a Program for tests."""
    return str(program)
