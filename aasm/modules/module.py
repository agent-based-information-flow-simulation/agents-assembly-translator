from __future__ import annotations

from typing import List, Dict, Tuple

from aasm.modules.instruction import Instruction
from aasm.modules.type import Type
from aasm.utils.exception import PanicException


class Target:
    def __init__(self, target: str):
        self.name = target

    def __repr__(self):
        return f"Target[{self.name}]"

    def __str__(self):
        return f"Target[{self.name}]"


class Module:
    def __init__(self, module_code_lines: List[str]):
        self.name = None
        # TODO: Change targets and types into classes
        self.targets: List[Target] = []
        self.types: List[Type] = []
        self.instructions: List[Instruction] = []
        self.preambles: Dict[str, List[str]] = {}
        self.impls: Dict[Tuple[str, str], List[str]] = {}
        self.description: List[str] = []

        self._in_targets = False
        self._in_instructions = False
        self._in_preamble = False
        self._in_impl = False
        self._in_init = False
        self._in_types = False
        self._in_description = False
        self._current_type = None
        self._current_target = None
        self._current_instruction = None

        self._parse_module_code(module_code_lines)
        # TODO: validate module -- check that all instructions are implemented for all targets, has a name etc.
        self._validate_module()

    def _validate_module(self):
        # has name
        if self.name is None:
            raise PanicException(
                "Error while loading unkown module",
                "Module has no name",
                "Please add a name to the module using !name",
            )
        # has at least one target
        if len(self.targets) == 0:
            raise PanicException(
                f"Error while loading module {self.name}",
                "Module has no targets",
                "Please add at least one target to the module using !targets",
            )

        # each type has an init for each target
        for type in self.types:
            for target in self.targets:
                if target.name not in type.init_lines:
                    raise PanicException(
                        f"Error while loading module {self.name}",
                        f"Type {type.name} has no init for target {target.name}",
                        "Please add an init for the target using !init [type] [target]",
                    )

        # each instruction has impl for each target
        for target in self.targets:
            for instruction in self.instructions:
                try:
                    self.impls[(target.name, instruction.opcode)]
                except KeyError:
                    raise PanicException(
                        f"Error while loading module {self.name}",
                        f"Instruction {instruction.opcode} has no impl for target {target.name}",
                        "Please add an impl for the target using !impl [instruction] [target]",
                    )

    def get_args_for_instruction(self, instruction_name: str) -> Dict[str, List[Type]]:
        for instruction in self.instructions:
            if instruction.opcode == instruction_name:
                return instruction.args_dict
        return {}

    def does_target(self, target: str) -> bool:
        return target in [target.name for target in self.targets]

    def _reset_scope(self):
        self._in_targets = False
        self._in_instructions = False
        self._in_preamble = False
        self._in_impl = False
        self._in_init = False
        self._in_types = False
        self._in_description = False
        self._current_target = None
        self._current_type = None
        self._current_instruction = None

    def _parse_module_code(self, lines: List[str]):
        for line in lines:
            tokens = line.strip().split()
            tokens = [token.strip().strip(",") for token in tokens]
            match tokens:
                case ["!name", name]:
                    self._reset_scope()
                    self.name = name
                case ["!types"]:
                    self._reset_scope()
                    self._in_types = True
                case ["!description"]:
                    self._reset_scope()
                    self._in_description = True
                case ["!targets"]:
                    self._reset_scope()
                    self._in_targets = True
                case ["!instructions"]:
                    self._reset_scope()
                    self._in_instructions = True
                case ["!preamble", target]:
                    self._reset_scope()
                    self._in_preamble = True
                    self._current_target = target
                case ["!impl", instruction, target]:
                    self._reset_scope()
                    self._in_impl = True
                    self._current_target = target
                    self._current_instruction = instruction
                case ["!init", type, target]:
                    self._reset_scope()
                    self._in_init = True
                    self._current_target = target
                    self._current_type = type
                case _:
                    if len(tokens) == 0:
                        continue
                    elif tokens[0].startswith("#"):
                        continue
                    elif tokens[0].startswith("!"):
                        raise PanicException(
                            "Invalid line: " + line,
                            "Unkown module directive",
                            "Only module directives can start with !",
                        )
                    elif self._in_targets:
                        if len(tokens) != 1:
                            raise PanicException(
                                "Invalid target line: " + line,
                                "Multiple tokens in target line",
                                "Target lines must have exactly one token: e.g. spade",
                            )
                        self.targets.append(Target(tokens[0]))
                    elif self._in_instructions:
                        if self.name is None:
                            raise PanicException(
                                "Invalid instruction line: " + line,
                                "Module name is undefined",
                                "Module name must be defined before instructions. Define module name with !name [name]",
                            )
                        else:
                            self.instructions.append(
                                Instruction(
                                    self.name, self.types, tokens[0], tokens[1:]
                                )
                            )
                    elif self._in_preamble:
                        if self._current_target is None:
                            raise PanicException(
                                "Invalid preamble line: Target is undefined: " + line,
                                "Target is undefined",
                                "Target must be defined before preamble. Define target with !preamble [target]",
                            )
                        self.preambles.setdefault(self._current_target, []).append(line)
                    elif self._in_impl:
                        if self._current_target is None:
                            raise PanicException(
                                "Invalid impl line: Target is undefined: " + line,
                                "Target is undefined",
                                "Target must be defined before impl. Define target with !impl [instruction] [target]",
                            )
                        if self._current_instruction is None:
                            raise PanicException(
                                "Invalid impl line: Instruction is undefined: " + line,
                                "Instruction is undefined",
                                "Instruction must be defined before impl. Define instruction with !impl [instruction] [target]",
                            )
                        self.impls.setdefault(
                            (self._current_target, self._current_instruction), []
                        ).append(line)
                    elif self._in_types:
                        if len(tokens) != 1:
                            raise PanicException(
                                "Invalid type line: " + line,
                                "Multiple tokens in type line",
                                "Type lines must have exactly one token: e.g. int64",
                            )
                        if self.name is None:
                            raise PanicException(
                                "Invalid instruction line: " + line,
                                "Module name is undefined",
                                "Module name must be defined before instructions. Define module name with !name [name]",
                            )
                        else:
                            self.types.append(Type(tokens[0], self.name))
                    elif self._in_init:
                        if self._current_target is None:
                            raise PanicException(
                                "Invalid init line: Target is undefined: " + line,
                                "Target is undefined",
                                "Target must be defined before init. Define target with !init [type] [target]",
                            )
                        if self._current_type is None:
                            raise PanicException(
                                "Invalid init line: Type is undefined: " + line,
                                "Type is undefined",
                                "Type must be defined before init. Define type with !init [type] [target]",
                            )
                        # find the type
                        found = False
                        for t in self.types:
                            if t.name == self._current_type:
                                t.add_init_line(self._current_target, line)
                                found = True
                                break
                        if not found:
                            raise PanicException(
                                "Invalid init line: Type is undefined: " + line,
                                f"Unkown type {self._current_type}",
                                "Type must be defined before init. Define type with !init [type] [target]",
                            )

                    elif self._in_description:
                        self.description.append(line)
                    else:
                        raise PanicException(
                            "Invalid line: " + line,
                            "Unkown line",
                            "Line is not a module directive, target, instruction, preamble or impl",
                        )

    def __repr__(self):
        return (
            f"Module[{self.name}] ("
            + repr(self.targets)
            + "\n"
            + repr(self.types)
            + "\n"
            + repr(self.instructions)
            + "\n"
            + repr(self.preambles)
            + "\n"
            + repr(self.impls)
            + ")"
        )

    def __str__(self):
        return (
            f"Module[{self.name}] (\n"
            + str(self.description)
            + "\n"
            + str(self.targets)
            + "\n"
            + str(self.types)
            + "\n"
            + str(self.instructions)
            + "\n"
            + str(self.preambles)
            + "\n"
            + str(self.impls)
            + ")"
        )
