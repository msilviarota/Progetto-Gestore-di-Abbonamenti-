import os
import sys
import json

# Calcolo del percorso radice del progetto per gli import
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazioni corrette dalle repository e modelli
from repository.repositoryUtente import RepositoryUtente
from models.utente import Utente
from models.notifica import Notifica

class GestoreProfilo:
    """
    Gestisce le operazioni legate al profilo utente (CDU7, CDU9, CDU16).
    """

    def __init__(self, repoUtente: RepositoryUtente, notifica: Notifica):
        """Inizializza il gestore con la repository degli utenti."""
        self._repo_Utente = repoUtente
        self._notifica = notifica

    def ottieni_dati_utente(self, email: str):
        """
        CDU7: Recupera i dati completi dell'utente dal database.
        """
        utente_dict = self._repo_Utente.ottieni_per_email(email)
        if utente_dict:
            # Crea un oggetto modello Utente dai dati grezzi
            return Utente(
                nome=utente_dict.get('nome'),
                cognome=utente_dict.get('cognome'),
                eta=utente_dict.get('eta'),
                email=utente_dict.get('email'),
                password=utente_dict.get('password')
            )
        return None

    def aggiorna_dati_personali(self, utente_aggiornato: Utente):
        """
        Permette di modificare nome, cognome ed età dell'utente.
        """
        successo = self._repo_Utente.aggiorna_utente(utente_aggiornato)
        if successo:
            self._notifica = Notifica("Profilo aggiornato con successo.", "Successo")
        else:
            self._notifica = Notifica("Errore durante l'aggiornamento del profilo.", "Errore")
        return successo

    def cambia_password_utente(self, email: str, vecchia_pass: str, nuova_pass: str):
        """
        CDU9: Gestisce il cambio password verificando la corrispondenza 
        con quella attuale.
        """
        utente = self.ottieni_dati_utente(email)
        if utente and utente._password == vecchia_pass:
            utente._password = nuova_pass
            self._repo_Utente.aggiorna_utente(utente)
            self._notifica = Notifica("Password cambiata correttamente.", "Successo")
            return True
        
        self._notifica = Notifica("La vecchia password non è corretta.", "Errore")
        return False
    def cambia_carta_utente(self, email: str, vecchia: str, nuova: str):
        utente = self.ottieni_dati_utente(email)

        if utente and utente._carta == vecchia:
         utente._carta = nuova
         self._repo_Utente.aggiorna_utente(utente)
         self._notifica = Notifica("Carta aggiornata correttamente.", "Successo")
         return True

        self._notifica = Notifica("Il vecchio numero carta non è corretto.", "Errore")
        return False
