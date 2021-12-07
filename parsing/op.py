from __future__ import annotations

from typing import TYPE_CHECKING, List

from intermediate.action import (Add, AddElement, Clear, Declaration, Divide, ExpDist,
                                 IfEqual, IfGreaterThan, IfGreaterThanOrEqual,
                                 IfInList, IfLessThan, IfLessThanOrEqual,
                                 IfNotEqual, IfNotInList, Length,
                                 ModifySelfAction, Multiply, NormalDist, RemoveElement,
                                 RemoveNElements, Round, Send, SendMessageAction, Set,
                                 Subset, Subtract, UniformDist, WhileEqual,
                                 WhileGreaterThan, WhileGreaterThanOrEqual,
                                 WhileLessThan, WhileLessThanOrEqual,
                                 WhileNotEqual)
from intermediate.agent import Agent
from intermediate.argument import Argument
from intermediate.behaviour import (CyclicBehaviour, MessageReceivedBehaviour,
                                    OneTimeBehaviour, SetupBehaviour)
from intermediate.message import Message
from intermediate.param import (AgentConnectionListParam,
                                AgentDistExpFloatParam,
                                AgentDistNormalFloatParam, AgentEnumParam,
                                AgentInitFloatParam, AgentMessageListParam,
                                MessageFloatParam)
from utils.validation import (is_float, is_valid_enum_list, is_valid_name,
                              print_invalid_names)

if TYPE_CHECKING:
    from parsing.state import State


# def op_AGENT(state: State, name: str) -> None:    
#     state.require(not state.in_agent, 'Already inside an agent.', 'First end current agent using EAGENT.')
#     state.require(
#         not state.in_message, 
#         'Cannot define agents inside messages.', 
#         'First end current message using EMESSAGE.'
#     )
#     state.require(not state.agent_exists(name), f'Agent {name} already exists in the current environment.')
#     state.require(
#         is_valid_name(name), 
#         f'{name} is not a correct name.', 
#         f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
#     )
    
#     state.in_agent = True
#     state.add_agent(Agent(name))


# def op_EAGENT(state: State) -> None:    
#     state.require(state.in_agent, 'Not inside any agent.', 'Try defining new agents using AGENT.')
#     state.require(
#         not state.in_behaviour, 
#         'Cannot end an agent inside a behaviour.', 
#         'First end current behaviour using EBEHAV.'
#     )
    
#     state.in_agent = False


# def op_MESSAGE(state: State, msg_type: str, msg_performative) -> None:
#     state.require(not state.in_message, 'Already inside a message.', 'First end current message using EMESSAGE.')
#     state.require(not state.in_agent, 'Cannot define messages inside agents.', 'First end current agent using EAGENT.')
#     state.require(
#         not state.message_exists(msg_type, msg_performative), 
#         f'Message {msg_type}/{msg_performative} already exists in the current environment.'
#     )
#     state.require(
#         is_valid_name(msg_type), 
#         f'{msg_type} is not a correct name.', 
#         f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
#     )
#     state.require(
#         is_valid_name(msg_performative), 
#         f'{msg_performative} is not a correct name.', 
#         f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
#     )
    
#     state.in_message = True
#     state.add_message(Message(msg_type, msg_performative))


# def op_EMESSAGE(state: State) -> None:    
#     state.require(state.in_message, 'Not inside any message.', 'Try defining new messages using MESSAGE.')
    
#     state.in_message = False


# def op_agent_PRM(state: State, name: str, category: str, args: List[str]) -> None:    
#     state.require(
#         state.in_agent, 
#         'Cannot define agent parameters outside agent scope.', 
#         'Try defining new agents using AGENT.'
#     )
#     state.require(
#         not state.in_behaviour, 
#         'Cannot define agent parameters inside a behaviour.', 
#         'Parameters must appear after AGENT.'
#     )
#     state.require(not state.last_agent.param_exists(name), f'Parameter {name} already exists inside current agent.')
#     state.require(
#         is_valid_name(name), 
#         f'{name} is not a correct name.', 
#         f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
#     )
    
#     match category, args:
#         case 'float', [ 'init', value ]:
#             state.require(is_float(value), f'{value} is not a valid float.')

#             state.last_agent.add_init_float(AgentInitFloatParam(name, value))
            
#         case 'float', [ 'dist', 'normal', mean, std_dev ]:
#             state.require(is_float(mean), f'{mean} is not a valid float.')
#             state.require(is_float(std_dev), f'{std_dev} is not a valid float.')

#             state.last_agent.add_dist_normal_float(AgentDistNormalFloatParam(name, mean, std_dev))
            
#         case 'float', [ 'dist', 'exp', lambda_ ]:
#             state.require(is_float(lambda_), f'{lambda_} is not a valid float.')
#             state.require(
#                 float(lambda_) > 0, 
#                 f'{lambda_} is not a valid lambda parameter.', 
#                 'Lambda must be non-negative.'
#             )

#             state.last_agent.add_dist_exp_float(AgentDistExpFloatParam(name, lambda_))
            
#         case 'list', [ 'conn' ]:
#             state.last_agent.add_connection_list(AgentConnectionListParam(name))
            
#         case 'list', [ 'msg' ]:
#             state.last_agent.add_message_list(AgentMessageListParam(name))
            
#         case 'enum', enums:
#             state.require(
#                 is_valid_enum_list(enums),
#                 f'{enums} is not a valid enum list.', 
#                 'The correct pattern is [name, percent, ...], where percent(s) sum up to 100 (+/- 1).'
#             )

#             state.last_agent.add_enum(AgentEnumParam(name, enums))
            
#         case _:
#             state.panic(f'Incorrect operation: (agent) PRM {name} {category} {args}')


# def op_message_PRM(state: State, name: str, category: str) -> None:    
#     state.require(
#         state.in_message, 
#         'Cannot define message parameters outside message scope.', 
#         'Try defining new messages using MESSAGE.'
#     )
#     state.require(not state.last_message.param_exists(name), f'Parameter {name} already exists inside current message.')
#     state.require(
#         is_valid_name(name), 
#         f'{name} is not a correct name.', 
#         f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
#     )
    
#     match category:
#         case 'float':
#             state.last_message.add_float(MessageFloatParam(name))

#         case _:
#             state.panic(f'Incorrect operation: (message) PRM {name} {category}')


# def op_BEHAV(state: State, name: str, category: str, args: List[str]):
#     state.require(state.in_agent, 'Cannot define behaviours outside agents.', 'Try defining new agents using AGENT.')
#     state.require(
#         not state.in_behaviour,
#         'Cannot define behaviours inside other behaviours.',
#         'First end current behaviour using EBEHAV.'
#     )
#     state.require(not state.last_agent.behaviour_exists(name), f'Behaviour {name} already exists in current agent.')
#     state.require(
#         is_valid_name(name), 
#         f'{name} is not a correct name.', 
#         f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
#     )
    
#     match category, args:
#         case 'setup', [ ]:
#             state.last_agent.add_setup_behaviour(SetupBehaviour(name))
            
#         case 'one_time', [ delay ]:
#             state.require(is_float(delay) and float(delay) >= 0, f'{delay} is not a valid delay value.')

#             state.last_agent.add_one_time_behaviour(OneTimeBehaviour(name, delay))
            
#         case 'cyclic', [ period ]:
#             state.require(is_float(period) and float(period) > 0, f'{period} is not a valid period value.')

#             state.last_agent.add_cyclic_behaviour(CyclicBehaviour(name, period))
            
#         case 'msg_rcv', [ msg_type, msg_performative ]:
#             state.require(
#                 state.message_exists(msg_type, msg_performative), 
#                 f'Message {msg_type}/{msg_performative} does not exist.', 
#                 'Try defining new messages using MESSAGE'
#             )
#             state.require(
#                 not state.last_agent.behaviour_for_template_exists(msg_type, msg_performative), 
#                 f'Behaviour for template {msg_type}/{msg_performative} already exists in current agent.'
#             )

#             state.last_agent.add_message_received_behaviour(
#                 MessageReceivedBehaviour(name, state.get_message_instance(msg_type, msg_performative))
#             )
            
#         case _:
#             state.panic(f'Incorrect operation: BEHAV {name} {category} {args}')
    
#     state.in_behaviour = True


# def op_EBEHAV(state: State) -> None:            
#     state.require(state.in_behaviour, 'Not inside any behaviour.', 'Try defining new behaviours using BEHAV.')
#     state.require(
#         not state.in_action, 
#         'Cannot end behaviours inside actions.', 
#         'Try ending current action using EACTION.'
#     )
    
#     state.in_behaviour = False


# def op_ACTION(state: State, name: str, category: str, args: List[str]) -> None:
#     state.require(
#         state.in_behaviour, 
#         'Actions must be definied inside behaviours.', 
#         'Try defining new behaviours using BEHAV.'
#     )
#     state.require(
#         not state.in_action, 
#         'Cannot define an action in another action.', 
#         'Try finishing current action using EACTION.'
#     )
#     state.require(not state.last_behaviour.action_exists(name), f'Action {name} already exists in current behaviour.')
#     state.require(
#         is_valid_name(name), 
#         f'{name} is not a correct name.', 
#         f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
#     )
    
#     match category, args:
#         case 'modify_self', [ ]:
#             state.last_behaviour.add_action(ModifySelfAction(name))
            
#         case 'send_msg', [ msg_type, msg_performative ]:
#             state.require(
#                 state.message_exists(msg_type, msg_performative), 
#                 f'Message {msg_type}/{msg_performative} does not exist.', 
#                 'Try defining new messages using MESSAGE.'
#             )

#             state.last_behaviour.add_action(SendMessageAction(name, state.get_message_instance(msg_type, msg_performative)))
            
#         case _:
#             state.panic(f'Incorrect operation: ACTION {category} {args}')
    
#     state.in_action = True


# def op_EACTION(state: State) -> None:            
#     state.require(state.in_action, 'Not inside any action.', 'Try defining new actions using ACTION.')
#     state.require(
#         state.last_action._nested_blocks_count == 0, 
#         'There are unclosed blocks.', 
#         'Try closing them using EBLOCK.'
#     )
    
#     state.in_action = False


# def op_DECL(state: State, name: str, value: str) -> None:            
#     state.require(state.in_action, 'Cannot declare variables outside actions.')
#     state.require(
#         is_valid_name(name), 
#         f'{name} is not a correct name.', 
#         f'Names can only contain alphanumeric signs, underscores and cannot be: {print_invalid_names()}.'
#     )
#     state.require(not state.last_agent.param_exists(name), f'{name} is already defined in current agent.')
#     state.require(
#         not state.last_action.is_declaration_in_scope(name), 
#         f'{name} is already declared in current action scope.'
#     )
#     lhs = Argument(state, name)
#     rhs = Argument(state, value)
#     state.require(
#         lhs.declaration_context(rhs), 
#         'Mismatched types in the declaration context.', 
#         f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
#     )
    
#     state.last_action.add_declaration(Declaration(lhs, rhs))


# def op_EBLOCK(state: State) -> None:            
#     state.require(state.in_action, 'Cannot end blocks outside actions.')
#     state.require(state.last_action._nested_blocks_count > 0, 'No more blocks to close', 'Try removing this statement.')
    
#     state.last_action.end_block()


# def handle_unordered_conditional_statement(state: State, op: str, arg1: str, arg2: str) -> None:
#     state.require(state.in_action, 'Not inside any action.', f'{op} can be used inside actions.')     
#     lhs = Argument(state, arg1)
#     rhs = Argument(state, arg2)
#     state.require(
#         lhs.unordered_comparaison_context(rhs), 
#         'Mismatched types in the unordered comparaison context.', 
#         f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
#     )
    
#     match op:
#         case 'IEQ':
#             state.last_action.add_instruction(IfEqual(lhs, rhs))

#         case 'INEQ':
#             state.last_action.add_instruction(IfNotEqual(lhs, rhs))

#         case 'WEQ':
#             state.last_action.add_instruction(WhileEqual(lhs, rhs))

#         case 'WNEQ':
#             state.last_action.add_instruction(WhileNotEqual(lhs, rhs))

#         case _:
#             state.panic(f'Unexpected error: {op} {arg1} {arg2}')
    
#     state.last_action.start_block()


# def handle_ordered_conditional_statement(state: State, op: str, arg1: str, arg2: str) -> None:
#     state.require(state.in_action, 'Not inside any action.', f'{op} can be used inside actions.')     
#     lhs = Argument(state, arg1)
#     rhs = Argument(state, arg2)
#     state.require(
#         lhs.ordered_comparaison_context(rhs),
#         'Mismatched types in the ordered comparaison context.', 
#         f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
#     )
    
#     match op:
#         case 'IGT':
#             state.last_action.add_instruction(IfGreaterThan(lhs, rhs))

#         case 'IGTEQ':
#             state.last_action.add_instruction(IfGreaterThanOrEqual(lhs, rhs))

#         case 'ILT':
#             state.last_action.add_instruction(IfLessThan(lhs, rhs))

#         case 'ILTEQ':
#             state.last_action.add_instruction(IfLessThanOrEqual(lhs, rhs))

#         case 'WGT':
#             state.last_action.add_instruction(WhileGreaterThan(lhs, rhs))

#         case 'WGTEQ':
#             state.last_action.add_instruction(WhileGreaterThanOrEqual(lhs, rhs))

#         case 'WLT':
#             state.last_action.add_instruction(WhileLessThan(lhs, rhs))

#         case 'WLTEQ':
#             state.last_action.add_instruction(WhileLessThanOrEqual(lhs, rhs))

#         case _:
#             state.panic(f'Unexpected error: {op} {arg1} {arg2}')
    
#     state.last_action.start_block()


# def handle_math_statement(state: State, op: str, arg1: str, arg2: str) -> None:
#     state.require(state.in_action, 'Not inside any action', f'{op} can be used inside actions.')
#     lhs = Argument(state, arg1)
#     rhs = Argument(state, arg2)
#     state.require(
#         lhs.math_context(rhs),
#         'Mismatched types in the math statement.', 
#         f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
#     )

#     match op:
#         case 'ADD':
#             state.last_action.add_instruction(Add(lhs, rhs))

#         case 'SUBT':
#             state.last_action.add_instruction(Subtract(lhs, rhs))

#         case 'MULT':
#             state.last_action.add_instruction(Multiply(lhs, rhs))

#         case 'DIV':
#             state.last_action.add_instruction(Divide(lhs, rhs))

#         case _:
#             state.panic(f'Unexpected error: {op} {arg1} {arg2}')


# def handle_list_modification(state: State, op: str, arg1: str, arg2: str) -> None:
#     state.require(state.in_action, 'Not inside any action.', 'List modifications can be used inside actions.')
#     lhs = Argument(state, arg1)
#     rhs = Argument(state, arg2)
#     state.require(
#         lhs.list_modification_context(rhs), 
#         'Mismatched types in the list modification context.', 
#         f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
#     )
    
#     match op:
#         case 'ADDE':
#             state.last_action.add_instruction(AddElement(lhs, rhs))

#         case 'REME':
#             state.last_action.add_instruction(RemoveElement(lhs, rhs))

#         case _:
#             state.panic(f'Unexpected error: {op} {arg1} {arg2}')
            
            
# def op_REMEN(state: State, arg1: str, arg2: str) -> None:
#     state.require(state.in_action, 'Not inside any action.', 'List modifications can be used inside actions.')
#     lhs = Argument(state, arg1)
#     rhs = Argument(state, arg2)
#     state.require(
#         lhs.list_n_removal_context(rhs), 
#         'Mismatched types in the list n removal context.', 
#         f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
#     )
    
#     state.last_action.add_instruction(RemoveNElements(lhs, rhs))

# def op_LEN(state: State, arg1: str, arg2: str) -> None:
#     state.require(state.in_action, 'Not inside any action.', 'LEN can be used inside actions.')
#     lhs = Argument(state, arg1)
#     rhs = Argument(state, arg2)
#     state.require(
#         lhs.list_length_context(rhs), 
#         'Mismatched types in the list length context.', 
#         f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
#     )
    
#     state.last_action.add_instruction(Length(lhs, rhs))


# def op_CLR(state: State, arg1: str) -> None:
#     state.require(state.in_action, 'Not inside any action.', 'CLR can be used inside actions.')
#     list_ = Argument(state, arg1)
#     state.require(list_.list_clear_context(), 'Mismatched type in the list clear context.', f'ARG {list_.explain()}')

#     state.last_action.add_instruction(Clear(list_))


# def handle_list_inclusion(state: State, op: str, arg1: str, arg2: str):
#     state.require(state.in_action, 'Not inside any action.', 'List inclusion check can be used inside actions.')
#     lhs = Argument(state, arg1)
#     rhs = Argument(state, arg2)
#     state.require(
#         lhs.list_inclusion_context(rhs), 
#         'Mismatched types in the list inclusion context.', 
#         f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
#     )
    
#     match op:
#         case 'IN':
#             state.last_action.add_instruction(IfInList(lhs, rhs))

#         case 'NIN':
#             state.last_action.add_instruction(IfNotInList(lhs, rhs))

#         case _:
#             state.panic(f'Unexpected error: {op} {arg1} {arg2}')
            
#     state.last_action.start_block()


# def op_SEND(state: State, arg1: str) -> None:
#     state.require(state.in_action, 'Not inside any action.', 'SEND can be used inside send_msg actions.')
#     state.require(
#         isinstance(state.last_action, SendMessageAction), 
#         'Not inside send_msg action.', 
#         'SEND can be used inside send_msg actions.'
#     )
#     receivers = Argument(state, arg1)
#     state.require(receivers.send_context(), 'Mismatched type in the send context.', f'ARG1 {receivers.explain()}')

#     state.last_action.add_instruction(Send(receivers))


# def op_SET(state: State, arg1: str, arg2: str) -> None:
#     state.require(state.in_action, 'Not inside any action.', f'SET can be used inside actions.')
#     lhs = Argument(state, arg1)
#     rhs = Argument(state, arg2)
#     state.require(
#         lhs.assignment_context(rhs), 
#         'Mismatched types in the assignment context.', 
#         f'ARG1 {lhs.explain()}, ARG2 {rhs.explain()}'
#     )    
    
#     state.last_action.add_instruction(Set(lhs, rhs))


# def op_SUBS(state: State, arg1: str, arg2: str, arg3: str) -> None:
#     state.require(state.in_action, 'Not inside any action.', f'SUBS can be used inside actions.')
#     dst_list = Argument(state, arg1)
#     src_list = Argument(state, arg2)
#     num = Argument(state, arg3)
#     state.require(
#         dst_list.list_subset_context(src_list, num), 
#         'Mismatched types in the subset context.', 
#         f'ARG1 {dst_list.explain()}, ARG2 {src_list.explain()}, ARG3 {num.explain()}'
#     )
    
#     state.last_action.add_instruction(Subset(dst_list, src_list, num))


# def op_RAND(state: State, arg1: str, arg2: str, arg3: str, args: List[str]) -> None:
#     state.require(state.in_action, 'Not inside any action.', f'RAND can be used inside actions.')
#     result = Argument(state, arg1)

#     match arg3, args:
#         case 'uniform', [ a, b ]:
#             a_arg = Argument(state, a)
#             b_arg = Argument(state, b)
#             state.require(
#                 result.random_number_generation_context(a_arg, b_arg), 
#                 'Mismatched types in the random number generation context.', 
#                 f'RESULT {result.explain()}, A {a_arg.explain()}, B {b_arg.explain()}'
#             )

#             state.last_action.add_instruction(UniformDist(result, a_arg, b_arg))

#         case 'normal', [ mean, std_dev ]:
#             mean_arg = Argument(state, mean)
#             std_dev_arg = Argument(state, std_dev)
#             state.require(
#                 result.random_number_generation_context(mean_arg, std_dev_arg), 
#                 'Mismatched types in the random number generation context.', 
#                 f'RESULT {result.explain()}, MEAN {mean_arg.explain()}, STD_DEV {std_dev_arg.explain()}'
#             )

#             state.last_action.add_instruction(NormalDist(result, mean_arg, std_dev_arg))

#         case 'exp', [ lambda_ ]:
#             lambda_arg = Argument(state, lambda_)
#             state.require(
#                 result.random_number_generation_context(lambda_arg), 
#                 'Mismatched types in the random number generation context.', 
#                 f'RESULT {result.explain()}, LAMBDA {lambda_arg.explain()}'
#             )

#             state.last_action.add_instruction(ExpDist(result, lambda_arg))

#         case _:
#             state.panic(f'Incorrect operation: RAND {arg1} {arg2} {arg3} {args}')

#     match arg2:
#         case 'float':
#             ...

#         case 'int':
#             op_ROUND(arg1)

#         case _:
#             state.panic(f'Incorrect operation: RAND {arg1} {arg2} {arg3} {args}')


# def op_ROUND(state: State, arg1: str) -> None:
#     state.require(state.in_action, 'Not inside any action.', f'ROUND can be used inside actions.')
#     num = Argument(state, arg1)
#     state.require(num.round_number_context(), 'Mismatched type in the round number context.', f'NUM {num.explain()}')

#     state.last_action.add_instruction(Round(num))
