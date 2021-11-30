from environment import Environment
from state import State
from agent import Agent
from param import EnumParam, FloatParam, ListParam


def op_ENVIRONMENT(state: State) -> None:
    match state.in_environment, state.in_agent:
        case False, False:
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
            state.panic(f'Incorrect operation: EAGENT {name}')


def op_EAGENT(state: State) -> None:
    match state.in_environment, state.in_agent:
        case True, True:
            state.in_agent = False
        case _:
            state.panic('Incorrect operation: EAGENT')


def op_PRM(state: State, name: str, category: str) -> None:
    match state.in_environment, state.in_agent:
        case True, True if not state.last_agent.param_exists(name):
            match category:
                case 'float':
                    state.last_agent.add_float(FloatParam(name))
                case 'enum':
                    state.last_agent.add_enum(EnumParam(name))
                case 'list':
                    state.last_agent.add_list(ListParam(name))
                case _:
                    state.panic(f'Incorrect operation: PRM {name} {category}')
        case _:
            state.panic(f'Incorrect operation: PRM {name} {category}')


def op_SPRM(state: State, name: str, subcategory: str) -> None:
    match state.in_environment, state.in_agent:
        case True, True if state.last_agent.param_exists(name):
            match state.last_agent.get_param(name).category:
                case 'float' if subcategory in ('init', 'dist_normal'):
                    state.last_agent.get_param(name).subcategory = subcategory
                case 'enum' if subcategory in ('enum_init', 'enum_percent'):
                    state.last_agent.get_param(name).subcategory = subcategory
                case 'list' if subcategory in ('conn_list', 'msg_list'):
                    state.last_agent.get_param(name).subcategory = subcategory
                case _:
                    state.panic(f'Incorrect operation: SPRM {name} {subcategory}')
        case _:
            state.panic(f'Incorrect operation: SPRM {name} {subcategory}')
            

def op_EVAL(state: State, name: str, value: str) -> None:
    match state.in_environment, state.in_agent:
        case True, True if not state.last_agent.enum_value_exists(name):
            state.last_agent.add_enum_value(name, value)
        case _:
            state.panic(f'Incorrect operation: EVAL {name} {value}')


def op_AARG(state: State, name: str, value: str) -> None:
    match state.in_environment, state.in_agent:
        case True, True if state.last_agent.param_exists(name):
            match state.last_agent.get_param(name).category:
                case 'float':
                    state.last_agent.get_param(name).add_subcategory_arg(value)
                case 'enum' if state.last_agent.enum_value_exists(value):
                    state.last_agent.get_param(name).add_subcategory_arg(state.last_agent.get_enum_value(value))
                case _:
                    state.panic(f'Incorrect operation: AARG {name} {value}')
        case _:
            state.panic(f'Incorrect operation: AARG {name} {value}')
