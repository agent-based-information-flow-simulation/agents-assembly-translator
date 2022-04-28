from __future__ import annotations

from typing import List
from aasm.preprocessor.macro import Macro
from aasm.utils.exception import PanicException


def preprocess(aasm_lines: List[str]) -> List[str]:
    preprocessor = Preprocessor(aasm_lines)
    preprocessor.parseItems()
    preprocessor.expandMacros()

    return preprocessor.processed_lines


class Preprocessor:
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.ignore = []
        self.processed_lines = lines
        self.macros = []

    def expandMacros(self):
        line_idx = 0
        to_expand = []
        names = [macro.name for macro in self.macros]
        for line in self.lines:
            if line_idx not in ignore:
                tokens = [token.strip() for token in line.strip().replace(',', ' ')]
                if tokens[0] in names:
                    to_expand.append(line_idx)

    def parseItems(self):
        line_idx = 0
        currentItem = None
        for line in self.lines:
            line_idx += 1
            tmp = line.strip()
            # enter preprocessor directive
            if tmp[0] == '%':
                self.ignore.append(line_idx - 1)
                signature = tmp.lstrip('%')
                tokens = [token.strip() for token in tmp.replace(',', ' ')]
                match tokens:
                    case ['MAKRO', *makro_def]:
                        if currentItem is None:
                            currentItem = Macro(signature)
                            currentItem.add_definition(makro_def)
                        else:
                            raise PanicException(f"Error in line: {line_idx}", "Nested preprocessor directives!", "Make sure that you don't use preprocessor directives inside each other.")
                    case ['EMAKRO']:
                        if isinstance(currentItem, Macro):
                            self.macros.append(currentItem)
                            currentItem = None
                        else:
                            raise PanicException(f"Error in line: {line_idx}", "Closing a makro without opening one!", "Add a matching %MAKRO directive")
                        pass
                    case _:
                        raise PanicException(f"Error in line: {line_idx}", "Unknown preprocessor directive", "Remove '%' from beggining of the line")
            elif tmp[0] == '#':
                self.ignore.append(line_idx - 1)
            elif currentItem is not None:
                self.ignore.append(line_idx - 1)
                if isinstance(currentItem, Macro):
                    currentItem.add_line(line)


