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

    # Controlla che F sia compatibile con l'immagine
    if F > img_array.shape[0] or F > img_array.shape[1]:
        raise ValueError(
            f"F troppo grande ({F}) per le dimensioni dell'immagine ({img_array.shape[1]}x{img_array.shape[0]})")

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

    # Salva immagine originale temporanea per calcolare dimensione in byte
    original_temp_path = os.path.join(output_folder, "original_temp.png")
    img.save(original_temp_path)

    # Calcola dimensioni in byte
    original_size = os.path.getsize(original_temp_path)
    compressed_size = os.path.getsize(compressed_path)

    # Crea figura confronto
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Originale
    axs[0].imshow(img_array, cmap='gray', vmin=0, vmax=255)
    axs[0].set_title('Originale')
    axs[0].axis('off')
    axs[0].text(0.5, -0.1, f"Dimensione: {original_size} byte",
                transform=axs[0].transAxes, ha='center', fontsize=10)

    # Compressa
    axs[1].imshow(img_rec, cmap='gray', vmin=0, vmax=255)
    axs[1].set_title(f'Compressa (F={F}, d={d})')
    axs[1].axis('off')
    axs[1].text(0.5, -0.1, f"Dimensione: {compressed_size} byte",
                transform=axs[1].transAxes, ha='center', fontsize=10)

    # Sistema margini per non far tagliare le scritte sotto
    plt.subplots_adjust(top=0.9, bottom=0.2, wspace=0.3)

    # Salva immagine confronto
    comparison_path = os.path.join(output_folder, "comparison.png")
    fig.savefig(comparison_path)
    plt.close(fig)

    # Mostra la figura a schermo
    img_fig = plt.imread(comparison_path)
    plt.figure(figsize=(10, 5))
    plt.imshow(img_fig)
    plt.axis('off')
    plt.show()

    # Rimuove l'immagine originale temporanea
    os.remove(original_temp_path)

    return compressed_path, comparison_path
