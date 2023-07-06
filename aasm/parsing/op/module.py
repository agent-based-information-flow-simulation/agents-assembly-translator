from __future__ import annotations

from typing import TYPE_CHECKING
from aasm.intermediate.module import Module
from aasm.utils.validation import is_valid_name, print_invalid_names

if TYPE_CHECKING:
    from aasm.parsing.state import State


def op_MODULE(state: State, name: str) -> None:
    state.require(
        not state.in_agent,
        "Cannot define modules inside agents.",
        "First end current agent using EAGENT.",
    )
    state.require(
        not state.in_graph,
        "Cannot define modules inside graphs.",
        "First end current graph using EGRAPH.",
    )
    state.require(
        not state.module_exists(name),
        f"Module {name} already exists in the current environment.",
    )

    state.require(
        state.module_is_loaded(name),
        f"Module {name} is not loaded.",
    )

    # NOTE: I don't think that's necessary for modules
    # state.require(
    #     is_valid_name(name),
    #     f"{name} is not a correct name.",
    #     f"Names can only contain alphanumeric characters, underscores and cannot be: {print_invalid_names()}.",
    # )
    state.add_module(Module(name))
