import sys
import os

cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, "..", "gestore"))
sys.path.insert(0, radice_progetto)

from repository.repositoryUtente import RepositoryUtente
from repository.repositoryLog import RepositoryLog
from models.notifica import Notifica
from Service.registrazione import GestoreRegistrazione
from Service.gestoreLogin import GestoreLogin

# --- Setup ---
repo_utente = RepositoryUtente()
repo_log = RepositoryLog()
notifica = Notifica("", "")

gestore_reg = GestoreRegistrazione(repo_utente, notifica)
gestore_login = GestoreLogin(repo_utente, repo_log, notifica)

EMAIL_TEST = "silvia@email.com"
PASSWORD_TEST = "password123"

# --- 1. Registrazione (salta se l'utente esiste già) ---
if repo_utente.ottieni_per_email(EMAIL_TEST):
    print(f"Utente {EMAIL_TEST} già esistente, salto la registrazione.")
else:
    codice = gestore_reg.registra_nuovo_utente(
        nome="Silvia",
        cognome="Test",
        eta=22,
        email=EMAIL_TEST,
        password=PASSWORD_TEST,
        conferma_password=PASSWORD_TEST
    )
    print("Codice ricevuto:", codice)

# --- 2. Login con le stesse credenziali ---
risultato = gestore_login.verifica_accesso(EMAIL_TEST, PASSWORD_TEST)
print("Risultato login:", risultato)