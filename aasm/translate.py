from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime
from typing import TYPE_CHECKING, List, Tuple

from aasm.generating.python_spade import get_spade_code
from aasm.utils.exception import PanicException
from aasm.utils.exception_handler import ExceptionHandler
from aasm.preprocessor.preprocessor import Preprocessor

if TYPE_CHECKING:
    from aasm.generating.code import Code


def get_args() -> Tuple[str, str, bool, bool]:
    parser = ArgumentParser()
    parser.add_argument('input_path', type=str, help='path to the input file')
    parser.add_argument('-d', '--debug', action='store_true', help='toggle the compiler debug mode')
    parser.add_argument('-P', '--enable-preprocessor', action='store_true', help="enable preprocessor directives")
    parser.add_argument('-o', '--output-path', type=str, default='out', help='the output file path')
    args = parser.parse_args()
    return args.input_path, args.output_path, args.debug, args.enable_preprocessor


def get_input(input_path: str) -> List[str]:
    with open(input_path, 'r') as f:
        lines = f.readlines()
    return lines


def save_output(output_path: str, code: Code) -> None:
    with open(output_path, 'w') as f:
        for code_line in code:
            f.write(code_line)


def main(input_path: str, output_path: str, debug: bool, enable_preprocessor: bool) -> None:
    lines = get_input(input_path)
    start_time = datetime.now()
    preprocessor = None
    if enable_preprocessor:
        preprocessor = Preprocessor(lines)
        try:
            lines = preprocessor.run()
        except PanicException as e:
            e.print()
            exit(1)
    try:
        spade_code = get_spade_code(lines, indent_size=4, debug=debug)
    except PanicException as e:
        eh = ExceptionHandler(preprocessor)
        e = eh.translate_panic_exception(e)
        e.print()
        exit(1)
    time_delta = (datetime.now() - start_time).total_seconds()
    save_output(output_path, spade_code)
    print(f'({time_delta}s) Your results are saved in the file "{output_path}" 😎')


if __name__ == '__main__':
    input_path, output_path, debug, enable_preprocessor = get_args()
    main(input_path, output_path, debug, enable_preprocessor)
