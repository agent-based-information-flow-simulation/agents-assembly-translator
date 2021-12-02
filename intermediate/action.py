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


class Instruction:
    def __init__(self, arg1: str, arg2: str):
        self.arg1: VariableValue = VariableValue(arg1)
        self.arg2: VariableValue = VariableValue(arg2)
  
    def print(self) -> None:
        print('Instruction')
        self.arg1.print()
        self.arg2.print()


class GreaterThan(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)
 
    def print(self) -> None:
        print('GreaterThan')
        super().print()


class LessThanOrEqual(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('LessThanOrEqual')
        super().print()
        

class Multiply(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('Multiply')
        super().print()
        
        
class Subtract(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('Subtract')
        super().print()


class Block:    
    def __init__(self, names_declared_in_parent: List[str] = []):
        self.declarations: Dict[str, Declaration] = {}
        self.statements: List[Instruction | Block] = []
        self._names_declared_in_parent: List[str] = names_declared_in_parent
    
    @property 
    def declared_names(self) -> List[str]:
        return [ *list(self.declarations), *self._names_declared_in_parent ]
        
    def add_declaration(self, declaration: Declaration) -> None:
        self.declarations[declaration.name] = declaration
        
    def declaration_exists(self, name: str) -> bool:
        return name in self.declared_names
        
    def add_statement(self, statement: Instruction | Block) -> None:
        self.statements.append(statement)
        
    def print(self) -> None:
        print(f'Block')
        print(f'Names from parent:')
        print(self._names_declared_in_parent)
        for declaration in self.declarations.values():
            declaration.print()
        for instruction in self.statements:
            instruction.print()
        print('(EndBlock)')


class Action:
    def __init__(self, name: str, agent_param_names: List[str]):
        self.name: str = name
        self._block_stack: List[Block] = [Block()]
        self._agent_param_names: List[str] = agent_param_names
        self._nested_blocks_count: int = 0
        
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
    
    def add_instruction(self, instruction: Instruction) -> None:
        if instruction.arg1.value in self._agent_param_names:
            instruction.arg1.is_value_from_agent = True
        if instruction.arg2.value in self._agent_param_names:
            instruction.arg2.is_value_from_agent = True
        self.current_block.add_statement(instruction)
        
    def start_block(self) -> None:
        new_block = Block(self.current_block.declared_names)
        self.current_block.add_statement(new_block)
        self._block_stack.append(new_block)
        self._nested_blocks_count += 1
    
    def end_block(self) -> None:
        self._block_stack.pop()
        self._nested_blocks_count -= 1
        
    def print(self) -> None:
        print(f'Action {self.name}')
        self.main_block.print()
