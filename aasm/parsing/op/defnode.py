from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.intermediate.graph import AdjRow, MatrixAgent, MatrixGraph

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_DEFNODE(state: State, agent_name: str, agent_row: str) -> None:
    state.require(state.agent_exists(agent_name), f"Agent {agent_name} is not defined.")
    state.require(
        state.in_graph,
        "Cannot define agent node outside of graph scope.",
        "Try defining new graph using GRAPH.",
    )
    state.require(
        isinstance(state.last_graph, MatrixGraph),
        "DEFNODE can be used only in matrix graphs.",
        "Define matrix graphs with GRAPH matrix.",
    )
    state.require(
        agent_row.startswith("R"), "Agent Row must start with R", "Example: R101"
    )
    row = agent_row[1:]
    row = [int(x) for x in row]
    adj_row = AdjRow(row)

    state.last_graph.add_agent(MatrixAgent(agent_name, adj_row))
