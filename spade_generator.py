from agent import Agent
from typing import List


def get_imports() -> List[str]:
    code = []
    code.append(f'import random as r\n')
    code.append(f'import spade\n')
    code.append(f'from numpy.random import normal\n')
    code.append('\n')
    return code


def generate_agent(agent_name: str, agent_body: Agent):
    code = []
    code.append('\n')
    code.append(f'class {agent_name}(spade.agent.Agent):\n')
    code.append(f'    def __init__(self, jid, password, location, connections):\n')
    code.append(f'        super().__init__(jid, password, verify_security=False)\n')
    
    for param in agent_body.floats.values():
        if param.subcategory == 'init':
            code.append(f'        self.{param.name} = {param.subcategory_args[0]}\n')

        elif param.subcategory == 'dist_normal':
            code.append(f'        self.{param.name} = normal({param.subcategory_args[0]}, {param.subcategory_args[1]})\n')
    
    for param in agent_body.enums.values():
        if param.subcategory == 'enum_init':
            inital_value = ''
            for name, value in param.subcategory_args:
                if value == '100':
                    inital_value = name
            code.append(f'        self.{param.name} = "{inital_value}"\n')
            
        elif param.subcategory == 'enum_percent':
            names = []
            weights = []
            for name, value in param.subcategory_args:
                names.append(f'\"{name}\"')
                weights.append(value)
            names = f'[{", ".join(names)}]'
            weights = f'[{", ".join(weights)}]'
            choose_enum = f'r.choices({names}, {weights})'
            code.append(f'        self.{param.name} = {choose_enum}\n')
    
    for param in agent_body.lists.values():
        code.append(f'        self.{param.name} = []\n')
            
    return code
