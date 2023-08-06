import pytest
import numpy
import random
import pprint
import re

from aasm import get_spade_code


def get_agent_names(graph_code_lines):
    agent_names = []
    for line in graph_code_lines:
        if line.startswith("agent") or line.startswith("AGENT"):
            agent_names.append(line.split(" ")[1])
    return agent_names


def assert_common_properties(generated_agents, expected_length, agent_names):
    assert (
        len(generated_agents) == expected_length
    ), f"Expected the graph to contain {expected_length} nodes, got {len(generated_agents)} instead"
    for agent in generated_agents:
        assert (
            agent["type"] in agent_names
        ), f"Generated {agent['type']} not declared in code"
        for name in agent_names:
            list_name = name + "_list"
            assert (
                list_name in agent
            ), f"Generated {agent['type']} does not contain {list_name}"


def test_irg_graph(irg_graph_code, algo_runner):
    spade_code = get_spade_code(irg_graph_code)
    agent_names = get_agent_names(irg_graph_code)
    generated = algo_runner(spade_code.graph_code_lines, "irg", "test_id")
    # pprint.pprint(generated)
    assert_common_properties(generated, 23, agent_names)
    null_count = 0
    for agent in generated:
        if agent["type"] == "null":
            assert (
                len(agent["null_list"]) == 0
            ), f'null agent {agent["jid"]} has non-zero null_list'
            assert (
                len(agent["media_source_list"]) == 0
            ), f'null agent {agent["jid"]} has non-zero media_source_list'
        if agent["type"] == "user":
            assert (
                len(agent["media_source_list"]) == 2
            ), f'user agent {agent["jid"]} has an incomplete media_source_list'
            if len(agent["null_list"]) == 0:
                null_count += 1
    # this test depends on the random seed
    assert (
        null_count == 6
    ), f"Expected 6 user agents, connected to null ones got {null_count}"


def test_statistical_graph(statistical_graph_code, algo_runner):
    spade_code = get_spade_code(statistical_graph_code)
    agent_names = get_agent_names(statistical_graph_code)
    generated = algo_runner(spade_code.graph_code_lines, "statistical", "test_id")
    # pprint.pprint(generated)
    assert_common_properties(generated, 170, agent_names)


def test_matrix_graph(matrix_graph_code, algo_runner):
    spade_code = get_spade_code(matrix_graph_code)
    agent_names = get_agent_names(matrix_graph_code)
    generated = algo_runner(spade_code.graph_code_lines, "matrix", "test_id")
    # pprint.pprint(generated)
    assert_common_properties(generated, 15, agent_names)


def test_barabasi_graph(barabasi_graph_code, algo_runner):
    spade_code = get_spade_code(barabasi_graph_code)
    agent_names = get_agent_names(barabasi_graph_code)
    generated = algo_runner(spade_code.graph_code_lines, "barabasi", "test_id")
    # pprint.pprint(generated)
    assert_common_properties(generated, 60, agent_names)
