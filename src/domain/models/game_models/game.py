from .level import Level
from ..player import Player
from ..backpack import Backpack
from ...services.generate.level_generator_servise import LevelGenerator
from functools import singledispatch


class Game:    
    lvl: Level
    hero: Player
    inventory: Backpack    
    
    @singledispatch
    def __init__(self, size_x: int, size_y: int) -> None:
        # Create level using LevelGenerator instance
        generator = LevelGenerator()
        self.lvl: Level = generator.generate(size_x, size_y)
        self.hero: Player = Player()
        self.inventory: Backpack = Backpack()
      
      
    @__init__.register  
    def _(self, hero:Player, lvl: Level, inventory: Backpack) -> None:
        self.lvl: Level = lvl
        self.hero: Player = hero
        self.inventory: Backpack = inventory