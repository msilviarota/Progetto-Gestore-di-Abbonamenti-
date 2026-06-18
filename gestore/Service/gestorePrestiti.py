import os
import sys

# Calcolo del percorso radice del progetto per gestire gli import
# Corretto l'uso di __file__ (doppio underscore)
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazioni corrette dai moduli del progetto
from repository.repositoryUtente import RepositoryUtente
from repository.repositoryLog import RepositoryLog
from repository.repositoryAbbonamento import RepositoryAbbonamento
from models.notifica import Notifica

class GestorePrestiti:
    """
    Rappresenta il gestore che si occupa della condivisione temporanea 
    degli abbonamenti tra utenti registrati (CDU11).
    """

    # Corretto il nome del costruttore in __init__
    def __init__(self, repo_utente: RepositoryUtente, repo_abbonamento: RepositoryAbbonamento, 
                 repo_log: RepositoryLog, notifica: Notifica):
        """Inizializza il gestore con le repository necessarie."""
        self._repo_utente = repo_utente
        self._repo_abbonamento = repo_abbonamento
        self._repo_log = repo_log
        self._notifica = notifica

    def presta_abbonamento(self, id_abbonamento: str, email_amico: str):
        """
        CDU11: Permette di prestare un abbonamento a un amico registrato.
        Verifica la presenza dell'amico nel database e invia la notifica di accesso.
        """
        # 1. Recupera l'email dell'utente corrente (il proprietario) dal log di sessione
        email_proprietario = self._repo_log.recuperaUltimoLog()
        
        # 2. Il sistema controlla che l’amico abbia un account sul gestore (CDU11 - Punto 4)
        amico_esistente = self._repo_utente.ottieni_per_email(email_amico)
        
        if not amico_esistente:
            # Flusso alternativo A: Se l'amico non è registrato, invia notifica di errore [3]
            self._notifica = Notifica(f"L'utente {email_amico} non è registrato al gestore.", "Errore")
            print(f"Prestito fallito: {email_amico} non trovato.")
            return False

        # 3. Verifica che l'abbonamento appartenga all'utente e sia attivo
        # (Requisito: L'abbonamento deve permettere la condivisione [2])
        abbonamento = self._repo_abbonamento.ottieni_per_id(id_abbonamento)
        if not abbonamento or abbonamento._email != email_proprietario:
            self._notifica = Notifica("Abbonamento non disponibile per il prestito.", "Errore")
            return False

        # 4. Il sistema invia una notifica di accesso all'amico indicato (CDU11 - Punto 5)
        # In un'implementazione completa, qui si aggiornerebbe anche il database 'prestiti.json'
        successo_msg = f"Accesso all'abbonamento {id_abbonamento} condiviso con {email_amico}."
        self._notifica = Notifica(successo_msg, "Successo")
        print(f"Successo: {successo_msg}")
        
        return True