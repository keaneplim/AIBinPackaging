from dataclasses import dataclass, field
from src.core.data_structures import State, Barang, Kontainer

# Konfigurasi & Bobot Penalti
OVERFILL_PENALTY_MULTIPLIER = 1_000_000
FRAGILE_PENALTY = 500_000
INCOMPATIBLE_PENALTY = 500_000

@dataclass
class ObjectiveConfig:
    # Konfigurasi untuk perhitungan fungsi objektif.
    fragile_threshold: int = 50
    incompatible_pairs: list[tuple[str, str]] = field(default_factory=lambda: [('makanan', 'kimia')])
    use_fragile_constraint: bool = False
    use_incompatible_constraint: bool = False

def calculate_objective(state: State, config: ObjectiveConfig) -> float:
    # Menghitung skor total dari sebuah state berdasarkan konfigurasi.
    # 1. Penalti Kapasitas Berlebih (Wajib)
    overfill_penalty = 0.0
    for kontainer in state.kontainer_list:
        if kontainer.muatan_saat_ini > kontainer.kapasitas:
            overfill_penalty += (kontainer.muatan_saat_ini - kontainer.kapasitas) * OVERFILL_PENALTY_MULTIPLIER
    
    # Jika ada penalti kelebihan muatan, langsung kembalikan skor yang sangat tinggi
    # Ini adalah optimisasi agar pencarian tidak mengeksplorasi solusi tidak valid
    if overfill_penalty > 0:
        return overfill_penalty

    # 2. Skor Jumlah Kontainer (Wajib)
    container_score = len(state.kontainer_list)

    # 3. Skor Kepadatan (Bonus untuk mendorong solusi rapi)
    # Semakin padat, semakin kecil (baik) skornya.
    # Rata-rata dari (1 - kepadatan^2) untuk setiap kontainer.
    total_density_score = 0
    if container_score > 0:
        for k in state.kontainer_list:
            density = k.muatan_saat_ini / k.kapasitas
            total_density_score += (1 - density**2)
        density_bonus = total_density_score / container_score
    else:
        density_bonus = 0

    # Penalti untuk Batasan Bonus
    fragile_penalty = 0.0
    if config.use_fragile_constraint:
        for k in state.kontainer_list:
            # Cek apakah ada barang rapuh di kontainer ini
            if any(b.rapuh for b in k.barang_di_dalam):
                # Hitung total ukuran barang non-rapuh
                muatan_non_rapuh = sum(b.ukuran for b in k.barang_di_dalam if not b.rapuh)
                if muatan_non_rapuh > config.fragile_threshold:
                    fragile_penalty += FRAGILE_PENALTY

    incompatible_penalty = 0.0
    if config.use_incompatible_constraint:
        for k in state.kontainer_list:
            tipe_barang = {b.tipe for b in k.barang_di_dalam if b.tipe is not None}
            # Cek setiap pasangan tipe yang tidak kompatibel
            for pair in config.incompatible_pairs:
                if pair[0] in tipe_barang and pair[1] in tipe_barang:
                    incompatible_penalty += INCOMPATIBLE_PENALTY

    # Kombinasi Skor Final
    # Skor utama adalah jumlah kontainer. Bonus kepadatan mengurangi skor sedikit.
    # Penalti ditambahkan dengan bobot besar untuk menghindari solusi tidak valid.
    total_score = (container_score + density_bonus + 
                   fragile_penalty + incompatible_penalty)
    
    return total_score

