from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.utils.validation import is_int
from aasm.intermediate.graph import InhomogenousRandomGraph

if TYPE_CHECKING:
    from aasm.parsing.state import State
    from typing import List


def op_ORDER(state: State, order: List[str]) -> None:
    state.require(
        state.in_graph, "Not inside any graph.", "SIZE can be used inside graphs."
    )
    state.require(
        isinstance(state.last_graph, InhomogenousRandomGraph),
        "ORDER can only be used inside IRG graphs.",
    )
    state.require(not state.last_graph.is_order_defined(), "Order is already defined")
    for agent in order:
        state.require(
            state.agent_exists(agent),
            f"Agent {agent} does not exist.",
            "First define the agent using AGENT.",
        )
    state.last_graph.set_order(order)
    # state.require(not state.last_graph.is_size_defined(), "Size is already defined")
    # state.require(is_int(size), "Graph size must be an integer value.")
    # state.require(int(size) >= 0, "Graph size cannot be a negative number.")

    # state.last_graph.set_size(int(size))
