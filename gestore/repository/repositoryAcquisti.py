import os
import sys
import json

# Calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from models.abbonamento import Abbonamento


class RepositoryAcquisti:
    def __init__(self, percorsoFile="acquisti.json"): 
        self._percorsoFile = percorsoFile

   
    def caricaFile(self):
        try:
            with open(self._percorsoFile, "r", encoding="utf-8") as file:
                return json.load(file)        
        except FileNotFoundError:
            return {}

  
    def salvaFile(self, storico):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(storico, file, indent=4)

  
    def registra_acquisto(self, email: str, abbonamento: Abbonamento):
        storico_totale = self.caricaFile()
        
        if email not in storico_totale: 
            storico_totale[email] = []
            
        # Convertiamo l'oggetto in dizionario (.to_dict()) prima di salvarlo nel JSON
        storico_totale[email].append(abbonamento.to_dict())
        
        self.salvaFile(storico_totale)

    
    def get_storico_utente(self, email: str):
        storico_totale = self.caricaFile()
        return storico_totale.get(email, [])