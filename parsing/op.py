from typing import List

from intermediate.action import (Action, Declaration, GreaterThan,
                                 LessThanOrEqual, Multiply, Subtract)
from intermediate.agent import Agent
from intermediate.behaviour import Behaviour
from intermediate.param import (DistNormalFloatParam, EnumParam,
                                InitFloatParam, ListParam)
from parsing.state import State
from utils.validation import is_float, is_valid_enum_list


def op_AGENT(state: State, name: str) -> None:    
    state.require(not state.in_agent, 'Already inside an agent.', 'First end current agent using EAGENT.')
    state.require(not state.agent_exists(name), f'Agent {name} already exists in the current environment.')
    
    state.in_agent = True
    state.add_agent(Agent(name))


def op_EAGENT(state: State) -> None:    
    state.require(state.in_agent, 'Not inside any agent.', 'Try defining new agents using AGENT.')
    state.require(not state.in_behaviour, 'Cannot end an agent inside a behaviour.', 'First end current behaviour using EBEHAV.')
    
    state.in_agent = False


def op_PRM(state: State, name: str, category: str, args: List[str]) -> None:    
    state.require(state.in_agent, 'Cannot define parameters outside agent scope.', 'Try defining new agents using AGENT.')
    state.require(not state.in_behaviour, 'Cannot define agent parameters inside a behaviour.', 'Parameters must appear after AGENT.')
    state.require(not state.last_agent.param_exists(name), f'Parameter {name} already exists inside current agent.')
    
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


def op_SETUPBEHAV(state: State, name: str) -> None:    
    state.require(state.in_agent, 'Cannot define behaviours outside agents.', 'Try defining new agents using AGENT.')
    state.require(not state.in_behaviour, 'Cannot define behaviours inside other behaviours.', 'First end current behaviour using EBEHAV.')
    state.require(not state.last_agent.behaviour_exists(name), f'Behaviour {name} already exists in current agent.')
    
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
    
    state.in_action = True
    state.last_behaviour.add_action(Action(name, state.last_agent.param_names))


def op_EACTION(state: State) -> None:            
    state.require(state.in_action, 'Not inside any action.', 'Try defining new actions using ACTION.')
    state.require(state.last_action._nested_blocks_count == 0, 'There are unclosed blocks.', 'Try closing them using EBLOCK.')
    
    state.in_action = False


def op_DECL(state: State, name: str, value: str) -> None:            
    state.require(state.in_action, 'Cannot declare variables outside actions.')
    state.require(not state.last_action.is_name_in_scope(name), f'{name} is already in current scope.')
    state.require(state.last_action.is_name_in_scope(value) or is_float(value), f'{value} not found in current scope.')
    
    state.last_action.add_declaration(Declaration(name, value))


def op_EBLOCK(state: State) -> None:            
    state.require(state.in_action, 'Cannot end blocks outside actions.')
    state.require(state.last_action._nested_blocks_count > 0, 'No more blocks to close', 'Try removing this statement.')
    
    state.last_action.end_block()

    
def handle_non_mutating_statement(state: State, op: str, arg1: str, arg2: str) -> None:
    state.require(state.in_action, 'Not inside any action.', f'{op} can be used inside actions.')     
    state.require(state.last_action.is_name_in_scope(arg1) or is_float(arg1), f'{arg1} is not in the current scope.')
    state.require(state.last_action.is_name_in_scope(arg2) or is_float(arg2), f'{arg2} is not in the current scope.')
    
    match op:
        case 'GT':
            state.last_action.add_instruction(GreaterThan(arg1, arg2))
        case 'LTE':
            state.last_action.add_instruction(LessThanOrEqual(arg1, arg2))
        case _:
            state.panic(f'Unexpected error: {op} {arg1} {arg2}')
    
    state.last_action.start_block()


def handle_mutating_statement(state: State, op: str, arg1: str, arg2: str) -> None:
    state.require(state.in_action, 'Not inside any action', f'{op} can be used inside actions.')
    state.require(state.last_action.is_name_in_scope(arg1) or is_float(arg1), f'{arg1} is not in the current scope.')
    state.require(state.last_action.is_name_in_scope(arg2) or is_float(arg2), f'{arg2} is not in the current scope.')
    state.require(state.last_agent.is_mutable(arg1), f'{arg1} is immutable.', 'If you want to use its value try saving it into a variable declared using DECL.')
    
    match op:
        case 'MULT':
            state.last_action.add_instruction(Multiply(arg1, arg2))
        case 'SUBT':
            state.last_action.add_instruction(Subtract(arg1, arg2))
        case _:
            state.panic(f'Unexpected error: {op} {arg1} {arg2}')
