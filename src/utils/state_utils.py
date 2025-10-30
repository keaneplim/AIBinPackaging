from typing import List, Optional
from src.core.data_structures import Kontainer, State, Barang

def renumber_container_ids(kontainer_list: List[Kontainer]) -> None:
    """
    Memberi nomor ulang ID kontainer dalam sebuah list secara berurutan mulai dari 0.
    Fungsi ini memodifikasi list secara langsung (in-place).

    Args:
        kontainer_list: List objek Kontainer yang akan dinomori ulang.
    """
    for idx, kontainer in enumerate(kontainer_list):
        kontainer.id = idx

def extract_all_items(state: State) -> List[Barang]:
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


def resolve_capacity(state: State, kapasitas_override: Optional[int]) -> int:
    if kapasitas_override is not None:
        return kapasitas_override
    if state.kontainer_list:
        return state.kontainer_list[0].kapasitas
    raise ValueError("kapasitas_kontainer harus diberikan jika state awal tidak memiliki kontainer.")

