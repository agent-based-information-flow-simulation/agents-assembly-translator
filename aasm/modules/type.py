from aasm.intermediate.argument import ModuleVariable


class Type:
    def __init__(self, name: str, module: str):
        self.name = name
        self.type_class = type(name, (ModuleVariable,), {})
        self.module = module

    def full_qualified_name(self) -> str:
        return f"{self.module}::{self.name}"

    def __eq__(self, other):
        if isinstance(other, Type):
            return self.name == other.name and self.module == other.module
        return False

    def __repr__(self):
        return f"Type[{self.full_qualified_name()}]"

    def __str__(self):
        return f"Type[{self.full_qualified_name()}]"
