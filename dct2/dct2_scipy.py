from scipy.fft import dct
import numpy as np

def dct2_scipy(matrix):
    # type 2 DCT sulle righe
    temp = dct(matrix, type=2, axis=0, norm='ortho')
    # type 2 DCT sulle colonne
    result = dct(temp, type=2, axis=1, norm='ortho')
    return result
