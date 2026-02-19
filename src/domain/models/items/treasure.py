from BasicItem import item

class treasure(item):
    def __init__(self, value: int):
        super().__init__(name="treasure", type="treasure")
        self.value: int = value