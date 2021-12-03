from __future__ import annotations
from pprint import pprint
from typing import Dict
from parsing.state import State
from utils.validation import is_float


class ArgumentType:
    def __init__(self, is_agent_param: bool, is_enum: bool, is_float: bool, is_list: bool, is_mutable: bool):
        self.is_agent_param: bool = is_agent_param
        self.is_enum: bool = is_enum
        self.is_float: bool = is_float
        self.is_list: bool = is_list
        self.is_mutable: bool = is_mutable
    
    def explain(self) -> Dict[str, bool]:
        return {
            'is_agent_param': self.is_agent_param,
            'is_enum': self.is_enum,
            'is_float': self.is_float,
            'is_list': self.is_list,
            'is_mutable': self.is_mutable,
        }
    
    def print(self) -> None:
        print('ArgumentType')
        pprint(self.__dict__)
    

class Argument:
    """Doesn't panic. Use in the action context."""
    
    def __init__(self, state: State, arg: str):
        self.arg: str = arg
        self.types: Dict[str, ArgumentType] = {}
        self.type_in_op: str = ''
        self.is_name_available: bool = True
        self._set_types(state)
        
    @property
    def is_agent_param(self) -> bool:
        return self.types[self.type_in_op].is_agent_param
    
    @property
    def is_enum(self) -> bool:
        return self.types[self.type_in_op].is_enum
    
    @property
    def is_float(self) -> bool:
        return self.types[self.type_in_op].is_float
    
    @property
    def is_list(self) -> bool:
        return self.types[self.type_in_op].is_list
        
    def _set_types(self, state: State) -> None:
        if self.arg in state.last_agent.RESERVED_FLOAT_PARAMS:
            self.types['float'] = ArgumentType(True, False, True, False, False)
            self.is_name_available = False
        elif self.arg in state.last_agent.init_floats or self.arg in state.last_agent.dist_normal_floats:
            self.types['float'] = ArgumentType(True, False, True, False, True)
            self.is_name_available = False
        elif self.arg in state.last_agent.enums:
            self.types[f'{self.arg}_enum'] = ArgumentType(True, True, False, False, True)
            self.is_name_available = False
        elif self.arg in state.last_agent.lists:
            self.types['list'] = ArgumentType(True, False, False, True, True)
            self.is_name_available = False
        elif state.last_action.is_name_declared_in_action(self.arg):
            self.types['float'] = ArgumentType(False, False, True, False, True)
            self.is_name_available = False
        elif is_float(self.arg):
            self.types['float'] = ArgumentType(False, False, True, False, False)
        for enum_param in state.last_agent.enums.values():
            for enum_value, _ in enum_param.enums:
                if self.arg == enum_value:
                    self.types[f'{enum_param.name}_enum'] = ArgumentType(False, True, False, False, False)
        
    def declaration_context(self, rhs: Argument) -> bool:
        if 'float' in rhs.types:
            self.type_in_op = 'float'
            rhs.type_in_op = 'float'
            return True
        return False
    
    def comparaison_context(self, rhs: Argument) -> bool:
        available_types = set(self.types).intersection(set(rhs.types)) - {'list'}
        if not available_types:
            return False
        if 'float' in available_types:
            self.type_in_op = 'float'
            rhs.type_in_op = 'float'
        else:
            available_type = available_types.pop()
            self.type_in_op = available_type
            rhs.type_in_op = available_type
        return True
    
    def math_context(self, rhs: Argument) -> bool:
        available_types = set(self.types).intersection(set(rhs.types))
        if 'float' in available_types and self.types['float'].is_mutable:
            self.type_in_op = 'float'
            rhs.type_in_op = 'float'
            return True
        return False
    
    def explain(self) -> Dict[str, Dict[str, bool]]:
        types: Dict[str, Dict[str, bool]] = {}
        for type_name, argument_type in self.types.items():
            types[type_name] = argument_type.explain()
        return types
    
    def print(self) -> None:
        print(f'Argument {self.arg}')
        print(f'Type in op: {self.type_in_op}')
        print(f'Is name available: {self.is_name_available}')
        for _type in self.types.values():
            _type.print()
