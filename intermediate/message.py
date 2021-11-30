class Message:
    def __init__(self, name: str):
        self.name: str = name
        
    def print(self) -> None:
        print(f'Message {self.name}')
