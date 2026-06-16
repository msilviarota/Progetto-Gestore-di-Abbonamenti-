import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Ora puoi importare utente direttamente senza usare i punti!
from models.abbonamento import Abbonamento


class RepositoryAbbonamento:
    def __init__(self, percorsoFile = "abbonamenti.json"):
        self.attivi = {}   # email -> lista oggetti Abbonamento
        self.scaduti = {}  # email -> lista oggetti Abbonamento
        self._percorsoFile = percorsoFile


    
    def caricaFile(self):
        try:
            with open(self._percorsoFile, "r", encoding="utf-8") as file:
                return json.load(file)        
        except FileNotFoundError:
            return {}


    # Salviamo il file con le nuove informazioni nella repository
    def salvaFile(self, abbonamenti):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(abbonamenti, file, indent=4)


    def salva_abbonamento(self, email: str, abbonamento: Abbonamento):
        abbonamenti = self.caricaFile()
        abbonamenti[abbonamento.get_email()] = abbonamento.to_dict()
        self.salvaFile(abbonamenti)
    
    def elimina_abbonamento(self, abbonamento: Abbonamento):
        abbonamenti = self.caricaFile()
        
    def getAbbonamentiAttivi(self, email):
        return self.attivi.get(email, [])
    
    def getAbbonamentiScaduti(self, email):
        return self.scaduti.get(email, [])
    
    def getAbbonamentiPossibili(self, email):
        return self.attivi.get(email, []) + self.scaduti.get(email, [])
    
