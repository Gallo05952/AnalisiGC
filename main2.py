import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk
import plotly.graph_objects as go
import numpy as np
import os, json

class Finestra():
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My App")
        self.root.geometry("800x300")
        self.root.resizable(True, True)
        self.variabili = []
        self.Widgets()
        self.root.mainloop()

    def Widgets(self):
        # Titolo finestra
        self.Title = tk.Label(self.root, text="Visualizzazione Dati GC", font=("Arial", 20))
        self.Title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Pulsante per input CSV
        self.InputButton = tk.Button(self.root, text="File Input CSV", command=self.FileInput)
        self.InputButton.grid(row=2, column=0, padx=10, pady=10)

        # Pulsante per input JSON
        self.InputButtonJson = tk.Button(self.root, text="Cartella Input JSON", command=self.FileInputJson)
        self.InputButtonJson.grid(row=3, column=0, padx=10, pady=10)

        # Combobox per selezione variabili
        self.comboBox = ttk.Combobox(self.root, values=self.variabili)
        self.comboBox.grid(row=4, column=0, padx=10, pady=10)

        # Pulsante per visualizzare il grafico
        self.graficoButton = tk.Button(self.root, text="Visualizza Grafico", command=self.Grafico)
        self.graficoButton.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Altre combobox per selezione di variabili aggiuntive
        self.var2 = ttk.Combobox(self.root, values=self.variabili)
        self.var2.grid(row=4, column=1, padx=10, pady=10)

        self.var3 = ttk.Combobox(self.root, values=self.variabili)
        self.var3.grid(row=4, column=2, padx=10, pady=10)

        self.var4 = ttk.Combobox(self.root, values=self.variabili)
        self.var4.grid(row=4, column=3, padx=10, pady=10)

    # Apre una finestra per la selezione del file CSV
    def FileInput(self):
        self.filePath = filedialog.askopenfilename()
        if self.filePath:
            self.OpenFile()

    # Apre e gestisce il file CSV
    def OpenFile(self):
        self.df = pd.read_csv(self.filePath, header=2)
        index = self.df.columns.get_loc("Area")
        self.df = self.df.drop(self.df.columns[index:], axis=1)
        index_NC = self.df.columns.get_loc("NormalizedConcentration")
        index_C = self.df.columns.get_loc("Concentration")
        self.df.columns = list(self.df.iloc[1, :])
        colonne = list(self.df.columns[index_C:])
        colonne_rename = []
        seen = {}

        for col in colonne:
            if col not in seen:
                seen[col] = 0
                colonne_rename.append(col + "C")
            else:
                seen[col] += 1
                if seen[col] == 1:
                    colonne_rename.append(col + "Normalized")
                else:
                    colonne_rename.append(col + f"Normalized{seen[col]}")

        # Rinomina la colonna Sample Name
        nuove_colonne = list(self.df.columns[:index_C]) + colonne_rename
        nuove_colonne[1] = "Sample Name"
        self.df.columns = nuove_colonne
        self.df.drop([0, 1], inplace=True)
        self.df.drop(self.df.tail(1).index, inplace=True)
        self.ColonneDati()

    # Gestisce i dati delle colonne e aggiorna le combobox
    def ColonneDati(self):
        colonneConvertite = self.df.columns[2:]
        for c in colonneConvertite:
            self.df[c] = self.df[c].str.replace(",", ".").astype(float)
        
        # Filtra i dati per rimuovere righe e colonne vuote
        df_filtered = self.df.loc[(self.df != 0).any(axis=1)]
        df_filtered = df_filtered.loc[:, (df_filtered != 0).any(axis=0)]
        self.variabili = list(df_filtered.columns)

        # Aggiorna le combobox con le nuove variabili
        self.comboBox['values'] = self.variabili
        self.var2['values'] = self.variabili
        self.var3['values'] = self.variabili
        self.var4['values'] = self.variabili

    # Visualizza il grafico basato sui dati selezionati
    def Grafico(self):
        variabile_selezionata1 = self.comboBox.get()
        variabile_selezionata2 = self.var2.get()
        variabile_selezionata3 = self.var3.get()
        variabile_selezionata4 = self.var4.get()
        variabili_selezionate = [variabile_selezionata1, variabile_selezionata2, variabile_selezionata3, variabile_selezionata4]
        variabili_selezionate = [v for v in variabili_selezionate if v]
        
        fig = go.Figure()
        for variabile_selezionata in variabili_selezionate:
            fig.add_trace
            fig.add_trace(go.Scatter(x=self.df["Time (GMT 120 mins)"], y=self.df[variabile_selezionata], mode='lines', name=variabile_selezionata))
        
        fig.show()

    # Gestisce il caricamento dei file JSON
    def FileInputJson(self):
        cartella = filedialog.askdirectory()
        file_json = [f for f in os.listdir(cartella) if f.endswith('.fusion-data')]
        dati = []
        for file in file_json:
            with open(os.path.join(cartella, file), 'r') as f:
                df3 = json.load(f)
                moduli = ['moduleA:tcd', 'moduleB:tcd', 'moduleC:tcd']
                time = df3['runTimeStamp']
                for modulo in moduli:
                    for peak in df3['detectors'][modulo]['analysis']['peaks']:
                        if 'label' in peak:
                            dati.append({
                                "Time": time,
                                "Specie Chimica": peak['label'],
                                "Concentrazione Normalizzata": peak['normalizedConcentration'],
                                "Modulo": modulo
                            })
        
        df = pd.DataFrame(dati)
        df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%Y-%m-%d %H:%M')
        df.rename(columns={'Time': 'Time (GMT 120 mins)'}, inplace=True)
        df_pivot = df.pivot_table(index='Time (GMT 120 mins)', columns='Specie Chimica', values='Concentrazione Normalizzata')
        df_pivot = df_pivot.sort_index().reset_index()
        self.df = df_pivot
        variabili = self.df.columns

        # Aggiorna le combobox con le nuove variabili
        self.comboBox['values'] = list(variabili)
        self.var2['values'] = list(variabili)
        self.var3['values'] = list(variabili)
        self.var4['values'] = list(variabili)

if __name__ == "__main__":
    Finestra()
