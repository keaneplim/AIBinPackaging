import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.data_structures import Barang, Kontainer, State
from src.core.objective_function import calculate_objective, ObjectiveConfig
from src.core.initial_state import generate_ffd_state
from src.utils.file_parser import parse_problem

class TestCoreComponents(unittest.TestCase):

    def test_data_structures(self):
        # Mengecek fungsionalitas dasar dari dataclass Barang dan Kontainer
        barang = Barang(id="B01", ukuran=10, tipe="elektronik", rapuh=True)
        self.assertEqual(barang.id, "B01")
        self.assertEqual(barang.ukuran, 10)

        kontainer = Kontainer(id=1, kapasitas=100)
        self.assertEqual(kontainer.id, 1)
        self.assertEqual(kontainer.kapasitas, 100)
        self.assertEqual(kontainer.muatan_saat_ini, 0)
        
        kontainer.tambah_barang(barang)
        self.assertEqual(kontainer.muatan_saat_ini, 10)
        self.assertEqual(kontainer.sisa_kapasitas, 90)
        self.assertTrue(kontainer.bisa_tambah_barang(Barang('B02', 90)))
        self.assertFalse(kontainer.bisa_tambah_barang(Barang('B03', 91)))

    def test_file_parser(self):
        # Mengecek fungsi parse_problem dari file_parser
        file_path = 'src/data/problem_A.json'
        barang_list, kapasitas = parse_problem(file_path)

        self.assertEqual(kapasitas, 100)
        self.assertEqual(len(barang_list), 3)
        # Verifikasi barang pertama
        item1 = barang_list[0]
        self.assertEqual(item1.id, 'BRG001')
        self.assertEqual(item1.ukuran, 40)
        self.assertEqual(item1.tipe, 'elektronik')
        self.assertTrue(item1.rapuh)

    def test_ffd_state_generator(self):
        # Mengecek generator keadaan awal menggunakan heuristik First Fit Decreasing
        # Barang: B02(80), B01(30), B03(20)
        # FFD: C1=[B02, B03], C2=[B01]
        barang_list = [Barang('B01', 30), Barang('B02', 80), Barang('B03', 20)]
        state = generate_ffd_state(barang_list, kapasitas_kontainer=100)
        
        self.assertIsInstance(state, State)
        self.assertEqual(len(state.kontainer_list), 2)
        
        # Cek kontainer pertama
        c1 = state.kontainer_list[0]
        self.assertEqual(c1.muatan_saat_ini, 100)
        self.assertIn(Barang('B02', 80), c1.barang_di_dalam)
        self.assertIn(Barang('B03', 20), c1.barang_di_dalam)

        # Cek kontainer kedua
        c2 = state.kontainer_list[1]
        self.assertEqual(c2.muatan_saat_ini, 30)
        self.assertIn(Barang('B01', 30), c2.barang_di_dalam)

    def test_objective_function_base(self):
        # Mengecek komponen dasar (jumlah kontainer & kepadatan) dari fungsi objektif
        config = ObjectiveConfig()
        # State ideal: 2 kontainer penuh
        k1 = Kontainer(1, 100, [Barang('B01', 100)])
        k2 = Kontainer(2, 100, [Barang('B02', 100)])
        state_ideal = State([k1, k2])
        # Skor = 2 kontainer + 2 * (1 - 1^2) = 2.0
        self.assertAlmostEqual(calculate_objective(state_ideal, config), 2.0)

        # State dengan 1 kontainer setengah penuh
        k3 = Kontainer(1, 100, [Barang('B03', 50)])
        state_setengah = State([k3])
        # Skor = 1 kontainer + (1 - 0.5^2) = 1.75
        self.assertAlmostEqual(calculate_objective(state_setengah, config), 1.75)

    def test_objective_function_overfill(self):
        # Mengecek penalti kelebihan muatan
        config = ObjectiveConfig()
        k1 = Kontainer(1, 100, [Barang('B01', 101)])
        state_overfill = State([k1])
        # Skor harus > 1,000,000
        self.assertTrue(calculate_objective(state_overfill, config) >= 1_000_000)

    def test_objective_function_bonus_constraints(self):
        # Mengecek penalti untuk batasan bonus (rapuh & tidak kompatibel)
        # 1. Tes Penalti Barang Rapuh
        config_fragile = ObjectiveConfig(use_fragile_constraint=True, fragile_threshold=50)
        k_fragile = Kontainer(1, 100, [
            Barang('rapuh', 10, rapuh=True),
            Barang('berat', 51) # Melebihi threshold
        ])
        state_fragile = State([k_fragile])
        self.assertTrue(calculate_objective(state_fragile, config_fragile) >= 500_000)

        # 2. Tes Tanpa Penalti Barang Rapuh (di bawah threshold)
        k_fragile_ok = Kontainer(1, 100, [
            Barang('rapuh', 10, rapuh=True),
            Barang('ringan', 50) # Pas di threshold
        ])
        state_fragile_ok = State([k_fragile_ok])
        self.assertTrue(calculate_objective(state_fragile_ok, config_fragile) < 500_000)

        # 3. Tes Penalti Barang Tidak Kompatibel
        config_incompatible = ObjectiveConfig(use_incompatible_constraint=True)
        k_incompatible = Kontainer(1, 100, [
            Barang('makanan1', 10, tipe='makanan'),
            Barang('kimia1', 10, tipe='kimia')
        ])
        state_incompatible = State([k_incompatible])
        self.assertTrue(calculate_objective(state_incompatible, config_incompatible) >= 500_000)

        # 4. Tes Tanpa Penalti (tipe sama)
        k_incompatible_ok = Kontainer(1, 100, [
            Barang('makanan1', 10, tipe='makanan'),
            Barang('makanan2', 10, tipe='makanan')
        ])
        state_incompatible_ok = State([k_incompatible_ok])
        self.assertTrue(calculate_objective(state_incompatible_ok, config_incompatible) < 500_000)

if __name__ == '__main__':
    unittest.main()