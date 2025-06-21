import numpy as np

from dct2.Utils import *
from dct2.benchmark import benchmark
from dct2.plot_times import plot_times

def main_dct2_custom():
    N_values = [8, 16, 32, 64, 128, 256]

    # Esegui benchmark
    times_custom, times_scipy = benchmark(N_values)

    # Pulisci cartella e salva dati
    clear_folder(RESULT_DIR)
    np.savetxt(os.path.join(RESULT_DIR, "times_custom.txt"), times_custom)
    np.savetxt(os.path.join(RESULT_DIR, "times_scipy.txt"), times_scipy)
    np.savetxt(os.path.join(RESULT_DIR, "N_values.txt"), N_values)

    # Genera grafico e salva
    fig = plot_times(N_values, times_custom, times_scipy)
    fig.savefig(os.path.join(RESULT_DIR, "confronto_tempi.png"))
    fig.show()

if __name__ == "__main__":
    main_dct2_custom()

