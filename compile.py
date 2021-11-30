from typing import Tuple
from argparse import ArgumentParser
from parse import get_environments
from spade_generator import generate_agent, get_imports


def get_args() -> Tuple[str, str, bool]:
    parser = ArgumentParser()
    parser.add_argument('input_path', type=str, help='path to input file in .aa format')
    parser.add_argument('-d', '--debug', action='store_true', help='toggle compiler debug mode')
    parser.add_argument('-o', '--output_path', type=str, default='out', help='output path')
    args = parser.parse_args()
    return args.input_path, args.output_path, args.debug

def main(input_path: str, output_path: str, debug: bool) -> None:
    with open(input_path, 'r') as f:
        lines = f.readlines()
    environments = get_environments(lines, debug)
    code_lines = get_imports()
    for environment in environments:
        if debug:
            environment.print()
        for agent_name, agent_def in environment.agents.items():
            agent_code = generate_agent(agent_name, agent_def)
            code_lines.extend(agent_code)
    with open(output_path, 'w') as f:
        for code_line in code_lines:
            f.write(code_line)


if __name__ == '__main__':
    input_path, output_path, debug = get_args()
    main(input_path, output_path, debug)
