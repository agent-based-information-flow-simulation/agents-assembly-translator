from typing import Dict

from intermediate.action import Action


class Behaviour:
    def __init__(self, name: str):
        self.name = name
        self.actions: Dict[str, Action] = {}
        
    @property
    def last_action(self) -> Action:
        return self.actions[list(self.actions.keys())[-1]]
    
    def add_action(self, action: Action) -> None:
        self.actions[action.name] = action
        
    def action_exists(self, name: str) -> bool:
        return name in self.actions

    def print(self) -> None:
        print(f'Behaviour {self.name}')
        for action in self.actions.values():
            action.print()
