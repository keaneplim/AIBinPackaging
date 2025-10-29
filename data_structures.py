class Item:
    """Represents an item with its ID, size, and optional constraints."""
    def __init__(self, id, size, fragile=False, item_type=None):
        self.id = id
        self.size = size
        self.fragile = fragile
        self.item_type = item_type

    def __repr__(self):
        return f"Item({self.id}, size={self.size})"

class Container:
    """Represents a container that holds items."""
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def current_load(self):
        """Calculates the sum of the sizes of all items in the container."""
        return sum(item.size for item in self.items)

    def remaining_capacity(self):
        """Calculates the remaining capacity of the container."""
        return self.capacity - self.current_load()

    def add_item(self, item):
        """Adds an item to the container. Does not check for capacity."""
        self.items.append(item)

    def __repr__(self):
        return f"Container(load={self.current_load()}/{self.capacity}, items={len(self.items)})"

# A State is a list of Container objects
State = list[Container]
