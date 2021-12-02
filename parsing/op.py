from typing import List

from intermediate.action import (Action, Declaration, GreaterThan,
                                 LessThanOrEqual, Multiply, Subtract)
from intermediate.agent import Agent
from intermediate.behaviour import Behaviour
from intermediate.environment import Environment
from intermediate.param import (DistNormalFloatParam, EnumParam,
                                InitFloatParam, ListParam)
from parsing.state import State
from utils.validation import is_float, is_valid_enum_list


def op_ENVIRONMENT(state: State) -> None:    
    state.require_not(state.in_environment, 'Already inside environment')
    
    state.in_environment = True
    state.add_environment(Environment())


def op_EENVIRONMENT(state: State) -> None:
    state.require(state.in_environment, 'Not inside environment')
    state.require_not(state.in_agent, 'Inside agent')
    
    state.in_environment = False


def op_AGENT(state: State, name: str) -> None:    
    state.require(state.in_environment, 'Not inside environment')
    state.require_not(state.in_agent, 'Already inside agent')
    state.require_not(state.last_environment.agent_exists(name), f'Agent {name} already exists')
    
    state.in_agent = True
    state.last_environment.add_agent(Agent(name))


def op_EAGENT(state: State) -> None:    
    state.require(state.in_agent, 'Not inside agent')
    state.require_not(state.in_behaviour, 'Inside behaviour')
    
    state.in_agent = False


def op_PRM(state: State, name: str, category: str, args: List[str]) -> None:    
    state.require(state.in_agent, 'Not inside agent')
    state.require_not(state.in_behaviour, 'Cannot define agent parameters inside behaviour')
    state.require_not(state.last_agent.param_exists(name), f'Parameter {name} already exists inside agent')
    
    match category, args:
        case 'float', ['init', val]:
            state.require(is_float(val), f'{val} is not valid float')
            state.last_agent.add_init_float(InitFloatParam(name, val))
            
        case 'float', ['dist_normal', mean, std_dev]:
            state.require(is_float(mean), f'{mean} is not valid float')
            state.require(is_float(std_dev), f'{std_dev} is not valid float')
            state.last_agent.add_dist_normal_float(DistNormalFloatParam(name, mean, std_dev))
            
        case 'list', ['conn_list' | 'msg_list']:
            state.last_agent.add_list(ListParam(name))
            
        case 'enum', enums:
            state.require(is_valid_enum_list(enums), f'{enums} is not valid enum list')
            state.last_agent.add_enum(EnumParam(name, enums))
            
        case _:
            state.panic(f'Incorrect operation: PRM {name} {category} {args}')
    

def op_SETUPBEHAV(state: State, name: str):    
    state.require(state.in_agent, 'Not inside agent')
    state.require_not(state.in_behaviour, 'Already inside behaviour')
    state.require_not(state.last_agent.behaviour_exists(name), f'Behaviour {name} already exists in agent')
    
    state.in_behaviour = True
    state.last_agent.add_setup_behaviour(Behaviour(name))
    

def op_EBEHAV(state: State):            
    state.require(state.in_behaviour, 'Not inside behaviour')
    state.require_not(state.in_action, 'Inside action')
    
    state.in_behaviour = False
    

def op_ACTION(state: State, name: str):
    state.require(state.in_behaviour, 'Not inside behaviour')
    state.require_not(state.in_action, 'Already inside action')
    state.require_not(state.last_behaviour.action_exists(name), f'Action {name} already exists in behaviour')
    
    state.in_action = True
    state.last_behaviour.add_action(Action(name, state.last_agent.param_names))
            
    
def op_EACTION(state: State):            
    state.require(state.in_action, 'Not inside action')
    state.require(state.last_action._nested_blocks_count == 0, 'There are unclosed blocks')
    
    state.in_action = False


def op_DECL(state: State, name: str, value: str):            
    state.require(state.in_action, 'Not inside action')
    state.require_not(state.last_action.is_name_in_scope(name), f'{name} already in scope')
    
    state.last_action.add_declaration(Declaration(name, value))


def op_EBLOCK(state: State):            
    state.require(state.in_action, 'Not inside action')
    state.require(state.last_action._nested_blocks_count > 0, 'No more blocks to close')
    
    state.last_action.end_block()
    
    
def handle_non_mutating_statement(state: State, op: str, arg1: str, arg2: str) -> None:
    state.require(state.in_action, 'Not inside action')     
    state.require(state.last_action.is_name_in_scope(arg1), f'{arg1} not in scope')
    state.require(state.last_action.is_name_in_scope(arg2), f'{arg2} not in scope')
    
    match op:
        case 'GT':
            state.last_action.add_instruction(GreaterThan(arg1, arg2))
        case 'LTE':
            state.last_action.add_instruction(LessThanOrEqual(arg1, arg2))
        case _:
            state.panic(f'Unexpected error: {op} {arg1} {arg2}')
    
    state.last_action.start_block()


def handle_mutating_statement(state: State, op: str, arg1: str, arg2: str) -> None:
    state.require(state.in_action, 'Not inside action')
    state.require(state.last_action.is_name_in_scope(arg1), f'{arg1} not in scope')
    state.require(state.last_action.is_name_in_scope(arg2), f'{arg2} not in scope')
    state.require(state.last_agent.is_mutable(arg1), f'{arg1} is immutable')
    
    match op:
        case 'MULT':
            state.last_action.add_instruction(Multiply(arg1, arg2))
        case 'SUBT':
            state.last_action.add_instruction(Subtract(arg1, arg2))
        case _:
            state.panic(f'Unexpected error: {op} {arg1} {arg2}')
