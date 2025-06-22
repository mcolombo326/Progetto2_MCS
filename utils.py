import os
import shutil

import numpy as np

RESULT_DIR = "benchmark_result"
COMPRESSED_IMAGE_DIR = "compressed_image"

def clear_folder(folder):
    if os.path.exists(folder):
        # Rimuove tutti i file dentro la cartella
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # elimina file o link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # elimina cartelle ricorsivamente
    else:
        os.makedirs(folder)

def split_into_blocks(image_array, F):
    H, W = image_array.shape
    H_cropped, W_cropped = H - H % F, W - W % F
    image_cropped = image_array[:H_cropped, :W_cropped]
    blocks = image_cropped.reshape(H_cropped // F, F, W_cropped // F, F).swapaxes(1, 2)
    return blocks

def merge_blocks(blocks):
    n_blocks_y, n_blocks_x, F, _ = blocks.shape
    H, W = n_blocks_y * F, n_blocks_x * F
    image = blocks.swapaxes(1, 2).reshape(H, W)
    return image

def zero_high_freq(coeffs, d):
    F = coeffs.shape[0]
    mask = np.fromfunction(lambda k, l: (k + l) < d, (F, F))
    return coeffs * mask