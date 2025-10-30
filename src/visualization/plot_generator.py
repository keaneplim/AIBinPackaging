import os
from typing import List, Optional
import matplotlib.pyplot as plt

def plot_progress(
    score_history: List[float],
    title: str,
    filename: str,
    algorithm_name: str,
    plots_dir: str,
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
        plots_dir: Direktori absolut untuk menyimpan plot.
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

    # Simpan plot
    os.makedirs(plots_dir, exist_ok=True)
    full_path = os.path.join(plots_dir, filename)
    plt.savefig(full_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Plot skor disimpan di: {full_path}")

def plot_sa_acceptance_probability(
    prob_history: List[float],
    title: str,
    filename: str,
    plots_dir: str,
    iterations: int,
    duration: float
):
    """
    Membuat dan menyimpan plot khusus untuk probabilitas penerimaan Simulated Annealing.

    Args:
        prob_history: List probabilitas penerimaan per iterasi.
        title: Judul untuk plot.
        filename: Nama file untuk menyimpan plot.
        plots_dir: Direktori absolut untuk menyimpan plot.
        iterations: Jumlah total iterasi.
        duration: Durasi eksekusi dalam detik.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(prob_history, color='tab:red', linestyle='None', marker='o', alpha=0.8, label='Acceptance Probability')
    ax.set_xlabel("Iterasi")
    ax.set_ylabel("Acceptance Probability")
    ax.set_title(title, pad=20)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_ylim(0, 1.05)

    # Statistik
    stats_text = (
        f"Total Iterasi: {iterations}\n"
        f"Durasi: {duration:.4f} detik"
    )
    fig.text(0.98, 0.02, stats_text, ha='right', va='bottom', fontsize=12)

    plt.tight_layout(rect=[0, 0.1, 1, 1])

    # Simpan plot
    os.makedirs(plots_dir, exist_ok=True)
    full_path = os.path.join(plots_dir, filename)
    plt.savefig(full_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Plot probabilitas SA disimpan di: {full_path}")
