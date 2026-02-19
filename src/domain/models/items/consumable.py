from BasicItem import  item, ABC

class consumable(item, ABC): 
    def __init__(self, name:str, restore:int):
        super().__init__(name, type="consumable")
        # Возможно будет необходимо прописать subtype для food, scroll... и name оставить в них 
        self.health_restore: int = restore
        
        
class food(consumable):
    def __init__(self, name: str, restore: int):
        super().__init__(name="food", restore=restore)
        

class scroll(consumable):
    def __init__(self, restore: int, mhealth_bonus:int, dext_bonus:int, strength_bonus:int):
        super().__init__(name="scroll", restore=restore)
        self.max_health_bonus:int = mhealth_bonus
        self.dexterity_bonus:int = dext_bonus
        self.strength_bonus:int = strength_bonus
        
        
class elixir(consumable):
    def __init__(self, restore: int, mhealth_bonus:int, dext_bonus:int, strength_bonus:int, time:int):
        super().__init__(name="elixir", restore=restore)
        self.max_health_bonus:int = mhealth_bonus
        self.dexterity_bonus:int = dext_bonus
        self.strength_bonus:int = strength_bonus
        self.time_action:int = time