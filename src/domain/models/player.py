from items.weapons import weapon, arm

class player:
    def __init__(self):
        self.max_health = 200
        self.health = 200
        self.dexterity = 10
        self.strenght = 10
        self.current_wearpon:weapon = arm()