from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Barang:
    # Merepresentasikan satu barang dengan semua atributnya.
    id: str
    ukuran: int
    tipe: Optional[str] = None
    rapuh: bool = False

@dataclass
class Kontainer:
    # Merepresentasikan satu kontainer.
    id: int
    kapasitas: int
    barang_di_dalam: List[Barang] = field(default_factory=list)

    @property
    def muatan_saat_ini(self) -> int:
        # Menghitung total ukuran barang di dalam kontainer.
        return sum(b.ukuran for b in self.barang_di_dalam)

    @property
    def sisa_kapasitas(self) -> int:
        # Menghitung sisa kapasitas yang tersedia.
        return self.kapasitas - self.muatan_saat_ini

    def bisa_tambah_barang(self, barang: Barang) -> bool:
        # Mengecek apakah sebuah barang masih muat.
        return self.sisa_kapasitas >= barang.ukuran
    
    def tambah_barang(self, barang: Barang):
        # Menambahkan barang ke dalam kontainer.
        self.barang_di_dalam.append(barang)

@dataclass
class State:
    # Merepresentasikan sebuah solusi lengkap (alokasi barang ke kontainer).
    kontainer_list: List[Kontainer]
    barang_belum_dialokasi: List[Barang] = field(default_factory=list)

    def salin(self) -> 'State':
        # Membuat deep copy dari state saat ini untuk eksplorasi oleh algoritma.
        return State(
            kontainer_list=[
                Kontainer(
                    id=k.id,
                    kapasitas=k.kapasitas,
                    barang_di_dalam=list(k.barang_di_dalam)
                ) for k in self.kontainer_list
            ],
            barang_belum_dialokasi=list(self.barang_belum_dialokasi)
        )