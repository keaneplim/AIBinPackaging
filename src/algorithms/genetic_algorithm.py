from __future__ import annotations

import random
from typing import Dict, List, Optional, Sequence, Tuple

from src.core.data_structures import Barang, Kontainer, State
from src.core.objective_function import ObjectiveConfig, calculate_objective


def genetic_algorithm(
    initial_state: State,
    config: ObjectiveConfig,
    *,
    kapasitas_kontainer: Optional[int] = None,
    max_generations: int = 100,
    population_size: int = 30,
    crossover_rate: float = 0.8,
    mutation_rate: float = 0.2,
    tournament_size: int = 3,
    elitism: int = 1,
    rng: Optional[random.Random] = None,
) -> Tuple[State, List[float]]:
    """
    Menjalankan Genetic Algorithm untuk masalah Bin Packing.

    Args:
        initial_state: State awal yang digunakan sebagai baseline populasi.
        config: Konfigurasi fungsi objektif.
        kapasitas_kontainer: Kapasitas kontainer (opsional, akan diambil dari state bila tidak disediakan).
        max_generations: Jumlah generasi yang disimulasikan.
        population_size: Jumlah individu dalam populasi.
        crossover_rate: Peluang crossover antar pasangan orang tua.
        mutation_rate: Peluang mutasi diterapkan pada individu.
        tournament_size: Ukuran turnamen untuk seleksi.
        elitism: Jumlah individu terbaik yang dibawa langsung ke generasi berikutnya.
        rng: Random generator agar eksperimen dapat direplikasi.

    Returns:
        Pasangan (State terbaik, histori skor terbaik per generasi).
    """
    if population_size < 2:
        raise ValueError("population_size minimal bernilai 2 agar GA dapat bekerja.")
    if max_generations < 0:
        raise ValueError("max_generations tidak boleh negatif.")
    if tournament_size < 1:
        raise ValueError("tournament_size minimal bernilai 1.")
    if elitism < 0:
        raise ValueError("elitism tidak boleh negatif.")

    rng = rng or random.Random()
    items = _extract_all_items(initial_state)
    if not items:
        base_score = calculate_objective(initial_state, config)
        return initial_state.salin(), [base_score]

    kapasitas = _resolve_capacity(initial_state, kapasitas_kontainer)

    population: List[State] = [initial_state.salin()]
    while len(population) < population_size:
        population.append(_generate_random_state(items, kapasitas, rng))

    scores = [calculate_objective(individu, config) for individu in population]
    best_idx = min(range(len(population)), key=lambda idx: scores[idx])
    best_state = population[best_idx].salin()
    best_score = scores[best_idx]
    history: List[float] = [best_score]

    for _ in range(max_generations):
        new_population: List[State] = []
        if elitism > 0:
            elite_indices = _top_indices(scores, elitism)
            for idx in elite_indices:
                new_population.append(population[idx].salin())

        while len(new_population) < population_size:
            parent1 = _tournament_selection(population, scores, tournament_size, rng)
            parent2 = _tournament_selection(population, scores, tournament_size, rng)

            if rng.random() < crossover_rate:
                child1, child2 = _crossover(parent1, parent2, items, kapasitas, rng)
            else:
                child1, child2 = parent1.salin(), parent2.salin()

            if rng.random() < mutation_rate:
                _mutate_state(child1, kapasitas, rng)
            if rng.random() < mutation_rate:
                _mutate_state(child2, kapasitas, rng)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population
        scores = [calculate_objective(individu, config) for individu in population]
        generation_best_idx = min(range(len(population)), key=lambda idx: scores[idx])
        generation_best_score = scores[generation_best_idx]

        if generation_best_score < best_score:
            best_score = generation_best_score
            best_state = population[generation_best_idx].salin()

        history.append(best_score)

    return best_state, history


def _extract_all_items(state: State) -> List[Barang]:
    # Mengumpulkan seluruh barang dari kontainer maupun yang belum dialokasikan.
    items: List[Barang] = []
    seen: set[str] = set()
    for kontainer in state.kontainer_list:
        for barang in kontainer.barang_di_dalam:
            if barang.id not in seen:
                seen.add(barang.id)
                items.append(barang)
    for barang in state.barang_belum_dialokasi:
        if barang.id not in seen:
            seen.add(barang.id)
            items.append(barang)
    return items


def _resolve_capacity(state: State, kapasitas_override: Optional[int]) -> int:
    if kapasitas_override is not None:
        return kapasitas_override
    for kontainer in state.kontainer_list:
        return kontainer.kapasitas
    raise ValueError("kapasitas_kontainer harus diberikan jika state awal tidak memiliki kontainer.")


def _generate_random_state(items: Sequence[Barang], kapasitas: int, rng: random.Random) -> State:
    kontainer_list: List[Kontainer] = []
    for barang in rng.sample(list(items), len(items)):
        if not kontainer_list:
            kontainer_list.append(Kontainer(id=0, kapasitas=kapasitas, barang_di_dalam=[barang]))
            continue
        kandidat = rng.sample(kontainer_list, len(kontainer_list))
        ditempatkan = False
        for kontainer in kandidat:
            if kontainer.bisa_tambah_barang(barang):
                kontainer.barang_di_dalam.append(barang)
                ditempatkan = True
                break
        if not ditempatkan:
            kontainer_baru = Kontainer(id=len(kontainer_list), kapasitas=kapasitas, barang_di_dalam=[barang])
            kontainer_list.append(kontainer_baru)
    _renumber_container_ids(kontainer_list)
    return State(kontainer_list=kontainer_list, barang_belum_dialokasi=[])


def _tournament_selection(
    population: Sequence[State],
    scores: Sequence[float],
    tournament_size: int,
    rng: random.Random,
) -> State:
    size = min(tournament_size, len(population))
    kandidat_idx = rng.sample(range(len(population)), size)
    best_idx = min(kandidat_idx, key=lambda idx: scores[idx])
    return population[best_idx]


def _crossover(
    parent1: State,
    parent2: State,
    items: Sequence[Barang],
    kapasitas: int,
    rng: random.Random,
) -> Tuple[State, State]:
    if len(items) < 2:
        return parent1.salin(), parent2.salin()

    assignment1 = _item_assignment(parent1)
    assignment2 = _item_assignment(parent2)
    cut_point = rng.randint(1, len(items) - 1)

    child1_map: Dict[str, Optional[int]] = {}
    child2_map: Dict[str, Optional[int]] = {}
    for idx, barang in enumerate(items):
        if idx < cut_point:
            child1_map[barang.id] = assignment1.get(barang.id)
            child2_map[barang.id] = assignment2.get(barang.id)
        else:
            child1_map[barang.id] = assignment2.get(barang.id)
            child2_map[barang.id] = assignment1.get(barang.id)

    return (
        _build_state_from_assignment(child1_map, items, kapasitas),
        _build_state_from_assignment(child2_map, items, kapasitas),
    )


def _item_assignment(state: State) -> Dict[str, Optional[int]]:
    assignment: Dict[str, Optional[int]] = {}
    for kontainer in state.kontainer_list:
        for barang in kontainer.barang_di_dalam:
            assignment[barang.id] = kontainer.id
    for barang in state.barang_belum_dialokasi:
        assignment[barang.id] = None
    return assignment


def _build_state_from_assignment(
    assignment_map: Dict[str, Optional[int]],
    items: Sequence[Barang],
    kapasitas: int,
) -> State:
    grouped: Dict[Optional[int], List[Barang]] = {}
    for barang in items:
        key = assignment_map.get(barang.id)
        grouped.setdefault(key, []).append(barang)

    kontainer_list: List[Kontainer] = []
    for _, group_items in sorted(grouped.items(), key=lambda item: str(item[0])):
        if not group_items:
            continue
        kontainer = Kontainer(id=len(kontainer_list), kapasitas=kapasitas, barang_di_dalam=[])
        for barang in group_items:
            if kontainer.bisa_tambah_barang(barang):
                kontainer.barang_di_dalam.append(barang)
            else:
                kontainer_list.append(kontainer)
                kontainer = Kontainer(id=len(kontainer_list), kapasitas=kapasitas, barang_di_dalam=[barang])
        kontainer_list.append(kontainer)

    _renumber_container_ids(kontainer_list)
    return State(kontainer_list=kontainer_list, barang_belum_dialokasi=[])


def _mutate_state(state: State, kapasitas: int, rng: random.Random) -> None:
    if not state.kontainer_list:
        return

    operasi_pindah = rng.random() < 0.5

    if operasi_pindah:
        kontainer_dengan_barang = [k for k in state.kontainer_list if k.barang_di_dalam]
        if not kontainer_dengan_barang:
            return
        sumber = rng.choice(kontainer_dengan_barang)
        barang = rng.choice(sumber.barang_di_dalam)
        sumber.barang_di_dalam.remove(barang)

        kandidat = [k for k in state.kontainer_list if k is not sumber and k.bisa_tambah_barang(barang)]
        if kandidat:
            tujuan = rng.choice(kandidat)
            tujuan.barang_di_dalam.append(barang)
        else:
            kontainer_baru = Kontainer(id=len(state.kontainer_list), kapasitas=kapasitas, barang_di_dalam=[barang])
            state.kontainer_list.append(kontainer_baru)

        if not sumber.barang_di_dalam:
            state.kontainer_list.remove(sumber)
    else:
        if len(state.kontainer_list) < 2:
            return
        kontainer_dengan_barang = [k for k in state.kontainer_list if k.barang_di_dalam]
        if len(kontainer_dengan_barang) < 2:
            return
        c1, c2 = rng.sample(kontainer_dengan_barang, 2)
        b1 = rng.choice(c1.barang_di_dalam)
        b2 = rng.choice(c2.barang_di_dalam)
        muatan1 = c1.muatan_saat_ini - b1.ukuran + b2.ukuran
        muatan2 = c2.muatan_saat_ini - b2.ukuran + b1.ukuran
        if muatan1 <= kapasitas and muatan2 <= kapasitas:
            c1.barang_di_dalam.remove(b1)
            c2.barang_di_dalam.remove(b2)
            c1.barang_di_dalam.append(b2)
            c2.barang_di_dalam.append(b1)

    _remove_empty_and_renumber(state)


def _remove_empty_and_renumber(state: State) -> None:
    state.kontainer_list = [k for k in state.kontainer_list if k.barang_di_dalam]
    _renumber_container_ids(state.kontainer_list)


def _renumber_container_ids(kontainer_list: List[Kontainer]) -> None:
    for idx, kontainer in enumerate(kontainer_list):
        kontainer.id = idx


def _top_indices(scores: Sequence[float], jumlah: int) -> List[int]:
    jumlah = min(jumlah, len(scores))
    return sorted(range(len(scores)), key=lambda idx: scores[idx])[:jumlah]
