from __future__ import annotations

from typing import TYPE_CHECKING, List

from intermediate.action import (Action, Add, AddElement, Declaration, Divide,
                                 IfEqual, IfGreaterThan, IfGreaterThanOrEqual,
                                 IfLessThan, IfLessThanOrEqual, IfNotEqual,
                                 Multiply, Set, Subtract, WhileEqual,
                                 WhileGreaterThan, WhileGreaterThanOrEqual,
                                 WhileLessThan, WhileLessThanOrEqual,
                                 WhileNotEqual)
from intermediate.agent import Agent
from intermediate.behaviour import Behaviour
from intermediate.message import Message
from intermediate.param import (DistNormalFloatParam, EnumParam,
                                InitFloatParam, ListParam, MessageFloatParam)
from parsing.argument import Argument
from utils.validation import is_float, is_valid_enum_list

if TYPE_CHECKING:
    from parsing.state import State


def op_AGENT(state: State, name: str) -> None:    
    state.require(not state.in_agent, 'Already inside an agent.', 'First end current agent using EAGENT.')
    state.require(not state.in_message, 'Cannot define agents inside messages.', 'First end current message using EMESSAGE.')
    state.require(not state.agent_exists(name), f'Agent {name} already exists in the current environment.')
    state.require(not name[0].isdigit(), f'{name} is not correct.', 'Names cannot start with a digit.')
    
    state.in_agent = True
    state.add_agent(Agent(name))


def op_EAGENT(state: State) -> None:    
    state.require(state.in_agent, 'Not inside any agent.', 'Try defining new agents using AGENT.')
    state.require(not state.in_behaviour, 'Cannot end an agent inside a behaviour.', 'First end current behaviour using EBEHAV.')
    
    state.in_agent = False
    
    
def op_MESSAGE(state: State, name: str) -> None:
    state.require(not state.in_message, 'Already inside a message.', 'First end current message using EMESSAGE.')
    state.require(not state.in_agent, 'Cannot define messages inside agents.', 'First end current agent using EAGENT.')
    state.require(not state.message_exists(name), f'Message {name} already exists in the current environment.')
    state.require(not name[0].isdigit(), f'{name} is not correct.', 'Names cannot start with a digit.')
    
    state.in_message = True
    state.add_message(Message(name))


def op_EMESSAGE(state: State) -> None:    
    state.require(state.in_message, 'Not inside any message.', 'Try defining new messages using MESSAGE.')
    
    state.in_message = False


def op_agent_PRM(state: State, name: str, category: str, args: List[str]) -> None:    
    state.require(state.in_agent, 'Cannot define agent parameters outside agent scope.', 'Try defining new agents using AGENT.')
    state.require(not state.in_behaviour, 'Cannot define agent parameters inside a behaviour.', 'Parameters must appear after AGENT.')
    state.require(not state.last_agent.param_exists(name), f'Parameter {name} already exists inside current agent.')
    state.require(not name[0].isdigit(), f'{name} is not correct.', 'Names cannot start with a digit.')
    
    match category, args:
        case 'float', ['init', val]:
            state.require(is_float(val), f'{val} is not a valid float.')
            state.last_agent.add_init_float(InitFloatParam(name, val))
            
        case 'float', ['dist_normal', mean, std_dev]:
            state.require(is_float(mean), f'{mean} is not a valid float.')
            state.require(is_float(std_dev), f'{std_dev} is not a valid float.')
            state.last_agent.add_dist_normal_float(DistNormalFloatParam(name, mean, std_dev))
            
        case 'list', ['conn_list' | 'msg_list']:
            state.last_agent.add_list(ListParam(name))
            
        case 'enum', enums:
            state.require(is_valid_enum_list(enums), f'{enums} is not a valid enum list.', 'The correct pattern is [name, percent, ...], where percent(s) sum up to 100 (+/- 1).')
            state.last_agent.add_enum(EnumParam(name, enums))
            
        case _:
            state.panic(f'Incorrect operation: PRM {name} {category} {args}')
 

def op_message_PRM(state: State, name: str, category: str) -> None:    
    state.require(state.in_message, 'Cannot define message parameters outside message scope.', 'Try defining new messages using MESSAGE.')
    state.require(not state.last_message.param_exists(name), f'Parameter {name} already exists inside current message.')
    state.require(not name[0].isdigit(), f'{name} is not correct.', 'Names cannot start with a digit.')
    
    state.last_message.add_float(MessageFloatParam(name))


def op_SETUPBEHAV(state: State, name: str) -> None:    
    state.require(state.in_agent, 'Cannot define behaviours outside agents.', 'Try defining new agents using AGENT.')
    state.require(not state.in_behaviour, 'Cannot define behaviours inside other behaviours.', 'First end current behaviour using EBEHAV.')
    state.require(not state.last_agent.behaviour_exists(name), f'Behaviour {name} already exists in current agent.')
    state.require(not name[0].isdigit(), f'{name} is not correct.', 'Names cannot start with a digit.')
    
    state.in_behaviour = True
    state.last_agent.add_setup_behaviour(Behaviour(name))


def op_EBEHAV(state: State) -> None:            
    state.require(state.in_behaviour, 'Not inside any behaviour.', 'Try defining new behaviours using BEHAV.')
    state.require(not state.in_action, 'Cannot end behaviours inside actions.', 'Try ending current action using EACTION.')
    
    state.in_behaviour = False


def op_ACTION(state: State, name: str) -> None:
    state.require(state.in_behaviour, 'Actions must be definied inside behaviours.', 'Try defining new behaviours using BEHAV.')
    state.require(not state.in_action, 'Cannot define an action in another action.', 'Try finishing current action using EACTION.')
    state.require(not state.last_behaviour.action_exists(name), f'Action {name} already exists in current behaviour.')
    state.require(not name[0].isdigit(), f'{name} is not correct.', 'Names cannot start with a digit.')
    
    state.in_action = True
    state.last_behaviour.add_action(Action(name))


def op_EACTION(state: State) -> None:            
    state.require(state.in_action, 'Not inside any action.', 'Try defining new actions using ACTION.')
    state.require(state.last_action._nested_blocks_count == 0, 'There are unclosed blocks.', 'Try closing them using EBLOCK.')
    
    state.in_action = False


def op_DECL(state: State, name: str, value: str) -> None:            
    state.require(state.in_action, 'Cannot declare variables outside actions.')
    state.require(not name[0].isdigit(), f'{name} is not correct.', 'Names cannot start with a digit.')
    lhs = Argument(state, name)
    rhs = Argument(state, value)
    state.require(lhs.declaration_context(rhs), 'Mismatched types in the declaration context.', f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}')
    
    state.last_action.add_declaration(Declaration(lhs, rhs))


def op_EBLOCK(state: State) -> None:            
    state.require(state.in_action, 'Cannot end blocks outside actions.')
    state.require(state.last_action._nested_blocks_count > 0, 'No more blocks to close', 'Try removing this statement.')
    
    state.last_action.end_block()


def handle_unordered_conditional_statement(state: State, op: str, arg1: str, arg2: str) -> None:
    state.require(state.in_action, 'Not inside any action.', f'{op} can be used inside actions.')     
    lhs = Argument(state, arg1)
    rhs = Argument(state, arg2)
    state.require(lhs.unordered_comparaison_context(rhs), 'Mismatched types in the unordered comparaison context.', f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}')
    
    match op:
        case 'IE':
            state.last_action.add_instruction(IfEqual(lhs, rhs))
        case 'INE':
            state.last_action.add_instruction(IfNotEqual(lhs, rhs))
        case 'WE':
            state.last_action.add_instruction(WhileEqual(lhs, rhs))
        case 'WNE':
            state.last_action.add_instruction(WhileNotEqual(lhs, rhs))
        case _:
            state.panic(f'Unexpected error: {op} {arg1} {arg2}')
    
    state.last_action.start_block()
    
    
def handle_ordered_conditional_statement(state: State, op: str, arg1: str, arg2: str) -> None:
    state.require(state.in_action, 'Not inside any action.', f'{op} can be used inside actions.')     
    lhs = Argument(state, arg1)
    rhs = Argument(state, arg2)
    state.require(lhs.ordered_comparaison_context(rhs), 'Mismatched types in the ordered comparaison context.', f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}')
    
    match op:
        case 'IGT':
            state.last_action.add_instruction(IfGreaterThan(lhs, rhs))
        case 'IGTE':
            state.last_action.add_instruction(IfGreaterThanOrEqual(lhs, rhs))
        case 'ILT':
            state.last_action.add_instruction(IfLessThan(lhs, rhs))
        case 'ILTE':
            state.last_action.add_instruction(IfLessThanOrEqual(lhs, rhs))
        case 'WGT':
            state.last_action.add_instruction(WhileGreaterThan(lhs, rhs))
        case 'WGTE':
            state.last_action.add_instruction(WhileGreaterThanOrEqual(lhs, rhs))
        case 'WLT':
            state.last_action.add_instruction(WhileLessThan(lhs, rhs))
        case 'WLTE':
            state.last_action.add_instruction(WhileLessThanOrEqual(lhs, rhs))
        case _:
            state.panic(f'Unexpected error: {op} {arg1} {arg2}')
    
    state.last_action.start_block()


def handle_math_statement(state: State, op: str, arg1: str, arg2: str) -> None:
    state.require(state.in_action, 'Not inside any action', f'{op} can be used inside actions.')
    lhs = Argument(state, arg1)
    rhs = Argument(state, arg2)
    state.require(lhs.math_context(rhs), 'Mismatched types in the math statement.', f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}')
    match op:
        case 'ADD':
            state.last_action.add_instruction(Add(lhs, rhs))
        case 'SUBT':
            state.last_action.add_instruction(Subtract(lhs, rhs))
        case 'MULT':
            state.last_action.add_instruction(Multiply(lhs, rhs))
        case 'DIV':
            state.last_action.add_instruction(Divide(lhs, rhs))
        case _:
            state.panic(f'Unexpected error: {op} {arg1} {arg2}')


def op_ADDELEM(state: State, arg1: str, arg2: str) -> None:            
    state.require(state.in_action, 'Not inside any action.', f'ADDELEM can be used inside actions.')
    lhs = Argument(state, arg1)
    rhs = Argument(state, arg2)
    state.require(lhs.array_modification_context(rhs), 'Mismatched types in the list modification context.', f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}')
    
    state.last_action.add_instruction(AddElement(lhs, rhs))


def op_SET(state: State, arg1: str, arg2: str) -> None:
    state.require(state.in_action, 'Not inside any action.', f'SET can be used inside actions.')
    lhs = Argument(state, arg1)
    rhs = Argument(state, arg2)
    state.require(lhs.assignment_context(rhs), 'Mismatched types in the assignment context.', f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}')
    
    state.last_action.add_instruction(Set(lhs, rhs))
