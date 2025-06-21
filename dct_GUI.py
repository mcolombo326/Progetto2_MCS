import tkinter as tk
from tkinter import filedialog, messagebox
from processor import process_image
import os

class ImageCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compressore DCT")

        self.file_path = None

        # Pulsante per selezionare immagine
        self.load_button = tk.Button(root, text="Carica immagine", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        self.file_label = tk.Label(root, text="Nessun file selezionato")
        self.file_label.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Dimensione blocco F:").grid(row=1, column=0, padx=10, pady=5)
        self.F_entry = tk.Entry(root)
        self.F_entry.grid(row=1, column=1, padx=10, pady=5)
        self.F_entry.bind("<KeyRelease>", self.update_d_range)

        tk.Label(root, text="Soglia frequenze d:").grid(row=2, column=0, padx=10, pady=5)
        self.d_entry = tk.Entry(root)
        self.d_entry.grid(row=2, column=1, padx=10, pady=5)

        self.d_range_label = tk.Label(root, text="Range d: n.d.")
        self.d_range_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.run_button = tk.Button(root, text="Esegui compressione", command=self.run_compression)
        self.run_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

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

        # Esegue compressione e salva direttamente
        process_image(self.file_path, F, d)

        messagebox.showinfo("Completato", "Compressione completata.\nImmagini salvate nella cartella di output.")

def run_gui():
    root = tk.Tk()
    app = ImageCompressorGUI(root)
    root.mainloop()
