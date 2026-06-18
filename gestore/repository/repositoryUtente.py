import os
import json
import sys

# Calcolo del percorso radice del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from models.utente import Utente

class RepositoryUtente:
    """
    Gestisce il salvataggio e il recupero dei dati degli utenti nel file JSON.
    """

    def __init__(self):
        # Percorso robusto verso la cartella repository2
        self._cartella_dati = os.path.join(radice_progetto, "repository2")
        self._percorso_file = os.path.join(self._cartella_dati, "utente.json")
        
        # Crea la cartella repository2 se non esiste (sicurezza aggiuntiva)
        if not os.path.exists(self._cartella_dati):
            os.makedirs(self._cartella_dati)
            
        # Carica i dati all'avvio
        self._utenti = self._carica_dati()

    def _carica_dati(self):
        """Legge il file JSON e restituisce un dizionario di utenti."""
        if not os.path.exists(self._percorso_file):
            return {}
        try:
            with open(self._percorso_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def salva_tutto(self):
        """Scrive l'intero dizionario utenti sul file JSON."""
        with open(self._percorso_file, "w", encoding="utf-8") as f:
            json.dump(self._utenti, f, indent=4, ensure_ascii=False)

    def ottieni_per_email(self, email):
        """Recupera i dati di un utente tramite la sua email (chiave primaria)."""
        return self._utenti.get(email)

    def aggiungi_utente(self, utente: Utente):
        """Salva un nuovo oggetto Utente nel database JSON."""
        self._utenti[utente._email] = {
            "nome": utente._nome,
            "cognome": utente._cognome,
            "eta": utente._eta,
            "email": utente._email,
            "password": utente._password # Nota: in produzione andrebbe hashata
        }
        self.salva_tutto()
        return True

    def aggiorna_utente(self, utente: Utente):
        """Aggiorna i dati di un utente esistente."""
        return self.aggiungi_utente(utente)

    def aggiorna_password(self, email, nuova_password):
        """CDU8/CDU9: Aggiorna specificamente la password di un utente."""
        if email in self._utenti:
            self._utenti[email]["password"] = nuova_password
            self.salva_tutto()
            return True
        return False