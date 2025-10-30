
import argparse
import random
import time
import csv
import os
from datetime import datetime
from typing import List, Optional

from src.core.data_structures import State
from src.core.initial_state import generate_ffd_state, generate_random_state
from src.core.objective_function import ObjectiveConfig, calculate_objective
from src.utils.file_parser import parse_problem
from src.algorithms.simulated_annealing import simulated_annealing
from src.algorithms.genetic_algorithm import genetic_algorithm
from src.algorithms.hill_climbing import (
    steepest_ascent_hill_climbing,
    stochastic_hill_climbing,
    hill_climbing_with_sideways_moves,
    random_restart_hill_climbing
)
from src.visualization.plot_generator import plot_progress, plot_sa_extra

def print_state_summary(state: State, title: str):
    """Mencetak ringkasan keadaan (solusi) ke konsol."""
    print(f"\n--- {title} ---")
    print(f"Total Kontainer Digunakan: {len(state.kontainer_list)}")
    for i, kontainer in enumerate(sorted(state.kontainer_list, key=lambda k: k.id)):
        item_ids = [item.id for item in kontainer.barang_di_dalam]
        print(f"  Kontainer {kontainer.id} (Muatan: {kontainer.muatan_saat_ini}/{kontainer.kapasitas}): {item_ids}")

def main():
    parser = argparse.ArgumentParser(description="AI Bin Packaging Solver")
    # Argumen Umum
    parser.add_argument("--algoritma", type=str, required=True, choices=['sa', 'hc', 'ga'], help="Algoritma yang akan dijalankan.")
    parser.add_argument("--data_file", type=str, required=True, help="Path ke file data JSON.")
    parser.add_argument("--seed", type=int, default=None, help="Seed RNG (opsional) untuk replikasi hasil.")
    parser.add_argument("--run_count", type=int, default=1, help="Jumlah eksekusi per skenario.")
    parser.add_argument("--max_iter", type=int, default=1000, help="Jumlah iterasi maksimum (untuk SA, HC). Juga sebagai fallback untuk max_generasi GA.")
    parser.add_argument("--initial_state_method", type=str, default='ffd', choices=['ffd', 'random'], help="Metode pembuatan state awal.")

    # Argumen GA
    parser.add_argument("--max_generasi", type=int, default=None, help="Jumlah generasi maksimum untuk GA.")
    parser.add_argument("--populasi_size", type=int, default=30, help="Ukuran populasi untuk GA.")
    parser.add_argument("--crossover_rate", type=float, default=0.8, help="Peluang crossover untuk GA.")
    parser.add_argument("--mutation_rate", type=float, default=0.2, help="Peluang mutasi untuk GA.")
    parser.add_argument("--tournament_size", type=int, default=3, help="Ukuran turnamen seleksi GA.")
    parser.add_argument("--elitism", type=int, default=1, help="Jumlah individu elit yang dipertahankan GA.")
    
    # Argumen SA
    parser.add_argument("--suhu_awal", type=float, default=1000.0, help="Suhu awal untuk SA.")
    parser.add_argument("--cooling_rate", type=float, default=0.99, help="Cooling rate untuk SA.")

    # Argumen HC
    parser.add_argument("--hc_variant", type=str, default='steepest', choices=['steepest', 'stochastic', 'sideways', 'random_restart'], help="Varian Hill Climbing yang akan digunakan.")
    parser.add_argument("--max_sideways_moves", type=int, default=10, help="Jumlah maksimum gerakan menyamping untuk varian 'sideways'.")
    parser.add_argument("--num_restarts", type=int, default=5, help="Jumlah restart untuk varian 'random_restart'.")

    # Argumen Constraint
    parser.add_argument("--enable_fragile", action="store_true", help="Aktifkan constraint barang rapuh.")
    parser.add_argument("--enable_incompatible", action="store_true", help="Aktifkan constraint barang tidak kompatibel.")

    args = parser.parse_args()

    # Pengaturan Direktori Hasil
    base_results_dir = os.path.join("src", "results")
    csv_dir = os.path.join(base_results_dir, "csv")
    plots_dir = os.path.join(base_results_dir, "plots")
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)
    
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = os.path.join(csv_dir, f"results_{run_timestamp}.csv")

    csv_header = [
        'timestamp', 'algorithm', 'hc_variant', 'data_file', 'run_id', 'initial_state_method',
        'initial_score', 'final_score', 'duration_seconds', 'iterations', 'num_containers_initial', 'num_containers_final',
        'fragile_enabled', 'incompatible_enabled', 'seed', 'max_iter_generations', 'population_size', 'crossover_rate',
        'mutation_rate', 'tournament_size', 'elitism', 'initial_temp', 'cooling_rate', 'max_sideways_moves', 'num_restarts'
    ]

    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)

    print(f"Menyimpan hasil CSV ke: {csv_filename}")
    # --------------------------

    # Konfigurasi Fungsi Objektif
    obj_config = ObjectiveConfig(
        use_fragile_constraint=args.enable_fragile,
        use_incompatible_constraint=args.enable_incompatible
    )

    # Baca Data Masalah
    try:
        items, container_capacity = parse_problem(args.data_file)
    except FileNotFoundError:
        print(f"Error: File data tidak ditemukan di '{args.data_file}'")
        return

    # Jalankan Eksperimen
    for i in range(args.run_count):
        run_id = i + 1
        print(f"\n================ RUN {run_id} / {args.run_count} ================")
        
        rng_for_initial_state = random.Random(args.seed) if args.seed is not None else random.Random()
        if args.initial_state_method == 'random':
            keadaan_awal = generate_random_state(items, container_capacity, rng_for_initial_state)
            method_name = "Acak"
        else:
            keadaan_awal = generate_ffd_state(items, container_capacity)
            method_name = "FFD"

        skor_awal = calculate_objective(keadaan_awal, obj_config)
        print_state_summary(keadaan_awal, f"Keadaan Awal ({method_name})")
        print(f"Skor Awal: {skor_awal:.2f}")

        start_time = time.time()
        rng = random.Random(args.seed) if args.seed is not None else None
        histori_skor: List[float] = []
        histori_probabilitas: Optional[List[float]] = None
        iterations = 0

        full_algo_name = args.algoritma
        if args.algoritma == 'hc':
            full_algo_name = f"hc_{args.hc_variant}"

        if args.algoritma == 'sa':
            print(f"\nMenjalankan Simulated Annealing...")
            keadaan_akhir, histori_skor, histori_probabilitas = simulated_annealing(
                keadaan_awal=keadaan_awal,
                suhu_awal=args.suhu_awal,
                cooling_rate=args.cooling_rate,
                max_iter=args.max_iter,
                config=obj_config
            )
            iterations = len(histori_skor) - 1
        elif args.algoritma == 'hc':
            print(f"\nMenjalankan Hill Climbing (Varian: {args.hc_variant})...")
            if args.hc_variant == 'steepest':
                keadaan_akhir, histori_skor = steepest_ascent_hill_climbing(
                    initial_state=keadaan_awal, config=obj_config, max_iter=args.max_iter
                )
            elif args.hc_variant == 'stochastic':
                keadaan_akhir, histori_skor = stochastic_hill_climbing(
                    initial_state=keadaan_awal, config=obj_config, max_iter=args.max_iter
                )
            elif args.hc_variant == 'sideways':
                keadaan_akhir, histori_skor = hill_climbing_with_sideways_moves(
                    initial_state=keadaan_awal, config=obj_config, max_iter=args.max_iter, max_sideways_moves=args.max_sideways_moves
                )
            elif args.hc_variant == 'random_restart':
                keadaan_akhir, histori_skor = random_restart_hill_climbing(
                    initial_state=keadaan_awal, 
                    config=obj_config, 
                    num_restarts=args.num_restarts, 
                    max_iter_per_restart=args.max_iter, 
                    rng=rng,
                    kapasitas_kontainer=container_capacity
                )
            iterations = len(histori_skor) - 1
        elif args.algoritma == 'ga':
            print(f"\nMenjalankan Genetic Algorithm...")
            max_generasi = args.max_generasi if args.max_generasi is not None else args.max_iter
            keadaan_akhir, histori_skor = genetic_algorithm(
                initial_state=keadaan_awal,
                config=obj_config,
                kapasitas_kontainer=container_capacity,
                max_generations=max_generasi,
                population_size=args.populasi_size,
                crossover_rate=args.crossover_rate,
                mutation_rate=args.mutation_rate,
                tournament_size=args.tournament_size,
                elitism=args.elitism,
                rng=rng,
            )
            iterations = len(histori_skor) - 1
        else:
            print(f"Error: Algoritma '{args.algoritma}' tidak dikenal.")
            return
            
        end_time = time.time()
        durasi = end_time - start_time
        skor_akhir = calculate_objective(keadaan_akhir, obj_config)

        print_state_summary(keadaan_akhir, f"Keadaan Akhir ({full_algo_name.upper()})")
        print(f"Skor Akhir: {skor_akhir:.2f}")
        print(f"Durasi Eksekusi: {durasi:.4f} detik")

        # Simpan Hasil ke CSV
        with open(csv_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            row_data = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), full_algo_name, args.hc_variant if args.algoritma == 'hc' else 'N/A',
                os.path.basename(args.data_file), run_id, args.initial_state_method, f"{skor_awal:.4f}", f"{skor_akhir:.4f}",
                f"{durasi:.4f}", iterations, len(keadaan_awal.kontainer_list), len(keadaan_akhir.kontainer_list),
                args.enable_fragile, args.enable_incompatible, args.seed,
                args.max_iter if args.algoritma != 'ga' else max_generasi, 
                args.populasi_size if args.algoritma == 'ga' else 'N/A', 
                args.crossover_rate if args.algoritma == 'ga' else 'N/A',
                args.mutation_rate if args.algoritma == 'ga' else 'N/A',
                args.tournament_size if args.algoritma == 'ga' else 'N/A',
                args.elitism if args.algoritma == 'ga' else 'N/A',
                args.suhu_awal if args.algoritma == 'sa' else 'N/A',
                args.cooling_rate if args.algoritma == 'sa' else 'N/A',
                args.max_sideways_moves if args.algoritma == 'hc' and args.hc_variant == 'sideways' else 'N/A',
                args.num_restarts if args.algoritma == 'hc' and args.hc_variant == 'random_restart' else 'N/A'
            ]
            writer.writerow(row_data)

        # Buat dan Simpan Plot
        plot_filename_base = f"{full_algo_name}_{os.path.splitext(os.path.basename(args.data_file))[0]}_run{run_id}_{run_timestamp}.png"
        plot_title = f"Progres Skor: {full_algo_name.upper()} pada {os.path.basename(args.data_file)} (Run {run_id})"

        if args.algoritma == 'sa' and histori_probabilitas:
            plot_sa_extra(
                score_history=histori_skor,
                prob_history=histori_probabilitas,
                title=plot_title,
                filename=plot_filename_base
            )
        else:
            plot_progress(
                score_history=histori_skor,
                title=plot_title,
                filename=plot_filename_base,
                algorithm_name=full_algo_name.upper()
            )

if __name__ == "__main__":
    main()
