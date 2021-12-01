from __future__ import annotations

from pprint import pprint
from typing import Dict, List


class VariableValue: 
    def __init__(self, value: str):
        self.value: str = value
        self.is_value_from_agent: bool = False

    def print(self) -> None:
        print('VariableValue')
        pprint(self.__dict__)


class Declaration(VariableValue):  
    def __init__(self, name: str, value: str):
        super().__init__(value)
        self.name: str = name
        
    def print(self) -> None:
        print(f'Declaration: {self.name}')
        super().print()


class Expression:
    def __init__(self, arg1: str, arg2: str):
        self.arg1: VariableValue = VariableValue(arg1)
        self.arg2: VariableValue = VariableValue(arg2)
  
    def print(self) -> None:
        print('Expression')
        self.arg1.print()
        self.arg2.print()


class GreaterThan(Expression):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)
 
    def print(self) -> None:
        print('GreaterThan')
        super().print()


class LessThanOrEqual(Expression):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('LessThanOrEqual')
        super().print()
        

class Multiply(Expression):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('Multiply')
        super().print()
        
        
class Subtract(Expression):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('Subtract')
        super().print()


class Block:    
    def __init__(self, names_declared_in_parent: List[str] = []):
        self.declarations: Dict[str, Declaration] = {}
        self.instructions: List[Expression | Block] = []
        self._names_declared_in_parent = names_declared_in_parent
        
    def add_declaration(self, declaration: Declaration) -> None:
        self.declarations[declaration.name] = declaration
        
    def declaration_exists(self, name: str) -> bool:
        return name in self._names_declared_in_parent or name in self.declarations
        
    def add_instruction(self, instruction: Expression | Block) -> None:
        self.instructions.append(instruction)
        
    def print(self) -> None:
        print(f'Block')
        print(f'Names from parent:')
        print(self._names_declared_in_parent)
        for declaration in self.declarations.values():
            declaration.print()
        for instruction in self.instructions:
            instruction.print()
        print('(EndBlock)')


class Action:
    def __init__(self, name: str, agent_param_names: List[str]):
        self.name: str = name
        self._block_stack: List[Block] = [Block()]
        self._agent_param_names: List[str] = agent_param_names
        
    @property
    def main_block(self) -> Block:
        return self._block_stack[0]
    
    @property
    def current_block(self) -> Block:
        return self._block_stack[-1]
    
    def is_name_in_scope(self, name: str) -> bool:
        return name in self._agent_param_names or self.current_block.declaration_exists(name)
    
    def add_declaration(self, declaration: Declaration) -> None:
        if declaration.value in self._agent_param_names:
            declaration.is_value_from_agent = True
        self.current_block.add_declaration(declaration)
    
    def add_expression(self, expression: Expression) -> None:
        if expression.arg1.value in self._agent_param_names:
            expression.arg1.is_value_from_agent = True
        if expression.arg2.value in self._agent_param_names:
            expression.arg2.is_value_from_agent = True
        self.current_block.add_instruction(expression)
        
    def start_block(self) -> None:
        new_block = Block(list(self.current_block.declarations))
        self.current_block.add_instruction(new_block)
        self._block_stack.append(new_block)
    
    def end_block(self) -> None:
        self._block_stack.pop()
        
    def print(self) -> None:
        print(f'Action {self.name}')
        self.main_block.print()
