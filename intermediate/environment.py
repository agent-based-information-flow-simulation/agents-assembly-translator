from typing import Dict

from intermediate.agent import Agent
from intermediate.message import Message


class Environment:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.messages: Dict[str, Message] = {}
        
    @property
    def last_agent(self) -> Agent:
        return self.agents[list(self.agents.keys())[-1]]
    
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
        
    def print(self) -> None:
        print('Environment:')
        print('- Agents:')
        for agent in self.agents.values():
            agent.print()
        print('- Messages:')
        for message in self.messages.values():
            message.print()
