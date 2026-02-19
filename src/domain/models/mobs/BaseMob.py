class BaseMob:
    def __init__(self, health: int, dexterity: int, strenght: int, hostility: int, type: str):
        self.health = health
        self.dexterity = dexterity
        self.strenght = strenght
        self.hostility = hostility
        self.type = type
        
    # Расчёт хар-к в детях брать по некой формуле (позже выдумаю) из богатства и уровня
    # по типу base * (score / 100) * lvl + 1
    # взять эти параметры в конструктор и от них высчитывать
    # Возможно занести в базовый класс ( для просчёта всем )