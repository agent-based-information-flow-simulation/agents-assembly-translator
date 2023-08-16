from __future__ import annotations

from itertools import compress
from typing import TYPE_CHECKING, List

from aasm.generating.python_code import PythonCode
from aasm.intermediate.graph import (
    AgentConstantAmount,
    AgentPercentAmount,
    ConnectionConstantAmount,
    ConnectionDistExpAmount,
    ConnectionDistNormalAmount,
    ConnectionDistUniformAmount,
    MatrixGraph,
    StatisticalGraph,
    BarabasiGraph,
    InhomogenousRandomGraph,
)

if TYPE_CHECKING:
    from aasm.intermediate.graph import Graph


class PythonGraph(PythonCode):
    def __init__(self, indent_size: int, graph: Graph | None):
        super().__init__(indent_size)
        if graph:
            self.add_required_imports()
            self.generate_graph(graph)

    def add_agent_class_definition(self):
        self.add_line("class Agent:")
        self.indent_right()
        self.add_line(
            "def __init__(self, jid: str, type: str, connections = None, sim_id: str = '', conn_list_names = None):"
        )
        self.indent_right()
        self.add_line("self.jid = jid")
        self.add_line("self.type = type")
        self.add_line("self.sim_id = sim_id")
        self.add_line("if conn_list_names is not None:")
        self.indent_right()
        self.add_line("self.conn_lists = {}")
        self.add_line("for name in conn_list_names:")
        self.indent_right()
        self.add_line(f"self.conn_lists[name + '_list'] = []")
        self.indent_left()
        self.indent_left()
        self.add_line("else:")
        self.indent_right()
        self.add_line("self.conn_lists = {}")
        self.indent_left()
        self.add_line("if connections is not None:")
        self.indent_right()
        self.add_line("self.connections = connections")
        self.indent_left()
        self.add_line("else:")
        self.indent_right()
        self.add_line("self.connections = []")
        self.indent_left()
        self.indent_left()
        self.add_newline()
        self.add_line("def add_connection(self, connection: str, type: str):")
        self.indent_right()
        self.add_line("self.connections.append(connection)")
        self.add_line("self.conn_lists[type + '_list'].append(connection)")
        self.indent_left()
        self.add_newline()
        self.add_line("def add_to_list(self, connection: str, type: str):")
        self.indent_right()
        self.add_line("self.conn_lists[type + '_list'].append(connection)")
        self.indent_left()
        self.add_newline()
        self.add_line("def to_dict(self):")
        self.indent_right()
        self.add_line("ret = {}")
        self.add_line("ret['jid'] = self.jid")
        self.add_line("ret['type'] = self.type")
        self.add_line("ret['connections'] = self.connections")
        self.add_line("ret['sim_id'] = self.sim_id")
        self.add_line("for name, conn_list in self.conn_lists.items():")
        self.indent_right()
        self.add_line("ret[name] = conn_list")
        self.indent_left()
        self.add_line("return ret")
        self.indent_left()
        self.indent_left()

    def add_required_imports(self) -> None:
        self.add_line("import random")
        self.add_line("import uuid")
        self.add_line("import numpy")

    def generate_graph(self, graph: Graph) -> None:
        match graph:
            case StatisticalGraph():
                self.add_statistical_graph(graph)

            case MatrixGraph():
                self.add_matrix_graph(graph)

            case BarabasiGraph():
                self.add_barabasi_graph(graph)

            case InhomogenousRandomGraph():
                self.add_irg_graph(graph)

            case _:
                raise Exception(f"Unknown graph type: {graph.print()}")

    def add_statistical_graph(self, graph: StatisticalGraph) -> None:
        self.add_line('def generate_graph_structure(domain, sim_id=""):')
        self.indent_right()
        self.add_agent_class_definition()

        if not graph.agents:
            self.add_line("return []")
            self.indent_left()
            return
        num_agents_expr: List[str] = []
        self.add_line("agent_types = []")
        for agent in graph.agents.values():
            self.add_line(f"agent_types += ['{agent.name}']")
            match agent.amount:
                case AgentConstantAmount():
                    self.add_line(f"_num_{agent.name} = {agent.amount.value}")

                case AgentPercentAmount():
                    self.add_line(
                        f"_num_{agent.name} = round({agent.amount.value} / 100 * {graph.size})"
                    )

                case _:
                    raise Exception(
                        f"Unknown agent amount type: {agent.amount.print()}"
                    )

            num_agents_expr.append(f"_num_{agent.name}")

        self.add_line(f'num_agents = {" + ".join(num_agents_expr)}')

        self.add_line('if sim_id == "":')
        self.indent_right()
        self.add_line("random_id = str(uuid.uuid4())[:5]")
        self.indent_left()
        self.add_line("else:")
        self.indent_right()
        self.add_line("random_id = sim_id")
        self.indent_left()
        self.add_line('jids = [f"{i}_{random_id}@{domain}" for i in range(num_agents)]')
        self.add_line("agents = []")
        self.add_line("next_agent_idx = 0")
        for agent in graph.agents.values():
            self.add_line(f"for _ in range(_num_{agent.name}):")
            self.indent_right()

            match agent.connections:
                case ConnectionConstantAmount():
                    self.add_line(f"num_connections = {agent.connections.value}")

                case ConnectionDistNormalAmount():
                    self.add_line(
                        f"num_connections = int(numpy.random.normal({agent.connections.mean}, {agent.connections.std_dev}))"
                    )

                case ConnectionDistExpAmount():
                    self.add_line(
                        f"num_connections = int(numpy.random.exponential(1 / {agent.connections.lambda_}))"
                    )

                case ConnectionDistUniformAmount():
                    self.add_line(
                        f"num_connections = int(random.uniform({agent.connections.a}, {agent.connections.b}))"
                    )

                case _:
                    raise Exception(
                        f"Unknown connection amount: {agent.connections.print()}"
                    )

            self.add_line(
                "num_connections = max(min(num_connections, len(jids) - 1), 0)"
            )
            self.add_line("jid = jids[next_agent_idx]")
            self.add_line(
                "connections = random.sample([other_jid for other_jid in jids if other_jid != jid], num_connections)"
            )
            self.add_line(
                f"new_agent = Agent(jid, '{agent.name}', connections, random_id, agent_types)"
            )
            self.add_line("agents.append(new_agent)")
            self.add_line("next_agent_idx += 1")
            self.indent_left()
        self.add_line("for agent in agents:")
        self.indent_right()
        self.add_line("for other_agent in agents:")
        self.indent_right()
        self.add_line("if agent.jid in other_agent.connections:")
        self.indent_right()
        self.add_line("other_agent.add_to_list(agent.jid, agent.type)")
        self.indent_left()
        self.indent_left()
        self.indent_left()
        self.add_line("return [agent.to_dict() for agent in agents]")
        self.indent_left()

    def add_matrix_graph(self, graph: MatrixGraph):
        self.add_line('def generate_graph_structure(domain, sim_id=""):')
        self.indent_right()
        self.add_agent_class_definition()
        if not graph.agents:
            self.add_line("return []")
            self.indent_left()
            return
        if graph.is_scale_defined():
            self.add_line(f"scale_factor = {graph.scale}")
        else:
            self.add_line(f"scale_factor = 1")
        self.add_line(f"n_agent_types = {len(graph.agents)}")
        self.add_line("graph_size = scale_factor * n_agent_types")
        self.add_line('if sim_id == "":')
        self.indent_right()
        self.add_line("random_id = str(uuid.uuid4())[:5]")
        self.indent_left()
        self.add_line("else:")
        self.indent_right()
        self.add_line("random_id = sim_id")
        self.indent_left()
        self.add_line('jids = [f"{i}_{random_id}@{domain}" for i in range(graph_size)]')
        self.add_line("agent_types = []")
        self.add_line("agents = []")
        self.add_line("indx_sets = []")
        for agent in graph.agents:
            self.add_line(f"agent_types.append('{agent.name}')")
            adj_indx = [True if x == 1 else False for x in agent.adj_row.row]
            adj_indx = list(compress(range(len(adj_indx)), adj_indx))
            self.add_line(f"indx_sets.append({adj_indx})")

        self.add_line("agent_types = agent_types * scale_factor")

        self.add_line("for base_agent_index in range(n_agent_types):")
        self.indent_right()
        self.add_line("indices = indx_sets[base_agent_index]")
        self.add_line("for shift in range(1, scale_factor):")
        self.indent_right()
        self.add_line(
            f"indices.append((base_agent_index + shift * n_agent_types) % graph_size)"
        )
        self.indent_left()
        self.add_line("for shift in range(scale_factor):")
        self.indent_right()
        self.add_line("agent_idx = base_agent_index + shift * n_agent_types")
        self.add_line("jid = jids[agent_idx]")
        self.add_line("agent_type = agent_types[agent_idx]")
        self.add_line("connections = []")
        self.add_line("for i in indices:")
        self.indent_right()
        self.add_line(
            f"connections.append(jids[(i + shift * n_agent_types) % graph_size])"
        )
        self.indent_left()
        self.add_line(
            "new_agent = Agent(jid, agent_type, connections, random_id, list(set(agent_types)))"
        )
        self.add_line("agents.append(new_agent)")
        self.indent_left()
        self.indent_left()
        self.add_line("for agent in agents:")
        self.indent_right()
        self.add_line("for other_agent in agents:")
        self.indent_right()
        self.add_line("if agent.jid in other_agent.connections:")
        self.indent_right()
        self.add_line("other_agent.add_to_list(agent.jid, agent.type)")
        self.indent_left()
        self.indent_left()
        self.indent_left()
        self.add_line("return [agent.to_dict() for agent in agents]")
        self.indent_left()

    def add_barabasi_graph(self, graph: BarabasiGraph):
        # generate jid list using draw by draw Barabasi-Albert algorithm for the provided graph with its m0 and m
        self.add_line('def generate_graph_structure(domain, sim_id=""):')
        self.indent_right()
        self.add_agent_class_definition()
        if not graph.agents:
            self.add_line("return []")
            self.indent_left()
            return

        self.add_line(f"agent_types = []")

        num_agents_expr: List[str] = []
        for agent in graph.agents.values():
            match agent.amount:
                case AgentConstantAmount():
                    self.add_line(f"_num_{agent.name} = {agent.amount.value}")

                case AgentPercentAmount():
                    self.add_line(
                        f"_num_{agent.name} = round({agent.amount.value} / 100 * {graph.size})"
                    )

                case _:
                    raise Exception(
                        f"Unknown agent amount type: {agent.amount.print()}"
                    )

            num_agents_expr.append(f"_num_{agent.name}")
            self.add_line(f"tmp = ['{agent.name}'] * _num_{agent.name}")
            self.add_line("agent_types.extend(tmp)")

        self.add_line(f'num_agents = {" + ".join(num_agents_expr)}')
        self.add_line("random.shuffle(agent_types)")

        self.add_line('if sim_id == "":')
        self.indent_right()
        self.add_line("random_id = str(uuid.uuid4())[:5]")
        self.indent_left()
        self.add_line("else:")
        self.indent_right()
        self.add_line("random_id = sim_id")
        self.indent_left()
        if graph.m_params is not None:
            self.add_line(f"m0 = {graph.m_params.m0}")
            self.add_line(f"m = {graph.m_params.m_inc}")
        self.add_line('jids = [f"{i}_{random_id}@{domain}" for i in range(num_agents)]')
        # self.add_line("agents = []")
        self.add_line("connection_lists = []")
        self.add_line("next_agent_idx = 0")
        # begin by creating the initial complete graph
        self.add_line("init_jids = random.choices(jids, k=m0)")
        self.add_line("for jid in init_jids:")
        self.indent_right()
        self.add_line("copy = init_jids.copy()")
        self.add_line("copy.remove(jid)")
        self.add_line("connection_lists.append(copy)")
        self.indent_left()
        self.add_line("next_agent_idx += m0")
        self.add_line("for i in range(m0, num_agents):")
        self.indent_right()
        self.add_line("to_connect = []")
        self.add_line("ids = list(range(next_agent_idx))")
        self.add_line("while len(to_connect) < m:")
        self.indent_right()
        self.add_line("weights = [len(connection_lists[ident]) for ident in ids]")
        self.add_line("to_connect.append(random.choices(ids, weights=weights)[0])")
        self.add_line("ids.remove(to_connect[-1])")
        self.indent_left()
        self.add_line("to_connect_jids = [jids[ident] for ident in to_connect]")
        self.add_line("connection_lists.append(to_connect_jids)")
        self.add_line("for id in to_connect:")
        self.indent_right()
        # two sided connections
        self.add_line("connection_lists[id].append(jids[next_agent_idx])")
        self.add_line("connection_lists[id] = list(set(connection_lists[id]))")
        self.indent_left()
        self.add_line("next_agent_idx += 1")
        self.indent_left()
        self.add_line("agents = []")
        self.add_line("for i in range(num_agents):")
        self.indent_right()
        self.add_line(
            "agent = Agent(jids[i], agent_types[i], connection_lists[i], random_id, list(set(agent_types)))"
        )
        self.add_line("agents.append(agent)")
        self.indent_left()
        self.add_line("for agent in agents:")
        self.indent_right()
        self.add_line("for other_agent in agents:")
        self.indent_right()
        self.add_line("if agent.jid in other_agent.connections:")
        self.indent_right()
        self.add_line("other_agent.add_to_list(agent.jid, agent.type)")
        self.indent_left()
        self.indent_left()
        self.indent_left()
        self.add_line("return [agent.to_dict() for agent in agents]")
        self.indent_left()

    def add_irg_graph(self, graph: InhomogenousRandomGraph):
        self.add_line('def generate_graph_structure(domain, sim_id=""):')
        self.indent_right()
        self.add_newline()
        self.add_agent_class_definition()
        self.add_newline()
        if not graph.agents:
            self.add_line("return []")
            self.indent_left()
            return
        self.add_line("agent_types = []")
        self.add_line("probo_matrix = {}")
        num_agents_expr: List[str] = []
        for agent in graph.agents.values():
            self.add_line(f"probo_matrix['{agent.name}'] = []")
            for probo in agent.amounts:
                self.add_line(f"probo_matrix['{agent.name}'].append({probo.value})")
            match agent.amount:
                case AgentConstantAmount():
                    self.add_line(f"_num_{agent.name} = {agent.amount.value}")

                case AgentPercentAmount():
                    self.add_line(
                        f"_num_{agent.name} = round({agent.amount.value} / 100 * {graph.size})"
                    )

                case _:
                    raise Exception(
                        f"Unknown agent amount type: {agent.amount.print()}"
                    )

            num_agents_expr.append(f"_num_{agent.name}")
            self.add_line(f"tmp = ['{agent.name}'] * _num_{agent.name}")
            self.add_line("agent_types.extend(tmp)")

        self.add_line(f'num_agents = {" + ".join(num_agents_expr)}')

        self.add_line('if sim_id == "":')
        self.indent_right()
        self.add_line("random_id = str(uuid.uuid4())[:5]")
        self.indent_left()
        self.add_line("else:")
        self.indent_right()
        self.add_line("random_id = sim_id")
        self.indent_left()
        self.add_line('jids = [f"{i}_{random_id}@{domain}" for i in range(num_agents)]')
        self.add_line(f"order = {graph.order}")
        self.add_line("agents = []")
        self.add_line("for i in range(num_agents):")
        self.indent_right()
        self.add_line(
            "agents.append(Agent(jids[i], agent_types[i], sim_id = random_id, conn_list_names=agent_types))"
        )
        self.indent_left()
        self.add_line("for agent in agents:")
        self.indent_right()
        self.add_line("for agent2 in agents:")
        self.indent_right()
        self.add_line("if agent != agent2:")
        self.indent_right()
        self.add_line("conn_index = order.index(agent2.type)")
        self.add_line("probo = probo_matrix[agent.type][conn_index]")
        self.add_line("if random.random() * 100 < probo:")
        self.indent_right()
        self.add_line("agent.add_connection(agent2.jid, agent2.type)")
        self.indent_left()
        self.indent_left()
        self.indent_left()
        self.indent_left()
        self.add_line("return [agent.to_dict() for agent in agents]")
        self.indent_left()
