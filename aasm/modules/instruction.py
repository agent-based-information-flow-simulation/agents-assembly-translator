from __future__ import annotations

from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from aasm.parsing.state import State


class Instruction:
    def __init__(self, opcode: str, args: List[str]):
        self.opcode = opcode
        self.args = args

    def op(self, state: State, arguments: List[str]) -> None:
        state.require(
            state.in_action,
            "Not inside any action.",
            f"{self.opcode} can be used inside actions.",
        )
        state.require(
            len(arguments) == len(self.args),
            f"Wrong number of arguments for {self.opcode}.",
            f"Expected {len(self.args)}, got {len(arguments)}.",
        )
