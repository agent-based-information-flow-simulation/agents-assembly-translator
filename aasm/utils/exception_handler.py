from __future__ import annotations
import re
from aasm.preprocessor.preprocessor import Preprocessor
from aasm.utils.exception import PanicException


class ExceptionHandler:
    def __init__(self, preprocessor: Preprocessor):
        self.preprocessor = preprocessor

    def _get_line_number(self, place: str) -> int:
        try:
            return int(re.search(r'\d+', place).group())
        except AttributeError:
            return -1

    def translate_panic_exception(self, exception: PanicException) -> PanicException:
        if self.preprocessor is not None:
            line = self._get_line_number(exception.place)
            if line != -1:
                line = self.preprocessor.get_original_line_number(line)
                makro = self.preprocessor.get_makro_name(line-1)
                if makro != "":
                    exception.place = f"Error in makro {makro}:"
                else:
                    exception.place = f"Error in line {line}:"
        return exception
