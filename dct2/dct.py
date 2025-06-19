import numpy as np

PI = np.pi


def dct_1d(v: np.ndarray) -> np.ndarray:
    """
    Calcola la DCT 1D di un vettore v di lunghezza N.
    Implementazione naive, O(N^2), come nel codice C++.

    v: vettore input (numpy array 1D)
    ritorna: vettore DCT (numpy array 1D)
    """
    N = len(v)
    result = np.zeros(N, dtype=np.float64)
    factor = PI / (2 * N)

    for k in range(N):
        sum_val = 0.0
        for n in range(N):
            sum_val += v[n] * np.cos((2 * n + 1) * k * factor)
        c = np.sqrt(1 / N) if k == 0 else np.sqrt(2 / N)
        result[k] = c * sum_val

    return result


def dct2(matrix: np.ndarray) -> np.ndarray:
    """
    Calcola la DCT 2D applicando la DCT 1D sulle righe e poi sulle colonne.
    matrix: array 2D numpy NxM
    ritorna: array 2D numpy NxM con la DCT2 applicata
    """
    N, M = matrix.shape
    # DCT sulle righe
    temp = np.zeros((N, M), dtype=np.float64)
    for i in range(N):
        temp[i, :] = dct_1d(matrix[i, :])

    # DCT sulle colonne
    result = np.zeros((N, M), dtype=np.float64)
    for j in range(M):
        result[:, j] = dct_1d(temp[:, j])

    return result
