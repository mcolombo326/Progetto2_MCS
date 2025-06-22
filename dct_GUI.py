import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from processor import process_image
import os

class ImageCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compressore DCT")

        self.file_path = None

        main_frame = ttk.Frame(root, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Titolo centrato (riga 0)
        title_label = ttk.Label(main_frame, text="Compressore DCT", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        # Pulsante carica (riga 1)
        self.load_button = ttk.Button(main_frame, text="Carica immagine", command=self.load_image)
        self.load_button.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        # Etichetta nome file sotto il pulsante (riga 2), centrata orizzontalmente
        self.file_label = ttk.Label(main_frame, text="Nessun file selezionato", anchor="center")
        self.file_label.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        # Label F (riga 3, col 0)
        ttk.Label(main_frame, text="Dimensione blocco F:").grid(row=3, column=0, sticky="w", padx=5)

        # Entry F (riga 4, col 0), centrata
        self.F_entry = ttk.Entry(main_frame, justify="center")
        self.F_entry.grid(row=4, column=0, padx=5, pady=(0,10), sticky="ew")

        # Label d con range (riga 3, col 1)
        d_label_frame = ttk.Frame(main_frame)
        d_label_frame.grid(row=3, column=1, sticky="ew", padx=5)

        self.d_label = ttk.Label(d_label_frame, text="Soglia frequenze d:")
        self.d_label.pack(side="left")

        self.d_range_label = ttk.Label(d_label_frame, text="Range d: n.d.")
        self.d_range_label.pack(side="right")

        # Entry d (riga 4, col 1), centrata
        self.d_entry = ttk.Entry(main_frame, justify="center")
        self.d_entry.grid(row=4, column=1, padx=5, pady=(0,10), sticky="ew")

        # Pulsante esegui compressione (riga 5, col 0 e 1)
        self.run_button = ttk.Button(main_frame, text="Esegui compressione", command=self.run_compression)
        self.run_button.grid(row=5, column=0, columnspan=2, pady=20, sticky="ew")

        # Configura il peso delle colonne per farle espandere correttamente
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)



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

        try:
            compressed_path, comparison_path = process_image(self.file_path, F, d)
        except ValueError as e:
            messagebox.showerror("Errore", str(e))
            return

        # Mostra l'immagine di confronto dentro Tkinter
        img = Image.open(comparison_path)
        img.thumbnail((600, 300))  # opzionale, per ridimensionare e adattare
        self.comparison_img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.comparison_img_tk)

        messagebox.showinfo("Completato", "Compressione completata.\nImmagini salvate nella cartella di output.")

def run_gui():
    root = tk.Tk()
    app = ImageCompressorGUI(root)
    root.mainloop()
