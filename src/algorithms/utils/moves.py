
import random
from typing import List, Tuple

from src.core.data_structures import State, Kontainer, Barang

def get_random_neighbor(state: State) -> State:
    
    # Menghasilkan keadaan tetangga secara acak dengan melakukan salah satu dari dua operasi:
    # 1. Memindahkan satu barang secara acak ke kontainer lain (bisa kontainer baru).
    # 2. Menukar dua barang secara acak dari dua kontainer yang berbeda.
    
    new_state = state.salin()
    
    # Pilih antara memindahkan (move) atau menukar (swap) barang
    if random.random() < 0.7 or len(new_state.kontainer_list) < 2: # Lebih sering memindahkan
        return _relocate_random_item(new_state)
    else:
        return _swap_random_items(new_state)

def _relocate_random_item(state: State) -> State:
    # Memindahkan satu barang acak ke kontainer acak (termasuk kemungkinan membuat kontainer baru)
    
    # Pilih kontainer yang tidak kosong
    non_empty_containers = [k for k in state.kontainer_list if k.barang_di_dalam]
    if not non_empty_containers:
        return state 

    source_container = random.choice(non_empty_containers)
    item_to_move = random.choice(source_container.barang_di_dalam)

    # Pilih kontainer tujuan, bisa juga membuat yang baru
    # Peluang 1/N untuk membuat kontainer baru, dimana N adalah jumlah kontainer
    if random.random() < 1 / (len(state.kontainer_list) + 1):
        # Buat kontainer baru
        new_container_id = max([k.id for k in state.kontainer_list]) + 1 if state.kontainer_list else 1
        # Asumsi kapasitas sama untuk semua, ambil dari kontainer pertama
        new_capacity = state.kontainer_list[0].kapasitas if state.kontainer_list else 100 
        target_container = Kontainer(id=new_container_id, kapasitas=new_capacity)
        state.kontainer_list.append(target_container)
    else:
        # Pilih dari kontainer yang sudah ada
        target_container = random.choice(state.kontainer_list)

    # Pindahkan barang
    source_container.barang_di_dalam.remove(item_to_move)
    target_container.tambah_barang(item_to_move)

    # Hapus kontainer kosong jika ada (kecuali hanya ada satu)
    if not source_container.barang_di_dalam and len(state.kontainer_list) > 1:
        state.kontainer_list.remove(source_container)

    return state

def _swap_random_items(state: State) -> State:
    # Menukar dua barang acak dari dua kontainer yang berbeda
    
    # Pilih dua kontainer berbeda yang tidak kosong
    non_empty_containers = [k for k in state.kontainer_list if k.barang_di_dalam]
    if len(non_empty_containers) < 2:
        return state # Tidak cukup kontainer untuk menukar

    container1, container2 = random.sample(non_empty_containers, 2)

    item1 = random.choice(container1.barang_di_dalam)
    item2 = random.choice(container2.barang_di_dalam)

    # Tukar barang
    container1.barang_di_dalam.remove(item1)
    container2.barang_di_dalam.remove(item2)
    container1.tambah_barang(item2)
    container2.tambah_barang(item1)

    return state
