from .room import Room
from typing import List, Tuple, Optional
from random import randint

class Level:
    def __init__(self, uuid: int) -> None:
        self.uuid = uuid
        self.rooms: List[Room] = []
        self.corridors: List[Tuple[int, int]] = []
        self.global_map: List[List[str]] = []
        self.start_room = randint(0, len(self.rooms) - 1) if self.rooms else 0