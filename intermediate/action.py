from __future__ import annotations

from pprint import pprint
from typing import Dict, List, Tuple


class Statement:
    def __init__(self, arg1: str, arg2: str):
        self.arg1: str = arg1
        self.arg2: str = arg2
        

class GreaterThan(Statement):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)
 
        
class LessThanOrEqual(Statement):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)


class Declaration:    
    def __init__(self, name: str, value: str):
        self.name: str = name
        self.value: str = value
        
    def print(self) -> None:
        print(f'Declaration: {self.name} = {self.value}')

class Block:    
    def __init__(self, parent_declarations_copy: Dict[str, Declaration]):
        self.declarations: Dict[str, Declaration] = parent_declarations_copy
        self.instructions: List[Statement | Block] = []
        # self._is_in_declarations = True
        
    def add_declaration(self, declaration: Declaration) -> None:
        self.declarations[declaration.name] = declaration
        
    def declaration_exists(self, name: str) -> bool:
        return name in self.declarations
        
    def add_instruction(self, instruction: Statement | Block) -> None:
        self.instructions.append(instruction)
        # self._is_in_declarations = False
        
    def print(self) -> None:
        print(f'Block')
        for declaration in self.declarations.values():
            declaration.print()
        for instruction in self.instructions:
            instruction.print()


class Action:
    def __init__(self, name: str):
        self.name: str = name
        self._block_stack = [Block({})]
        
    @property
    def main_block(self) -> Block:
        return self._block_stack[0]
    
    @property
    def current_block(self) -> Block:
        return self._block_stack[-1]
    
    def add_declaration(self, declaration: Declaration) -> None:
        self.current_block.add_declaration(declaration)
    
    def declaration_exists(self, name: str) -> bool:
        return self.current_block.declaration_exists(name)
        
    # def is_in_declarations(self) -> bool:
    #     return self.current_block._in_declarations
    
    def add_statement(self, statement: Statement) -> None:
        self.current_block.add_instruction(statement)
        
    def start_block(self) -> None:
        new_block = Block(dict(self.current_block.declarations.items()))
        self.current_block.add_instruction(new_block)
        self._block_stack.append(new_block)
    
    def end_block(self) -> None:
        self._block_stack.pop()
        
    def print(self) -> None:
        print(f'Action {self.name}')
        self.main_block.print()
