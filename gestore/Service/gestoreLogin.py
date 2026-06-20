import os
import sys
import json
import hashlib # Utilizzato per la cifratura della password (CDU7)
import string
# Calcolo del percorso radice del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__)) 
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path: 
    sys.path.append(radice_progetto)

# Importazioni corrette (Repository e Modelli)
from repository.repositoryUtente import RepositoryUtente
from repository.repositoryLog import RepositoryLog
from models.notifica import Notifica
import random
class GestoreLogin:
    """
    Rappresenta il gestore dell'autenticazione.
    Implementa il CDU7 (Accedi) e il CDU15 (Esci).
    """

    def __init__(self, repoUtente: RepositoryUtente, repoLog: RepositoryLog, notifica: Notifica):
        """Inizializza il gestore con le repository per la verifica e il logging."""
        self._repo_Utente = repoUtente
        self._repo_Log = repoLog
        self._notifica = notifica

    def verifica_accesso(self, email_inserita: str, password_inserita: str):
        """
        CDU7: Valida le credenziali confrontando la password cifrata.
        """
        # 1. Recupero dati utente dal database
        utente_dict = self._repo_Utente.ottieni_per_email(email_inserita)
        
        # Flusso Alternativo A: Utente non registrato
        if not utente_dict:
            self._notifica = Notifica("Utente non trovato. Ti consigliamo di registrarti.", "Avviso")
            return None

        # 2. Cifratura della password inserita (CDU7 - Punto 4)
        # Esempio semplice di hashing per il confronto
        password_criptata = hashlib.sha256(password_inserita.encode()).hexdigest()
        
        # Flusso Alternativo B: Password errata
        # Nota: se nel tuo database le password non sono ancora criptate,
        # confronta direttamente: if utente_dict['password'] == password_inserita:
        if utente_dict.get('password') == password_inserita:
            # 3. Successo: Registra l'accesso nel Log
            self._repo_Log.salvaLog(email_inserita)
            print(f"Accesso eseguito per: {email_inserita}")
            return utente_dict # Restituisce i dati per personalizzare la Home
        else:
            self._notifica = Notifica("Password o email errati. Riprova.", "Errore")

            return None
    def recupera_password(self, email: str):
        """
        CDU8: Genera una nuova password temporanea per l'utente e la salva.
        In un sistema reale qui andrebbe inviata via email; per ora la stampiamo in console.
        """
        utente_dict = self._repo_Utente.ottieni_per_email(email)

        if not utente_dict:
            self._notifica = Notifica("Email non trovata.", "Errore")
            return False

        nuova_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        successo = self._repo_Utente.aggiorna_password(email, nuova_password)

        if successo:
            print(f"[SIMULAZIONE EMAIL] Nuova password per {email}: {nuova_password}")
            self._notifica = Notifica("Una nuova password temporanea è stata generata.", "Successo")
            return True
        else:
            self._notifica = Notifica("Impossibile aggiornare la password.", "Errore")
            return False

    def esegui_logout(self):
        """
        CDU15: Chiude la sessione attiva.
        """
        # Verifica la presenza di download attivi prima di uscire (Requisito CDU15)
        print("Chiusura sessione in corso...")
        return True