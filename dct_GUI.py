import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from processor import process_image
import os

class ImageCompressorGUI:
    def __init__(self, root):  # <-- CORRETTO: era "_init_" con un solo underscore
        self.root = root
        self.root.title("Compressore DCT")

        self.file_path = None

        # Frame principale
        main_frame = ttk.Frame(root, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # RIGA 0: Titolo centrato
        title_label = ttk.Label(main_frame, text="Compressore DCT", font=("Arial", 18, "bold"), anchor="center")
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")

        # RIGA 1: Pulsante carica immagine
        self.load_button = ttk.Button(main_frame, text="Carica immagine", command=self.load_image)
        self.load_button.grid(row=1, column=0, pady=5, sticky="ew")

        # RIGA 2: Etichetta file selezionato
        self.file_label = ttk.Label(main_frame, text="Nessun file selezionato", anchor="center")
        self.file_label.grid(row=2, column=0, pady=(0, 15), sticky="ew")

        # RIGA 3: Label F centrata
        self.f_label = ttk.Label(main_frame, text="Dimensione blocco F:", anchor="center")
        self.f_label.grid(row=3, column=0, pady=(0, 2), sticky="ew")

        # RIGA 4: Entry F
        self.F_entry = ttk.Entry(main_frame, justify="center")
        self.F_entry.grid(row=4, column=0, pady=(0, 10), sticky="ew")
        self.F_entry.bind("<KeyRelease>", self.update_d_range)

        # RIGA 5: Range d dinamico
        self.d_range_label = ttk.Label(main_frame, text="Range d: n.d.", anchor="center")
        self.d_range_label.grid(row=5, column=0, pady=(0, 10), sticky="ew")

        # RIGA 6: Label soglia d
        self.d_label = ttk.Label(main_frame, text="Soglia frequenze d:", anchor="center")
        self.d_label.grid(row=6, column=0, pady=(0, 2), sticky="ew")

        # RIGA 7: Entry d
        self.d_entry = ttk.Entry(main_frame, justify="center")
        self.d_entry.grid(row=7, column=0, pady=(0, 20), sticky="ew")

        # RIGA 8: Pulsante esegui compressione
        self.run_button = ttk.Button(main_frame, text="Esegui compressione", command=self.run_compression)
        self.run_button.grid(row=8, column=0, pady=10, sticky="ew")

        # RIGA 9: Visualizzazione immagine risultante
        self.image_label = ttk.Label(main_frame)
        self.image_label.grid(row=9, column=0, pady=(10, 0), sticky="ew")

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

        # Mostra l'immagine di confronto
        img = Image.open(comparison_path)

        # Adatta esattamente alle dimensioni desiderate (finestra fissa 900x700)
        target_width = 860  # spazio interno stimato (900 - padding/margini)
        target_height = 400  # altezza ideale per l’immagine

        # Ridimensiona con proporzioni mantenute
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height

        if img_ratio > target_ratio:
            new_width = target_width
            new_height = int(target_width / img_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * img_ratio)

        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        self.comparison_img_tk = ImageTk.PhotoImage(resized_img)
        self.image_label.config(image=self.comparison_img_tk)
        self.image_label.image = self.comparison_img_tk

        messagebox.showinfo("Completato", "Compressione completata.\nImmagini salvate nella cartella di output.")
def run_gui():
    root = tk.Tk()
    # Dimensioni fisse della finestra
    window_width = 900
    window_height = 700
    # Ottieni dimensioni dello schermo
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Calcola posizione per centrare
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    # Imposta dimensioni e posizione centrata
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)
    app = ImageCompressorGUI(root)
    root.mainloop()
