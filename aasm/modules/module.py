from __future__ import annotations

from typing import List

from aasm.modules.instruction import Instruction
from aasm.utils.exception import PanicException


class Module:
    def __init__(self, module_code_lines: List[str]):
        self.name = None
        self.targets: List[str] = []
        self.instructions: List[Instruction] = []
        self.preambles = {}
        self.impls = {}

        self._in_targets = False
        self._in_instructions = False
        self._in_preamble = False
        self._in_impl = False
        self._current_target = None
        self._current_instruction = None

        self._parse_module_code(module_code_lines)
        # TODO: validate module -- check that all instructions are implemented for all targets, has a name etc.
        # self._validate_module()

    def _reset_scope(self):
        self._in_targets = False
        self._in_instructions = False
        self._in_preamble = False
        self._in_impl = False
        self._current_target = None
        self._current_instruction = None

    def _parse_module_code(self, lines: List[str]):
        for line in lines:
            tokens = line.strip().split()
            match tokens:
                case ["!name", name]:
                    self.name = name
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
                    # FIX: change to PanicException
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
                        self.targets.append(tokens[0])
                    elif self._in_instructions:
                        if self.name is None:
                            raise PanicException(
                                "Invalid instruction line: " + line,
                                "Module name is undefined",
                                "Module name must be defined before instructions. Define module name with !name [name]",
                            )
                        else:
                            self.instructions.append(
                                Instruction(self.name, tokens[0], tokens[1:])
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
            + ", "
            + repr(self.instructions)
            + ", "
            + repr(self.preambles)
            + ", "
            + repr(self.impls)
            + ")"
        )

    def __str__(self):
        return (
            f"Module[{self.name}] ("
            + str(self.targets)
            + ", "
            + str(self.instructions)
            + ", "
            + str(self.preambles)
            + ", "
            + str(self.impls)
            + ")"
        )
