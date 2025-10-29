from src.core.data_structures import Barang, Kontainer, State

def generate_ffd_state(daftar_barang: list[Barang], kapasitas_kontainer: int) -> State:
    # Membuat state awal menggunakan heuristik First Fit Decreasing (FFD).
    # Barang diurutkan dari yang terbesar ke terkecil, lalu dimasukkan ke kontainer pertama yang muat.
    # Urutkan barang berdasarkan ukuran secara menurun
    barang_diurutkan = sorted(daftar_barang, key=lambda b: b.ukuran, reverse=True)

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
            
    return State(kontainer_list=kontainer_list)

