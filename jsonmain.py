import pandas as pd
import customtkinter as ctk
from tkinter import filedialog
import glob
import os

class Finestra():
    
    def __init__(self):
        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue") 
        self.root = ctk.CTk()
        self.root.title("My App")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.variabili = []
        self.df = pd.DataFrame()
        self.Widgets()
        self.root.mainloop()

    def Widgets(self):
        #* TITOLO FINESTRA
        self.Title = ctk.CTkLabel(self.root, text="Visualizzazione Dati JSON", font=("Arial", 20))
        self.Title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.InputButton = ctk.CTkButton(self.root, text="Seleziona Cartella", command=self.FolderInput)
        self.InputButton.grid(row=2, column=0, padx=10, pady=10)

        self.comboBox = ctk.CTkComboBox(self.root, values=self.variabili)
        self.comboBox.grid(row=2, column=1, padx=10, pady=10)
             
    # Apri una finestra per la selezione della cartella
    def FolderInput(self):
        self.folderPath = filedialog.askdirectory()
        if self.folderPath:
            self.LoadFiles()

    def LoadFiles(self):
        # Trova tutti i file JSON nella cartella selezionata
        json_files = glob.glob(os.path.join(self.folderPath, "*.fusion-data"))
        
        # Carica e concatena tutti i file JSON in un unico DataFrame
        df_list = []
        for file in json_files:
            try:
                df_temp = pd.read_json(file)
                df_list.append(df_temp)
            except Exception as e:
                print(f"Errore nel caricamento del file {file}: {e}")
        
        if df_list:
            self.df = pd.concat(df_list, ignore_index=True)
            print("Dati caricati correttamente.")
            print(self.df.head())  # Visualizza le prime righe del dataframe caricato
            self.ColonneDati()
        else:
            print("Nessun file JSON caricato.")

    def ColonneDati(self):
        if not self.df.empty:
            colonneConvertite = self.df.columns
            print("Colonne del DataFrame:", colonneConvertite)
            self.variabili = list(colonneConvertite)
            # Setta i valori della combobox
            self.comboBox.configure(values=self.variabili)
        else:
            print("Il dataframe è vuoto.")

if __name__ == "__main__":
    Finestra()
