from items.consumable import food, scroll, elixir
from items.treasure import treasure
from items.weapons import weapon
from items.BasicItem import item


class Backpack:
    
    MAX_SLOTS = 9
    
    def __init__(self):
        self.food_list: list[food] = []
        self.scroll_list: list[scroll] = []
        self.elixir_list: list[elixir] = []
        self.weapon_list: list[weapon] = []
        self.treasure_list: list[treasure] = []
        
    
    def add_item(self, it: item):
        slots = {
            food: self.food_list,
            scroll: self.scroll_list,
            elixir: self.elixir_list,
            weapon: self.weapon_list,
            treasure: self.treasure_list
        }
        
        for item_type, slot_list in slots.items():
            if isinstance(it, item_type) and len(slot_list) < self.MAX_SLOTS:
                slot_list.append(it)
                return True
        
        return False