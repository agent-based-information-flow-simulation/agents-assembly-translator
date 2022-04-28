from __future__ import annotations

from typing import List
from aasm.preprocessor.preprocessor_item import PreprocessorItem


class Macro(PreprocessorItem):
    def __init__(self, signature):
        super().__init__(signature)
        self.lines = []
        self.argument_names = []
        self.name = ""

    def expand(self, macro_args: List[str]) -> List[str]:
        expanded = []
        if len(macro_args) != len(self.argument_names):
            raise MacroException("Not enough arguments in macro call!")
        substitutions = list(zip(macro_args, self.argument_names))
        for line in self.lines:
            expand_line = line
            for sub in substitutions:
                expand_line = expand_line.replace(sub[0], sub[1])
            expanded.append(line)
        return expanded

    def add_definition(self, definition: List[str]):
        self.name = definition[0]
        self.argument_names = definition[1:]

    def add_line(self, line: str):
        self.lines.append(line)

class MacroException(Exception):
    pass
