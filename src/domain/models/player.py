from .items.weapons import weapon, arm

class Player:
    def __init__(self):
        self._max_health = 200
        self._health = 200
        self.dexterity = 10
        self.strenght = 10
        self._current_weapon:weapon = arm()
        
    @property
    def pweapon(self) -> weapon:
        return self._current_weapon
        
    @pweapon.setter
    def pweapon(self, value:weapon) -> None:
        if issubclass(type(value), weapon):
            self._current_weapon = value
            
    @pweapon.deleter
    def pweapon(self) -> None:
        self._current_weapon = arm()
        
        
    @property
    def health(self) -> int:
        return self._health
    
    @health.setter
    def health(self, value) -> None:
        if value > self._max_health:
            self._health = self._max_health
        else:
            self._health = value
            
            
    @property
    def max_health(self) -> int:
        return self._max_health
    
    @max_health.setter
    def max_health(self, value) -> None:
        if value < self._health:
            diff = self._max_health - value
            self._health -= diff
            self._max_health = value
        else:
            self._max_health = value