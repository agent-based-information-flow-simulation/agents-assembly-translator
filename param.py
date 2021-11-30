from typing import List, Tuple
from pprint import pprint


class InitFloatParam:
    def __init__(self, name: str, value: str):
        self.name: str = name
        self.value: str = value
        
    def print(self) -> None:
        print(self.__class__)
        pprint(self.__dict__)


class DistNormalFloatParam:
    def __init__(self, name: str, mean: str, std_dev: str):
        self.name: str = name
        self.mean: str = mean
        self.std_dev: str = std_dev

    def print(self) -> None:
        print(self.__class__)
        pprint(self.__dict__)


class EnumParam:
    def __init__(self, name: str, enums: List[str]):
        self.name: str = name
        self.enums: List[Tuple[str, str]] = [enum_pair for enum_pair in zip(*[iter(enums)] * 2)]
        
    def print(self) -> None:
        print(self.__class__)
        pprint(self.__dict__)


class ListParam:
    def __init__(self, name: str):
        self.name: str = name
        
    def print(self) -> None:
        print(self.__class__)
        pprint(self.__dict__)
