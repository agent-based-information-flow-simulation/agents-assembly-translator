from __future__ import annotations

from typing import List, Tuple

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
        self.ignore_offsets = []
        self.macro_offsets = []
        self.item_names = []
        self.post_ignore = {}
        self.post_macros = {}

    def get_original_line_number(self, line_idx: int) -> Tuple[int, str]:
        for exp in self.line_expansions:
            if line_idx == exp[0]:
                return (exp[1].declare_line, f"MAKRO call: {exp[1].name}")
        post_macro_idx = self.post_macros[line_idx]
        return (self.post_ignore[post_macro_idx], "")

    def get_makro_name(self, line_idx: int) -> str:
        line = self.lines[line_idx - 1]
        tokens = [token.strip() for token in line.strip().replace(",", " ").split()]
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
            for offset_idx in range(len(self.ignore_offsets)):
                if offset_idx >= idx:
                    self.ignore_offsets[offset_idx] -= 1
            del self.processed_lines[idx]
        self.ignore_offsets = list(reversed(self.ignore_offsets))

    def expand_constants(self):
        line_idx = 0
        for line in self.processed_lines:
            expanded = line
            for const in self.constants:
                expanded = const.expand(expanded)
            self.processed_lines[line_idx] = expanded
            line_idx += 1

    def expand_macros(self):
        line_idx = 0
        to_expand = []
        names = [macro.name for macro in self.macros]
        for line in self.processed_lines:
            tokens = [token.strip() for token in line.strip().replace(",", " ").split()]
            if len(tokens) != 0 and tokens[0] in names:
                to_expand.append((line_idx, tokens[0], tokens[1:]))
            line_idx += 1

        offset = 0
        makro_lines = []
        for makro in to_expand:
            line_idx, name, args = makro
            line_idx += offset
            macro_item = self.macros[names.index(name)]
            if len(makro[2]) != len(macro_item.argument_regexes):
                raise PanicException(
                    f"Error in line: {line_idx}",
                    "Wrong number of arguments",
                    f"Expected {len(macro_item.argument_regexes)} arguments, got {len(args)}",
                )
            self.processed_lines[line_idx:line_idx] = macro_item.expand(args)
            for offset_idx in range(macro_item.expand_len - 1):
                self.macro_offsets.append(line_idx + offset_idx + 2)
            del self.processed_lines[line_idx + macro_item.expand_len]
            for line_offset in range(macro_item.expand_len - 1):
                makro_lines.append(line_idx + line_offset + 2)
            self.line_expansions.append((line_idx + 1, macro_item))
            offset += macro_item.expand_len - 1

        line_idx = 0
        post_idx = 0
        for line in self.processed_lines:
            post_idx += 1
            if post_idx not in makro_lines:
                line_idx += 1
            self.post_macros[post_idx] = line_idx

    def parse_items(self):
        line_idx = 0
        currentItem = None
        post_ignore_idx = 1
        for line in self.lines:
            self.ignore_offsets.append(0)
            self.post_ignore[post_ignore_idx] = line_idx + 1
            line_idx += 1
            tmp = line.strip()
            # enter preprocessor directive
            if len(tmp) == 0:
                self.ignore.append(line_idx - 1)
                continue
            elif tmp[0] == "%":
                self.ignore.append(line_idx - 1)
                signature = tmp.lstrip("%")
                tokens = [
                    token.strip() for token in signature.replace(",", " ").split()
                ]
                if tokens:
                    tokens[0] = tokens[0].upper()
                match tokens:
                    case ["MAKRO", *makro_def]:
                        if currentItem is None:
                            currentItem = Macro(signature)
                            currentItem.add_definition(makro_def, line_idx)
                            if currentItem.name in self.item_names:
                                raise PanicException(
                                    f"Error in line: {line_idx}",
                                    "Duplicate preprocessor item name",
                                    currentItem.name,
                                )
                            self.item_names.append(currentItem.name)
                        else:
                            raise PanicException(
                                f"Error in line: {line_idx}",
                                "Nested preprocessor directives!",
                                "Make sure that you don't use preprocessor directives inside each other.",
                            )
                    case ["EMAKRO"]:
                        if isinstance(currentItem, Macro):
                            self.macros.append(currentItem)
                            currentItem = None
                        else:
                            raise PanicException(
                                f"Error in line: {line_idx}",
                                "Closing a makro without opening one!",
                                "Add a matching %MAKRO directive",
                            )
                        pass
                    case ["CONST", const_name, const_value]:
                        if currentItem is None:
                            currentItem = Constant(signature)
                            currentItem.add_definition(const_name, const_value)
                            self.constants.append(currentItem)
                            if currentItem.name in self.item_names:
                                raise PanicException(
                                    f"Error in line: {line_idx}",
                                    "Duplicate preprocessor item name",
                                    currentItem.name,
                                )
                            self.item_names.append(currentItem.name)
                            currentItem = None
                        else:
                            raise PanicException(
                                f"Error in line: {line_idx}",
                                "Nested preprocessor directive!",
                                "Make sure that you don't use preprocessor directives inside each other",
                            )
                    case _:
                        raise PanicException(
                            f"Error in line: {line_idx}",
                            "Unknown preprocessor directive",
                            "Remove '%' from beggining of the line",
                        )
            elif tmp[0] == "#":
                self.ignore.append(line_idx - 1)
            elif currentItem is not None:
                self.ignore.append(line_idx - 1)
                if isinstance(currentItem, Macro):
                    currentItem.add_line(line)
            else:
                # The case where the line is not ignored
                post_ignore_idx += 1
