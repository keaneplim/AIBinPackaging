
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

def get_all_neighbors(state: State) -> List[State]:
    """
    Menghasilkan semua kemungkinan keadaan tetangga dari keadaan saat ini dengan menerapkan
    semua kemungkinan gerakan relokasi dan pertukaran.

    Args:
        state: Keadaan saat ini.

    Returns:
        Sebuah list dari semua kemungkinan keadaan tetangga.
    """
    neighbors = get_all_relocation_moves(state)
    neighbors.extend(get_all_swap_moves(state))
    return neighbors

def get_all_relocation_moves(state: State) -> List[State]:
    """
    Menghasilkan semua keadaan tetangga dengan memindahkan satu barang ke kontainer lain
    (termasuk yang baru).

    Args:
        state: Keadaan saat ini.

    Returns:
        Sebuah list keadaan tetangga yang dibuat oleh gerakan relokasi.
    """
    neighbors = []
    all_items = [item for container in state.kontainer_list for item in container.barang_di_dalam]
    
    for item_to_move in all_items:
        source_container = next((c for c in state.kontainer_list if item_to_move in c.barang_di_dalam), None)
        if not source_container:
            continue

        # Coba pindah ke setiap kontainer lain yang ada
        for target_container in state.kontainer_list:
            if source_container.id == target_container.id:
                continue

            if target_container.bisa_tambah_barang(item_to_move):
                new_state = state.salin()
                
                # Ambil referensi objek dari keadaan baru
                new_source_container = next(c for c in new_state.kontainer_list if c.id == source_container.id)
                new_target_container = next(c for c in new_state.kontainer_list if c.id == target_container.id)
                new_item = next(i for i in new_source_container.barang_di_dalam if i.id == item_to_move.id)

                # Lakukan pemindahan
                new_source_container.barang_di_dalam.remove(new_item)
                new_target_container.barang_di_dalam.append(new_item)
                
                # Hapus kontainer asal jika menjadi kosong
                if not new_source_container.barang_di_dalam:
                    new_state.kontainer_list.remove(new_source_container)
                
                neighbors.append(new_state)

        # Coba pindah ke kontainer baru
        new_state_for_new_container = state.salin()
        source_in_new_state = next(c for c in new_state_for_new_container.kontainer_list if c.id == source_container.id)
        item_in_new_state = next(i for i in source_in_new_state.barang_di_dalam if i.id == item_to_move.id)
        
        source_in_new_state.barang_di_dalam.remove(item_in_new_state)
        
        new_container_id = max(c.id for c in new_state_for_new_container.kontainer_list) + 1 if new_state_for_new_container.kontainer_list else 1
        new_container = Kontainer(id=new_container_id, kapasitas=source_container.kapasitas, barang_di_dalam=[item_in_new_state])
        new_state_for_new_container.kontainer_list.append(new_container)

        if not source_in_new_state.barang_di_dalam:
            new_state_for_new_container.kontainer_list.remove(source_in_new_state)

        neighbors.append(new_state_for_new_container)

    return neighbors

def get_all_swap_moves(state: State) -> List[State]:
    """
    Menghasilkan semua keadaan tetangga dengan menukar dua barang dari dua kontainer yang berbeda.

    Args:
        state: Keadaan saat ini.

    Returns:
        Sebuah list keadaan tetangga yang dibuat oleh gerakan pertukaran.
    """
    neighbors = []
    
    # Loop semua pasangan kontainer yang unik
    for i in range(len(state.kontainer_list)):
        for j in range(i + 1, len(state.kontainer_list)):
            container1 = state.kontainer_list[i]
            container2 = state.kontainer_list[j]

            # Loop semua pasangan barang dari dua kontainer tersebut
            for item1 in container1.barang_di_dalam:
                for item2 in container2.barang_di_dalam:
                    # Cek apakah pertukaran valid (tidak melebihi kapasitas)
                    new_load1 = container1.muatan_saat_ini - item1.ukuran + item2.ukuran
                    new_load2 = container2.muatan_saat_ini - item2.ukuran + item1.ukuran

                    if new_load1 <= container1.kapasitas and new_load2 <= container2.kapasitas:
                        new_state = state.salin()
                        
                        # Ambil referensi objek dari keadaan baru
                        new_container1 = next(c for c in new_state.kontainer_list if c.id == container1.id)
                        new_container2 = next(c for c in new_state.kontainer_list if c.id == container2.id)
                        new_item1 = next(it for it in new_container1.barang_di_dalam if it.id == item1.id)
                        new_item2 = next(it for it in new_container2.barang_di_dalam if it.id == item2.id)

                        # Lakukan pertukaran
                        new_container1.barang_di_dalam.remove(new_item1)
                        new_container2.barang_di_dalam.remove(new_item2)
                        new_container1.barang_di_dalam.append(new_item2)
                        new_container2.barang_di_dalam.append(new_item1)
                        
                        neighbors.append(new_state)
                        
    return neighbors
