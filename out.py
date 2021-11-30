import random as r
import spade
from numpy.random import normal


class a1(spade.agent.Agent):
    def __init__(self, jid, password, location, connections):
        super().__init__(jid, password, verify_security=False)
        self.param1 = 200
        self.param2 = normal(2138, 2137)
        self.param3 = "enum_val1"
        self.param4 = r.choices(["enum_val3", "enum_val4"], [99, 1])
        self.param5 = []
        self.param6 = []
