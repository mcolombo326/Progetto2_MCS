import os
import shutil

RESULT_DIR = "benchmark_result"

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