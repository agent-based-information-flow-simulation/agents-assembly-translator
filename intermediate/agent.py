from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from intermediate.behaviour import Behaviour
    from intermediate.param import (DistNormalFloatParam, EnumParam,
                                    InitFloatParam, ListParam)


class Agent:
    RESERVED_FLOAT_PARAMS = [ 'connCount' ]
    
    def __init__(self, name: str):
        self.name: str = name
        self.init_floats: Dict[str, InitFloatParam] = {}
        self.dist_normal_floats: Dict[str, DistNormalFloatParam] = {}
        self.enums: Dict[str, EnumParam] = {}
        self.lists: Dict[str, ListParam] = {}
        self.setup_behaviours: Dict[str, Behaviour] = {}
        self._last_modified_behaviours: Dict[str, Behaviour] | None = None
        
    @property
    def last_behaviour(self) -> Behaviour:
        return self._last_modified_behaviours[list(self._last_modified_behaviours.keys())[-1]]
    
    @property
    def param_names(self) -> List[str]:
        return [ *Agent.RESERVED_FLOAT_PARAMS,
                 *list(self.init_floats), 
                 *list(self.dist_normal_floats), 
                 *list(self.enums), 
                 *list(self.lists) ]
        
    @property
    def behaviour_names(self) -> List[str]:
        return [ *list(self.setup_behaviours) ]
    
    # def is_mutable(self, name: str) -> bool:
    #     return name not in Agent.RESERVED_FLOAT_PARAMS
        
    def add_init_float(self, float_param: InitFloatParam) -> None:
        self.init_floats[float_param.name] = float_param

    def add_dist_normal_float(self, float_param: DistNormalFloatParam) -> None:
        self.dist_normal_floats[float_param.name] = float_param
    
    def add_enum(self, enum_param: EnumParam) -> None:
        self.enums[enum_param.name] = enum_param
        
    def add_list(self, list_param: ListParam) -> None:
        self.lists[list_param.name] = list_param
        
    def add_setup_behaviour(self, behaviour: Behaviour) -> None:
        self.setup_behaviours[behaviour.name] = behaviour
        self._last_modified_behaviours = self.setup_behaviours

    def param_exists(self, name: str) -> bool:
        return name in self.param_names
    
    def behaviour_exists(self, name: str) -> bool:
        return name in self.behaviour_names
    
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
        for setup_behaviour in self.setup_behaviours.values():
            setup_behaviour.print()
