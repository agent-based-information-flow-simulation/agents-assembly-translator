import sys
from parse import get_environments
from spade_generator import generate_agent, get_imports


def main(file_path: str, debug: bool) -> None:
    with open(file_path, 'r') as f:
        lines = f.readlines()
    environments = get_environments(lines, debug)
    code_lines = get_imports()
    for environment in environments:
        if debug:
            environment.print()
        for agent_name, agent_def in environment.agents.items():
            agent_code = generate_agent(agent_name, agent_def)
            code_lines.extend(agent_code)
    with open('out.py', 'w') as f:
        for code_line in code_lines:
            f.write(code_line)


if __name__ == '__main__':
    main(sys.argv[1], False)
