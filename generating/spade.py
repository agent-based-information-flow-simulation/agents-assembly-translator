from typing import List

from intermediate.agent import Agent
from parsing.state import ParsedData

class SpadeCode:
    INDENT_SIZE = 4
    
    def __init__(self, parsed_data: ParsedData):
        self.indent: int = 0
        self.code_lines: List[str] = []
        self.add_required_imports()
        for agent in parsed_data.agents:
            self.generate_agent(agent)
        for message in parsed_data.messages:
            self.generate_message(message)
        
    def add_required_imports(self) -> List[str]:
        self.add_line(f'import random as r')
        self.add_line(f'import spade')
        self.add_line(f'from numpy.random import normal')
        self.add_line('')
        
    def indent_left(self) -> None:
        self.indent -= 1
        
    def indent_right(self) -> None:
        self.indent += 1
        
    def add_line(self, line: str) -> None:
        self.code_lines.append(SpadeCode.INDENT_SIZE * self.indent * ' ' + line + '\n')

    def generate_agent(self, agent: Agent) -> None:
        self.add_line('')
        self.add_line(f'class {agent.name}(spade.agent.Agent):')
        self.indent_right()
        self.add_line('def __init__(self, jid, password, location, connections):')
        self.indent_right()
        self.add_line('super().__init__(jid, password, verify_security=False)')
        
        for param in agent.init_floats.values():
            self.add_line(f'self.{param.name} = {param.value}')
            
        for param in agent.dist_normal_floats.values():
            self.add_line(f'self.{param.name} = normal({param.mean}, {param.std_dev})')
        
        for param in agent.enums.values():            
            names = []
            weights = []
            for name, weight in param.enums:
                names.append(f'\"{name}\"')
                weights.append(weight)
            names = f'[{", ".join(names)}]'
            weights = f'[{", ".join(weights)}]'
            self.add_line(f'self.{param.name} = r.choices({names}, {weights})[0]')
        
        for param in agent.lists.values():
            self.add_line(f'self.{param.name} = []')
            
    def generate_message(agent: Agent) -> None:
        ...
