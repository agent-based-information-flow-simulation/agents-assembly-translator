from __future__ import annotations

from typing import TYPE_CHECKING, List

from aasm.intermediate.graph import (
    InhomogenousRandomGraph,
    InhomogeneousAgent,
    AgentConstantAmount,
    ConnectionConstantAmount,
)


from aasm.utils.validation import is_int, is_float

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_DEFTYPE(
    state: State, agent_name: str, amount: str, conn_amounts: List[str]
) -> None:
    state.require(state.agent_exists(agent_name), f"Agent {agent_name} is not defined.")
    state.require(
        not state.last_graph.is_agent_defined(agent_name),
        f"Agent {agent_name} is already defined.",
    )
    state.require(
        state.in_graph,
        "Cannot define agent type outside of graph scope.",
        "Try defining new graph using GRAPH.",
    )
    state.require(
        isinstance(state.last_graph, InhomogenousRandomGraph),
        "DEFTYPE can be used only in irg graphs.",
        "Define irg graphs with GRAPH irg.",
    )
    state.require(
        state.last_graph.is_types_amount_defined(),
        "The amount of types is not defined.",
        "Define the amount of types using TYPES.",
    )
    agent_amount: AgentConstantAmount | None = None
    state.require(is_int(amount), f"{amount} is not a valid integer.")
    agent_amount = AgentConstantAmount(amount)
    connection_amounts: List[ConnectionConstantAmount] = []
    state.require(
        len(conn_amounts) == state.last_graph.get_types_amount(),
        f"Amount of connection amounts ({len(conn_amounts)}) does not match the amount of types ({state.last_graph.get_types_amount()}).",
    )
    for conn_amount in conn_amounts:
        state.require(
            is_float(conn_amount), f"{conn_amount} is not a valid floating number."
        )
        state.require(
            float(conn_amount) >= 0,
            f"{conn_amount} is less than zero.",
            "Connection amounts must be between 0 and 100.",
        )
        state.require(
            float(conn_amount) <= 100,
            f"{conn_amount} is greater than 100.",
            "Connection amounts must be between 0 and 100.",
        )
        connection_amounts.append(ConnectionConstantAmount(conn_amount))

    state.last_graph.add_agent(
        InhomogeneousAgent(agent_name, agent_amount, connection_amounts)
    )
