import pytest
import os

import random
import numpy
import json

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture(autouse=True)
def set_random_seed():
    # Set a fixed seed value for numpy and random number generators.
    seed_value = 42
    numpy.random.seed(seed_value)
    random.seed(seed_value)


@pytest.fixture(scope="package")
def irg_graph_code():
    with open(os.path.join(FIXTURE_PATH, "inhomogenous.aasm")) as f:
        return f.read().split("\n")


@pytest.fixture(scope="package")
def statistical_graph_code():
    with open(os.path.join(FIXTURE_PATH, "statistical.aasm")) as f:
        return f.read().split("\n")


@pytest.fixture(scope="package")
def matrix_graph_code():
    with open(os.path.join(FIXTURE_PATH, "matrix.aasm")) as f:
        return f.read().split("\n")


@pytest.fixture(scope="package")
def barabasi_graph_code():
    with open(os.path.join(FIXTURE_PATH, "barabasi-albert.aasm")) as f:
        return f.read().split("\n")


@pytest.fixture(scope="package")
def algo_runner():
    def run_algorithm(graph_code_lines, domain, sim_id):
        exec("\n".join(graph_code_lines))
        try:
            algorithm = locals()["generate_graph_structure"]
        except KeyError:
            return []
        return algorithm(domain, sim_id)

    return run_algorithm
