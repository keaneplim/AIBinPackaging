import json
from src.core.data_structures import Barang

def parse_problem(file_path: str) -> tuple[list[Barang], int]:
    """
     Membaca file masalah dalam format JSON dan mengembalikannya sebagai daftar objek Barang
     dan kapasitas kontainer."
    
     Args:
         file_path: Path ke file JSON masalah.
    
     Returns:
         Tuple berisi (list[Barang], kapasitas_kontainer).
    """
    with open(file_path, 'r') as f:
        data = json.load(f)

    kapasitas_kontainer = data['kapasitas_kontainer']
    
    daftar_barang = []
    for item_data in data['barang']:
        barang = Barang(
            id=item_data['id'],
            ukuran=item_data['ukuran'],
            tipe=item_data.get('tipe'),
            rapuh=item_data.get('rapuh', False)
        )
        daftar_barang.append(barang)

    return daftar_barang, kapasitas_kontainer
