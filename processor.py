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
            f"F troppo grande ({F}) per le dimensioni dell'immagine ({img_array.shape[1]}x{img_array.shape[0]})"
        )

    # Suddivide in blocchi
    blocks = split_into_blocks(img_array, F)
    new_blocks = np.empty_like(blocks)

    # Applica DCT, filtra alte frequenze e IDCT
    for i in range(blocks.shape[0]):
        for j in range(blocks.shape[1]):
            c = dct2_fast(blocks[i, j])
            c_filtered = zero_high_freq(c, d)
            f_rec = idct2_fast(c_filtered)
            f_rec = np.clip(np.round(f_rec), 0, 255)
            new_blocks[i, j] = f_rec

    # Ricostruisce immagine compressa
    img_rec_array = merge_blocks(new_blocks)
    img_rec = Image.fromarray(img_rec_array.astype(np.uint8))

    # Chiama funzione di salvataggio/confronto
    compressed_path, comparison_path = create_output_images(img, img_rec, F, d, output_folder)

    return compressed_path, comparison_path


def create_output_images(original_img, compressed_img, F, d, output_folder):
    """
    Salva immagine compressa, immagine originale temporanea per il calcolo dimensioni,
    genera il grafico di confronto, lo salva e lo mostra a schermo.
    """
    # Percorsi file
    compressed_path = os.path.join(output_folder, "compressed.png")
    original_temp_path = os.path.join(output_folder, "original_temp.png")
    comparison_path = os.path.join(output_folder, "comparison.png")

    # Salva immagini
    compressed_img.save(compressed_path)
    original_img.save(original_temp_path)

    # Calcola dimensioni in byte
    original_size = os.path.getsize(original_temp_path)
    compressed_size = os.path.getsize(compressed_path)

    # Crea figura di confronto
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Originale
    axs[0].imshow(np.array(original_img), cmap='gray', vmin=0, vmax=255)
    axs[0].set_title('Originale')
    axs[0].axis('off')
    axs[0].text(0.5, -0.1, f"Dimensione: {original_size} byte",
                transform=axs[0].transAxes, ha='center', fontsize=10)

    # Compressa
    axs[1].imshow(compressed_img, cmap='gray', vmin=0, vmax=255)
    axs[1].set_title(f'Compressa (F={F}, d={d})')
    axs[1].axis('off')
    axs[1].text(0.5, -0.1, f"Dimensione: {compressed_size} byte",
                transform=axs[1].transAxes, ha='center', fontsize=10)

    # Sistema margini per non far tagliare le scritte sotto
    plt.subplots_adjust(top=0.9, bottom=0.2, wspace=0.3)

    # Salva figura confronto
    fig.savefig(comparison_path)
    plt.close(fig)

    # Mostra la figura a schermo
    img_fig = plt.imread(comparison_path)
    plt.figure(figsize=(10, 5))
    plt.imshow(img_fig)
    plt.axis('off')
    plt.show()

    # Rimuove immagine originale temporanea
    os.remove(original_temp_path)

    return compressed_path, comparison_path
