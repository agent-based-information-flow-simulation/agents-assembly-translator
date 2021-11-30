from typing import Dict, Tuple

from intermediate.param import (DistNormalFloatParam, EnumParam,
                                InitFloatParam, ListParam)


class Agent:
    def __init__(self, name: str):
        self.name: str = name
        self.init_floats: Dict[str, InitFloatParam] = {}
        self.dist_normal_floats: Dict[str, DistNormalFloatParam] = {}
        self.enums: Dict[str, EnumParam] = {}
        self.lists: Dict[str, ListParam] = {}
        
    def add_init_float(self, float_param: InitFloatParam) -> None:
        self.init_floats[float_param.name] = float_param

    def add_dist_normal_float(self, float_param: DistNormalFloatParam) -> None:
        self.dist_normal_floats[float_param.name] = float_param
    
    def add_enum(self, enum_param: EnumParam) -> None:
        self.enums[enum_param.name] = enum_param
        
    def add_list(self, list_param: ListParam) -> None:
        self.lists[list_param.name] = list_param

    def param_exists(self, name: str) -> bool:
        if name in (*list(self.init_floats), *list(self.dist_normal_floats), *list(self.enums), *list(self.lists)):
            return True
        return False

    def print(self) -> None:
        print(f'Agent {self.name}')
        for init_float_param in self.init_floats.values():
            init_float_param.print()
        for dist_normal_float_param in self.dist_normal_floats.values():
            dist_normal_float_param.print()
        for enum_param in self.enums.values():
            enum_param.print()
        for list_param in self.lists.values():
            list_param.print()
