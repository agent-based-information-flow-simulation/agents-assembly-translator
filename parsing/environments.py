from parsing.state import State
from parsing.op import op_AGENT, op_EAGENT, op_EENVIRONMENT, op_ENVIRONMENT, op_PRM
from intermediate.environment import Environment
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
                
            case ['PRM', name, category, *args]:
                op_PRM(state, name, category, args)
                
            case _:
                state.panic(f'Unknown tokens: {tokens}')
                
    state.verify_end_state()
    return state.environments
