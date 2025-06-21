import time
import numpy as np

from dct2_custom import dct2_custom
from dct2_scipy import dct2_scipy

def benchmark(N_values):
    times_custom = []
    times_scipy = []

    for N in N_values:
        A = np.random.rand(N, N)

        # Tempo DCT custom
        start = time.perf_counter()
        dct2_custom(A)
        end = time.perf_counter()
        times_custom.append(end - start)

        # Tempo DCT scipy
        start = time.perf_counter()
        dct2_scipy(A)
        end = time.perf_counter()
        times_scipy.append(end - start)

        print(f"N={N} completato")

    return times_custom, times_scipy

