from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.utils.validation import is_int

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_MPARAMS(state: State, m0: str, m_inc: str) -> None:
    state.require(
        state.in_graph,
        "Not inside any graph",
        "MPARAMS can only be used inside graphs.",
    )
    state.require(not state.last_graph.is_m_defined(), "MPARAMS already defined.")
    state.require(is_int(m0) and is_int(m_inc), "MPARAMS must be integers.")
    m_begin = int(m0)
    m_increment = int(m_inc)
    state.require(m_begin >= 0 and m_increment >= 0, "MPARAMS must be non-negative.")

    state.last_graph.set_m((m_begin, m_increment))
