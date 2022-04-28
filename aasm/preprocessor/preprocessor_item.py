class PreprocessorItem:
    def __init__(self, signature: str):
        self.signature = signature

    def expand(self):
        raise NotImplementedError

    def add_definition(self, definition):
        raise NotImplementedError
