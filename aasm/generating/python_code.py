from __future__ import annotations

from typing import List


class PythonCode:
    def __init__(self, indent_size: int):
        self.indent_size = indent_size
        self.indent: int = 0
        self.code_lines: List[str] = []

    def indent_left(self) -> None:
        self.indent -= self.indent_size

    def indent_right(self) -> None:
        self.indent += self.indent_size

    def add_line(self, line: str) -> None:
        self.code_lines.append(self.indent * " " + line + "\n")

    def add_newline(self) -> None:
        self.add_line("")

    def add_newlines(self, count: int) -> None:
        for _ in range(count):
            self.add_newline()

    def add_template(self, template: str, **kwargs: Any) -> None:
        lines = template.render(kwargs).splitlines()
        current_indent = 0
        for line in lines:
            space_count = len(line) - len(
                line.lstrip(" ")
            )  # templates should have 4 space indents per pep8
            indent_count = space_count // 4
            if indent_count < current_indent:
                for _ in range(current_indent - indent_count):
                    self.indent_left()
            elif indent_count > current_indent:
                for _ in range(indent_count - current_indent):
                    self.indent_right()
            self.add_line(line.strip())
