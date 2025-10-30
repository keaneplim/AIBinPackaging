
import math
import random
from typing import List, Tuple

from src.core.data_structures import State
from src.core.objective_function import calculate_objective, ObjectiveConfig
from src.algorithms.utils.moves import get_random_neighbor

def simulated_annealing(
    keadaan_awal: State,
    suhu_awal: float,
    cooling_rate: float,
    max_iter: int,
    config: ObjectiveConfig
) -> Tuple[State, List[float], List[float]]:
    
    #     keadaan_awal: State awal untuk memulai pencarian.
    #     suhu_awal: Temperatur awal untuk proses annealing.
    #     cooling_rate: Faktor pengurangan temperatur (e.g., 0.99).
    #     max_iter: Jumlah iterasi maksimum yang akan dijalankan.
    #     config: Konfigurasi untuk fungsi objektif (e.g., penggunaan constraint bonus).
    #

    # Salin keadaan awal untuk menghindari modifikasi objek aslinya
    keadaan_saat_ini = keadaan_awal.salin()
    skor_saat_ini = calculate_objective(keadaan_saat_ini, config)

    # Inisialisasi state terbaik global dengan keadaan awal
    keadaan_terbaik_global = keadaan_saat_ini
    skor_terbaik_global = skor_saat_ini

    histori_skor = [skor_saat_ini]
    histori_probabilitas = [1.0] # Probabilitas awal adalah 1.0
    suhu = suhu_awal

    for _ in range(max_iter):
        # Hasilkan tetangga secara acak
        keadaan_tetangga = get_random_neighbor(keadaan_saat_ini)

        # Hitung skor tetangga
        skor_tetangga = calculate_objective(keadaan_tetangga, config)

        # Hitung perbedaan energi (skor)
        delta_e = skor_tetangga - skor_saat_ini

        # Tentukan apakah akan menerima keadaan baru
        if delta_e < 0:
            probabilitas_penerimaan = 1.0
            keadaan_saat_ini = keadaan_tetangga
            skor_saat_ini = skor_tetangga
        else:
            # Jika tetangga lebih buruk, terima dengan probabilitas tertentu
            # Ini adalah inti dari SA untuk keluar dari optimum lokal
            probabilitas_penerimaan = math.exp(-delta_e / suhu)
            if random.random() < probabilitas_penerimaan:
                keadaan_saat_ini = keadaan_tetangga
                skor_saat_ini = skor_tetangga

        # Perbarui solusi terbaik global jika ditemukan yang lebih baik
        if skor_saat_ini < skor_terbaik_global:
            keadaan_terbaik_global = keadaan_saat_ini
            skor_terbaik_global = skor_saat_ini

        # Simpan data saat ini untuk analisis
        histori_skor.append(skor_saat_ini)
        histori_probabilitas.append(probabilitas_penerimaan)

        # Turunkan suhu
        suhu *= cooling_rate

    return keadaan_terbaik_global, histori_skor, histori_probabilitas
