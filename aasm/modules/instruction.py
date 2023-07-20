from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict
from aasm.intermediate.argument import Argument
from aasm.modules.type import Type

from aasm.utils.exception import PanicException

from aasm.intermediate.argument import Mutable, Float, ModuleVariable
from aasm.intermediate.instruction import ModuleInstruction

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
        if opcode.endswith("*"):
            self.opcode = opcode[:-1]
            self.is_block = True
        else:
            self.opcode = opcode
            self.is_block = False
        self.available_types = available_types
        self.args_dict: Dict[str, List[str]] = {}
        self.arg_names = []
        self._parse_args(args)

    def _parse_args(self, args: List[str]):
        current_var_name = ""
        current_var_type = ""
        first_arg = True
        for arg in args:
            if arg.endswith(":"):
                if not first_arg:
                    self._validate_var_declaration(current_var_name)
                current_var_name = arg[:-1]
                self.arg_names.append(current_var_name)
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

        # print(f"Parsing arguments from self.args_dict: {self.args_dict} and arguments: {arguments}")
        parsed_args = [Argument(state, arg) for arg in arguments]
        state.require(
            self._validate_types_in_op_context(parsed_args),
            f"Mismatched types in the {self.module}::{self.opcode} context.: {[arg.explain() for arg in parsed_args]}",
            f"Refer to module documentation for further help.",
        )

        state.last_action.add_instruction(
            ModuleInstruction(parsed_args, self.opcode, self.module, self.is_block)
        )
        # for arg in parsed_args:
        #     arg.print()
        if self.is_block:
            state.last_action.start_block()

    def _validate_types_in_op_context(self, parsed_args) -> bool:
        arg_idx = 0
        types_to_check = []
        for arg in parsed_args:
            for arg_type in self.args_dict[self.arg_names[arg_idx]]:
                if arg_type == "mut":
                    types_to_check.append(Mutable)
                elif arg_type == "float":
                    types_to_check.append(Float)
                else:
                    new_type = arg.get_modvar_type(arg_type)
                    types_to_check.append(new_type)

            for arg_type in types_to_check:
                if not arg.has_type(arg_type):
                    return False
            arg.set_op_type(*types_to_check)
            arg_idx += 1

        return True

    def __str__(self) -> str:
        ret = f"{self.module}.{self.opcode}({', '.join(self.args_dict.keys())})"
        if self.is_block:
            ret += "[BLOCK]"
        return ret

    def __repr__(self) -> str:
        return str(self)
