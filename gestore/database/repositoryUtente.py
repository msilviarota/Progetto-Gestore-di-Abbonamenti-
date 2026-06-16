import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Ora puoi importare utente direttamente senza usare i punti!
from models.utente import Utente



class RepositoryUtente:
    def __init__(self, percorsoFile = "utenti.json"): 
        self._percorsoFile = percorsoFile


    # Scarichiamo tutte le informazione dalla repository e carichiamole nel file
    def caricaFile(self):
        try:
            with open(self._percorsoFile, "r", encoding="utf-8") as file:
                return json.load(file)        
        except FileNotFoundError:
            return {}


    # Salviamo il file con le nuove informazioni nella repository
    def salvaFile(self, utenti):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(utenti, file, indent=4)


    # Salviamo il nuovo utente che ha effettuato la registrazione
    def salva_utente(self, utente: Utente):
        utenti = self.caricaFile() 
        utenti[utente.get_email()] = utente.to_dict()
        self.salvaFile(utenti)


    # Otteniamo le informazioni dell'utente
    def getInformazioni(self, email):
        utenti = self.caricaFile()
        if email in utenti: 
            return utenti[email]
        return None
    

    # Sostituiamo la precedente password dell'utente con un'altra
    def aggiornaPassword(self, email, nuova_password):
        utenti = self.caricaFile()
        if email in utenti:
            utenti[email]["password"] = nuova_password
            self.salvaFile(utenti)
            return True
        return False
    

    # Verifichiamo che l'email impiegata non sia già associata ad altri utenti
    def verifica(self, email):
        utenti = self.caricaFile()
        return email in utenti