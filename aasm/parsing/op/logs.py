from __future__ import annotations

from typing import TYPE_CHECKING, List

from aasm.intermediate.argument import Argument
from aasm.intermediate.instruction import (
    LogsCritical,
    LogsDebug,
    LogsError,
    LogsInfo,
    LogsWarning,
)
from aasm.utils.validation import print_valid_logs_levels

if TYPE_CHECKING:
    from parsing.state import State


def op_LOGS(state: State, level: str, args: List[str]) -> None:
    state.require(
        state.in_action, "Not inside any action", f"LOGS can be used inside actions."
    )

    intermediate_args: List[Argument] = []
    for arg in [Argument(state, arg) for arg in args]:
        intermediate_args.extend(arg.create_all_possible_types(state))

    match level:
        case "debug":
            state.last_action.add_instruction(LogsDebug(intermediate_args))

        case "info":
            state.last_action.add_instruction(LogsInfo(intermediate_args))

        case "warning":
            state.last_action.add_instruction(LogsWarning(intermediate_args))

        case "error":
            state.last_action.add_instruction(LogsError(intermediate_args))

        case "critical":
            state.last_action.add_instruction(LogsCritical(intermediate_args))

        case _:
            state.panic(
                f"Unexpected error: LOGS {level} {args}",
                f"Supported LOGS levels are: {print_valid_logs_levels()}",
            )
