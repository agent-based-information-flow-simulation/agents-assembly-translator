from __future__ import annotations

from typing import TYPE_CHECKING, List

from aasm.generating.python_code import PythonCode

if TYPE_CHECKING:
    from aasm.modules.module import Module


class PythonModule(PythonCode):
    def __init__(self, indent_size, module: Module):
        super().__init__(indent_size)
        self.module: Module = module
        self.target: str = "spade"
        self.add_newlines(2)
        self.create_module_header()
        self.add_newline()
        self.create_module_imports()
        self.add_newline()
        self.create_module_implementations()

    def create_module_header(self) -> None:
        self.add_line(f"# Module: {self.module.name}")
        for line in self.module.description:
            self.add_line(f"# {line}", add_newline=False)

    def create_module_imports(self):
        try:
            preamble = self.module.preambles[self.target]
            for line in preamble:
                self.add_line(line)
        except KeyError:
            return

    def create_module_implementations(self):
        for impl in self.module.impls:
            if impl[0] == self.target:
                self.add_line(f"def {impl[1]}():")
                for line in self.module.impls[impl]:
                    self.add_line(line)
                self.add_newline()
