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
    """Merepresentasikan sebuah container yang mengandung item"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def current_load(self):
        """Menghitung jumlah ukuran semua item dalam container"""
        return sum(item.size for item in self.items)

    def remaining_capacity(self):
        """Menghitung sisa kapasitas container"""
        return self.capacity - self.current_load()

    def add_item(self, item):
        """Menambahkan item ke container. Tidak memeriksa kapasitas."""
        self.items.append(item)

    def __repr__(self):
        return f"Container(load={self.current_load()}/{self.capacity}, items={len(self.items)})"

State = list[Container]
