from __future__ import annotations

from typing import TYPE_CHECKING, List

from aasm.generating.python_code import PythonCode
from aasm.modules.module import Module, Type


def get_modules_for_target(
    module_code_lines: List[List[str]], target: str
) -> List[Module]:
    """
    Get all modules from `module_code_lines` that target the given `target`.

    :param module_code_lines: the code lines of all modules
    :param target: the target to filter by

    :return: the modules that target the given `target`
    """
    target_modules = []
    for module_lines in module_code_lines:
        module = Module(module_lines)
        if module.does_target(target):
            target_modules.append(module)
    return target_modules


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
        for type in self.module.types:
            impl_lines = type.init_lines[self.target]
            self.add_line(f"def {type.name}__init():")
            self.indent_right()
            for line in impl_lines:
                self.add_line(line)
            self.indent_left()
            self.add_newline()

        for impl in self.module.impls:
            if impl[0] == self.target:
                args_data = self.module.get_args_for_instruction(impl[1])
                args_string = ", ".join(args_data.keys())
                self.add_line(f"def {impl[1]}({args_string}):")
                self.indent_right()
                for line in self.module.impls[impl]:
                    self.add_line(line)
                self.indent_left()
                self.add_newline()
