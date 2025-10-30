# AI Bin Packaging Solver

Proyek ini adalah implementasi dari berbagai algoritma *local search* dan metaheuristik untuk menyelesaikan *Bin Packing Problem* (BPP). Tujuannya adalah untuk menemukan solusi pengepakan yang efisien dengan meminimalkan jumlah kontainer yang digunakan.

## 1. Instalasi

Pastikan Anda memiliki Python 3.8+ terpasang. Untuk menginstal semua dependensi yang diperlukan, jalankan perintah berikut dari direktori root proyek:

```bash
pip install -r requirements.txt
```

## 2. Cara Menjalankan

Semua eksekusi dilakukan melalui skrip `src/main.py`. Cara terbaik untuk menjalankannya adalah sebagai modul dari direktori root untuk memastikan semua *import* berfungsi dengan benar.

Untuk melihat daftar lengkap semua argumen yang tersedia, gunakan perintah `--help`:

```bash
python -m src.main --help
```

### Argumen Utama

Berikut adalah argumen yang paling penting dan bersifat umum:

*   `--algoritma`: **(Wajib)** Memilih algoritma yang akan dijalankan.
    *   Pilihan: `hc` (Hill Climbing), `sa` (Simulated Annealing), `ga` (Genetic Algorithm).
*   `--data_file`: **(Wajib)** Path menuju file data JSON yang akan digunakan (misal: `src/data/problem_A.json`).
*   `--initial_state_method`: Metode untuk membuat solusi awal.
    *   Pilihan: `ffd` (First Fit Decreasing), `random` (Acak).
    *   Default: `ffd`.
*   `--max_iter`: Jumlah iterasi maksimum untuk algoritma HC dan SA. Juga digunakan sebagai jumlah generasi untuk GA jika `--max_generasi` tidak disetel.
    *   Default: `1000`.
*   `--run_count`: Berapa kali sebuah skenario eksperimen akan diulang.
    *   Default: `1`.
    *   `--seed`: *Seed* untuk generator angka acak agar hasil dapat direplikasi.

### Argumen Spesifik Hill Climbing (`--algoritma hc`)

*   `--hc_variant`: Memilih varian dari algoritma Hill Climbing.
    *   Pilihan:
        *   `steepest`: Steepest Ascent Hill Climbing.
        *   `stochastic`: Stochastic Hill Climbing.
        *   `sideways`: Hill Climbing with Sideways Moves.
        *   `random_restart`: Random-Restart Hill Climbing.
    *   Default: `steepest`.
*   `--max_sideways_moves`: Jumlah maksimum gerakan menyamping (plateau) yang diizinkan sebelum berhenti (hanya untuk varian `sideways`).
    *   Default: `10`.
*   `--num_restarts`: Jumlah restart yang akan dilakukan setelah pencarian awal (hanya untuk varian `random_restart`).
    *   Default: `5`.

### Argumen Spesifik Simulated Annealing (`--algoritma sa`)

*   `--suhu_awal`: Temperatur awal untuk proses *annealing*.
    *   Default: `1000.0`.
*   `--cooling_rate`: Faktor pengali untuk menurunkan suhu di setiap iterasi (misal: 0.99).
    *   Default: `0.99`.

### Argumen Spesifik Genetic Algorithm (`--algoritma ga`)

*   `--max_generasi`: Jumlah generasi maksimum. Jika tidak disetel, akan menggunakan nilai dari `--max_iter`.
*   `--populasi_size`: Jumlah individu (solusi) dalam satu populasi.
    *   Default: `30`.
*   `--crossover_rate`: Peluang (0.0 - 1.0) untuk melakukan *crossover* pada dua orang tua.
    *   Default: `0.8`.
*   `--mutation_rate`: Peluang (0.0 - 1.0) sebuah individu akan mengalami mutasi.
    *   Default: `0.2`.
*   `--tournament_size`: Jumlah individu yang diambil secara acak untuk seleksi turnamen.
    *   Default: `3`.
*   `--elitism`: Jumlah individu terbaik yang akan langsung dibawa ke generasi berikutnya tanpa perubahan.
    *   Default: `1`.

## 3. Contoh Penggunaan

Berikut adalah beberapa contoh cara menjalankan skrip dengan konfigurasi yang berbeda.

**Contoh 1: Menjalankan Steepest Ascent Hill Climbing (dasar)**

Perintah ini menjalankan varian `steepest` dari Hill Climbing pada `problem_A.json` menggunakan metode FFD (default).

```bash
python -m src.main --algoritma hc --hc_variant steepest --data_file src/data/problem_A.json
```

**Contoh 2: Menjalankan Random-Restart Hill Climbing**

Perintah ini menggunakan varian `random_restart` dengan 10 kali restart, di mana setiap pencarian memiliki maksimal 500 iterasi.

```bash
python -m src.main --algoritma hc --hc_variant random_restart --data_file src/data/problem_B.json --num_restarts 10 --max_iter 500
```

**Contoh 3: Menjalankan Simulated Annealing dengan State Awal Acak**

Perintah ini menjalankan SA dengan suhu awal `5000` dan *cooling rate* `0.995`. State awal dibuat secara acak (`random`).

```bash
python -m src.main --algoritma sa --data_file src/data/problem_C.json --initial_state_method random --suhu_awal 5000 --cooling_rate 0.995
```

**Contoh 4: Menjalankan Genetic Algorithm dengan Parameter Khusus**

Perintah ini menjalankan GA dengan populasi `100` dan `2000` generasi. Peluang mutasi juga diubah menjadi `0.1`.

```bash
python -m src.main --algoritma ga --data_file src/data/problem_D.json --populasi_size 100 --max_generasi 2000 --mutation_rate 0.1
```

**Contoh 5: Menjalankan Eksperimen dengan Constraint**

Perintah ini menjalankan algoritma SA pada `problem_edge_incompatible.json` sambil mengaktifkan kedua *constraint* bonus (`--enable_fragile` dan `--enable_incompatible`).

```bash
python -m src.main --algoritma sa --data_file src/data/problem_edge_incompatible.json --enable_fragile --enable_incompatible
```

