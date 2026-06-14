import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Ora puoi importare utente direttamente senza usare i punti!
from models import utente



class RepositoryUtente:
    def __init__(self): 
        self.utenti = {} # email -> Oggetto Utente


    def salva_utente(self, utente: utente): 
        self.utenti[utente.get_email()] = utente


    def getInformazioni(self, email):
        if email in self.utenti:
            utente = self.utenti[email]
            return utente
        return None
    

    def aggiornaPassword(self, email, nuova_password):
        if email in self.utenti:
            self.utenti[email] = nuova_password
            return True
        return False
    

    def verifica(self, email):
        return email in self.utenti