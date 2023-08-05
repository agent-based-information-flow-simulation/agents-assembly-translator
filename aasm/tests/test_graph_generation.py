import pytest
import numpy
import random

from aasm import get_spade_code


def test_irg_graph(irg_graph_code, algo_runner):
    spade_code = get_spade_code(irg_graph_code)
    print(spade_code.graph_code_lines)
    generated = algo_runner(spade_code.graph_code_lines, "irg", 0)
    print(generated)
    assert spade_code.graph_code_lines == "XD"
