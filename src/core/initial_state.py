import random
from typing import List, Sequence
from src.core.data_structures import Barang, Kontainer, State
from src.utils.state_utils import renumber_container_ids

def generate_ffd_state(daftar_barang: list[Barang], kapasitas_kontainer: int) -> State:
    # Membuat state awal menggunakan heuristik First Fit Decreasing (FFD).
    # Pisahkan barang yang bisa dimuat dan yang tidak (karena terlalu besar)
    barang_untuk_ditempatkan = []
    barang_belum_dialokasi = []
    for barang in daftar_barang:
        if barang.ukuran > kapasitas_kontainer:
            barang_belum_dialokasi.append(barang)
        else:
            barang_untuk_ditempatkan.append(barang)

    # Barang diurutkan dari yang terbesar ke terkecil, lalu dimasukkan ke kontainer pertama yang muat.
    barang_diurutkan = sorted(barang_untuk_ditempatkan, key=lambda b: b.ukuran, reverse=True)

    kontainer_list: list[Kontainer] = []
    id_kontainer_selanjutnya = 0

    for barang in barang_diurutkan:
        ditempatkan = False
        # Coba tempatkan di kontainer yang ada
        for kontainer in kontainer_list:
            if kontainer.bisa_tambah_barang(barang):
                kontainer.tambah_barang(barang)
                ditempatkan = True
                break
        
        # Jika tidak muat di mana pun, buat kontainer baru
        if not ditempatkan:
            kontainer_baru = Kontainer(id=id_kontainer_selanjutnya, kapasitas=kapasitas_kontainer)
            kontainer_baru.tambah_barang(barang)
            kontainer_list.append(kontainer_baru)
            id_kontainer_selanjutnya += 1
            
    return State(kontainer_list=kontainer_list, barang_belum_dialokasi=barang_belum_dialokasi)

def generate_random_state(items: Sequence[Barang], kapasitas: int, rng: random.Random) -> State:
    """
    Membuat state awal secara acak.

    Barang-barang (dalam urutan acak) ditempatkan ke dalam kontainer yang dipilih
    secara acak. Jika tidak ada kontainer yang muat, kontainer baru akan dibuat.

    Args:
        items: Sekumpulan barang yang akan ditempatkan.
        kapasitas: Kapasitas untuk setiap kontainer baru.
        rng: Generator angka acak untuk memastikan hasil yang dapat direplikasi.

    Returns:
        Sebuah state baru yang dihasilkan secara acak.
    """
    # Pisahkan barang yang bisa dimuat dan yang tidak
    barang_untuk_ditempatkan = []
    barang_belum_dialokasi = []
    for barang in items:
        if barang.ukuran > kapasitas:
            barang_belum_dialokasi.append(barang)
        else:
            barang_untuk_ditempatkan.append(barang)

    kontainer_list: List[Kontainer] = []
    # Acak urutan barang untuk variasi penempatan
    if barang_untuk_ditempatkan:
        for barang in rng.sample(barang_untuk_ditempatkan, len(barang_untuk_ditempatkan)):
            # Coba tempatkan di kontainer yang ada terlebih dahulu
            ditempatkan = False
            if kontainer_list:
                # Acak urutan kontainer yang akan dicoba
                kandidat_kontainer = rng.sample(kontainer_list, len(kontainer_list))
                for kontainer in kandidat_kontainer:
                    if kontainer.bisa_tambah_barang(barang):
                        kontainer.barang_di_dalam.append(barang)
                        ditempatkan = True
                        break
            
            # Jika tidak muat dimanapun, buat kontainer baru
            if not ditempatkan:
                kontainer_baru = Kontainer(id=len(kontainer_list), kapasitas=kapasitas, barang_di_dalam=[barang])
                kontainer_list.append(kontainer_baru)
            
    renumber_container_ids(kontainer_list)
    return State(kontainer_list=kontainer_list, barang_belum_dialokasi=barang_belum_dialokasi)

