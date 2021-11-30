from typing import List, Dict, Tuple
from pprint import pprint


class Param:
    def __init__(self, name: str, category: str):
        self.name: str = name
        self.category: str = category
        self.subcategory: str = ''    

    def set_subcategory(self, name: str) -> None:
        self.subcategory = name
        

class FloatParam(Param):
    def __init__(self, name: str):
        super().__init__(name, 'float')
        self.subcategory_args: List[str] = []
        
    def add_subcategory_arg(self, arg: str) -> None:
        self.subcategory_args.append(arg)
        
    def print(self) -> None:
        pprint(self.__dict__)
    

class EnumParam(Param):
    def __init__(self, name: str):
        super().__init__(name, 'enum')
        self.subcategory_args: List[Tuple[str, str]] = []
        
    def add_subcategory_arg(self, arg: Tuple[str, str]) -> None:
        self.subcategory_args.append(arg)
        
    def print(self) -> None:
        pprint(self.__dict__)


class ListParam(Param):
    def __init__(self, name: str):
        super().__init__(name, 'list')
        
    def print(self) -> None:
        pprint(self.__dict__)
