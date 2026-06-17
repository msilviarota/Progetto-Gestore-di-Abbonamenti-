import sys
import os
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)


# Dichiariamo la RepositoryPreferenze
class RepositoryPreferenze:
    def __init__(self, percorsoFile = "preferenze.json"): 
        self._percorsoFile = percorsoFile


    # Scarichiamo tutte le informazione dalla repository e carichiamole nel file
    def caricaFile(self):
        try:
            with open(self._percorsoFile, "r", encoding="utf-8") as file:
                return json.load(file)        
        except FileNotFoundError:
            return {}


    # Salviamo il file con le nuove informazioni nella repository
    def salvaFile(self, preferenze):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(preferenze, file, indent=4)
    

    # Aggiorniamo le preferenze all'interno della repository
    def aggiornaPreferenze(self, categorieScelte: list):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(categorieScelte, file, indent=4)