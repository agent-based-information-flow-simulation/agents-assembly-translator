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

    def panic(self, reason: str) -> None:
        if self.debug:
            for environment in self.environments:
                environment.print()
            pprint(self.__dict__)
        print(f'Line {self.line_num}: {self.lines[self.line_num - 1].strip()}')
        print(reason)
        exit(1)
        
    # def require_in(self, state: bool, msg_on_error: str) -> None:
    #     if not state:
    #         self.panic(msg_on_error)
            
    # def require_not_in(self, state: bool, msg_on_error: str) -> None:
    #     if state:
    #         self.panic(msg_on_error)
            
    # def require_agent_doesnt_exist(self, agent_name: str, msg_on_error: str) -> None:
    #     if self.last_environment.agent_exists(agent_name):
    #         self.panic(msg_on_error)
            
    # def require_agent_param_doesnt_exist(self, param_name: str, msg_on_error: str) -> None:
    #     if self.last_agent.param_exists(param_name):
    #         self.panic(msg_on_error)
            
    # def require_agent_behaviour_doesnt_exist(self, behaviour_name: str, msg_on_error: str) -> None:
    #     if self.last_agent.behaviour_exists(behaviour_name):
    #         self.panic(msg_on_error)
            
    def require(self, expr: bool, msg_on_error: str):
        if not expr:
            self.panic(msg_on_error)
            
    def require_not(self, expr: bool, msg_on_error: str):
        if expr:
            self.panic(msg_on_error)


# class Require:
#     def __init__(self, state: State):
#         self.state = state

#     def in_state(self, required_state: bool, msg_on_error: str):
#         if not required_state:
#             self.state.panic(f'Invalid state: {msg_on_error}')
    
#     @classmethod
#     def in_block_scope(state: State, arg_name: str):
#         if not state.last_action.is_name_in_scope(arg_name):
#             state.panic(f'{arg_name} not in scope')
        
#     @classmethod
#     def mutable(state: State, arg_name: str):
#         if not state.last_agent.is_immutable(arg_name):
#             state.panic(f'{arg_name} is immutable')
        
#     @classmethod
#     def require_