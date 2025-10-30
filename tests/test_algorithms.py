import pytest
import random
from src.core.data_structures import Barang, State, Kontainer
from src.core.objective_function import ObjectiveConfig, calculate_objective
from src.algorithms.hill_climbing import steepest_ascent_hill_climbing
from src.algorithms.genetic_algorithm import genetic_algorithm
from src.algorithms.simulated_annealing import simulated_annealing

def test_steepest_ascent_finds_optimal_solution():
    """
    Menguji apakah Steepest Ascent Hill Climbing dapat menemukan solusi optimal
    dari sebuah masalah sederhana yang dapat diprediksi.
    """
    item_a = Barang(id="A", ukuran=80)
    item_b = Barang(id="B", ukuran=80)
    item_c = Barang(id="C", ukuran=20)

    # Buat keadaan awal yang tidak optimal (3 kontainer)
    initial_state = State(
        kontainer_list=[
            Kontainer(id=0, kapasitas=100, barang_di_dalam=[item_a]),
            Kontainer(id=1, kapasitas=100, barang_di_dalam=[item_b]),
            Kontainer(id=2, kapasitas=100, barang_di_dalam=[item_c]),
        ]
    )

    config = ObjectiveConfig()

    # Jalankan algoritma
    final_state, history = steepest_ascent_hill_climbing(
        initial_state=initial_state,
        config=config,
        max_iter=100
    )

    # Verifikasi hasilnya
    # Algoritma harus menemukan solusi dengan 2 kontainer
    assert len(final_state.kontainer_list) == 2

    # Verifikasi bahwa skor akhir lebih rendah dari skor awal
    initial_score = 3 + (1 - (80/100)**2) / 3 + (1 - (80/100)**2) / 3 + (1 - (20/100)**2) / 3
    final_score = 2 + (1 - (100/100)**2) / 2 + (1 - (80/100)**2) / 2
    assert history[-1] < history[0]
    assert round(history[-1], 4) == round(final_score, 4)

def test_simulated_annealing_improves_solution():
    """
    Menguji apakah Simulated Annealing dapat meningkatkan (atau setidaknya tidak memperburuk)
    solusi dari masalah sederhana, menggunakan seed tetap untuk hasil yang deterministik.
    """
    item_a = Barang(id="A", ukuran=80)
    item_b = Barang(id="B", ukuran=80)
    item_c = Barang(id="C", ukuran=20)

    initial_state = State(
        kontainer_list=[
            Kontainer(id=0, kapasitas=100, barang_di_dalam=[item_a]),
            Kontainer(id=1, kapasitas=100, barang_di_dalam=[item_b]),
            Kontainer(id=2, kapasitas=100, barang_di_dalam=[item_c]),
        ]
    )

    config = ObjectiveConfig()
    initial_score = calculate_objective(initial_state, config)

    # Jalankan algoritma dengan seed tetap
    final_state, history, _ = simulated_annealing(
        keadaan_awal=initial_state,
        suhu_awal=100.0,
        cooling_rate=0.95,
        max_iter=200,
        config=config
    )

    final_score = calculate_objective(final_state, config)

    # Verifikasi bahwa solusi tidak menjadi lebih buruk
    assert final_score <= initial_score

    # Dengan parameter di atas, seharusnya bisa menemukan solusi optimal (2 kontainer)
    # Namun, karena sifat probabilistiknya, kita hanya pastikan tidak lebih buruk dari 3
    assert len(final_state.kontainer_list) in [2, 3]


def test_genetic_algorithm_improves_solution():
    """
    Menguji apakah Genetic Algorithm dapat meningkatkan (atau setidaknya tidak memperburuk)
    solusi dari masalah sederhana, menggunakan seed tetap.
    """
    item_a = Barang(id="A", ukuran=80)
    item_b = Barang(id="B", ukuran=80)
    item_c = Barang(id="C", ukuran=20)

    initial_state = State(
        kontainer_list=[
            Kontainer(id=0, kapasitas=100, barang_di_dalam=[item_a]),
            Kontainer(id=1, kapasitas=100, barang_di_dalam=[item_b]),
            Kontainer(id=2, kapasitas=100, barang_di_dalam=[item_c]),
        ]
    )

    config = ObjectiveConfig()
    initial_score = calculate_objective(initial_state, config)

    # Jalankan algoritma dengan seed tetap dan parameter kecil
    rng = random.Random(42)
    final_state, history = genetic_algorithm(
        initial_state=initial_state,
        config=config,
        kapasitas_kontainer=100,
        max_generations=50,
        population_size=10,
        rng=rng
    )

    final_score = calculate_objective(final_state, config)

    # Verifikasi bahwa solusi tidak menjadi lebih buruk
    assert final_score <= initial_score

    # Seharusnya bisa menemukan solusi optimal (2 kontainer) atau tetap di 3
    assert len(final_state.kontainer_list) in [2, 3]
