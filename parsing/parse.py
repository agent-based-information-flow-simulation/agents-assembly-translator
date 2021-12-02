from typing import List

from parsing.op import (handle_mutating_statement,
                        handle_non_mutating_statement, op_ACTION, op_AGENT,
                        op_DECL, op_EACTION, op_EAGENT, op_EBEHAV, op_EBLOCK,
                        op_PRM, op_SETUPBEHAV)
from parsing.state import State, ParsedData


def parse_lines(lines: List[str], debug: bool) -> ParsedData:
    state = State(lines, debug)
    for tokens in state.tokens_from_lines():
        match tokens:                                        
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
                
            case ['EBLOCK']:
                op_EBLOCK(state)
                
            case ['IGT' | 'ILTE' as op, arg1, arg2]:
                handle_non_mutating_statement(state, op, arg1, arg2)
                
            case ['MULT' | 'SUBT' as op, arg1, arg2]:
                handle_mutating_statement(state, op, arg1, arg2)
 
            case _:
                state.panic(f'Unknown tokens: {tokens}')

    return state.get_parsed_data()
