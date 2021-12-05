from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from intermediate.param import MessageFloatParam


class Message:
    RESERVED_PARAMS = [ 'sender', 'type', 'performative' ]
    
    def __init__(self, _type: str):
        self.type: str = _type
        self.float_params: Dict[str, MessageFloatParam] = {}
        
    @property
    def param_names(self) -> List[str]:
        return [ *Message.RESERVED_PARAMS, *list(self.float_params) ]
    
    def param_exists(self, name: str) -> bool:
        return name in self.param_names
    
    def add_float(self, float_param: MessageFloatParam) -> None:
        self.float_params[float_param.name] = float_param
        
    def print(self) -> None:
        print(f'Message {self.type}')
        for float_params in self.float_params.values():
            float_params.print()
