from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from intermediate.behaviour import (Behaviour, CyclicBehaviour,
                                        MessageReceivedBehaviour,
                                        OneTimeBehaviour, SetupBehaviour)
    from intermediate.param import (AgentConnectionListParam,
                                    AgentDistExpFloatParam,
                                    AgentDistNormalFloatParam, AgentEnumParam,
                                    AgentInitFloatParam, AgentMessageListParam)


class Agent:
    RESERVED_FLOAT_PARAMS = [ 'connCount', 'msgRCount', 'msgSCount' ]
    RESERVED_CONNECTION_LIST_PARAMS = [ 'connections' ]
    
    def __init__(self, name: str):
        self.name: str = name
        self.init_floats: Dict[str, AgentInitFloatParam] = {}
        self.dist_normal_floats: Dict[str, AgentDistNormalFloatParam] = {}
        self.dist_exp_floats: Dict[str, AgentDistExpFloatParam] = {}
        self.enums: Dict[str, AgentEnumParam] = {}
        self.connection_lists: Dict[str, AgentConnectionListParam] = {}
        self.message_lists: Dict[str, AgentMessageListParam] = {}
        self.setup_behaviours: Dict[str, SetupBehaviour] = {}
        self.one_time_behaviours: Dict[str, OneTimeBehaviour] = {}
        self.cyclic_behaviours: Dict[str, CyclicBehaviour] = {}
        self.message_received_behaviours: Dict[str, MessageReceivedBehaviour] = {}
        self._last_modified_behaviours: Dict[str, Behaviour] | None = None
    
    @property
    def last_behaviour(self) -> Behaviour:
        return self._last_modified_behaviours[list(self._last_modified_behaviours.keys())[-1]]
    
    @property
    def param_names(self) -> List[str]:
        return [ *Agent.RESERVED_FLOAT_PARAMS,
                 *Agent.RESERVED_CONNECTION_LIST_PARAMS,
                 *list(self.init_floats), 
                 *list(self.dist_normal_floats),
                 *list(self.dist_exp_floats),
                 *list(self.enums), 
                 *list(self.connection_lists),
                 *list(self.message_lists) ]
    
    @property
    def behaviour_names(self) -> List[str]:
        return [ *list(self.setup_behaviours),
                 *list(self.one_time_behaviours),
                 *list(self.cyclic_behaviours),
                 *list(self.message_received_behaviours) ]
    
    @property
    def float_param_names(self) -> List[str]:
        return [ *list(self.init_floats),
                 *list(self.dist_normal_floats), 
                 *list(self.dist_exp_floats) ]
    
    def add_init_float(self, float_param: AgentInitFloatParam) -> None:
        self.init_floats[float_param.name] = float_param

    def add_dist_normal_float(self, float_param: AgentDistNormalFloatParam) -> None:
        self.dist_normal_floats[float_param.name] = float_param
    
    def add_dist_exp_float(self, float_param: AgentDistExpFloatParam) -> None:
        self.dist_exp_floats[float_param.name] = float_param
    
    def add_enum(self, enum_param: AgentEnumParam) -> None:
        self.enums[enum_param.name] = enum_param
    
    def add_connection_list(self, list_param: AgentConnectionListParam) -> None:
        self.connection_lists[list_param.name] = list_param
    
    def add_message_list(self, list_param: AgentMessageListParam) -> None:
        self.message_lists[list_param.name] = list_param
    
    def add_setup_behaviour(self, behaviour: SetupBehaviour) -> None:
        self.setup_behaviours[behaviour.name] = behaviour
        self._last_modified_behaviours = self.setup_behaviours
    
    def add_one_time_behaviour(self, behaviour: OneTimeBehaviour) -> None:
        self.one_time_behaviours[behaviour.name] = behaviour
        self._last_modified_behaviours = self.one_time_behaviours
    
    def add_cyclic_behaviour(self, behaviour: CyclicBehaviour) -> None:
        self.cyclic_behaviours[behaviour.name] = behaviour
        self._last_modified_behaviours = self.cyclic_behaviours
    
    def add_message_received_behaviour(self, behaviour: MessageReceivedBehaviour) -> None:
        self.message_received_behaviours[behaviour.name] = behaviour
        self._last_modified_behaviours = self.message_received_behaviours

    def param_exists(self, name: str) -> bool:
        return name in self.param_names
    
    def behaviour_exists(self, name: str) -> bool:
        return name in self.behaviour_names
    
    def print(self) -> None:
        print(f'Agent {self.name}')
        for init_float_param in self.init_floats.values():
            init_float_param.print()
        for dist_normal_float_param in self.dist_normal_floats.values():
            dist_normal_float_param.print()
        for dist_exp_float_param in self.dist_exp_floats.values():
            dist_exp_float_param.print()
        for enum_param in self.enums.values():
            enum_param.print()
        for connection_list_param in self.connection_lists.values():
            connection_list_param.print()
        for message_list_param in self.message_lists.values():
            message_list_param.print()
        for setup_behaviour in self.setup_behaviours.values():
            setup_behaviour.print()
        for one_time_behaviour in self.one_time_behaviours.values():
            one_time_behaviour.print()
        for cyclic_behaviour in self.cyclic_behaviours.values():
            cyclic_behaviour.print()
        for message_received_behaviour in self.message_received_behaviours.values():
            message_received_behaviour.print()
