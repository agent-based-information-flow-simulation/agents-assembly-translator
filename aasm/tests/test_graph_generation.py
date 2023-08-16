import pytest
import numpy
import random
import pprint
import re

from aasm import get_spade_code


def get_agent_names(code):
    agent_names = []
    for line in code:
        line = line.strip()
        tmp_line = line.upper()
        if (
            tmp_line.startswith("DEFG")
            or tmp_line.startswith("DEFNODE")
            or tmp_line.startswith("DEFTYPE")
        ):
            line = re.sub(r"\s+", " ", line)
            line = re.sub(r",", " ", line)
            agent_names.append(line.split(" ")[1].strip())
    return list(set(agent_names))


def assert_common_properties(generated_agents, expected_length, agent_names):
    assert (
        len(generated_agents) == expected_length
    ), f"Expected the graph to contain {expected_length} nodes, got {len(generated_agents)} instead"
    list_names = []
    for name in agent_names:
        list_name = name + "_list"
        list_names.append(list_name)
    for agent in generated_agents:
        assert (
            agent["type"] in agent_names
        ), f"Generated {agent['type']} not declared in code"
        sum_in_lists = 0
        print(len(agent["connections"]))
        print(agent["connections"])
        for list_name in list_names:
            assert (
                list_name in agent
            ), f"Generated {agent['type']} does not contain {list_name}"
            print(list_name)
            print(agent[list_name])
            print(len(agent[list_name]))
            sum_in_lists += len(agent[list_name])
            print(sum_in_lists)
        assert sum_in_lists == len(
            agent["connections"]
        ), f'agent {agent["jid"]} has {len(agent["connections"])} connections, but {sum_in_lists} in agent specific lists'


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
    pprint.pprint(generated)
    assert_common_properties(generated, 170, agent_names)
    # ensure 20 users and 150 media_source agents
    user_count = 0
    media_source_count = 0
    for agent in generated:
        conn_list_len = len(agent["connections"])
        sum_other_lists = len(agent["user_list"]) + len(agent["media_source_list"])
        assert (
            conn_list_len == sum_other_lists
        ), f'agent {agent["jid"]} has {conn_list_len} connections, but {sum_other_lists} in agent specific lists'
        if agent["type"] == "user":
            user_count += 1
            assert (
                conn_list_len == 10
            ), f'user agent {agent["jid"]} has {conn_list_len} connections expected: 10'
        if agent["type"] == "media_source":
            media_source_count += 1
            assert (
                conn_list_len > 0
            ), f'media_source agent {agent["jid"]} has 0 connections'
    assert user_count == 20, f"Expected 20 user agents, got {user_count}"
    assert (
        media_source_count == 150
    ), f"Expected 150 media_source agents, got {media_source_count}"


def test_matrix_graph(matrix_graph_code, algo_runner):
    spade_code = get_spade_code(matrix_graph_code)
    agent_names = get_agent_names(matrix_graph_code)
    generated = algo_runner(spade_code.graph_code_lines, "matrix", "test_id")
    pprint.pprint(generated)
    assert_common_properties(generated, 15, agent_names)
    scale = 3  # from fixture, could be moved to a parsing function from code
    user_count = 0
    media_source_count = 0
    null_count = 0
    for agent in generated:
        if agent["type"] == "user":
            user_count += 1
            user_list_len = len(agent["user_list"])
            assert (
                user_list_len >= 1 + scale - 1 and user_list_len <= 2 + scale - 1
            ), f'user agent {agent["jid"]} has {user_list_len} user agents, expected between {1 + scale - 1} and {2 + scale - 1}'
        elif agent["type"] == "media_source":
            media_source_count += 1
            assert (
                len(agent["connections"]) == 3 + scale - 1
            ), f'media_source agent {agent["jid"]} has {len(agent["connections"])} connections, expected {3 + scale - 1}'
            assert (
                len(agent["media_source_list"]) == scale - 1
            ), f'media_source agent {agent["jid"]} has {len(agent["media_source_list"])} media_source agents, expected {scale - 1}'
        elif agent["type"] == "null":
            null_count += 1
            assert (
                len(agent["connections"]) == 1 + scale - 1
            ), f'media_source agent {agent["jid"]} has {len(agent["connections"])} connections, expected {1 + scale - 1}'
            assert (
                len(agent["null_list"]) == scale - 1
            ), f'media_source agent {agent["jid"]} has {len(agent["null_list"])} null agents, expected {scale - 1}'
    assert (
        user_count == 3 * scale
    ), f"Expected {3 * scale} user agents, got {user_count}"
    assert (
        media_source_count == 1 * scale
    ), f"Expected {3 * scale} media_source agents, got {media_source_count}"
    assert (
        null_count == 1 * scale
    ), f"Expected {3 * scale} null agents, got {null_count}"


def test_barabasi_graph(barabasi_graph_code, algo_runner):
    spade_code = get_spade_code(barabasi_graph_code)
    agent_names = get_agent_names(barabasi_graph_code)
    generated = algo_runner(spade_code.graph_code_lines, "barabasi", "test_id")
    # pprint.pprint(generated)
    assert_common_properties(generated, 60, agent_names)
    user_count = 0
    media_source_count = 0
    for agent in generated:
        if agent["type"] == "user":
            user_count += 1
        elif agent["type"] == "media_source":
            media_source_count += 1
    assert user_count == 50, f"Expected 10 user agents, got {user_count}"
    assert (
        media_source_count == 10
    ), f"Expected 10 media_source agents, got {media_source_count}"
