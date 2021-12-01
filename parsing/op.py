from typing import List

from intermediate.action import Action, Declaration, GreaterThan
from intermediate.agent import Agent
from intermediate.behaviour import Behaviour
from intermediate.environment import Environment
from intermediate.param import (DistNormalFloatParam, EnumParam,
                                InitFloatParam, ListParam)
from parsing.state import State
from utils.validation import is_float, is_valid_enum_list


def op_ENVIRONMENT(state: State) -> None:
    match state.in_environment:
        case False:
            state.in_environment = True
            state.add_environment(Environment())
        case _:
            state.panic('Incorrect operation: ENVIRONMENT')


def op_EENVIRONMENT(state: State) -> None:
    match state.in_environment, state.in_agent:
        case True, False:
            state.in_environment = False
        case _:
            state.panic('Incorrect operation: EENVIRONMENT')


def op_AGENT(state: State, name: str) -> None:
    match state.in_environment, state.in_agent:
        case True, False if not state.last_environment.agent_exists(name):
            state.in_agent = True
            state.last_environment.add_agent(Agent(name))
        case _:
            state.panic(f'Incorrect operation: AGENT {name}')


def op_EAGENT(state: State) -> None:
    match state.in_agent, state.in_behaviour:
        case True, False:
            state.in_agent = False
        case _:
            state.panic('Incorrect operation: EAGENT')


def op_PRM(state: State, name: str, category: str, args: List[str]) -> None:
    match state.in_agent, state.in_behaviour:
        case True, False if not state.last_agent.param_exists(name):
            match category, args:
                case 'float', ['init', val] if is_float(val):
                    state.last_agent.add_init_float(InitFloatParam(name, val))
                case 'float', ['dist_normal', mean, std_dev] if is_float(mean) and is_float(std_dev):
                    state.last_agent.add_dist_normal_float(DistNormalFloatParam(name, mean, std_dev))
                case 'list', ['conn_list' | 'msg_list']:
                    state.last_agent.add_list(ListParam(name))
                case 'enum', enums if is_valid_enum_list(enums):
                    state.last_agent.add_enum(EnumParam(name, enums))
                case _:
                    state.panic(f'Incorrect operation: PRM {name} {category} {args}')
        case _:
            state.panic(f'Incorrect operation: PRM {name} {category} {args}')


def op_SETUPBEHAV(state: State, name: str):
    match state.in_agent, state.in_behaviour:
        case True, False if not state.last_agent.behaviour_exists(name):
            state.last_agent.add_setup_behaviour(Behaviour(name))
            state.in_behaviour = True
        case _:
            state.panic(f'Incorrect operation: SETUPBEHAV {name}')


def op_EBEHAV(state: State):
    match state.in_behaviour, state.in_action:
        case True, False:
            state.in_behaviour = False
        case _:
            state.panic('Incorrect operation: EBEHAV')
    

def op_ACTION(state: State, name: str):
    match state.in_behaviour, state.in_action:
        case True, False if not state.last_behaviour.action_exists(name):
            state.last_agent.last_behaviour.add_action(Action(name))
            state.in_action = True
        case _:
            state.panic(f'Incorrect operation: ACTION {name}')

    
def op_EACTION(state: State):
    match state.in_action, state.nested_blocks_count:
        case True, 0:
            state.in_action = False
        case _:
            state.panic('Incorrect operation: EACTION')


def op_DECL(state: State, name: str, value: str):
    match state.in_action:
        case True if not state.last_action.declaration_exists(name):
            state.last_action.add_declaration(Declaration(name, value, state.last_agent))
        case _:
            state.panic(f'Incorrect operation: DECL {name} {value}')


def op_GT(state: State, arg1: str, arg2: str):
    match state.in_action:
        case True if state.last_action.is_name_in_scope(arg1) and state.last_action.is_name_in_scope(arg2):
            state.last_action.add_expression(GreaterThan(arg1, arg2))
        case _:
            state.panic(f'Incorrect operation: GT {arg1} {arg2}')
    
def op_LTE(state: State, arg1: str, arg2: str):
    ...
    
def op_EBLOCK(state: State):
    ...
    
    
def op_MULT(state: State, arg1: str, arg2: str):
    ...
    
    
def op_SUBT(state: State, arg1: str, arg2: str):
    ...