from typing import List

from intermediate.agent import Agent


def get_imports() -> List[str]:
    code = []
    code.append(f'import random as r\n')
    code.append(f'import spade\n')
    code.append(f'from numpy.random import normal\n')
    code.append('\n')
    return code


def generate_agent(agent_name: str, agent_body: Agent) -> List[str]:
    code = []
    code.append('\n')
    code.append(f'class {agent_name}(spade.agent.Agent):\n')
    code.append(f'    def __init__(self, jid, password, location, connections):\n')
    code.append(f'        super().__init__(jid, password, verify_security=False)\n')
    
    for param in agent_body.init_floats.values():
        code.append(f'        self.{param.name} = {param.value}\n')

    for param in agent_body.dist_normal_floats.values():
        code.append(f'        self.{param.name} = normal({param.mean}, {param.std_dev})\n')
    
    for param in agent_body.enums.values():            
        names = []
        weights = []
        for name, weight in param.enums:
            names.append(f'\"{name}\"')
            weights.append(weight)
        names = f'[{", ".join(names)}]'
        weights = f'[{", ".join(weights)}]'
        code.append(f'        self.{param.name} = r.choices({names}, {weights})[0]\n')
    
    for param in agent_body.lists.values():
        code.append(f'        self.{param.name} = []\n')
            
    return code
