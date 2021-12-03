from typing import List

from parsing.op import (handle_math_statement, handle_ordered_conditional_statement, handle_unordered_conditional_statement,
                        op_ACTION, op_AGENT,
                        op_DECL, op_EACTION, op_EAGENT, op_EBEHAV, op_EBLOCK,
                        op_PRM, op_SETUPBEHAV)
from parsing.state import ParsedData, State


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
                
            case [ 'IE' | 'INE' |   'WE' | 'WNE' as op, arg1, arg2]:
                handle_unordered_conditional_statement(state, op, arg1, arg2)
                
            case ['IGT' | 'IGTE' | 'ILT' | 'ILTE' | 'WGT' | 'WGTE' | 'WLT' | 'WLTE' as op, arg1, arg2]:
                handle_ordered_conditional_statement(state, op, arg1, arg2)
                
            case [ 'ADD' | 'SUBT' | 'MULT' | 'DIV' as op, arg1, arg2]:
                handle_math_statement(state, op, arg1, arg2)
 
            case _:
                state.panic(f'Unknown tokens: {tokens}')

    return state.get_parsed_data()
