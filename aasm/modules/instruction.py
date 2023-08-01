from __future__ import annotations

from typing import TYPE_CHECKING, List as TypingList, Dict
from aasm.intermediate.argument import Argument
from aasm.modules.type import Type

from aasm.utils.exception import PanicException

from aasm.intermediate.argument import (
    Mutable,
    Float,
    Enum,
    EnumValue,
    ConnectionList,
    MessageList,
    FloatList,
    List,
    Connection,
    Literal,
    Message,
)
from aasm.intermediate.instruction import ModuleInstruction

if TYPE_CHECKING:
    from aasm.parsing.state import State

from pprint import pprint


class Instruction:
    def __init__(
        self,
        module_name: str,
        available_types: TypingList[Type],
        opcode: str,
        args: TypingList[str],
    ):
        self.module = module_name
        if opcode.endswith("*"):
            self.opcode = opcode[:-1]
            self.is_block = True
        else:
            self.opcode = opcode
            self.is_block = False
        self.available_types = [
            Type("mut", "base"),
            Type("float", "base"),
            Type("enum", "base"),
            Type("enum_val", "base"),
            Type("list_conn", "base"),
            Type("list_msg", "base"),
            Type("list_float", "base"),
            Type("list", "base"),
            Type("conn", "base"),
            Type("literal", "base"),
            Type("msg", "base"),
        ]
        self.available_types.extend(available_types)
        self.args_dict: Dict[str, TypingList[str]] = {}
        self.arg_names = []
        self._parse_args(args)
        self._validate_args_dict()

        print("\n")
        print(f"Instruction {self.opcode} created with:")
        pprint(self.args_dict)
        print("\n")

    def _validate_args_dict(self):
        # ensure that at most one argument is mutable
        mutable_count = 0
        for arg_name in self.args_dict.keys():
            for arg_type in self.args_dict[arg_name]:
                if arg_type == "mut":
                    mutable_count += 1
        if mutable_count > 1:
            raise PanicException(
                f"Error in module {self.module}, instruction {self.opcode}.",
                f"Instruction {self.opcode} has more than one mutable argument.",
                "Ensure that at most one argument is mutable.",
            )
        elif mutable_count == 1 and self.is_block:
            raise PanicException(
                f"Error in module {self.module}, instruction {self.opcode}.",
                f"Instruction {self.opcode} is a block instruction and cannot have a mutable argument.",
                "Remove the mutable argument.",
            )

    def _parse_args(self, args: TypingList[str]):
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

        if len(self.args_dict[current_var_name]) > 1:
            if "mut" not in self.args_dict[current_var_name]:
                raise PanicException(
                    f"Error in module {self.module}, instruction {self.opcode}. Variable {current_var_name} cannot have multiple types.",
                    f"Variable {current_var_name} cannot have multiple types.",
                    "Specify only one type for the variable.",
                )
        # verify that the types associated with current_var_name are valid
        for var_type in self.args_dict[current_var_name]:
            if var_type not in [tmp_type.name for tmp_type in self.available_types]:
                raise PanicException(
                    f"Error in module {self.module}, instruction {self.opcode}. Type {var_type} is not defined.",
                    f"Type {var_type} is not defined.",
                    "Define the type.",
                )

    def op(self, state: State, arguments: TypingList[str]) -> None:
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
        for arg in parsed_args:
            types_to_check = []
            print(f"\nChecking arg: {arg.explain()}")
            for arg_type in self.args_dict[self.arg_names[arg_idx]]:
                if arg_type == "mut":
                    types_to_check.append(Mutable)
                elif arg_type == "float":
                    types_to_check.append(Float)
                elif arg_type == "enum":
                    types_to_check.append(Enum)
                elif arg_type == "enum_val":
                    types_to_check.append(EnumValue)
                elif arg_type == "list_conn":
                    types_to_check.append(List)
                    types_to_check.append(ConnectionList)
                elif arg_type == "list_msg":
                    types_to_check.append(List)
                    types_to_check.append(MessageList)
                elif arg_type == "list_float":
                    types_to_check.append(List)
                    types_to_check.append(FloatList)
                elif arg_type == "list":
                    types_to_check.append(List)
                elif arg_type == "conn":
                    types_to_check.append(Connection)
                elif arg_type == "literal":
                    types_to_check.append(Literal)
                elif arg_type == "msg":
                    types_to_check.append(Message)
                else:
                    new_type = arg.get_modvar_type(arg_type)
                    types_to_check.append(new_type)

            print(f"Checking types: {types_to_check} for arg: {arg.explain()}")
            for arg_type in types_to_check:
                if not arg.has_type(arg_type):
                    print(f"{arg_type} Failed!")
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
