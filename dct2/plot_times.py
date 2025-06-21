import matplotlib.pyplot as plt

def plot_times(N_values, times_custom, times_fast):
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.semilogy(N_values, times_custom, 'o-', label='DCT2 Custom (O(N^3))')
    ax.semilogy(N_values, times_fast, 's-', label='DCT2 Fast (O(N^2 logN))')

    ax.set_xlabel('Dimensione matrice N')
    ax.set_ylabel('Tempo di esecuzione (s)')
    ax.set_title('Confronto tempi DCT2 custom vs fast')
    ax.grid(True, which="major", linestyle='--', alpha=0.4)
    ax.legend()
    ax.minorticks_off()
    fig.tight_layout()

    return fig

