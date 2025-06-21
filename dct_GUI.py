import tkinter as tk
from tkinter import filedialog, messagebox
from processor import process_image
import os

class ImageCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compressore DCT")

        # Variabili
        self.file_path = None

        # Pulsante per selezionare immagine
        self.load_button = tk.Button(root, text="Carica immagine", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        # Label per mostrare il nome del file caricato
        self.file_label = tk.Label(root, text="Nessun file selezionato")
        self.file_label.grid(row=0, column=1, padx=10, pady=10)

        # Campo input per F
        tk.Label(root, text="Dimensione blocco F:").grid(row=1, column=0, padx=10, pady=5)
        self.F_entry = tk.Entry(root)
        self.F_entry.grid(row=1, column=1, padx=10, pady=5)
        self.F_entry.bind("<KeyRelease>", self.update_d_range)

        # Campo input per d
        tk.Label(root, text="Soglia frequenze d:").grid(row=2, column=0, padx=10, pady=5)
        self.d_entry = tk.Entry(root)
        self.d_entry.grid(row=2, column=1, padx=10, pady=5)

        # Label per range di d
        self.d_range_label = tk.Label(root, text="Range d: n.d.")
        self.d_range_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Pulsante per eseguire la compressione
        self.run_button = tk.Button(root, text="Esegui compressione", command=self.run_compression)
        self.run_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        # Pulsante per salvare l'immagine (inizialmente disabilitato)
        self.save_button = tk.Button(root, text="Salva immagini", state=tk.DISABLED, command=self.save_images)
        self.save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Variabili per percorsi immagine salvata
        self.compressed_path = None
        self.comparison_path = None

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Seleziona immagine BMP", filetypes=[("BMP files", "*.bmp")])
        if file_path:
            self.file_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=filename)

    def update_d_range(self, event=None):
        try:
            F = int(self.F_entry.get())
            max_d = 2 * F - 2
            self.d_range_label.config(text=f"Range d: 0 ≤ d ≤ {max_d}")
        except ValueError:
            self.d_range_label.config(text="Range d: n.d.")

    def run_compression(self):
        if not self.file_path:
            messagebox.showerror("Errore", "Seleziona prima un'immagine.")
            return

        try:
            F = int(self.F_entry.get())
            d = int(self.d_entry.get())
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori interi per F e d.")
            return

        if not (0 <= d <= 2 * F - 2):
            messagebox.showerror("Errore", f"Il valore di d deve essere tra 0 e {2 * F - 2}.")
            return

        compressed_path, comparison_path = process_image(self.file_path, F, d)

        self.compressed_path = compressed_path
        self.comparison_path = comparison_path

        messagebox.showinfo("Output salvato", f"Immagini salvate nella cartella 'Compression':\n"
                                              f"- compressa: {compressed_path}\n"
                                              f"- confronto: {comparison_path}")

        # Abilita il pulsante di salvataggio (puoi decidere se serve o meno)
        self.save_button.config(state=tk.NORMAL)

    def save_images(self):
        # Facoltativo: puoi implementare un salvataggio altrove o notifiche
        messagebox.showinfo("Salvataggio", f"Immagini già salvate in:\n{self.compressed_path}\n{self.comparison_path}")

def run_gui():
    root = tk.Tk()
    app = ImageCompressorGUI(root)
    root.mainloop()
