import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Ora puoi importare utente direttamente senza usare i punti!
from models import abbonamento


class RepositoryAbbonamenti:
    def __init__(self):
        self.attivi = {}   # email -> lista oggetti Abbonamento
        self.scaduti = {}  # email -> lista oggetti Abbonamento

    def salva_abbonamento(self, email: str, abbonamento: abbonamento):
        if email not in self.attivi: 
            self.attivi[email] = []
            self.attivi[email].append(abbonamento)
        else:
            self.attivi[email].append(abbonamento)

    def getAbbonamentiAttivi(self, email):
        return self.attivi.get(email, [])