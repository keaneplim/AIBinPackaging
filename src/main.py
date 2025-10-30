
import argparse
import time
from typing import List

from src.core.data_structures import State, Kontainer
from src.core.initial_state import generate_ffd_state
from src.core.objective_function import ObjectiveConfig, calculate_objective
from src.utils.file_parser import parse_problem
from src.algorithms.simulated_annealing import simulated_annealing

def print_state_summary(state: State, title: str):
    """Mencetak ringkasan keadaan (solusi) ke konsol."""
    print(f"\n--- {title} ---")
    print(f"Total Kontainer Digunakan: {len(state.kontainer_list)}")
    for i, kontainer in enumerate(sorted(state.kontainer_list, key=lambda k: k.id)):
        item_ids = [item.id for item in kontainer.barang_di_dalam]
        print(f"  Kontainer {kontainer.id} (Muatan: {kontainer.muatan_saat_ini}/{kontainer.kapasitas}): {item_ids}")

def main():
    parser = argparse.ArgumentParser(description="AI Bin Packaging Solver")
    parser.add_argument("--algoritma", type=str, required=True, choices=['sa', 'hc', 'ga'], help="Algoritma yang akan dijalankan.")
    parser.add_argument("--data_file", type=str, required=True, help="Path ke file data JSON.")
    parser.add_argument("--max_iter", type=int, default=1000, help="Jumlah iterasi maksimum.")
    parser.add_argument("--run_count", type=int, default=1, help="Jumlah eksekusi per skenario.")
    
    parser.add_argument("--suhu_awal", type=float, default=1000.0, help="Suhu awal untuk SA.")
    parser.add_argument("--cooling_rate", type=float, default=0.99, help="Cooling rate untuk SA.")

    parser.add_argument("--enable_fragile", action="store_true", help="Aktifkan constraint barang rapuh.")
    parser.add_argument("--enable_incompatible", action="store_true", help="Aktifkan constraint barang tidak kompatibel.")

    args = parser.parse_args()

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
        print(f"\n================ RUN {i + 1} / {args.run_count} ================")
        
        keadaan_awal = generate_ffd_state(items, container_capacity)
        skor_awal = calculate_objective(keadaan_awal, obj_config)
        print_state_summary(keadaan_awal, "Keadaan Awal (FFD)")
        print(f"Skor Awal: {skor_awal}")

        start_time = time.time()
        if args.algoritma == 'sa':
            keadaan_akhir, histori_skor, histori_probabilitas = simulated_annealing(
                keadaan_awal=keadaan_awal,
                suhu_awal=args.suhu_awal,
                cooling_rate=args.cooling_rate,
                max_iter=args.max_iter,
                config=obj_config
            )
        elif args.algoritma == 'hc':
            print("\nAlgoritma Hill Climbing belum diimplementasikan di main.py")
            return
        elif args.algoritma == 'ga':
            print("\nAlgoritma Genetic Algorithm belum diimplementasikan di main.py")
            return
        else:
            print(f"Algoritma '{args.algoritma}' tidak dikenal.")
            return
            
        end_time = time.time()
        durasi = end_time - start_time

        # Tampilkan Hasil
        skor_akhir = calculate_objective(keadaan_akhir, obj_config)
        print_state_summary(keadaan_akhir, "Keadaan Akhir")
        print(f"Skor Akhir: {skor_akhir}")
        print(f"Durasi Eksekusi: {durasi:.4f} detik")

        # Simpan Hasil (Placeholder)
        # TODO: Simpan hasil ke file CSV

        # Buat Plot (Placeholder)
        # plot_filename = f"plot_{args.algoritma}_{i+1}.png"
        # plot_progress(histori_skor, title=f"Run {i+1}: {args.algoritma}", filename=plot_filename)
        # print(f"\nPlot disimpan ke {plot_filename}")

        # Jika SA, buat plot probabilitas (Placeholder)
        if args.algoritma == 'sa':
            pass
            # sa_plot_filename = f"plot_sa_prob_{i+1}.png"
            # plot_acceptance_probability(histori_probabilitas, filename=sa_plot_filename)
            # print(f"Plot probabilitas SA disimpan ke {sa_plot_filename}")

if __name__ == "__main__":
    main()
