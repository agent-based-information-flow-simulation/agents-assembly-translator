from __future__ import annotations

from typing import List, Set


class PythonCode:
    def __init__(self, indent_size: int):
        self.indent_size = indent_size
        self.indent: int = 0
        self.code_lines: List[str] = []
        self.required_imports: Set[str] = set()

    def indent_left(self) -> None:
        self.indent -= self.indent_size

    def indent_right(self) -> None:
        self.indent += self.indent_size

    def add_line(
        self, line: str, required_imports: Set[str] | None = None, add_newline=True
    ) -> None:
        if required_imports is not None:
            self.required_imports.update(required_imports)
        if add_newline:
            self.code_lines.append(self.indent * " " + line + "\n")
        else:
            self.code_lines.append(self.indent * " " + line)

    def add_newline(self) -> None:
        self.add_line("")

    def add_newlines(self, count: int) -> None:
        for _ in range(count):
            self.add_newline()

    def add_required_imports(self) -> None:
        lines: List[str] = []
        for required_import in self.required_imports:
            lines.append(f"import {required_import}\n")
        lines.sort()
        self.code_lines = lines + self.code_lines
