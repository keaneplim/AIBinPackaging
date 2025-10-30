import random
from typing import List, Tuple, Optional

from src.core.data_structures import State, Barang
from src.core.objective_function import calculate_objective, ObjectiveConfig
from src.algorithms.utils.moves import get_all_neighbors
from src.core.initial_state import generate_random_state
from src.utils.state_utils import extract_all_items, resolve_capacity

def steepest_ascent_hill_climbing(
    initial_state: State,
    config: ObjectiveConfig,
    max_iter: int
) -> Tuple[State, List[float]]:
    """
    Mengimplementasikan Steepest Ascent Hill Climbing.
    
    Pada setiap iterasi, algoritma ini mengevaluasi semua keadaan tetangga dan
    memilih yang memberikan penurunan skor terbesar (paling curam). Pencarian
    berhenti jika tidak ada tetangga yang lebih baik atau iterasi maksimum tercapai.

    Args:
        initial_state: Keadaan awal untuk memulai pencarian.
        config: Konfigurasi untuk fungsi objektif.
        max_iter: Jumlah iterasi maksimum.

    Returns:
        Tuple berisi (keadaan terbaik yang ditemukan, histori skor).
    """
    current_state = initial_state.salin()
    current_score = calculate_objective(current_state, config)
    score_history = [current_score]

    for _ in range(max_iter):
        neighbors = get_all_neighbors(current_state)
        if not neighbors:
            break

        neighbor_scores = [calculate_objective(n, config) for n in neighbors]
        
        best_neighbor_score = min(neighbor_scores)
        best_neighbor_index = neighbor_scores.index(best_neighbor_score)
        best_neighbor = neighbors[best_neighbor_index]

        if best_neighbor_score < current_score:
            current_state = best_neighbor
            current_score = best_neighbor_score
            score_history.append(current_score)
        else:
            break
            
    return current_state, score_history

def stochastic_hill_climbing(
    initial_state: State,
    config: ObjectiveConfig,
    max_iter: int
) -> Tuple[State, List[float]]:
    """
    Mengimplementasikan Stochastic Hill Climbing.

    Pada setiap iterasi, algoritma ini menemukan semua keadaan tetangga yang
    memiliki skor lebih baik daripada keadaan saat ini, lalu memilih salah satu
    dari mereka secara acak untuk menjadi keadaan berikutnya.

    Args:
        initial_state: Keadaan awal untuk memulai pencarian.
        config: Konfigurasi untuk fungsi objektif.
        max_iter: Jumlah iterasi maksimum.

    Returns:
        Tuple berisi (keadaan terbaik yang ditemukan, histori skor).
    """
    current_state = initial_state.salin()
    current_score = calculate_objective(current_state, config)
    score_history = [current_score]

    for _ in range(max_iter):
        neighbors = get_all_neighbors(current_state)
        if not neighbors:
            break

        better_neighbors = []
        for neighbor in neighbors:
            neighbor_score = calculate_objective(neighbor, config)
            if neighbor_score < current_score:
                better_neighbors.append((neighbor, neighbor_score))

        if better_neighbors:
            chosen_neighbor, chosen_score = random.choice(better_neighbors)
            current_state = chosen_neighbor
            current_score = chosen_score
            score_history.append(current_score)
        else:
            break
            
    return current_state, score_history

def hill_climbing_with_sideways_moves(
    initial_state: State,
    config: ObjectiveConfig,
    max_iter: int,
    max_sideways_moves: int
) -> Tuple[State, List[float]]:
    """
    Mengimplementasikan Hill Climbing yang mengizinkan sideways moves.

    Varian ini mirip dengan Steepest Ascent, tetapi jika tidak ada tetangga yang
    lebih baik, ia akan menerima tetangga dengan skor yang sama. Ini berguna
    untuk melintasi 'plateau' dalam lanskap pencarian. Jumlah sideways moves
    dibatasi oleh `max_sideways_moves`.

    Args:
        initial_state: Keadaan awal untuk memulai pencarian.
        config: Konfigurasi untuk fungsi objektif.
        max_iter: Jumlah iterasi maksimum.
        max_sideways_moves: Jumlah maksimum gerakan menyamping yang diizinkan secara berurutan.

    Returns:
        Tuple berisi (keadaan terbaik yang ditemukan, histori skor).
    """
    current_state = initial_state.salin()
    current_score = calculate_objective(current_state, config)
    score_history = [current_score]
    sideways_moves_count = 0

    for _ in range(max_iter):
        neighbors = get_all_neighbors(current_state)
        if not neighbors:
            break

        neighbor_scores = [calculate_objective(n, config) for n in neighbors]
        
        best_neighbor_score = min(neighbor_scores)
        best_neighbor_index = neighbor_scores.index(best_neighbor_score)
        best_neighbor = neighbors[best_neighbor_index]

        if best_neighbor_score < current_score:
            current_state = best_neighbor
            current_score = best_neighbor_score
            score_history.append(current_score)
            sideways_moves_count = 0
        elif best_neighbor_score == current_score and sideways_moves_count < max_sideways_moves:
            current_state = best_neighbor
            sideways_moves_count += 1
        else:
            break
            
    return current_state, score_history

def random_restart_hill_climbing(
    initial_state: State,
    config: ObjectiveConfig,
    num_restarts: int,
    max_iter_per_restart: int,
    rng: Optional[random.Random] = None,
    kapasitas_kontainer: Optional[int] = None
) -> Tuple[State, List[float]]:
    """
    Mengimplementasikan Random-Restart Hill Climbing.

    Algoritma ini menjalankan Steepest Ascent Hill Climbing beberapa kali (`num_restarts`).
    Setiap restart dimulai dari sebuah keadaan awal yang dibuat secara acak.
    Solusi terbaik yang ditemukan dari semua restart akan menjadi hasil akhir.

    Args:
        initial_state: Digunakan untuk mengekstrak daftar barang dan kapasitas.
        config: Konfigurasi untuk fungsi objektif.
        num_restarts: Berapa kali pencarian akan diulang dari awal.
        max_iter_per_restart: Jumlah iterasi maksimum untuk setiap proses Hill Climbing.
        rng: Generator angka acak untuk pembuatan state.
        kapasitas_kontainer: Kapasitas kontainer (opsional).

    Returns:
        Tuple berisi (keadaan terbaik yang ditemukan, histori skor dari pencarian terbaik).
    """
    rng = rng or random.Random()
    best_state_overall = initial_state.salin()
    best_score_overall = calculate_objective(best_state_overall, config)
    best_history = [best_score_overall]

    all_items = extract_all_items(initial_state)
    if not all_items:
        return best_state_overall, best_history
        
    kapasitas = resolve_capacity(initial_state, kapasitas_kontainer)

    for i in range(num_restarts):
        print(f"  Restarting search ({i + 1}/{num_restarts})...")
        random_start_state = generate_random_state(all_items, kapasitas, rng)
        
        current_best_state, current_history = steepest_ascent_hill_climbing(
            initial_state=random_start_state,
            config=config,
            max_iter=max_iter_per_restart
        )
        current_best_score = current_history[-1]

        if current_best_score < best_score_overall:
            best_score_overall = current_best_score
            best_state_overall = current_best_state
            best_history = current_history

    return best_state_overall, best_history