import pandas as pd
import customtkinter as ctk
from tkinter import filedialog
import plotly.express as px


class Finestra():
    
    def __init__(self):
        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue") 
        self.root = ctk.CTk()
        self.root.title("My App")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.variabili=[]
        self.Widgets()
        self.root.mainloop()

    def Widgets(self):
        #* TITOLO FINESTRA
        self.Title=ctk.CTkLabel(self.root, text="Visauluzzazione Dati GC", font=("Arial", 20))
        self.Title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.InputButton=ctk.CTkButton(self.root, text="File Input", command=self.FileInput)
        self.InputButton.grid(row=2, column=0, padx=10, pady=10)

        self.comboBox = ctk.CTkComboBox(self.root, values=self.variabili)
        self.comboBox.grid(row=2, column=1, padx=10, pady=10)

        self.graficoButton = ctk.CTkButton(self.root, text="Visualizza Grafico", command=self.Grafico)
        self.graficoButton.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
             
    #apri una finestra per la selezione del file
    def FileInput(self):
        self.filePath=filedialog.askopenfilename()
        if self.filePath:
            self.OpenFile()

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
                    colonne_rename.append(col + "NC")
                else:
                    colonne_rename.append(col + f"NC{seen[col]}")

        # Rinomina la colonna Sample Name
        nuove_colonne = list(self.df.columns[:index_C]) + colonne_rename
        nuove_colonne[1]= "Sample Name"
        self.df.columns = nuove_colonne
        self.df.drop([0, 1], inplace=True)
        self.df.drop(self.df.tail(1).index, inplace=True)
        print(list(self.df.columns))
        self.ColonneDati()

    def ColonneDati(self):
        colonneConvertite = self.df.columns[2:]
        print(colonneConvertite)
        for c in colonneConvertite:
            self.df[c] = self.df[c].str.replace(",", ".").astype(float)
        # Identifica le righe con almeno un valore diverso da 0
        df_filtered = self.df.loc[(self.df != 0).any(axis=1)]

        # Rimuovi le colonne che contengono solo valori zero
        df_filtered = df_filtered.loc[:, (df_filtered != 0).any(axis=0)]
        self.variabili = list(df_filtered.columns)
        #setta i valori della combobox
        self.comboBox.configure(values=self.variabili)

    def Grafico(self):
        # Recupera la variabile selezionata dalla comboBox
        variabile_selezionata = self.comboBox.get()
        if variabile_selezionata:
            # Crea un grafico interattivo usando Plotly
            fig = px.line(self.df, x="Time (GMT 120 mins)", y=variabile_selezionata, title=f"Grafico della Variabile: {variabile_selezionata}")
            fig.show()
        else:
            print("Nessuna variabile selezionata.")
        #fai un grafico HTML della variabile selezionata
        
        


if __name__ == "__main__":
    Finestra()