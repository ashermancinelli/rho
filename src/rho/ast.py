"""AST nodes and string representation for Rho."""

from dataclasses import dataclass, fields
from typing import Union


def _to_tuple(x):
    """Recursively convert an AST node or collection to a tuple (for pprint)."""
    if hasattr(x, "to_tuple"):
        return x.to_tuple()
    if isinstance(x, (list, tuple)):
        return tuple(_to_tuple(e) for e in x)
    return x


class ASTNode:
    """Base for AST nodes. Subclasses must be @dataclass. Provides __len__, __getitem__, to_tuple from fields."""

    def __len__(self) -> int:
        return len(self.to_tuple())

    def __getitem__(self, i: int):
        return self.to_tuple()[i]

    def to_tuple(self):
        parts = [self.__class__.__name__]
        for f in fields(self.__class__):
            val = getattr(self, f.name)
            parts.append(_to_tuple(val))
        return tuple(parts)


@dataclass
class Lit(ASTNode):
    """Numeric literal (int or float)."""
    value: Union[int, float]

    def __str__(self) -> str:
        return f"Lit({self.value})"


@dataclass
class Word(ASTNode):
    """Identifier (variable or function name)."""
    name: str

    def __str__(self) -> str:
        return f"Word({self.name!r})"


@dataclass
class Primitive(ASTNode):
    """Built-in primitive (e.g. +, dup, swap)."""
    name: str

    def __str__(self) -> str:
        return f"Primitive({self.name!r})"


@dataclass
class Apply(ASTNode):
    """Stack application: sequence of expressions."""
    terms: list["Expr"]

    def __str__(self) -> str:
        inner = " ".join(str(t) for t in self.terms)
        return f"Apply({inner})"


@dataclass
class Fn(ASTNode):
    """Function: (params) body. Parens pop values off the stack and bind names.

    body is either a single Expr (inline) or a list of Expr (block).
    """
    params: list[str]
    body: Union["Expr", list["Expr"]]

    def __str__(self) -> str:
        params = " ".join(self.params)
        if isinstance(self.body, list):
            stmts = "; ".join(str(s) for s in self.body)
            return f"Fn(({params}) {{ {stmts} }})"
        return f"Fn(({params}) {self.body})"


@dataclass
class Drop(ASTNode):
    """Drop: '.' — discard top of stack (or used as fn body to discard params)."""

    def __str__(self) -> str:
        return "Drop()"


Expr = Union[Lit, Word, Primitive, Apply, Fn, Drop]


@dataclass
class Def(ASTNode):
    """Definition: name <- expression."""
    name: str
    body: Expr

    def __str__(self) -> str:
        return f"Def({self.name!r} <- {self.body})"


@dataclass
class Program(ASTNode):
    """Top-level program: list of definitions and optional trailing expression."""
    items: list[Union[Def, Expr]]

    def __str__(self) -> str:
        parts = [str(x) for x in self.items]
        return "Program(" + ", ".join(parts) + ")"


def ast_repr(program: Program) -> str:
    """Deterministic string representation of a Program for tests."""
    return str(program)


def ast_pprint(program: Program, indent: int = 2, width: int = 80) -> None:
    """Pretty-print a Program using the stdlib pprint module."""
    from pprint import pprint
    pprint(program.to_tuple(), indent=indent, width=width)
