from scipy.fft import dct, idct

def dct2_fast(matrix):
    # type 2 DCT sulle righe
    temp = dct(matrix, type=2, axis=0, norm='ortho')
    # type 2 DCT sulle colonne
    result = dct(temp, type=2, axis=1, norm='ortho')
    return result

def idct2_fast(matrix):
    # IDCT2 colonne
    temp = idct(matrix, type=2, axis=1, norm='ortho')
    # IDCT2 righe
    result = idct(temp, type=2, axis=0, norm='ortho')
    return result