from __future__ import annotations

from typing import TYPE_CHECKING, List

from parsing.op import (handle_math_statement,
                        handle_ordered_conditional_statement,
                        handle_unordered_conditional_statement, op_ACTION,
                        op_ADDELEM, op_AGENT, op_DECL, op_EACTION, op_EAGENT,
                        op_EBEHAV, op_EBLOCK, op_EMESSAGE, op_MESSAGE, op_SET, op_SETUPBEHAV, op_agent_PRM, op_message_PRM)
from parsing.state import State

if TYPE_CHECKING:
    from parsing.state import ParsedData


def parse_lines(lines: List[str], debug: bool) -> ParsedData:
    state = State(lines, debug)
    for tokens in state.tokens_from_lines():
        match tokens:                                        
            case [ 'AGENT', name ]:
                op_AGENT(state, name)
            
            case [ 'EAGENT' ]:
                op_EAGENT(state)
                
            case [ 'MESSAGE', name ]:
                op_MESSAGE(state, name)
            
            case [ 'EMESSAGE' ]:
                op_EMESSAGE(state)
                
            case [ 'PRM', name, category ]:
                op_message_PRM(state, name, category)
                
            case [ 'PRM', name, category, *args ]:
                op_agent_PRM(state, name, category, args)
                
            case [ 'SETUPBEHAV', name ]:
                op_SETUPBEHAV(state, name)
                
            case [ 'EBEHAV' ]:
                op_EBEHAV(state)
                
            case [ 'ACTION', name ]:
                op_ACTION(state, name)
                
            case [ 'EACTION' ]:
                op_EACTION(state)
                
            case [ 'DECL', name, value ]:
                op_DECL(state, name, value)
                
            case [ 'EBLOCK' ]:
                op_EBLOCK(state)
                
            case [ 'IE' | 'INE' | 'WE' | 'WNE' as op, arg1, arg2 ]:
                handle_unordered_conditional_statement(state, op, arg1, arg2)
                
            case [ 'IGT' | 'IGTE' | 'ILT' | 'ILTE' | 'WGT' | 'WGTE' | 'WLT' | 'WLTE' as op, arg1, arg2 ]:
                handle_ordered_conditional_statement(state, op, arg1, arg2)
                
            case [ 'ADD' | 'SUBT' | 'MULT' | 'DIV' as op, arg1, arg2 ]:
                handle_math_statement(state, op, arg1, arg2)
                
            case [ 'ADDELEM' | 'ADDE', arg1, arg2 ]:
                op_ADDELEM(state, arg1, arg2)
                
            case [ 'SET', arg1, arg2 ]:
                op_SET(state, arg1, arg2)
                
            case _:
                state.panic(f'Unknown tokens: {tokens}')

    return state.get_parsed_data()
