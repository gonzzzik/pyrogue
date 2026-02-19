from abc import ABC

class item(ABC):
    def __init__(self, name: str, type: str):
        self.type:str = type
        self.name:str = name