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
        self._in_types = False
        self._in_description = False
        self._current_target = None
        self._current_instruction = None

        self._parse_module_code(module_code_lines)
        # TODO: validate module -- check that all instructions are implemented for all targets, has a name etc.
        # self._validate_module()

    def does_target(self, target: str) -> bool:
        return target in [target.name for target in self.targets]

    def _reset_scope(self):
        self._in_targets = False
        self._in_instructions = False
        self._in_preamble = False
        self._in_impl = False
        self._in_types = False
        self._in_description = False
        self._current_target = None
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
