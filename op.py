from environment import Environment
from state import State
from agent import Agent
from param import EnumParam, ListParam, InitFloatParam, DistNormalFloatParam
from typing import List
from utils import is_float, is_valid_enum_list


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
    match state.in_agent:
        case True:
            state.in_agent = False
        case _:
            state.panic('Incorrect operation: EAGENT')


def op_PRM(state: State, name: str, category: str, args: List[str]) -> None:
    match state.in_agent:
        case True if not state.last_agent.param_exists(name):
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
