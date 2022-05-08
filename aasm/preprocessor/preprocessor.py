from __future__ import annotations

from typing import List

from aasm.preprocessor.constant import Constant
from aasm.preprocessor.macro import Macro
from aasm.utils.exception import PanicException


class Preprocessor:
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.ignore = []
        self.processed_lines = lines.copy()
        self.macros = []
        self.constants = []
        self.line_expansions = []

    def get_original_line_number(self, line_idx: int) -> int:
        idx_expand = line_idx
        for expansion in self.line_expansions:
            if line_idx >= expansion[0]:
                idx_expand -= expansion[1].expand_len - 1
        idx_ignore = idx_expand
        for idx in self.ignore:
            if line_idx >= idx:
                idx_ignore += 1
        return idx_ignore + 1

    def get_makro_name(self, line_idx: int) -> str:
        line = self.lines[line_idx-1]
        tokens = [token.strip() for token in line.strip().replace(',', ' ').split()]
        if len(tokens) > 0:
            m_name = tokens[0]
            if m_name in [macro.name for macro in self.macros]:
                return m_name
        return ""

    def run(self):
        self.parse_items()
        self.clean_ignored()
        self.expand_constants()
        self.expand_macros()
        return self.processed_lines

    def clean_ignored(self):
        for idx in sorted(self.ignore, reverse=True):
            del self.processed_lines[idx]

    def expand_constants(self):
        line_idx = 0
        for line in self.processed_lines:
            for const in self.constants:
                self.processed_lines[line_idx] = const.expand(line)
            line_idx += 1

    def expand_macros(self):
        line_idx = 0
        to_expand = []
        names = [macro.name for macro in self.macros]
        for line in self.processed_lines:
            tokens = [token.strip() for token in line.strip().replace(',', ' ').split()]
            if len(tokens) != 0 and tokens[0] in names:
                to_expand.append((line_idx, tokens[0], tokens[1:]))
            line_idx += 1
        offset = 0
        for makro in to_expand:
            line_idx = makro[0] + offset
            macro_item = [x for x in self.macros if x.name == makro[1]][0]  # guaranteed to exist
            if len(makro[2]) != len(macro_item.argument_regexes):
                raise PanicException(f"Error in line: {line_idx}", "Wrong number of arguments", f"Expected {len(macro_item.argument_regexes)} arguments, got {len(makro[2])}")
            self.processed_lines[line_idx:line_idx] = macro_item.expand(makro[2])
            del self.processed_lines[line_idx+macro_item.expand_len]
            self.line_expansions.append((line_idx, macro_item))
            offset += macro_item.expand_len - 1

    def parse_items(self):
        line_idx = 0
        currentItem = None
        for line in self.lines:
            line_idx += 1
            tmp = line.strip()
            # enter preprocessor directive
            if len(tmp) == 0:
                self.ignore.append(line_idx - 1)
                continue
            if tmp[0] == '%':
                self.ignore.append(line_idx - 1)
                signature = tmp.lstrip('%')
                tokens = [token.strip() for token in signature.replace(',', ' ').split()]
                if tokens:
                    tokens[0] = tokens[0].upper()
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
                    case ['CONST', const_name, const_value]:
                        if currentItem is None:
                            currentItem = Constant(signature)
                            currentItem.add_definition(const_name, const_value)
                            self.constants.append(currentItem)
                            currentItem = None
                        else:
                            raise PanicException(f"Error in line: {line_idx}", "Nested preprocessor directive!", "Make sure that you don't use preprocessor directives inside each other")
                    case _:
                        raise PanicException(f"Error in line: {line_idx}", "Unknown preprocessor directive", "Remove '%' from beggining of the line")
            elif tmp[0] == '#':
                self.ignore.append(line_idx - 1)
            elif currentItem is not None:
                self.ignore.append(line_idx - 1)
                if isinstance(currentItem, Macro):
                    currentItem.add_line(line)
