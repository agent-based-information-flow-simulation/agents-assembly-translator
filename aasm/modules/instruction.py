from __future__ import annotations

from typing import TYPE_CHECKING, List
from aasm.intermediate.argument import Argument
from aasm.modules.type import Type

from aasm.utils.exception import PanicException


if TYPE_CHECKING:
    from aasm.parsing.state import State


class Instruction:
    def __init__(
        self,
        module_name: str,
        available_types: List[Type],
        opcode: str,
        args: List[str],
    ):
        self.module = module_name
        self.opcode = opcode
        self.available_types = available_types
        self._parse_args(args)
        self.args_dict = {}

    def _parse_args(self, args: List[str]):
        print(f"Parsing args for: {self.opcode}")
        current_var_name = ""
        current_var_type = ""
        self.args_dict = {}
        first_arg = True
        for arg in args:
            print(arg)
            if arg.endswith(":"):
                current_var_name = arg[:-1]
                current_var_type = ""
                # verify that the variable name is not already used
                if current_var_name in self.args_dict:
                    raise PanicException(
                        f"Error in module {self.module}, instruction {self.opcode}. Variable {current_var_name} already defined.",
                        f"Variable {current_var_name} is already defined.",
                        "Rename the variable.",
                    )
                self.args_dict[current_var_name] = []
                first_arg = False
            else:
                current_var_type = arg
                self.args_dict[current_var_name].append(current_var_type)
        print("\n")
        print(self.args_dict)
        print("\n")

    def _validate_var_declaration(self, current_var_name: str):
        if len(self.args_dict[current_var_name]) == 0:
            raise PanicException(
                f"Error in module {self.module}, instruction {self.opcode}. Missing type for variable {current_var_name}.",
                f"Variable {current_var_name} has no type specified.",
                "Specify a type for the variable.",
            )
        # verify that the types associated with current_var_name are valid
        for var_type in self.args_dict[current_var_name]:
            if var_type not in [tmp_type.name for tmp_type in self.available_types]:
                raise PanicException(
                    f"Error in module {self.module}, instruction {self.opcode}. Type {var_type} is not defined.",
                    f"Type {var_type} is not defined.",
                    "Define the type.",
                )

    def op(self, state: State, arguments: List[str]) -> None:
        state.require(
            state.in_action,
            "Not inside any action.",
            f"{self.opcode} can be used inside actions.",
        )
        state.require(
            len(arguments) == len(self.args_dict.keys()),
            f"Wrong number of arguments for {self.opcode}.",
            f"Expected {len(self.args_dict.keys())}, got {len(arguments)}.",
        )

        print(self.args_dict)

        parsed_args = [Argument(state, arg) for arg in arguments]

        for arg in parsed_args:
            arg.print()

    def __str__(self) -> str:
        return f"{self.module}.{self.opcode}({', '.join(self.args_dict.keys())})"

    def __repr__(self) -> str:
        return str(self)
