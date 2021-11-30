from typing import Dict, Tuple
from param import Param, EnumParam, FloatParam, ListParam


class Agent:
    def __init__(self, name: str):
        self.name: str = name
        self.floats: Dict[str, FloatParam] = {}
        self.enums: Dict[str, EnumParam] = {}
        self.lists: Dict[str, ListParam] = {}
        self._enum_values: Dict[str, Tuple[str, str]] = {}
        
    def add_float(self, float_param: FloatParam) -> None:
        self.floats[float_param.name] = float_param
    
    def add_enum(self, enum_param: EnumParam) -> None:
        self.enums[enum_param.name] = enum_param
        
    def add_list(self, list_param: ListParam) -> None:
        self.lists[list_param.name] = list_param
        
    def add_enum_value(self, name: str, value: str) -> None:
        self._enum_values[name] = (name, value)
        
    def get_param(self, name: str) -> Param:
        if name in self.floats:
            return self.floats[name]
        elif name in self.enums:
            return self.enums[name]
        elif name in self.lists:
            return self.lists[name]

    def param_exists(self, name: str) -> bool:
        if name in self.floats or name in self.enums or name in self.lists:
            return True
        return False
    
    def get_enum_value(self, name: str) -> Tuple[str, str]:
        return self._enum_values[name]
    
    def enum_value_exists(self, name: str) -> bool:
        return name in self._enum_values

    def print(self) -> None:
        print(f'Agent {self.name}')
        for float_param in self.floats.values():
            float_param.print()
        for enum_param in self.enums.values():
            enum_param.print()
        for list_param in self.lists.values():
            list_param.print()
