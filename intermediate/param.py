from typing import List


class MessageFloatParam:
    def __init__(self, name: str):
        self.name: str = name
        self.value: str = ''
        self.is_value_set: bool = False
        
    def set_value(self, value: str) -> None:
        self.is_value_set = True
        self.value = value
        
    def print(self) -> None:
        print(f'MessageFloatParam {self.name} = {self.value}')


class AgentInitFloatParam:
    def __init__(self, name: str, value: str):
        self.name: str = name
        self.value: str = value
        
    def print(self) -> None:
        print(f'AgentInitFloatParam {self.name} = {self.value}')


class AgentDistNormalFloatParam:
    def __init__(self, name: str, mean: str, std_dev: str):
        self.name: str = name
        self.mean: str = mean
        self.std_dev: str = std_dev

    def print(self) -> None:
        print(f'AgentDistNormalFloatParam {self.name} = normal(mean={self.mean}, std_dev={self.std_dev})')


class AgentDistExpFloatParam:
    def __init__(self, name: str, lambda_: str):
        self.name: str = name
        self.lambda_: str = lambda_

    def print(self) -> None:
        print(f'AgentDistExpFloatParam {self.name} = exp(lambda={self.lambda_})')


class AgentEnumParam:
    def __init__(self, name: str, enums: List[str]):
        self.name: str = name
        self.enum_values: List[AgentEnumValue] = [AgentEnumValue(name, value, percentage) for value, percentage in zip(*[iter(enums)] * 2)]
        
    def print(self) -> None:
        print(f'AgentEnumParam {self.name} = {self.enum_values}')


class AgentEnumValue:
    def __init__(self, from_enum: str, value: str, percentage: str):
        self.from_enum: str = from_enum
        self.value: str = value
        self.percentage: str = percentage
        
    def __str__(self) -> str:
        return f'({self.value}, {self.percentage}; from_enum={self.from_enum})'


class AgentMessageListParam:
    def __init__(self, name: str):
        self.name: str = name
        
    def print(self) -> None:
        print(f'AgentMessageListParam {self.name} = []')


class AgentConnectionListParam:
    def __init__(self, name: str):
        self.name: str = name
        
    def print(self) -> None:
        print(f'AgentConnectionListParam {self.name} = []')
