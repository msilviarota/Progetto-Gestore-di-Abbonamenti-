import sys
import os
import json
from datetime import datetime 

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

class RepositoryLog:
    def __init__(self, percorsoFile = "logs.json"): 
        self._percorso = percorsoFile
    

    # Scarichiamo tutte le informazione dalla repository e carichiamole nel file
    def caricaFile(self):
        try:
            with open(self._percorsoFile, "r", encoding="utf-8") as file:
                return json.load(file)        
        except FileNotFoundError:
            return {}


    # Salviamo il file con le nuove informazioni nella repository
    def salvaFile(self, testoDelFile):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(testoDelFile, file, indent=4)


    def aggiungi_log(self, emailUtente: str): 
        logs = self.caricaFile()
        logs[datetime.now()] = emailUtente
        self.salvaFile(logs)
        return


    def recuperaUltimoLog(self):
        logs = self.caricaFile()
        ultimo_valore = next(reversed(logs))
        return ultimo_valore
    