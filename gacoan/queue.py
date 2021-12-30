class Queue:
    """Custom list class"""

    def __init__(self) -> None:
        self.list = []

    def add(self, name: int) -> None:
        """Add item if the item does not exist"""
        if name not in self.list:
            self.list.append(name)

    def done(self, name: int) -> None:
        """Remove item if exist"""
        if name in self.list:
            self.list.remove(name)
