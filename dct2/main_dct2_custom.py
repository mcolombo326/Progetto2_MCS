from utils import *
from dct2.benchmark import benchmark
from dct2.plot_times import plot_times
from dct2.test_dct2 import is_dct2_and_dct1d_correct

def main_dct2_custom():
    # Verifica preliminare della correttezza della DCT
    if is_dct2_and_dct1d_correct():
        print("✅ Test DCT2 e DCT1D superato. Avvio benchmark...\n")
    else:
        print("❌ ERRORE: DCT2 o DCT1D non producono risultati corretti. Interruzione del programma.")
        return

    N_values = [8, 16, 32, 64, 128, 256]

    # Esegui benchmark
    times_custom, times_fast = benchmark(N_values)

    # Pulisci cartella e salva dati
    clear_folder(RESULT_DIR)
    np.savetxt(os.path.join(RESULT_DIR, "times_custom.txt"), times_custom)
    np.savetxt(os.path.join(RESULT_DIR, "times_fast.txt"), times_fast)
    np.savetxt(os.path.join(RESULT_DIR, "N_values.txt"), N_values)

    # Genera grafico e salva
    fig = plot_times(N_values, times_custom, times_fast)
    fig.savefig(os.path.join(RESULT_DIR, "confronto_tempi.png"))
    fig.show()

if __name__ == "__main__":
    main_dct2_custom()

