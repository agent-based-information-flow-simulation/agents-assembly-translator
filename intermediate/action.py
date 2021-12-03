from __future__ import annotations

from pprint import pprint
from typing import List

# from parsing.argument import Argument
import parsing

# class VariableValue: 
#     def __init__(self, value: str):
#         self.value: str = value
#         self.is_value_from_agent: bool = False

#     def print(self) -> None:
#         print('VariableValue')
#         pprint(self.__dict__)


# class Declaration(VariableValue):  
#     def __init__(self, name: str, value: str):
#         super().__init__(value)
#         self.name: str = name
        
#     def print(self) -> None:
#         print(f'Declaration: {self.name}')
#         super().print()


class Declaration():  
    def __init__(self, name: parsing.Argument, value: parsing.Argument):
        self.name: str = name.arg
        self.value: parsing.Argument = value
        
    def print(self) -> None:
        print(f'Declaration: {self.name}')
        # self.name.print()
        self.value.print()


class Instruction:
    def __init__(self, arg1: parsing.Argument, arg2: parsing.Argument):
        self.arg1: parsing.Argument = arg1
        self.arg2: parsing.Argument = arg2
  
    def print(self) -> None:
        print('Instruction')
        self.arg1.print()
        self.arg2.print()


class IfGreaterThan(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)
 
    def print(self) -> None:
        print('IfGreaterThan')
        super().print()
        
        
class IfGreaterThanOrEqual(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)
 
    def print(self) -> None:
        print('IfGreaterThanOrEqual')
        super().print()


class IfLessThan(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('IfLessThan')
        super().print()


class IfLessThanOrEqual(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('IfLessThanOrEqual')
        super().print()
        
        
class IfEqual(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('IfEqual')
        super().print()
        
        
class IfNotEqual(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('IfNotEqual')
        super().print()

        
class WhileGreaterThan(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('WhileGreaterThan')
        super().print()

  
class WhileGreaterThanOrEqual(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('WhileGreaterThanOrEqual')
        super().print()


class WhileLessThan(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('WhileLessThan')
        super().print()
        
        
class WhileLessThanOrEqual(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('WhileLessThanOrEqual')
        super().print()


class WhileEqual(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('WhileEqual')
        super().print()


class WhileNotEqual(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('WhileNotEqual')
        super().print()


class Multiply(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('Multiply')
        super().print()
        
        
class Divide(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('Divide')
        super().print()


class Add(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('Add')
        super().print()
        

class Subtract(Instruction):
    def __init__(self, arg1: str, arg2: str):
        super().__init__(arg1, arg2)

    def print(self) -> None:
        print('Subtract')
        super().print()


class Block:    
    def __init__(self, names_declared_in_parent: List[str]):
        self.statements: List[Declaration | Instruction | Block] = []
        self._declared_names: List[str] = list(names_declared_in_parent)
        
    def add_declaration(self, declaration: Declaration) -> None:
        self._declared_names.append(declaration.name)
        self.statements.append(declaration)
        
    def is_name_in_scope_declarations(self, name: str) -> bool:
        return name in self._declared_names
        
    def add_statement(self, statement: Instruction | Block) -> None:
        self.statements.append(statement)
        
    def print(self) -> None:
        print(f'Block')
        print(f'Names in scope')
        print(self._declared_names)
        for instruction in self.statements:
            instruction.print()
        print('(EndBlock)')


class Action:
    def __init__(self, name: str):
        self.name: str = name
        self._block_stack: List[Block] = [Block([])]
        self._nested_blocks_count: int = 0
        
    @property
    def main_block(self) -> Block:
        return self._block_stack[0]
    
    @property
    def current_block(self) -> Block:
        return self._block_stack[-1]
    
    def is_name_declared_in_action(self, name: str) -> bool:
        return self.current_block.is_name_in_scope_declarations(name)
    
    def add_declaration(self, declaration: Declaration) -> None:
        self.current_block.add_declaration(declaration)
    
    def add_instruction(self, instruction: Instruction) -> None:
        self.current_block.add_statement(instruction)
        
    def start_block(self) -> None:
        new_block = Block(self.current_block._declared_names)
        self.current_block.add_statement(new_block)
        self._block_stack.append(new_block)
        self._nested_blocks_count += 1
    
    def end_block(self) -> None:
        self._block_stack.pop()
        self._nested_blocks_count -= 1
        
    def print(self) -> None:
        print(f'Action {self.name}')
        self.main_block.print()
