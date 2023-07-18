from __future__ import annotations

from typing import TYPE_CHECKING

from aasm.intermediate.action import SendMessageAction
from aasm.intermediate.behaviour import MessageReceivedBehaviour
from aasm.utils.validation import is_connection, is_float, is_int

if TYPE_CHECKING:
    from typing import List as TypingList
    from typing import Type, Tuple

    from parsing.state import State


class ArgumentType:
    ...


class Mutable(ArgumentType):
    ...


class Immutable(ArgumentType):
    ...


class Declared(ArgumentType):
    ...


class Float(ArgumentType):
    ...


class Integer(ArgumentType):
    ...


class Enum(ArgumentType):
    ...


class EnumValue(ArgumentType):
    ...


class List(ArgumentType):
    ...


class ConnectionList(ArgumentType):
    ...


class MessageList(ArgumentType):
    ...


class FloatList(ArgumentType):
    ...


class AgentParam(ArgumentType):
    ...


class Message(ArgumentType):
    ...


class MessageType(ArgumentType):
    ...


class ReceivedMessage(ArgumentType):
    ...


class ReceivedMessageParam(ArgumentType):
    ...


class SendMessage(ArgumentType):
    ...


class SendMessageParam(ArgumentType):
    ...


class Connection(ArgumentType):
    ...


class Literal(ArgumentType):
    ...


class ModuleVariable(ArgumentType):
    ...


class Argument:
    """Doesn't panic. Use in the action context."""

    def __init__(self, state: State, expr: str, set_types: bool = True):
        self.expr: str = expr
        self.types: TypingList[ArgumentType] = []
        self.type_in_op: ArgumentType | None = None
        if set_types:
            self.set_types(state)

    def create_all_possible_types(self, state: State) -> TypingList[Argument]:
        possible_types: TypingList[Argument] = []
        for type_ in self.types:
            possible_type = Argument(state, self.expr, set_types=False)
            possible_type.types = [type_]
            possible_type.type_in_op = type_
            possible_types.append(possible_type)
        return possible_types

    def set_types(self, state: State) -> None:
        self.check_agent_params(state)
        self.check_action_variables(state)
        self.check_received_message_params(state)
        self.check_send_message_params(state)
        self.check_numerical_values()
        self.check_connection_values()

    def check_agent_params(self, state: State) -> None:
        if self.expr in state.last_agent.RESERVED_FLOAT_PARAMS:
            self.types.append(self.compose(Float, AgentParam, Immutable))

        elif self.expr in state.last_agent.RESERVED_CONNECTION_LIST_PARAMS:
            self.types.append(self.compose(List, ConnectionList, AgentParam, Mutable))

        elif self.expr in state.last_agent.RESERVED_CONNECTION_PARAMS:
            self.types.append(self.compose(Connection, AgentParam, Immutable))

        elif self.expr in state.last_agent.float_param_names:
            self.types.append(self.compose(Float, AgentParam, Mutable))

        elif self.expr in state.last_agent.enums:
            self.types.append(self.compose(Enum, AgentParam, Mutable))

        elif self.expr in state.last_agent.message_lists:
            self.types.append(self.compose(List, MessageList, AgentParam, Mutable))

        elif self.expr in state.last_agent.connection_lists:
            self.types.append(self.compose(List, ConnectionList, AgentParam, Mutable))

        elif self.expr in state.last_agent.float_lists:
            self.types.append(self.compose(List, FloatList, AgentParam, Mutable))

        elif self.expr in state.last_agent.module_variables:
            subtype = state.last_agent.get_module_variable_type(self.expr)
            new_type = type(subtype, (ModuleVariable,), {})
            self.types.append(self.compose(new_type, AgentParam, Mutable))

        for enum_param in state.last_agent.enums.values():
            for enum_value in enum_param.enum_values:
                if self.expr == enum_value.value:
                    self.types.append(
                        self.compose(EnumValue, Immutable, from_enum=enum_param.name)
                    )

    def check_action_variables(self, state: State) -> None:
        if state.last_action.is_declared_float(self.expr):
            self.types.append(self.compose(Float, Declared, Mutable))

        elif state.last_action.is_declared_connection(self.expr):
            self.types.append(self.compose(Connection, Declared, Mutable))

        elif state.last_action.is_declared_module_variable(self.expr):
            try:
                subtype = state.last_action.get_module_variable_type(self.expr)
                new_type = type(subtype, (ModuleVariable,), {})
                self.types.append(self.compose(new_type, Declared, Mutable))
            except ValueError:
                pass

    def check_numerical_values(self) -> None:
        if is_float(self.expr):
            self.types.append(self.compose(Float, Immutable, Literal))

        if is_int(self.expr):
            self.types.append(self.compose(Integer, Immutable, Literal))

    def check_connection_values(self) -> None:
        if is_connection(self.expr):
            self.types.append(self.compose(Connection, Immutable, Literal))

    def check_received_message_params(self, state: State) -> None:
        if isinstance(state.last_behaviour, MessageReceivedBehaviour):
            if self.expr.lower().startswith("rcv."):
                prop = self.expr.split(".")[1]

                if (
                    prop
                    in state.last_behaviour.received_message.RESERVED_CONNECTION_PARAMS
                ):
                    self.types.append(
                        self.compose(Connection, ReceivedMessageParam, Immutable)
                    )

                elif prop in state.last_behaviour.received_message.RESERVED_TYPE_PARAMS:
                    self.types.append(
                        self.compose(MessageType, ReceivedMessageParam, Immutable)
                    )

                elif prop in state.last_behaviour.received_message.float_params:
                    self.types.append(
                        self.compose(Float, ReceivedMessageParam, Immutable)
                    )

                elif prop in state.last_behaviour.received_message.connection_params:
                    self.types.append(
                        self.compose(Connection, ReceivedMessageParam, Immutable)
                    )

                elif (
                    prop in state.last_behaviour.received_message.module_variable_params
                ):
                    subtype = (
                        state.last_behaviour.received_message.get_module_variable_type(
                            prop
                        )
                    )
                    new_type = type(subtype, (ModuleVariable,), {})
                    self.types.append(
                        self.compose(new_type, ReceivedMessageParam, Immutable)
                    )

            elif self.expr.lower() == "rcv":
                self.types.append(self.compose(Message, ReceivedMessage, Immutable))

    def check_send_message_params(self, state: State) -> None:
        if isinstance(state.last_action, SendMessageAction):
            if self.expr.lower().startswith("send."):
                prop = self.expr.split(".")[1]

                if prop in state.last_action.send_message.RESERVED_TYPE_PARAMS:
                    self.types.append(
                        self.compose(MessageType, SendMessageParam, Immutable)
                    )

                elif prop in state.last_action.send_message.float_params:
                    self.types.append(self.compose(Float, SendMessageParam, Mutable))

                elif prop in state.last_action.send_message.connection_params:
                    self.types.append(
                        self.compose(Connection, SendMessageParam, Mutable)
                    )

                elif prop in state.last_action.send_message.module_variable_params:
                    subtype = state.last_action.send_message.get_module_variable_type(
                        prop
                    )
                    new_type = type(subtype, (ModuleVariable,), {})
                    self.types.append(self.compose(new_type, SendMessageParam, Mutable))

            elif self.expr.lower() == "send":
                self.types.append(self.compose(Message, SendMessage, Mutable))

    def compose(self, *classes: Type[ArgumentType], **args: str) -> ArgumentType:
        name = "_".join([klass.__name__ for klass in classes])
        if args:
            name += "|" + "|".join([f"{key}={value}" for key, value in args.items()])
        return type(name, classes, args)()

    def has_arg(self, argument_type: ArgumentType, key: str, value: str) -> bool:
        try:
            if getattr(argument_type, key) == value:
                return True
        except AttributeError:
            ...
        return False

    def _check_subclasses(self, type_: ArgumentType, klass: Type[ArgumentType]) -> bool:
        class_strings = [
            f"{type_class.__module__}.{type_class.__name__}"
            for type_class in type_.__class__.mro()
        ]
        return any(
            [
                f"{klass.__module__}.{klass.__name__}" == class_name
                for class_name in class_strings
            ]
        )

    def has_type(self, *classes: Type[ArgumentType], **args: str) -> bool:
        for type_ in self.types:
            if all([self._check_subclasses(type_, klass) for klass in classes]) and all(
                [self.has_arg(type_, key, value) for key, value in args.items()]
            ):
                return True
        return False

    # def has_type(self, *classes: Type[ArgumentType], **args: str) -> bool:
    #     for type_ in self.types:
    #         all_classes = True
    #         for klass in classes:
    #             if not self._check_subclasses(type_, klass):
    #                 all_classes = False
    #                 break
    #         if all_classes:
    #             all_args = True
    #             for key, value in args.items():
    #                 if not self.has_arg(type_, key, value):
    #                     all_args = False
    #                     break
    #             if all_args:
    #                 return True
    #     return False

    def set_op_type(self, *classes: Type[ArgumentType], **args: str) -> None:
        for type_ in self.types:
            if all([self._check_subclasses(type_, klass) for klass in classes]) and all(
                [self.has_arg(type_, key, value) for key, value in args.items()]
            ):
                self.type_in_op = type_

    # DECL
    def declaration_context(self, rhs: Argument) -> bool:
        if rhs.has_type(Float):
            self.type_in_op = self.compose(Float, Declared, Mutable)
            rhs.set_op_type(Float)

        elif rhs.has_type(Connection):
            self.type_in_op = self.compose(Connection, Declared, Mutable)
            rhs.set_op_type(Connection)

        else:
            return False

        return True

    # IEQ, INEQ, WEQ, WNEQ
    def unordered_comparaison_context(self, rhs: Argument) -> bool:
        if self.has_type(Float) and rhs.has_type(Float):
            self.set_op_type(Float)
            rhs.set_op_type(Float)

        elif self.has_type(Enum) and rhs.has_type(EnumValue, from_enum=self.expr):
            self.set_op_type(Enum)
            rhs.set_op_type(EnumValue, from_enum=self.expr)

        else:
            return False

        return True

    # IGT, IGTEQ, ILT, ILTEQ, WGT, WGTEQ, WLT, WLTEQ
    def ordered_comparaison_context(self, rhs: Argument) -> bool:
        if self.has_type(Float) and rhs.has_type(Float):
            self.set_op_type(Float)
            rhs.set_op_type(Float)
            return True

        return False

    # ADD, SUBT, MULT, DIV, SIN, COS
    def math_context(self, rhs: Argument) -> bool:
        if self.has_type(Float, Mutable) and rhs.has_type(Float):
            self.set_op_type(Float, Mutable)
            rhs.set_op_type(Float)
            return True

        return False

    # POW, LOG
    def math_exponentiation_context(self, base: Argument, arg: Argument) -> bool:
        if (
            self.has_type(Float, Mutable)
            and base.has_type(Float)
            and arg.has_type(Float)
        ):
            self.set_op_type(Float, Mutable)
            base.set_op_type(Float)
            arg.set_op_type(Float)
            return True

        return False

    # MOD
    def math_modulo_context(self, dividend: Argument, divisor: Argument) -> bool:
        if (
            self.has_type(Float, Mutable)
            and dividend.has_type(Float)
            and divisor.has_type(Float)
        ):
            self.set_op_type(Float, Mutable)
            dividend.set_op_type(Float)
            divisor.set_op_type(Float)
            return True

        return False

    # ADDE, REME
    def list_modification_context(self, rhs: Argument) -> bool:
        if self.has_type(ConnectionList, Mutable) and rhs.has_type(Connection):
            self.set_op_type(ConnectionList, Mutable)
            rhs.set_op_type(Connection)

        elif self.has_type(MessageList, Mutable) and rhs.has_type(Message):
            self.set_op_type(MessageList, Mutable)
            rhs.set_op_type(Message)

        elif self.has_type(FloatList, Mutable) and rhs.has_type(Float):
            self.set_op_type(FloatList, Mutable)
            rhs.set_op_type(Float)

        else:
            return False

        return True

    # REMEN
    def list_n_removal_context(self, rhs: Argument) -> bool:
        if self.has_type(List, Mutable) and rhs.has_type(Float):
            self.set_op_type(List, Mutable)
            rhs.set_op_type(Float)
            return True

        return False

    # SET
    def assignment_context(self, rhs: Argument, state: State) -> bool:
        basic_assigment_types: TypingList[Tuple[Type, Type]] = [
            (Enum, EnumValue),
            (Float, Float),
            (Message, MessageList),
            (Connection, Connection),
            (ConnectionList, ConnectionList),
            (MessageList, MessageList),
            (FloatList, FloatList),
            (SendMessageParam, Float),
            (SendMessageParam, ModuleVariable),
        ]

        found_flag = False
        for assignment_possiblity in basic_assigment_types:
            if self.has_type(assignment_possiblity[0], Mutable) and rhs.has_type(
                assignment_possiblity[1]
            ):
                self.set_op_type(assignment_possiblity[0], Mutable)
                rhs.set_op_type(assignment_possiblity[1])
                found_flag = True
                break

        if self.has_type(ModuleVariable, Mutable) and rhs.has_type(ModuleVariable):
            lhs_type_name = self._find_module_variable_type(state)
            rhs_type_name = rhs._find_module_variable_type(state)
            if lhs_type_name == "" or rhs_type_name == "":
                return False
            lhs_type = self.get_modvar_type(lhs_type_name)
            rhs_type = rhs.get_modvar_type(rhs_type_name)
            self.set_op_type(lhs_type, Mutable)
            rhs.set_op_type(rhs_type)
            found_flag = True

        return found_flag

    def _find_module_variable_type(self, state: State) -> str:
        subtype = ""
        if not self.has_type(ModuleVariable):
            return subtype
        elif self.expr in state.last_agent.module_variables:
            subtype = state.last_agent.get_module_variable_type(self.expr)
        elif state.last_action.is_declared_module_variable(self.expr):
            subtype = state.last_action.get_module_variable_type(self.expr)
        elif self.has_type(ReceivedMessageParam):
            behav = state.last_behaviour
            if isinstance(behav, MessageReceivedBehaviour):
                subtype = behav.received_message.get_module_variable_type(self.expr)
        elif self.has_type(SendMessageParam):
            action = state.last_action
            if isinstance(action, SendMessageAction):
                # get the expr split after . character
                split_expr = self.expr.split(".")[-1]
                subtype = action.send_message.get_module_variable_type(split_expr)
        return subtype

    # SUBS
    def list_subset_context(self, from_list: Argument, num: Argument) -> bool:
        if (
            self.has_type(ConnectionList, Mutable)
            and from_list.has_type(ConnectionList)
            and num.has_type(Float)
        ):
            self.set_op_type(ConnectionList, Mutable)
            from_list.set_op_type(ConnectionList)
            num.set_op_type(Float)
            return True

        return False

    # IN, NIN
    def list_inclusion_context(self, rhs: Argument) -> bool:
        if self.has_type(ConnectionList) and rhs.has_type(Connection):
            self.set_op_type(ConnectionList)
            rhs.set_op_type(Connection)

        elif self.has_type(MessageList) and rhs.has_type(Message):
            self.set_op_type(MessageList)
            rhs.set_op_type(Message)

        elif self.has_type(FloatList) and rhs.has_type(Float):
            self.set_op_type(FloatList)
            rhs.set_op_type(Float)

        else:
            return False

        return True

    # CLR
    def list_clear_context(self) -> bool:
        if self.has_type(List, Mutable):
            self.set_op_type(List, Mutable)
            return True

        return False

    # LEN
    def list_length_context(self, rhs: Argument) -> bool:
        if self.has_type(Float, Mutable) and rhs.has_type(List):
            self.set_op_type(Float, Mutable)
            rhs.set_op_type(List)
            return True

        return False

    # SEND
    def send_context(self) -> bool:
        if self.has_type(ConnectionList):
            self.set_op_type(ConnectionList)

        elif self.has_type(Connection):
            self.set_op_type(Connection)

        else:
            return False

        return True

    # RAND
    def random_number_generation_context(self, *args: Argument) -> bool:
        if self.has_type(Float, Mutable) and all([arg.has_type(Float) for arg in args]):
            self.set_op_type(Float, Mutable)
            for arg in args:
                arg.set_op_type(Float)
            return True

        return False

    # ROUND
    def round_number_context(self) -> bool:
        if self.has_type(Float, Mutable):
            self.set_op_type(Float, Mutable)
            return True

        return False

    # LR
    def list_read_context(self, src: Argument, idx: Argument) -> bool:
        if (
            self.has_type(Float, Mutable)
            and src.has_type(FloatList)
            and idx.has_type(Float)
        ):
            self.set_op_type(Float, Mutable)
            src.set_op_type(FloatList)
            idx.set_op_type(Float)

        elif (
            self.has_type(Connection, Mutable)
            and src.has_type(ConnectionList)
            and idx.has_type(Float)
        ):
            self.set_op_type(Connection, Mutable)
            src.set_op_type(ConnectionList)
            idx.set_op_type(Float)

        else:
            return False

        return True

    # LW
    def list_write_context(self, idx: Argument, value: Argument) -> bool:
        if (
            self.has_type(FloatList, Mutable)
            and idx.has_type(Float)
            and value.has_type(Float)
        ):
            self.set_op_type(FloatList, Mutable)
            idx.set_op_type(Float)
            value.set_op_type(Float)

        elif (
            self.has_type(ConnectionList, Mutable)
            and idx.has_type(Float)
            and value.has_type(Connection)
        ):
            self.set_op_type(ConnectionList, Mutable)
            idx.set_op_type(Float)
            value.set_op_type(Connection)

        else:
            return False

        return True

    def get_modvar_type(self, subtype: str) -> Type:
        new_type = type(subtype, (ModuleVariable,), {})
        return new_type

    def explain(self) -> str:
        types = f"{self.expr}: [ "
        for argument_type in self.types:
            types += type(argument_type).__name__ + ", "
        types = types.rstrip().rsplit(",", 1)[0]
        types += " ]"
        return types

    def explain_type_in_op(self) -> str:
        return type(self.type_in_op).__name__ if self.type_in_op else "UNKNOWN"

    def print(self) -> None:
        print(f"Argument {self.expr}")
        print(f"Type in op: {self.explain_type_in_op()}")
        for argument_type in self.types:
            type(argument_type).__name__
