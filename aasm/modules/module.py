from __future__ import annotations

from typing import List


class Instruction:
    def __init__(self, identifier: str, args: List[str]):
        self.identifier = identifier
        self.args = args


class Module:
    def __init__(self, module_code_lines: List[str]):
        self.targets = []
        self.instructions = []
        self.preambles = {}
        self.impls = {}

        self._in_targets = False
        self._in_instructions = False
        self._in_preamble = False
        self._in_impl = False
        self._current_target = None
        self._current_instruction = None

        self._parse_module_code(module_code_lines)

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
                case ["%targets"]:
                    self._reset_scope()
                    self._in_targets = True
                case ["%instructions"]:
                    self._reset_scope()
                    self._in_instructions = True
                case ["%preamble", target]:
                    self._reset_scope()
                    self._in_preamble = True
                    self._current_target = target
                case ["%impl", instruction, target]:
                    self._reset_scope()
                    self._in_impl = True
                    self._current_target = target
                    self._current_instruction = instruction
                case _:
                    if len(tokens) == 0:
                        continue
                    elif self._in_targets:
                        if len(tokens) != 1:
                            raise Exception("Invalid target line: " + line)
                        self.targets.append(tokens[0])
                    elif self._in_instructions:
                        self.instructions.append(Instruction(tokens[0], tokens[1:]))
                    elif self._in_preamble:
                        if self._current_target is None:
                            raise Exception(
                                "Invalid preamble line: Target is undefined: " + line
                            )
                        self.preambles.setdefault(self._current_target, []).append(line)
                    elif self._in_impl:
                        if self._current_target is None:
                            raise Exception(
                                "Invalid impl line: Target is undefined: " + line
                            )
                        if self._current_instruction is None:
                            raise Exception(
                                "Invalid impl line: Instruction is undefined: " + line
                            )
                        self.impls.setdefault(
                            (self._current_target, self._current_instruction), []
                        ).append(line)
                    else:
                        raise Exception("Invalid line: " + line)

    def __repr__(self):
        return (
            "Module("
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
            "Module("
            + str(self.targets)
            + ", "
            + str(self.instructions)
            + ", "
            + str(self.preambles)
            + ", "
            + str(self.impls)
            + ")"
        )
