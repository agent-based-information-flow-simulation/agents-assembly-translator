from __future__ import annotations

from typing import TYPE_CHECKING, List

from aasm.intermediate.action import SendMessageAction
from aasm.intermediate.argument import (AgentParam, Connection, ConnectionList,
                                        EnumValue, MessageList,
                                        ReceivedMessageParam, SendMessageParam)
from aasm.intermediate.behaviour import MessageReceivedBehaviour
from aasm.intermediate.block import Block
from aasm.intermediate.declaration import Declaration
from aasm.intermediate.instruction import (Add, AddElement, Clear, Divide,
                                           ExpDist, IfEqual, IfGreaterThan,
                                           IfGreaterThanOrEqual, IfInList,
                                           IfLessThan, IfLessThanOrEqual,
                                           IfNotEqual, IfNotInList, Length,
                                           Multiply, NormalDist, RemoveElement,
                                           RemoveNElements, Round, Send, Set,
                                           Subset, Subtract, UniformDist,
                                           WhileEqual, WhileGreaterThan,
                                           WhileGreaterThanOrEqual,
                                           WhileLessThan, WhileLessThanOrEqual,
                                           WhileNotEqual)
from aasm.parsing.parse import parse_lines

if TYPE_CHECKING:
    from aasm.intermediate.agent import Agent
    from aasm.intermediate.argument import Argument
    from aasm.intermediate.behaviour import Behaviour
    from aasm.intermediate.message import Message as IntermediateMessage
    from aasm.parsing.state import ParsedData


def get_spade_code(aasm_lines: List[str], debug: bool = False) -> List[str]:
    """Generates SPADE code in Python from `aasm_lines`.

        Parameters
        ----------
        aasm_lines : List[str]
            Lines of code written in Agents Assembly
            
        debug: bool, optional
            Print the translator debug information to the standard output (default is False)

        Raises
        ------
        PanicException
            If an error is detected while parsing the `aasm_lines`.
    """
    return SpadeCode(aasm_lines, debug).code_lines


class SpadeCode:
    INDENT_SIZE = 4
    
    def __init__(self, lines: List[str], debug: bool):
        parsed_data: ParsedData = parse_lines(lines, debug)
        self.indent: int = 0
        self.code_lines: List[str] = []
        self.add_required_imports()
        if parsed_data.messages:
            self.add_newlines(2)
            self.add_base_message()
        for agent in parsed_data.agents:
            self.add_newlines(2)
            self.generate_agent(agent)
    
    ### COMMON ###
    def add_required_imports(self) -> List[str]:
        self.add_line('import datetime')
        self.add_line('import math')
        self.add_line('import random')
        self.add_line('import numpy')
        self.add_line('import orjson')
        self.add_line('import spade')
        
    def indent_left(self) -> None:
        self.indent -= SpadeCode.INDENT_SIZE 
        
    def indent_right(self) -> None:
        self.indent += SpadeCode.INDENT_SIZE 
        
    def add_line(self, line: str) -> None:
        self.code_lines.append(self.indent * ' ' + line + '\n')
        
    def add_newline(self) -> None:
        self.add_line('')
        
    def add_newlines(self, count: int) -> None:
        for _ in range(count):
            self.add_newline()
            
    ### BASE MESSAGE ###
    def add_base_message(self) -> None:
        self.add_line('class BaseMessage:')
        self.indent_right()
        self.add_line('def __init__(self, **kwargs):')
        self.indent_right()
        self.add_line('if \"type\" in kwargs and \"performative\" in kwargs:')
        self.indent_right()
        self.add_line('self.body = {')
        self.indent_right()
        self.add_line('\"type\": kwargs[\"type\"],')
        self.add_line('\"performative\": kwargs[\"performative\"],')
        self.indent_left()
        self.add_line('}')
        self.indent_left()
        self.add_line('elif \"rcv\" in kwargs:')
        self.indent_right()
        self.add_line('self.body = orjson.loads(kwargs[\"rcv\"].body)')
        self.indent_left()
        self.indent_left()
        self.add_newline()
        self.add_line('def get_spade_message(self):')
        self.indent_right()
        self.add_line('msg = spade.message.Message()')
        self.add_line('msg.metadata["type"] = self.body["type"]')
        self.add_line('msg.metadata["performative"] = self.body["performative"]')
        self.add_line('msg.body = orjson.dumps(self.body)')
        self.add_line('return msg')
        self.indent_left()
        self.indent_left()
    
    ### AGENT ###
    def generate_agent(self, agent: Agent) -> None:
        self.add_line(f'class {agent.name}(spade.agent.Agent):')
        self.indent_right()
        self.add_agent_constructor(agent)
        self.add_newline()
        self.add_agent_setup(agent)
        self.add_newline()
        for setup_behaviour in agent.setup_behaviours.values():
            self.add_agent_behaviour(setup_behaviour, 'spade.behaviour.OneShotBehaviour')
            self.add_newline()
        for one_time_behaviour in agent.one_time_behaviours.values():
            self.add_agent_behaviour(one_time_behaviour, 'spade.behaviour.TimeoutBehaviour')
            self.add_newline()
        for cyclic_behaviour in agent.cyclic_behaviours.values():
            self.add_agent_behaviour(cyclic_behaviour, 'spade.behaviour.PeriodicBehaviour')
            self.add_newline()
        for message_received_behaviour in agent.message_received_behaviours.values():
            self.add_agent_behaviour(message_received_behaviour, 'spade.behaviour.CyclicBehaviour')
            self.add_newline()
        self.indent_left()
        
    def add_agent_constructor(self, agent: Agent) -> None:
        self.add_line('def __init__(self, jid, password, location, connections):')
        self.indent_right()
        self.add_line('super().__init__(jid, password, verify_security=False)')
        self.add_line('self.location = location')
        self.add_line('self.connections = connections')
        self.add_line('self.msgRCount = 0')
        self.add_line('self.mSCount = 0')
        for init_float_param in agent.init_floats.values():
            self.add_line(f'self.{init_float_param.name} = {init_float_param.value}')
        for dist_normal_float_param in agent.dist_normal_floats.values():
            self.add_line(f'self.{dist_normal_float_param.name} = numpy.random.normal({dist_normal_float_param.mean}, {dist_normal_float_param.std_dev})')
        for dist_exp_float_param in agent.dist_exp_floats.values():
            self.add_line(f'self.{dist_exp_float_param.name} = numpy.random.exponential(1/{dist_exp_float_param.lambda_})')
        for enum_param in agent.enums.values():            
            values = []
            percentages = []
            for enum_value in enum_param.enum_values:
                values.append(f'\"{enum_value.value}\"')
                percentages.append(enum_value.percentage)
            values = f'[{", ".join(values)}]'
            percentages = f'[{", ".join(percentages)}]'
            self.add_line(f'self.{enum_param.name} = random.choices({values}, {percentages})[0]')
        for connection_list_param in agent.connection_lists.values():
            self.add_line(f'self.{connection_list_param.name} = []')
        for message_list_param in agent.message_lists.values():
            self.add_line(f'self.{message_list_param.name} = []')
        self.indent_left()
        self.add_newline()
        self.add_line('@property')
        self.add_line('def connCount(self):')
        self.indent_right()
        self.add_line('return len(self.connections)')
        self.indent_left()
        
    def add_agent_setup(self, agent: Agent) -> None:
        self.add_line('def setup(self):')
        self.indent_right()
        if not agent.behaviour_names:
            self.add_line('...')
        for setup_behaviour in agent.setup_behaviours.values():
            self.add_line(f'self.add_behaviour(self.{setup_behaviour.name}())')
        for one_time_behaviour in agent.one_time_behaviours.values():
            self.add_line(f'self.add_behaviour(self.{one_time_behaviour.name}(start_at=datetime.datetime.now() + datetime.timedelta(seconds={one_time_behaviour.delay})))')
        for cyclic_behaviour in agent.cyclic_behaviours.values():
            self.add_line(f'self.add_behaviour(self.{cyclic_behaviour.name}(period={cyclic_behaviour.period}))')
        for message_received_behaviour in agent.message_received_behaviours.values():
            self.add_line(f'{message_received_behaviour.name}_template = spade.template.Template()')
            self.add_line(f'{message_received_behaviour.name}_template.set_metadata(\"type\", \"{message_received_behaviour.received_message.type}\")')
            self.add_line(f'{message_received_behaviour.name}_template.set_metadata(\"performative\", \"{message_received_behaviour.received_message.performative}\")')
            self.add_line(f'self.add_behaviour(self.{message_received_behaviour.name}(), {message_received_behaviour.name}_template)')
        self.indent_left()

    def add_send_message(self, message: IntermediateMessage) -> None:
        self.add_line(f'send = BaseMessage(type=\"{message.type}\", performative=\"{message.performative}\")')
        for float_param_name in message.float_params:
            self.add_line(f'send.body[\"{float_param_name}\"] = 0.0')
        
    def add_agent_behaviour(self, behaviour: Behaviour, behaviour_type: str) -> None:
        self.add_line(f'class {behaviour.name}({behaviour_type}):')
        self.indent_right()
        if not behaviour.actions.values():
            self.add_line('...')
        for action in behaviour.actions.values():                
            match behaviour, action:
                case MessageReceivedBehaviour(), SendMessageAction():
                    self.add_line(f'async def {action.name}(self, rcv):')
                    self.indent_right()
                    self.add_send_message(action.send_message)
                    self.indent_left()
                case MessageReceivedBehaviour(), _:
                    self.add_line(f'def {action.name}(self, rcv):')
                case _, SendMessageAction():
                    self.add_line(f'async def {action.name}(self):')
                    self.indent_right()
                    self.add_send_message(action.send_message)
                    self.indent_left()
                case _:
                    self.add_line(f'def {action.name}(self):')
            self.indent_right()
            self.add_block(action.main_block)
            self.indent_left()
            self.add_newline()
            
        self.add_line('async def run(self):')
        self.indent_right()
        if isinstance(behaviour, MessageReceivedBehaviour):
            self.add_line('rcv = await self.receive(timeout=10)')
            self.add_line('if rcv:')
            self.indent_right()
            self.add_line('rcv = BaseMessage(rcv=rcv)')
            self.add_line('self.agent.msgRCount += 1')
        elif not behaviour.actions.values():
            self.add_line('...')
            
        for action in behaviour.actions.values():                
            match behaviour, action:
                case MessageReceivedBehaviour(), SendMessageAction():
                    self.add_line(f'await self.{action.name}(rcv)')
                case MessageReceivedBehaviour(), _:
                    self.add_line(f'self.{action.name}(rcv)')
                case _, SendMessageAction():
                    self.add_line(f'await self.{action.name}()')
                case _:
                    self.add_line(f'self.{action.name}()')
                    
        if isinstance(behaviour, MessageReceivedBehaviour):
            self.indent_left()
                    
        self.indent_left()
        self.indent_left()
    
    def parse_arg(self, arg: Argument) -> str:
        match arg.type_in_op:
            case AgentParam():
                return f'self.agent.{arg.expr}'
            
            case EnumValue():
                return f'\"{arg.expr}\"'
            
            case ReceivedMessageParam() if not isinstance(arg.type_in_op, Connection):
                prop = arg.expr.split('.')[1]
                return f'rcv.body[\"{prop}\"]'
            
            case SendMessageParam() if not isinstance(arg.type_in_op, Connection):
                prop = arg.expr.split('.')[1]
                return f'send.body[\"{prop}\"]'
            
            case _:
                return arg.expr
        
    def add_block(self, block: Block) -> None:
        if not block.statements:
            self.add_line('...')
            
        for statement in block.statements:
            match statement:
                case Block():
                    self.indent_right()
                    self.add_block(statement)
                    self.indent_left()
            
                case Declaration():
                    value = self.parse_arg(statement.value)
                    self.add_line(f'{statement.name} = {value}')
                    
                case Subset():
                    to_list = self.parse_arg(statement.arg1)
                    from_list = self.parse_arg(statement.arg2)
                    num = self.parse_arg(statement.arg3)
                    self.add_line(f'if math.ceil({num}) > 0:')
                    self.indent_right()
                    self.add_line(f'if math.ceil({num}) <= len({from_list}):')
                    self.indent_right()
                    self.add_line(f'{to_list} = random.sample({from_list}, math.ceil({num}))')
                    self.indent_left()
                    self.add_line('else:')
                    self.indent_right()
                    self.add_line(f'{to_list} = random.sample({from_list}, len({from_list}))')
                    self.indent_left()
                    self.indent_left()
                    self.add_line(f'else: {to_list} = []')
                    
                case Clear():
                    list_ = self.parse_arg(statement.arg1)
                    self.add_line(f'{list_}.clear()')
                    
                case Send() if isinstance(statement.arg1.type_in_op, Connection):
                    receiver = self.parse_arg(statement.arg1)
                    self.add_line(f'await self.send(send.get_spade_message({receiver}))')
                    self.add_line('self.agent.msgSCount += 1')
                    
                case Send() if isinstance(statement.arg1.type_in_op, ConnectionList):
                    receivers = self.parse_arg(statement.arg1)
                    self.add_line(f'for receiver in {receivers}:')
                    self.indent_right()
                    self.add_line(f'await self.send(send.get_spade_message(receiver))')
                    self.add_line('self.agent.msgSCount += 1')
                    self.indent_left()
                    
                case Set() if isinstance(statement.arg2.type_in_op, MessageList):
                    msg = self.parse_arg(statement.arg1)
                    msg_list = self.parse_arg(statement.arg2)
                    self.add_line(f'if len(list(filter(lambda msg: msg.body["type"] == {msg}.body["type"] and msg.body["performative"] == {msg}.body["performative"], {msg_list}))):')
                    self.indent_right()
                    self.add_line(f'{msg} = random.choice(list(filter(lambda msg: msg.body["type"] == {msg}.body["type"] and msg.body["performative"] == {msg}.body["performative"], {msg_list})))')
                    self.indent_left()
                    self.add_line('else:')
                    self.indent_right()
                    self.add_line('return')
                    self.indent_left()
                    
                case Set():
                    arg1 = self.parse_arg(statement.arg1)
                    arg2 = self.parse_arg(statement.arg2)
                    self.add_line(f'{arg1} = {arg2}')
                    
                case Round():
                    num = self.parse_arg(statement.arg1)
                    self.add_line(f'{num} = round({num})')
                    
                case UniformDist():
                    result = self.parse_arg(statement.arg1)
                    a = self.parse_arg(statement.arg2)
                    b = self.parse_arg(statement.arg3)
                    self.add_line(f'{result} = random.uniform({a}, {b})')
                    
                case NormalDist():
                    result = self.parse_arg(statement.arg1)
                    mean = self.parse_arg(statement.arg2)
                    std_dev = self.parse_arg(statement.arg3)
                    self.add_line(f'{result} = numpy.random.normal({mean}, {std_dev})')
                    
                case ExpDist():
                    result = self.parse_arg(statement.arg1)
                    lambda_ = self.parse_arg(statement.arg2)
                    self.add_line(f'{result} = numpy.random.exponential(1/{lambda_}) if {lambda_} > 0 else 0')
                
                case _:
                    arg1 = self.parse_arg(statement.arg1)
                    arg2 = self.parse_arg(statement.arg2)
                    match statement:
                        case IfGreaterThan():
                            self.add_line(f'if {arg1} > {arg2}:')
                            
                        case IfGreaterThanOrEqual():
                            self.add_line(f'if {arg1} >= {arg2}:')
                
                        case IfLessThan():
                            self.add_line(f'if {arg1} < {arg2}:')
                            
                        case IfLessThanOrEqual():
                            self.add_line(f'if {arg1} <= {arg2}:')
                    
                        case IfEqual():
                            self.add_line(f'if {arg1} == {arg2}:')

                        case IfNotEqual():
                            self.add_line(f'if {arg1} != {arg2}:')
                            
                        case WhileGreaterThan():
                            self.add_line(f'while {arg1} > {arg2}:')

                        case WhileGreaterThanOrEqual():
                            self.add_line(f'while {arg1} >= {arg2}:')

                        case WhileLessThan():
                            self.add_line(f'while {arg1} < {arg2}:')
                    
                        case WhileLessThanOrEqual():
                            self.add_line(f'while {arg1} <= {arg2}:')
                    
                        case WhileEqual():
                            self.add_line(f'while {arg1} == {arg2}:')
                    
                        case WhileNotEqual():
                            self.add_line(f'while {arg1} != {arg2}:')
                    
                        case Add():
                            self.add_line(f'{arg1} += {arg2}')

                        case Subtract():
                            self.add_line(f'{arg1} -= {arg2}')

                        case Multiply():
                            self.add_line(f'{arg1} *= {arg2}')

                        case Divide():
                            self.add_line(f'if {arg2} != 0: {arg1} /= {arg2}')
                            
                        case AddElement():
                            self.add_line(f'if {arg2} not in {arg1}: {arg1}.append({arg2})')
                    
                        case RemoveElement():
                            self.add_line(f'if {arg2} in {arg1}: {arg1}.remove({arg2})')
                            
                        case IfInList():
                            self.add_line(f'if {arg2} in {arg1}:')
                            
                        case IfNotInList():
                            self.add_line(f'if {arg2} not in {arg1}:')
                            
                        case Length():
                            self.add_line(f'{arg1} = len({arg2})')
                            
                        case RemoveNElements():
                            self.add_line(f'if math.ceil({arg2}) > 0:')
                            self.indent_right()
                            self.add_line(f'if math.ceil({arg2}) < len({arg1}):')
                            self.indent_right()
                            self.add_line(f'random.shuffle({arg1})')
                            self.add_line(f'{arg1} = {arg1}[:len({arg1}) - math.ceil({arg2})]')
                            self.indent_left()
                            self.add_line('else:')
                            self.indent_right()
                            self.add_line(f'{arg1} = []')
                            self.indent_left()
                            self.indent_left()
