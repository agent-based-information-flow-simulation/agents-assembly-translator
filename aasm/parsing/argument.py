from __future__ import annotations

from pprint import pprint
from typing import TYPE_CHECKING, Dict

from aasm.utils.validation import is_float

if TYPE_CHECKING:
    from aasm.parsing.state import State


class ArgumentType:
    def __init__(self, is_agent_param: bool, is_enum: bool, is_float: bool, is_list: bool, is_mutable: bool):
        self.is_agent_param: bool = is_agent_param
        self.is_enum: bool = is_enum
        self.is_float: bool = is_float
        self.is_list: bool = is_list
        self.is_mutable: bool = is_mutable
    
    def explain(self) -> str:
        types = '('
        if self.is_agent_param:
            types += 'agent parameter, '
        if self.is_enum:
            types += 'enum, '
        if self.is_float:
            types += 'float, '
        if self.is_list:
            types += 'list, '
        types += 'mutable' if self.is_mutable else 'immutable'
        types += ')'
        return types
    
    def print(self) -> None:
        print('ArgumentType')
        pprint(self.__dict__)
    

class Argument:
    """Doesn't panic. Use in the action context."""
    
    FLOAT = 'float'
    ENUM = 'enum'
    LIST = 'list'
    ENUM_VALUE_SUFFIX = '_enum_value'
    
    def __init__(self, state: State, expr: str):
        self.expr: str = expr
        self.types: Dict[str, ArgumentType] = {}
        self.type_in_op: str = ''
        self.is_name_available: bool = True
        self._set_types(state)
        
    @property
    def is_agent_param(self) -> bool:
        if not self.type_in_op:
            print(f'Warning: context not set for {self.expr}')
        return self.types[self.type_in_op].is_agent_param
    
    @property
    def is_enum(self) -> bool:
        if not self.type_in_op:
            print(f'Warning: context not set for {self.expr}')
        return self.types[self.type_in_op].is_enum
    
    @property
    def is_float(self) -> bool:
        if not self.type_in_op:
            print(f'Warning: context not set for {self.expr}')
        return self.types[self.type_in_op].is_float
    
    @property
    def is_list(self) -> bool:
        if not self.type_in_op:
            print(f'Warning: context not set for {self.expr}')
        return self.types[self.type_in_op].is_list
        
    def _set_types(self, state: State) -> None:
        if self.expr in state.last_agent.RESERVED_FLOAT_PARAMS:
            self.types[Argument.FLOAT] = ArgumentType(True, False, True, False, False)
            self.is_name_available = False
        elif self.expr in state.last_agent.init_floats or self.expr in state.last_agent.dist_normal_floats:
            self.types[Argument.FLOAT] = ArgumentType(True, False, True, False, True)
            self.is_name_available = False
        elif self.expr in state.last_agent.enums:
            self.types[Argument.ENUM] = ArgumentType(True, True, False, False, True)
            self.is_name_available = False
        elif self.expr in state.last_agent.lists:
            self.types[Argument.LIST] = ArgumentType(True, False, False, True, True)
            self.is_name_available = False
        elif state.last_action.is_name_declared_in_action(self.expr):
            self.types[Argument.FLOAT] = ArgumentType(False, False, True, False, True)
            self.is_name_available = False
        elif is_float(self.expr):
            self.types[Argument.FLOAT] = ArgumentType(False, False, True, False, False)
        for enum_param in state.last_agent.enums.values():
            for enum_value, _ in enum_param.enums:
                if self.expr == enum_value:
                    self.types[f'{enum_param.name}{Argument.ENUM_VALUE_SUFFIX}'] = ArgumentType(False, True, False, False, False)
        
    def declaration_context(self, rhs: Argument) -> bool:
        if self.is_name_available and Argument.FLOAT in rhs.types:
            self.type_in_op = Argument.FLOAT 
            rhs.type_in_op = Argument.FLOAT
            return True
        return False
    
    def unordered_comparaison_context(self, rhs: Argument) -> bool:
        lhs_enum_values = [_type for _type in self.types if Argument.ENUM_VALUE_SUFFIX in _type]
        rhs_enum_values = [_type for _type in rhs.types if Argument.ENUM_VALUE_SUFFIX in _type]
        available_types = set(self.types).intersection(set(rhs.types))
        if Argument.FLOAT in available_types:
            self.type_in_op = Argument.FLOAT
            rhs.type_in_op = Argument.FLOAT
        elif Argument.ENUM in available_types:
            self.type_in_op = Argument.ENUM
            rhs.type_in_op = Argument.ENUM
        elif Argument.ENUM in self.types and rhs_enum_values:
            self.type_in_op = Argument.ENUM
            rhs.type_in_op = rhs_enum_values[0]
        elif lhs_enum_values and Argument.ENUM in rhs.types:
            self.type_in_op = lhs_enum_values[0]
            rhs.type_in_op = Argument.ENUM
        else:
            return False
        return True
    
    def ordered_comparaison_context(self, rhs: Argument) -> bool:
        available_types = set(self.types).intersection(set(rhs.types))
        if Argument.FLOAT in available_types:
            self.type_in_op = Argument.FLOAT
            rhs.type_in_op = Argument.FLOAT
        else:
            return False
        return True
    
    def math_context(self, rhs: Argument) -> bool:
        available_types = set(self.types).intersection(set(rhs.types))
        if Argument.FLOAT in available_types and self.types[Argument.FLOAT].is_mutable:
            self.type_in_op = Argument.FLOAT
            rhs.type_in_op = Argument.FLOAT
            return True
        return False
    
    def array_modification_context(self, rhs: Argument) -> bool:
        raise Exception('array modification context not implemented')
    
    def assignment_context(self, rhs: Argument) -> bool:
        if Argument.ENUM in self.types and self.types[Argument.ENUM].is_mutable and f'{self.expr}{Argument.ENUM_VALUE_SUFFIX}' in rhs.types:
            self.type_in_op = Argument.ENUM
            rhs.type_in_op = f'{self.expr}{Argument.ENUM_VALUE_SUFFIX}'
        elif Argument.FLOAT in self.types and self.types[Argument.FLOAT].is_mutable and Argument.FLOAT in rhs.types:
            self.type_in_op = Argument.FLOAT
            rhs.type_in_op = Argument.FLOAT
        else:
            return False
        return True
    
    def explain(self) -> str:
        types = f'{self.expr}: [ '
        for type_name, argument_type in self.types.items():
            types += f'{type_name} ' + argument_type.explain() + ', '
        types = types.rstrip().rsplit(',', 1)[0]
        types += ' ]'
        return types
    
    def print(self) -> None:
        print(f'Argument {self.expr}')
        print(f'Type in op: {self.type_in_op}')
        print(f'Is name available: {self.is_name_available}')
        for _type in self.types.values():
            _type.print()
