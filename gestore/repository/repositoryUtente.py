import os
import json
from models.utente import Utente

class RepositoryUtente:
    def __init__(self): 
        self.utenti = {}
        # Assicurati che questo percorso punti al tuo file JSON reale
        self._percorsoFile = "repository2/utente.json" 

    def caricaFile(self):
        if not os.path.exists(self._percorsoFile):
            return {}
        try:
            with open(self._percorsoFile, "r", encoding="utf-8") as file:
                return json.load(file)        
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def salvaFile(self, utenti_dict):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(utenti_dict, file, indent=4)

    def salva_utente(self, utente: Utente):
        """Salva l'utente nella memoria e sul file JSON."""
        # Salva in memoria
        self.utenti[utente.get_email()] = utente
        # Opzionale: aggiorna anche il JSON subito se necessario
        
    def getInformazioni(self, email):
        """Restituisce l'oggetto Utente se esiste, altrimenti None."""
        return self.utenti.get(email, None)
    
    def aggiornaPassword(self, email, nuova_password_criptata):
        # NOTA: Qui dovresti gestire meglio il passaggio da oggetto Utente a dict JSON
        utente = self.getInformazioni(email)
        if utente :
          utente.set_password(nuova_password_criptata)
          dati_totali = self.caricaFile()
        if email in dati_totali:
           dati_totali[email]["password"]= nuova_password_criptata
           return True
        return False
    
    def verifica(self, email: str):
        """Controlla se l'utente esiste (ritorna True se esiste)."""
        return email in self.utenti