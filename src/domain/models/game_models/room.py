import random

class Room:
    def __init__(self) -> None:
        self.room_map = [[]]
        self.doors = []
        self.pos_x = 0
        self.pos_y = 0
        self.size_x = 0
        self.size_y = 0