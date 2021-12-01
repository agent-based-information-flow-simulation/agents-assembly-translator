from typing import List

from intermediate.environment import Environment
from parsing.op import (op_ACTION, op_AGENT, op_DECL, op_EACTION, op_EAGENT,
                        op_EBEHAV, op_EBLOCK, op_EENVIRONMENT, op_ENVIRONMENT,
                        op_GT, op_LTE, op_MULT, op_PRM, op_SETUPBEHAV, op_SUBT)
from parsing.state import State


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
                
            case ['SETUPBEHAV', name]:
                op_SETUPBEHAV(state, name)
                
            case ['EBEHAV']:
                op_EBEHAV(state)
                
            case ['ACTION', name]:
                op_ACTION(state, name)
                
            case ['EACTION']:
                op_EACTION(state)
                
            case ['DECL', name, value]:
                op_DECL(state, name, value)
                
            case ['GT', arg1, arg2]:
                op_GT(state, arg1, arg2)
                
            case ['LTE', arg1, arg2]:
                op_LTE(state, arg1, arg2)
                
            case ['EBLOCK']:
                op_EBLOCK(state)
                
            case ['MULT', arg1, arg2]:
                op_MULT(state, arg1, arg2)
                
            case ['SUBT', arg1, arg2]:
                op_SUBT(state, arg1, arg2)
 
            case _:
                state.panic(f'Unknown tokens: {tokens}')
                
    state.verify_end_state()
    return state.environments