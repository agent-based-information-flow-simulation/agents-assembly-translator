from pprint import pprint
from typing import Generator, List

from intermediate.action import Action
from intermediate.agent import Agent
from intermediate.behaviour import Behaviour
from intermediate.environment import Environment
from intermediate.message import Message


class State:
    def __init__(self, lines: List[str], debug: bool):
        self.debug: bool = debug
        self.lines: List[str] = lines
        self.line_num: int = 0
        self.environments: List[Environment] = []
        self.in_environment: bool = False
        self.in_agent: bool = False
        self.in_message: bool = False
        self.in_behaviour: bool = False
        self.in_action: bool = False
        self.in_block_declarations: bool = False
        self.nested_blocks_count: int = 0
        
    @property
    def last_environment(self) -> Environment:
        return self.environments[-1] 
    
    @property
    def last_agent(self) -> Agent:
        return self.last_environment.last_agent
    
    @property
    def last_behaviour(self) -> Behaviour:
        return self.last_environment.last_agent.last_behaviour
    
    @property
    def last_action(self) -> Action:
        return self.last_environment.last_agent.last_behaviour.last_action
    
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
        elif self.in_behaviour:
            self.panic('Missing EBEHAV')
        elif self.in_action:
            self.panic('Missing EACTION')
        elif self.nested_blocks_count > 0:
            self.panic('Unclosed blocks')
        elif self.nested_blocks_count < 0:
            self.panic('Blocks closed too many times')

    def panic(self, reason: str) -> None:
        if self.debug:
            for environment in self.environments:
                environment.print()
            pprint(self.__dict__)
        print(f'Line {self.line_num}: {self.lines[self.line_num - 1].strip()}')
        print(reason)
        exit(1)
