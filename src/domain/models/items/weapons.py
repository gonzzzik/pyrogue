from .BasicItem import item

class weapon(item): # maybe do it ABC if weapon will be in 
    def __init__(self, name: str, bonus: int):
        super().__init__(name, type="weapon")
        self.char = '༒'
        self.color_out = f'\033[1;34m{self.char}\033[0m'
        self.strenght_bonus: int = bonus
        
        
class arm(weapon):
    def __init__(self):
        super().__init__(name="arm", bonus=0)


class whole_sword(weapon):
    def __init__(self):
        super().__init__(name="whole_sword", bonus=3)
        
        
# Или отказаться от этой идеи...