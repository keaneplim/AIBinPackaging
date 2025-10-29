import unittest
from .data_structures import Item, Container, State
from .objective_function import calculate_objective
from .initial_state import generate_initial_state

class TestPhase1(unittest.TestCase):

    def test_data_structures(self):
        """Mengecek fungsi dasar dari class Item dan Container."""
        item = Item(id="I01", size=10, fragile=True, item_type="electronics")
        self.assertEqual(item.id, "I01")
        self.assertEqual(item.size, 10)
        self.assertTrue(item.fragile)
        self.assertEqual(item.item_type, "electronics")

        container = Container(capacity=100)
        self.assertEqual(container.capacity, 100)
        self.assertEqual(container.current_load(), 0)
        container.add_item(item)
        self.assertEqual(container.current_load(), 10)
        self.assertEqual(container.remaining_capacity(), 90)

    def test_initial_state_generator(self):
        """Mengecek generator state awal menggunakan First Fit heuristic."""
        items = [Item("I01", 50), Item("I02", 50), Item("I03", 50)]
        state = generate_initial_state(items, container_capacity=100)
        # Harus menggunakan 2 container: [I01, I02] dan [I03]
        self.assertEqual(len(state), 2)
        self.assertEqual(state[0].current_load(), 100)
        self.assertEqual(state[1].current_load(), 50)

    def test_objective_function_mandatory(self):
        """Mengecek bagian mandatory dari fungsi objective."""
        # State ideal: 2 container digunakan, tanpa penalty
        c1 = Container(100); c1.add_item(Item("I01", 100))
        c2 = Container(100); c2.add_item(Item("I02", 100))
        state_perfect = [c1, c2]
        self.assertEqual(calculate_objective(state_perfect), 2)

        # State overflow: 1 container, tapi overflow
        c_over = Container(100); c_over.add_item(Item("I01", 101))
        state_overfilled = [c_over]
        # Skor harus 1 (untuk container) + penalty besar
        self.assertTrue(calculate_objective(state_overfilled) > 1000000)

    def test_objective_function_bonus(self):
        """Tests the bonus parts of the objective function."""
        # Penalty untuk constraint violations bonus: Item yang mudah pecah
        c_fragile = Container(100)
        c_fragile.add_item(Item("fragile_item", 10, fragile=True))
        c_fragile.add_item(Item("heavy_item", 51)) # Exceeds threshold of 50
        state_fragile = [c_fragile]
        self.assertTrue(calculate_objective(state_fragile) > 500000)

        # Penalty untuk constraint violations bonus: Item yang tidak kompatibel
        c_incompatible = Container(100)
        c_incompatible.add_item(Item("food_item", 10, item_type="food"))
        c_incompatible.add_item(Item("chem_item", 10, item_type="chemical"))
        state_incompatible = [c_incompatible]
        self.assertTrue(calculate_objective(state_incompatible) > 500000)

        # State ideal dengan constraint violations bonus
        c_valid_bonus = Container(100)
        c_valid_bonus.add_item(Item("fragile_item", 10, fragile=True))
        c_valid_bonus.add_item(Item("light_item", 50)) # Tidak melebihi threshold
        state_valid_bonus = [c_valid_bonus]
        self.assertEqual(calculate_objective(state_valid_bonus), 1)

if __name__ == '__main__':
    unittest.main()
