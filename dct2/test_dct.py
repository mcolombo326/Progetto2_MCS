import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.fftpack import dct
from dct import dct2

def scipy_dct2(matrix: np.ndarray) -> np.ndarray:
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')

def measure_time(func, *args):
    start = time.time()
    func(*args)
    end = time.time()
    return end - start

def test_dct_correctness():
    """
    Test di correttezza confronto con scipy fftpack dct2.
    """
    np.random.seed(0)
    matrix = np.random.rand(8,8) * 255
    result_custom = dct2(matrix)
    result_scipy = scipy_dct2(matrix)
    diff = np.abs(result_custom - result_scipy)
    print("Massima differenza tra DCT2 custom e Scipy:", diff.max())
    assert diff.max() < 1e-10, "Differenza troppo grande tra DCT custom e Scipy"

def test_timing():
    """
    Misura i tempi di esecuzione per varie dimensioni.
    """
    sizes = [8, 16, 32, 64, 128]
    times_custom = []
    times_scipy = []

    for N in sizes:
        matrix = np.random.rand(N, N) * 255

        t_custom = measure_time(dct2, matrix)
        t_scipy = measure_time(scipy_dct2, matrix)

        print(f"N={N}: Custom DCT2 time = {t_custom:.4f}s, Scipy DCT2 time = {t_scipy:.4f}s")

        times_custom.append(t_custom)
        times_scipy.append(t_scipy)

    return sizes, times_custom, times_scipy

def plot_timings(sizes, times_custom, times_scipy):
    plt.figure(figsize=(8,5))
    plt.semilogy(sizes, times_custom, 'o-', label='DCT2 Custom (O(N^3))')
    plt.semilogy(sizes, times_scipy, 's-', label='DCT2 Scipy (FFT-based)')
    plt.xlabel('Dimensione matrice N x N')
    plt.ylabel('Tempo esecuzione (s, scala logaritmica)')
    plt.title('Confronto tempi esecuzione DCT2')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.savefig("dct2_performance.png")
    plt.show()
