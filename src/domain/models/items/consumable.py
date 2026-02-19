from BasicItem import  item, ABC

class consumable(item, ABC): 
    def __init__(self, name:str, restore:int, subtype: str):
        super().__init__(name, type="consumable")
        self.subtype: str = subtype
        self.health_restore: int = restore
        
        
class food(consumable):
    def __init__(self, name: str, restore: int):
        super().__init__(name, restore, subtype="food")
        
class apple(food): #for example
    def __init__(self):
        super().__init__("apple", 10)
        

class scroll(consumable):
    def __init__(self, name, restore: int, mhealth_bonus:int, dext_bonus:int, strength_bonus:int):
        super().__init__(name, restore, subtype="scroll")
        self.max_health_bonus:int = mhealth_bonus
        self.dexterity_bonus:int = dext_bonus
        self.strength_bonus:int = strength_bonus
        
class elder_hero(scroll): # for example
    def __init__(self):
        super().__init__("Elder Hero Scroll", 10, 0, 3, 15)
        
        
class elixir(consumable):
    def __init__(self, name:str, restore: int, mhealth_bonus:int, dext_bonus:int, strength_bonus:int, time:int):
        super().__init__(name, restore, subtype="elixir")
        self.max_health_bonus:int = mhealth_bonus
        self.dexterity_bonus:int = dext_bonus
        self.strength_bonus:int = strength_bonus
        self.time_action:int = time
        
class gaala(elixir): # for example
    def __init__(self):
        super().__init__("Gaal's Elixir", 20, 5, 15, 15, 20)