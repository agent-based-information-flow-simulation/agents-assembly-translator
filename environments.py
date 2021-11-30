from state import State
from op import op_AARG, op_AGENT, op_EAGENT, op_EENVIRONMENT, op_ENVIRONMENT, op_EVAL, op_PRM, op_SPRM
from environment import Environment
from typing import List


def get_environments(lines: List[str], debug: bool) -> List[Environment]:
    state = State(lines, debug)
    for tokens in state.tokens_from_lines():
        match tokens:                        
            case ['ENVIRONMENT']:
                op_ENVIRONMENT(state)
                
            case ['EENVIRONMENT']:
                op_EENVIRONMENT(state)
                
            case ['AGENT', name]:
                op_AGENT(state, name)
            
            case ['EAGENT']:
                op_EAGENT(state)
                
            case ['PRM', name, category]:
                op_PRM(state, name, category)
                
            case ['SPRM', name, subcategory]:
                op_SPRM(state, name, subcategory)
                
            case ['EVAL', name, value]:
                op_EVAL(state, name, value)
 
            case ['AARG', name, value]:
                op_AARG(state, name, value)
                
            case _:
                state.panic(f'Unknown tokens: {tokens}')
                
    state.verify_end_state()
    return state.environments
