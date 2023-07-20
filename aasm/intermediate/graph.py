from __future__ import annotations

from typing import Any, Dict, List, Tuple, Callable, List


class MParameters:
    def __init__(self, a: int, b: int):
        self.m0 = a
        self.m_inc = b

    def print(self) -> None:
        print(f"MParameters values = {self.m0}, {self.m_inc}")


class AgentAmount:
    def __init__(self, value: str):
        self.value = value

    def print(self) -> None:
        print(f"AgentAmount value = {self.value}")


class AgentConstantAmount(AgentAmount):
    def __init__(self, value: str):
        super().__init__(value)

    def print(self) -> None:
        print("AgentConstantAmount")
        super().print()


class AgentPercentAmount(AgentAmount):
    def __init__(self, value: str):
        super().__init__(value)

    def print(self) -> None:
        print("AgentPercentAmount")
        super().print()


class ConnectionAmount:
    def print(self) -> None:
        raise NotImplementedError()


class ConnectionConstantAmount(ConnectionAmount):
    def __init__(self, value: str):
        self.value = value

    def print(self) -> None:
        print(f"ConnectionConstantAmount value = {self.value}")


class ConnectionDistNormalAmount(ConnectionAmount):
    def __init__(self, mean: str, std_dev: str):
        self.mean = mean
        self.std_dev = std_dev

    def print(self) -> None:
        print(
            f"ConnectionDistNormalAmount mean = {self.mean}, std_dev = {self.std_dev}"
        )


class ConnectionDistExpAmount(ConnectionAmount):
    def __init__(self, lambda_: str):
        self.lambda_ = lambda_

    def print(self) -> None:
        print(f"ConnectionDistExpAmount lambda = {self.lambda_}")


class ConnectionDistUniformAmount(ConnectionAmount):
    def __init__(self, a: str, b: str):
        self.a = a
        self.b = b

    def print(self) -> None:
        print(f"ConnectionDistUniformAmount a = {self.a}, b = {self.b}")


class AdjRow:
    def __init__(self, row: List[int]):
        self.row = row

    def print(self) -> None:
        print("AdjRow")
        for key, value in enumerate(self.row):
            print(f"{key} = {value}")


class MatrixAgent:
    def __init__(self, name: str, adj_row: AdjRow):
        self.name = name
        self.adj_row = adj_row

    def print(self) -> None:
        print(f"MatrixAgent name = {self.name}")
        self.adj_row.print()


class StatisticalAgent:
    def __init__(self, name: str, amount: AgentAmount, connections: ConnectionAmount):
        self.name = name
        self.amount = amount
        self.connections = connections

    def print(self) -> None:
        print(f"StatisticalAgent name = {self.name}")
        self.amount.print()
        self.connections.print()


class BarabasiAgent:
    def __init__(self, name: str, amount: AgentAmount):
        self.name = name
        self.amount = amount

    def print(self) -> None:
        print(f"BarabasiAgent name = {self.name}")
        self.amount.print()


class InhomogeneousAgent:
    def __init__(
        self,
        name: str,
        amount: AgentConstantAmount,
        conn_amounts: List[ConnectionConstantAmount],
    ):
        self.name = name
        self.amount = amount
        self.amounts = conn_amounts

    def print(self) -> None:
        print(f"InhomogeneousAgent name = {self.name}")
        for amount in self.amounts:
            amount.print()


class Graph:
    def __init__(self):
        self.size = None

    def set_size(self, size: int) -> None:
        self.size = size

    def is_size_defined(self) -> bool:
        return self.size is not None

    def is_types_amount_defined(self) -> bool:
        return False

    def is_agent_defined(self, agent_type: str) -> bool:
        return False

    def set_types_amount(self, types_no: int) -> None:
        raise NotImplementedError()

    def get_types_amount(self) -> int:
        raise NotImplementedError()

    def set_scale(self, scale: int) -> None:
        raise NotImplementedError()

    def is_scale_defined(self) -> bool:
        return False

    def set_m(self, m: Tuple[int, int]) -> None:
        raise NotImplementedError()

    def is_m_defined(self) -> bool:
        return False

    def add_agent(self, graph_agent: Any) -> None:
        raise NotImplementedError()

    def print(self) -> None:
        print(f"Graph size = {self.size}")


class StatisticalGraph(Graph):
    def __init__(self):
        super().__init__()
        self.agents: Dict[str, StatisticalAgent] = {}

    def add_agent(self, graph_agent: StatisticalAgent) -> None:
        self.agents[graph_agent.name] = graph_agent

    def is_agent_defined(self, agent_type: str) -> bool:
        return agent_type in self.agents

    def is_agent_percent_amount_used(self) -> bool:
        for agent in self.agents.values():
            if isinstance(agent.amount, AgentPercentAmount):
                return True
        return False

    def print(self) -> None:
        super().print()
        print("StatisticalGraph")
        for agent in self.agents.values():
            agent.print()


class BarabasiGraph(Graph):
    def __init__(self):
        super().__init__()
        self.agents: Dict[str, BarabasiAgent] = {}
        self.m_params = None

    def add_agent(self, graph_agent: BarabasiAgent) -> None:
        self.agents[graph_agent.name] = graph_agent

    def is_agent_defined(self, agent_type: str) -> bool:
        return agent_type in self.agents

    def is_agent_percent_amount_used(self) -> bool:
        for agent in self.agents.values():
            if isinstance(agent.amount, AgentPercentAmount):
                return True
        return False

    def set_m(self, m: Tuple[int, int]) -> None:
        self.m_params = MParameters(*m)

    def is_m_defined(self) -> bool:
        return self.m_params is not None

    def print(self) -> None:
        super().print()
        print("BarabasiGraph")
        for agent in self.agents.values():
            agent.print()


class MatrixGraph(Graph):
    def __init__(self):
        super().__init__()
        self.agents: List[MatrixAgent] = []
        self.scale = None

    def add_agent(self, graph_agent: MatrixAgent) -> None:
        self.agents.append(graph_agent)

    def is_agent_defined(self, agent_type: str) -> bool:
        check_agent: Callable[[MatrixAgent], bool] = (
            lambda agent: agent.name == agent_type
        )
        return all(check_agent(agent) for agent in self.agents)

    def set_scale(self, scale: int) -> None:
        self.scale = scale

    def is_scale_defined(self) -> bool:
        return self.scale is not None

    def print(self) -> None:
        super().print()
        print("MatrixGraph")
        for agent in self.agents:
            agent.print()


class InhomogenousRandomGraph(Graph):
    def __init__(self):
        super().__init__()
        self.agents: Dict[str, InhomogeneousAgent] = {}
        self.types_no = None
        self.order: list[str] = []

    def add_agent(self, graph_agent: InhomogeneousAgent) -> None:
        self.order.append(graph_agent.name)
        self.agents[graph_agent.name] = graph_agent

    def is_agent_defined(self, agent_type: str) -> bool:
        return agent_type in self.agents

    def is_agent_percent_amount_used(self) -> bool:
        check_agent: Callable[[InhomogeneousAgent], bool] = lambda amount: isinstance(
            amount, AgentPercentAmount
        )
        if any(check_agent(agent) for agent in self.agents.values()):
            return True
        return False

    def is_types_amount_defined(self) -> bool:
        return self.types_no is not None

    def set_types_amount(self, types_no: int) -> None:
        self.types_no = types_no

    def get_types_amount(self) -> int:
        if self.types_no is None:
            raise ValueError("Types amount is not defined")
        return self.types_no

    def print(self) -> None:
        super().print()
        print("InhomogenousRandomGraph")
        for agent in self.agents.values():
            agent.print()
