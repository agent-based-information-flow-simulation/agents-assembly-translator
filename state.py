from pprint import pprint
from typing import List, Generator
from environment import Environment
from agent import Agent
from message import Message


class State:
    def __init__(self, lines: List[str], debug: bool):
        self.debug: bool = debug
        self.lines: List[str] = lines
        self.line_num: int = 0
        self.environments: List[Environment] = []
        self.in_environment: bool = False
        self.in_agent: bool = False
        self.in_message: bool = False
        
    @property
    def last_environment(self) -> Environment:
        return self.environments[-1] 
    
    @property
    def last_agent(self) -> Agent:
        return self.last_environment.last_agent
    
    @property
    def last_message(self) -> Message:
        return self.last_environment.last_message
    
    def add_environment(self, environment: Environment) -> None:
        self.environments.append(environment)
            
    def tokens_from_lines(self) -> Generator[list[str], None, None]:
        for line in self.lines:
            self.line_num += 1
            uncommented = line.split('#')[0]
            tokens = [token.strip() for token in uncommented.replace(',', ' ').split()]
            if tokens:
                yield tokens
            
    def verify_end_state(self) -> None:
        if self.in_environment:
            self.panic('Missing EENVIRONMENT')
        elif self.in_agent:
            self.panic('Missing EAGENT')
        elif self.in_message:
            self.panic('Missing EMESSAGE')

    def panic(self, reason: str) -> None:
        if self.debug:
            for environment in self.environments:
                environment.print()
            pprint(self.__dict__)
        print(f'Line {self.line_num}: {self.lines[self.line_num - 1].strip()}')
        print(reason)
        exit(1)
