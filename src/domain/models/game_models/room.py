import random
from typing import List, Tuple, Optional

class Room:
    def __init__(self) -> None:
        self.top_left: Tuple[int, int] = (0, 0)  # (x, y)
        self.bot_right: Tuple[int, int] = (0, 0)  # (x, y)
        self.doors: List[Tuple[int, int]] = []
        self.grid_x: int = 0  # which cell in 3x3 grid
        self.grid_y: int = 0
        self.sector: int = -1  # unique sector id
        self.connections: List[Optional['Room']] = [None, None, None, None]  # [up, right, down, left]
