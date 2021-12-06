from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from intermediate.argument import Argument
    from intermediate.message import Message


class Declaration:  
    def __init__(self, name: Argument, value: Argument):
        self.name: str = name.expr
        self.value: Argument = value
        
    def print(self) -> None:
        print(f'Declaration: {self.name}')
        self.value.print()


class Instruction:
    def __init__(self, **kwargs: Dict[str, Argument]):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
  
    def print(self) -> None:
        print('Instruction')
        for argument in self.__dict__.values():
            argument.print()


class IfGreaterThan(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)
 
    def print(self) -> None:
        print('IfGreaterThan')
        super().print()


class IfGreaterThanOrEqual(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)
 
    def print(self) -> None:
        print('IfGreaterThanOrEqual')
        super().print()


class IfLessThan(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('IfLessThan')
        super().print()


class IfLessThanOrEqual(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('IfLessThanOrEqual')
        super().print()


class IfEqual(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('IfEqual')
        super().print()


class IfNotEqual(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('IfNotEqual')
        super().print()


class WhileGreaterThan(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('WhileGreaterThan')
        super().print()


class WhileGreaterThanOrEqual(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('WhileGreaterThanOrEqual')
        super().print()


class WhileLessThan(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('WhileLessThan')
        super().print()


class WhileLessThanOrEqual(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('WhileLessThanOrEqual')
        super().print()


class WhileEqual(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('WhileEqual')
        super().print()


class WhileNotEqual(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('WhileNotEqual')
        super().print()


class Multiply(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('Multiply')
        super().print()


class Divide(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('Divide')
        super().print()


class Add(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('Add')
        super().print()


class Subtract(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('Subtract')
        super().print()


class AddElement(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('AddElement')
        super().print()


class RemoveElement(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('RemoveElement')
        super().print()


class Subset(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument, arg3: Argument):
        super().__init__(arg1=arg1, arg2=arg2, arg3=arg3)

    def print(self) -> None:
        print('RemoveElement')
        super().print()


class Set(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('Set')
        super().print()


class IfInList(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('IfInList')
        super().print()


class IfNotInList(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('IfNotInList')
        super().print()


class Clear(Instruction):
    def __init__(self, arg1: Argument):
        super().__init__(arg1=arg1)

    def print(self) -> None:
        print('Clear')
        super().print()


class Length(Instruction):
    def __init__(self, arg1: Argument, arg2: Argument):
        super().__init__(arg1=arg1, arg2=arg2)

    def print(self) -> None:
        print('Length')
        super().print()


class Send(Instruction):
    def __init__(self, arg1: Argument):
        super().__init__(arg1=arg1)

    def print(self) -> None:
        print('Send')
        super().print()


class Block:    
    def __init__(self, names_declared_in_parent: List[str]):
        self.statements: List[Declaration | Instruction | Block] = []
        self._declared_names: List[str] = list(names_declared_in_parent)
        
    @property
    def declarations_in_scope(self) -> List[str]:
        return self._declared_names
        
    def add_declaration(self, declaration: Declaration) -> None:
        self._declared_names.append(declaration.name)
        self.statements.append(declaration)
    
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
    
    def is_declaration_in_scope(self, name: str) -> bool:
        return name in self.current_block.declarations_in_scope
    
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


class ModifySelfAction(Action):
    def __init__(self, name: str):
        super().__init__(name)
        
    def print(self) -> None:
        print('ModifySelfAction')
        super().print()
        
        
class SendMessageAction(Action):
    def __init__(self, name: str, message: Message):
        super().__init__(name)
        self.send_message: Message = message
        
    def print(self) -> None:
        print('SendMessageAction')
        super().print()
        self.send_message.print()
