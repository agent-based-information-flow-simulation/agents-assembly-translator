from pprint import pprint
from typing import Generator, List, Dict

from intermediate.action import Action
from intermediate.agent import Agent
from intermediate.behaviour import Behaviour
from intermediate.message import Message


class ParsedData:
    def __init__(self, agents: List[Agent], messages: List[Message]):
        self.agents: List[Agent] = agents
        self.messages: List[Message] = messages


class State:
    def __init__(self, lines: List[str], debug: bool):
        self.debug: bool = debug
        self.lines: List[str] = lines
        self.line_num: int = 0
        self.in_agent: bool = False
        self.in_message: bool = False
        self.in_behaviour: bool = False
        self.in_action: bool = False
        self.agents: Dict[str, Agent] = {}
        self.messages: Dict[str, Message] = {}
        
    @property
    def last_agent(self) -> Agent:
        return self.agents[list(self.agents.keys())[-1]]
    
    @property
    def last_behaviour(self) -> Behaviour:
        return self.last_agent.last_behaviour
    
    @property
    def last_action(self) -> Action:
        return self.last_agent.last_behaviour.last_action
    
    @property
    def last_message(self) -> Message:
        return self.messages[list(self.messages.keys())[-1]]
    
    def add_agent(self, agent: Agent) -> None:
        self.agents[agent.name] = agent
        
    def add_message(self, message: Message) -> None:
        self.messages[message.name] = message
        
    def agent_exists(self, name: str) -> bool:
        return name in self.agents
    
    def message_exists(self, name: str) -> bool:
        return name in self.messages
            
    def tokens_from_lines(self) -> Generator[list[str], None, None]:
        for line in self.lines:
            self.line_num += 1
            uncommented = line.split('#')[0]
            tokens = [token.strip() for token in uncommented.replace(',', ' ').split()]
            if tokens:
                yield tokens
                
    def print(self) -> None:
        print('- Agents:')
        for agent in self.agents.values():
            agent.print()
        print('- Messages:')
        for message in self.messages.values():
            message.print()
            
    def verify_end_state(self) -> None:
        if self.in_agent:
            self.panic('Missing EAGENT')
            
    def get_parsed_data(self) -> ParsedData:
        self.verify_end_state()
        if self.debug:
            self.print()
        return ParsedData(list(self.agents.values()), list(self.messages.values()))

    def panic(self, reason: str, suggestion: str = '') -> None:
        if self.debug:
            pprint(self.__dict__)
            self.print()
        print(f'🔥 Error in line {self.line_num}: {self.lines[self.line_num - 1].strip()}')
        print(reason)
        if suggestion:
            print(suggestion)
        exit(1)

    def require(self, expr: bool, msg_on_error: str, suggestion_on_error: str = '') -> None:
        if not expr:
            self.panic(msg_on_error, suggestion_on_error)
