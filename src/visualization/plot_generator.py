import os
from typing import List, Optional
import matplotlib.pyplot as plt

def plot_progress(
    score_history: List[float],
    title: str,
    filename: str,
    algorithm_name: str,
    initial_score: float,
    final_score: float,
    iterations: int,
    duration: float
):
    """
    Membuat dan menyimpan plot yang menunjukkan progres skor (fungsi objektif)
    terhadap iterasi atau generasi.

    Args:
        score_history: List berisi nilai skor di setiap iterasi/generasi.
        title: Judul untuk plot.
        filename: Nama file untuk menyimpan plot (tanpa path).
        algorithm_name: Nama algoritma yang digunakan, untuk label.
        initial_score: Skor awal.
        final_score: Skor akhir.
        iterations: Jumlah total iterasi/generasi.
        duration: Durasi eksekusi dalam detik.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(score_history, label=f'Skor {algorithm_name}')
    ax.set_xlabel("Iterasi / Generasi")
    ax.set_ylabel("Skor Fungsi Objektif")
    ax.set_title(title, pad=20)
    ax.legend()
    ax.grid(True)

    # Statistik
    stats_text_left = (
        f"Skor Awal: {initial_score:.4f}\n"
        f"Skor Akhir: {final_score:.4f}"
    )
    stats_text_right = (
        f"Total Iterasi: {iterations}\n"
        f"Durasi: {duration:.4f} detik"
    )

    fig.text(0.02, 0.02, stats_text_left, ha='left', va='bottom', fontsize=12)
    fig.text(0.98, 0.02, stats_text_right, ha='right', va='bottom', fontsize=12)

    plt.tight_layout(rect=[0, 0.1, 1, 1])

    # Pastikan direktori plots ada
    plots_dir = os.path.join("src", "results", "plots")
    os.makedirs(plots_dir, exist_ok=True)
    
    # Simpan plot
    full_path = os.path.join(plots_dir, filename)
    plt.savefig(full_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Plot disimpan di: {full_path}")

def plot_sa_extra(
    score_history: List[float],
    prob_history: List[float],
    title: str,
    filename: str,
    initial_score: float,
    final_score: float,
    iterations: int,
    duration: float
):
    """
    Membuat plot khusus untuk Simulated Annealing yang menampilkan skor dan
    probabilitas penerimaan.

    Args:
        score_history: List skor per iterasi.
        prob_history: List probabilitas penerimaan per iterasi.
        title: Judul untuk plot.
        filename: Nama file untuk menyimpan plot.
        initial_score: Skor awal.
        final_score: Skor akhir.
        iterations: Jumlah total iterasi.
        duration: Durasi eksekusi dalam detik.
    """
    fig, ax1 = plt.subplots(figsize=(12, 8))

    fig.suptitle(title, y=1.02)

    # Plot Skor
    color = 'tab:blue'
    ax1.set_xlabel('Iterasi')
    ax1.set_ylabel('Skor Fungsi Objektif', color=color)
    ax1.plot(score_history, color=color, label='Skor')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Buat sumbu y kedua untuk probabilitas
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Probabilitas Penerimaan', color=color)
    ax2.plot(prob_history, color=color, linestyle='--', alpha=0.7, label='Probabilitas')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 1.05)

    # Statistik
    stats_text_left = (
        f"Skor Awal: {initial_score:.4f}\n"
        f"Skor Akhir: {final_score:.4f}"
    )
    stats_text_right = (
        f"Total Iterasi: {iterations}\n"
        f"Durasi: {duration:.4f} detik"
    )

    # Text
    fig.text(0.02, 0.02, stats_text_left, ha='left', va='bottom', fontsize=12)
    fig.text(0.98, 0.02, stats_text_right, ha='right', va='bottom', fontsize=12)

    fig.tight_layout(rect=[0, 0.1, 1, 1])

    # Simpan plot
    plots_dir = os.path.join("src", "results", "plots")
    os.makedirs(plots_dir, exist_ok=True)
    full_path = os.path.join(plots_dir, filename)
    plt.savefig(full_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Plot SA (skor & probabilitas) disimpan di: {full_path}")
