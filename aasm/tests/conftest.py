import pytest
import os

import random

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture(scope="package")
def irg_graph_code():
    with open(os.path.join(FIXTURE_PATH, "inhomogenous.aasm")) as f:
        return f.read().split("\n")


@pytest.fixture(scope="package")
def algo_runner():
    def run_algorithm(graph_code_lines, domain, seed):
        exec("\n".join(graph_code_lines))
        try:
            algorithm = locals()["generate_graph_structure"]
        except KeyError:
            return []
        return algorithm(domain, seed)

    return run_algorithm
