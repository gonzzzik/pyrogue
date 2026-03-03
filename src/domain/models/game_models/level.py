from room import Room
from typing import List, Tuple, Optional
from random import randint

class Level:
    def __init__(self, uuid: int) -> None:
        self.uuid = uuid
        self.rooms: List[Room] = []
        self.map: List[List[Room]] = []
        self.corridors: List[List[Tuple[int, int]]] = []
        self.global_map: List[List[str]] = []
        self.start_room = randint(0,8)