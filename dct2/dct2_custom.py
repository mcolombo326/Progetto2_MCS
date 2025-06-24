import numpy as np

def dct_1d(vector):
    N = len(vector)
    result = np.zeros(N)
    for k in range(N):
        sum_val = 0
        for n in range(N):
            sum_val += vector[n] * np.cos(np.pi * (n + 0.5) * k / N)
        # Normalizzazione ortonormale
        if k == 0:
            coeff = np.sqrt(1 / N)
        else:
            coeff = np.sqrt(2 / N)
        result[k] = coeff * sum_val
    return result

def dct2_custom(matrix):
    N, M = matrix.shape
    assert N == M, "Matrix must be square"

    # DCT sulle righe
    temp = np.zeros((N, N))
    for i in range(N):
        temp[i, :] = dct_1d(matrix[i, :])

    # DCT sulle colonne
    result = np.zeros((N, N))
    for j in range(N):
        result[:, j] = dct_1d(temp[:, j])

    return result
