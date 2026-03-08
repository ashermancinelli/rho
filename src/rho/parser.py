"""Parser for Rho: tree-sitter CST -> AST conversion."""

from typing import Union

import tree_sitter_rho
from tree_sitter import Language, Parser as TSParser

from rho.ast import Apply, Array, Drop, Fn, Def, Expr, Lit, Primitive, Program, Str, Word


PRIMITIVES = {"+", "-", "*", "/", "dup", "swap", "drop", "over"}

_language = Language(tree_sitter_rho.language())


class ParseError(Exception):
    pass


def _text(node) -> str:
    return node.text.decode("utf-8")


def _convert_expression(node) -> Expr:
    """Convert a tree-sitter node to an AST Expr."""
    t = node.type

    if t == "number":
        raw = _text(node)
        return Lit(float(raw) if "." in raw else int(raw))

    if t == "identifier":
        name = _text(node)
        if name in PRIMITIVES:
            return Primitive(name)
        return Word(name)

    if t == "primitive":
        return Primitive(_text(node))

    if t == "apply":
        terms = [_convert_expression(c) for c in node.named_children]
        return Apply(terms=terms)

    if t == "string":
        raw = _text(node)
        # Strip surrounding quotes and process escapes
        inner = raw[1:-1].replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\").replace('\\"', '"').replace("\\0", "\0")
        return Str(value=inner)

    if t == "array":
        elems = [_convert_expression(c) for c in node.named_children]
        return Array(elems=elems)

    if t == "drop":
        return Drop()

    if t == "fn":
        params: list[str] = []
        body: Expr | list[Expr] | None = None
        for child in node.named_children:
            if child.type == "param":
                for ident in child.named_children:
                    params.append(_text(ident))
            elif child.type == "block":
                body = _convert_block(child)
            else:
                body = _convert_expression(child)
        if body is None:
            raise ParseError("fn has no body")
        return Fn(params=params, body=body)

    raise ParseError(f"unexpected node type: {t}")


def _convert_block(node) -> list[Expr]:
    """Convert a block node to a list of statements."""
    return [_convert_expression(child) for child in node.named_children]


def _convert_statement(node) -> Union[Def, Expr]:
    """Convert a top-level statement node."""
    if node.type == "definition":
        name_node = node.child_by_field_name("name")
        body_node = node.child_by_field_name("body")
        if name_node is None or body_node is None:
            raise ParseError("malformed definition")
        return Def(name=_text(name_node), body=_convert_expression(body_node))
    return _convert_expression(node)


def parse(source: str) -> Program:
    """Parse Rho source into a Program AST using tree-sitter."""
    parser = TSParser(_language)
    tree = parser.parse(source.encode("utf-8"))
    root = tree.root_node

    if root.has_error:
        for child in root.children:
            if child.is_error or child.is_missing:
                line = child.start_point[0] + 1
                col = child.start_point[1] + 1
                raise ParseError(f"syntax error at line {line} col {col}")
        raise ParseError("syntax error")

    items: list[Def | Expr] = []
    for child in root.named_children:
        if child.type == "comment":
            continue
        items.append(_convert_statement(child))
    return Program(items=items)
