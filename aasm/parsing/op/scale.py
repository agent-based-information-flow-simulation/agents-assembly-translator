from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.utils.validation import is_int

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_SCALE(state: State, scale: str) -> None:
    state.require(
        state.in_graph,
        "Not inside any graph",
        "Try defining new graph using GRAPH.",
    )
    state.require(not state.last_graph.is_scale_defined(), "Scale is already defined")
    state.require(is_int(scale), "Scale must be an integer")
    state.require(int(scale) > 0, "Scale must be greater than 0")
    state.last_graph.set_scale(int(scale))
