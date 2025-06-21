from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

from dct2.dct2_fast import dct2_fast, idct2_fast
from utils import split_into_blocks, merge_blocks, zero_high_freq, clear_folder, COMPRESSED_IMAGE_DIR


def process_image(filename, F, d, output_folder=COMPRESSED_IMAGE_DIR):
    # Svuota o crea la cartella output
    clear_folder(output_folder)

    # Carica immagine e converte in scala di grigi
    img = Image.open(filename).convert('L')
    img_array = np.array(img, dtype=np.float32)
    blocks = split_into_blocks(img_array, F)

    new_blocks = np.empty_like(blocks)

    for i in range(blocks.shape[0]):
        for j in range(blocks.shape[1]):
            c = dct2_fast(blocks[i, j])
            c_filtered = zero_high_freq(c, d)
            f_rec = idct2_fast(c_filtered)
            f_rec = np.clip(np.round(f_rec), 0, 255)
            new_blocks[i, j] = f_rec

    img_rec_array = merge_blocks(new_blocks)
    img_rec = Image.fromarray(img_rec_array.astype(np.uint8))

    # Salva immagine compressa
    compressed_path = os.path.join(output_folder, "compressed.png")
    img_rec.save(compressed_path)

    # Crea figura confronto
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(img_array, cmap='gray', vmin=0, vmax=255)
    axs[0].set_title('Originale')
    axs[0].axis('off')

    axs[1].imshow(img_rec, cmap='gray', vmin=0, vmax=255)
    axs[1].set_title(f'Compressa (F={F}, d={d})')
    axs[1].axis('off')

    plt.tight_layout()

    # Salva immagine confronto
    comparison_path = os.path.join(output_folder, "comparison.png")
    fig.savefig(comparison_path)
    plt.close(fig)  # Chiude la figura per evitare finestre aperte multiple

    return compressed_path, comparison_path
