"""Outline pass: extract nested rho.fn bodies to module-level rho.fn_def ops.

This is a rho-to-rho transform. After this pass, no rho.fn ops with inline
body regions remain — they are replaced by rho.fn_ref ops that reference
the outlined rho.fn_def by name.
"""

from mlir.ir import InsertionPoint, Location, StringAttr

from rho.mlir.dialect import (
    FnOp, FnDefOp, FnRefOp, StackType,
)

_fn_counter = 0


def outline_functions(op, pass_):
    """PassManager-compatible pass that outlines rho.fn bodies."""
    global _fn_counter

    module_block = op.regions[0].blocks[0]
    fns_to_outline = []

    def collect_fns(operation):
        for region in operation.regions:
            for block in region:
                for child_op in list(block):
                    if child_op.name == "rho.fn":
                        fns_to_outline.append(child_op)
                    collect_fns(child_op)

    collect_fns(op)

    for fn_op in fns_to_outline:
        fn_name = f"rho_fn_{_fn_counter}"
        _fn_counter += 1

        with InsertionPoint.at_block_begin(module_block):
            fn_def = FnDefOp()
            fn_def.operation.attributes["sym_name"] = StringAttr.get(fn_name)
            fn_op.regions[0].blocks[0].append_to(fn_def.body)

        with InsertionPoint(fn_op.operation):
            stk_operand = fn_op.operation.operands[0]
            fn_ref = FnRefOp(stk_operand)
            fn_ref.operation.attributes["sym_name"] = StringAttr.get(fn_name)

        fn_op.operation.results[0].replace_all_uses_with(fn_ref.out)
        fn_op.operation.erase()
