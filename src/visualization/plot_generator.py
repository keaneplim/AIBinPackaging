import os
from typing import List, Optional
import matplotlib.pyplot as plt

def plot_progress(
    score_history: List[float],
    title: str,
    filename: str,
    algorithm_name: str
):
    """
    Membuat dan menyimpan plot yang menunjukkan progres skor (fungsi objektif)
    terhadap iterasi atau generasi.

    Args:
        score_history: List berisi nilai skor di setiap iterasi/generasi.
        title: Judul untuk plot.
        filename: Nama file untuk menyimpan plot (tanpa path).
        algorithm_name: Nama algoritma yang digunakan, untuk label.
    """
    plt.figure(figsize=(12, 7))
    plt.plot(score_history, label=f'Skor {algorithm_name}')
    plt.xlabel("Iterasi / Generasi")
    plt.ylabel("Skor Fungsi Objektif")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    
    # Pastikan direktori plots ada
    plots_dir = os.path.join("src", "results", "plots")
    os.makedirs(plots_dir, exist_ok=True)
    
    # Simpan plot
    full_path = os.path.join(plots_dir, filename)
    plt.savefig(full_path)
    plt.close()
    print(f"Plot disimpan di: {full_path}")

def plot_sa_extra(
    score_history: List[float],
    prob_history: List[float],
    title: str,
    filename: str
):
    """
    Membuat plot khusus untuk Simulated Annealing yang menampilkan skor dan
    probabilitas penerimaan.

    Args:
        score_history: List skor per iterasi.
        prob_history: List probabilitas penerimaan per iterasi.
        title: Judul untuk plot.
        filename: Nama file untuk menyimpan plot.
    """
    fig, ax1 = plt.subplots(figsize=(12, 7))

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
    # Plot probabilitas
    ax2.plot(prob_history, color=color, linestyle='--', alpha=0.7, label='Probabilitas')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 1.05)

    fig.suptitle(title)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    # Simpan plot
    plots_dir = os.path.join("src", "results", "plots")
    os.makedirs(plots_dir, exist_ok=True)
    full_path = os.path.join(plots_dir, filename)
    plt.savefig(full_path)
    plt.close()
    print(f"Plot SA (skor & probabilitas) disimpan di: {full_path}")
