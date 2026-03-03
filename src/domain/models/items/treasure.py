from BasicItem import item

class treasure(item):
    def __init__(self, value: int):
        super().__init__(name="treasure", type="treasure")
        self.char = '֎'
        self.color_out = f'\033[1;33m{self.char}\033[0m'
        self.value: int = value