from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime
from typing import TYPE_CHECKING, List, Tuple

from aasm.generating.python_spade import get_spade_code
from aasm.generating.python_module import get_modules_for_target
from aasm.utils.exception import PanicException

if TYPE_CHECKING:
    from aasm.generating.code import Code
    from aasm.modules.module import Module


def get_args() -> Tuple[str, str, bool, List[str]]:
    parser = ArgumentParser()
    parser.add_argument("input_path", type=str, help="path to the input file")
    parser.add_argument("-I", "--include", nargs="*", help="include paths")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="toggle the compiler debug mode"
    )
    parser.add_argument(
        "-o", "--output-path", type=str, default="out", help="the output file path"
    )
    args = parser.parse_args()
    return args.input_path, args.output_path, args.debug, args.include


def get_input(input_path: str) -> List[str]:
    with open(input_path, "r") as f:
        lines = f.readlines()
    return lines


def save_output(output_path: str, code: Code) -> None:
    with open(output_path, "w") as f:
        for code_line in code:
            f.write(code_line)


def main(
    input_path: str, output_path: str, debug: bool, includes: List[str] | None
) -> None:
    loaded_module_files: List[List[str]] = []
    if includes is not None:
        try:
            for include in includes:
                loaded_module_files.append(get_input(include))
        except PanicException as e:
            e.print()
            exit(1)

    lines = get_input(input_path)
    start_time = datetime.now()
    try:
        spade_modules = get_modules_for_target(loaded_module_files, "spade")
        print("Loaded modules:")
        for module in spade_modules:
            print(f"\t{module}")
        spade_code = get_spade_code(
            lines, indent_size=4, debug=debug, modules=spade_modules
        )
    except PanicException as e:
        e.print()
        exit(1)
    time_delta = (datetime.now() - start_time).total_seconds()
    save_output(output_path, spade_code)
    print(f'({time_delta}s) Your results are saved in the file "{output_path}" 😎')


if __name__ == "__main__":
    input_path, output_path, debug, includes = get_args()
    main(input_path, output_path, debug, includes)
