from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.utils.validation import is_int

from aasm.intermediate.graph import InhomogenousRandomGraph

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_TYPES(state: State, types: str) -> None:
    state.require(
        state.in_graph, "Not inside any graph.", "SIZE can be used inside graphs."
    )
    state.require(
        isinstance(state.last_graph, InhomogenousRandomGraph),
        "TYPES can be used only in irg graphs.",
        "Define irg graphs with GRAPH irg.",
    )
    state.require(
        not state.last_graph.is_types_amount_defined(), "Types are already defined."
    )
    state.require(is_int(types), "Types must be an integer value.", "Example: TYPES 3")
    state.require(int(types) >= 0, "Types cannot be a negative number.")
    state.last_graph.set_types_amount(int(types))
