import sys
import os
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from repository.repositoryLog import RepositoryLog
from models.notifica import Notifica

class RepositoryPreferenze:
    def __init__(self, nome_file="preferenze.json"): 
        cartella_corrente = os.path.dirname(os.path.abspath(__file__))
        self._percorsoFile = os.path.join(cartella_corrente,"..","database",nome_file)
        self._notifica = Notifica()
    # Scarichiamo tutte le informazioni dalla repository e carichiamole nel file
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
    
    # Sovrascriviamo le nuove preferenze a quelle vecchie all'interno della repository
    def aggiornaPreferenze(self,email, categorieScelte: list):
       if not categorieScelte:
           self._notifica.inviaErrore("Nessuna categoria selezionata")
           return False
    
       preferenze_totali = self.caricaFile()
       preferenze_totali[email]= categorieScelte
       self.salvaFile(preferenze_totali)
       self._notifica.invia("preferenze salvate")
       return True
    def getCategorie(self, emailUtente):
        preferenze_totali = self.caricaFile()
        return preferenze_totali.get(emailUtente, [])