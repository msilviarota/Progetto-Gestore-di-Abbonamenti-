import os
import sys
import random # Necessario per generare il codice identificativo (CDU3)

# Calcolo del percorso radice del progetto per gestire gli import
# Corretto l'uso di __file__ (doppio underscore)
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazioni corrette dai moduli del progetto
from repository.repositoryUtente import RepositoryUtente
from models.utente import Utente
from models.notifica import Notifica

class GestoreRegistrazione:
    """
    Rappresenta il gestore che si occupa della creazione di nuovi profili (CDU3).
    """

    def __init__(self, repo_utente: RepositoryUtente, notifica: Notifica):
        """Inizializza il gestore con la repository degli utenti."""
        self._repo_utente = repo_utente
        self._notifica = notifica

    def genera_codice_identificativo(self):
        """Genera un codice identificativo univoco per l'utente (Requisito 1.1.2)."""
        return f"ID-{random.randint(1000, 9999)}"

    def registra_nuovo_utente(self, nome, cognome, eta, email, password, conferma_password):
        """
        CDU3: Valida i dati e crea un nuovo profilo utente nel database.
        """
        # 1. Verifica che la password e la conferma coincidano (Requisito 1.1.1)
        if password != conferma_password:
            self._notifica = Notifica("Le password inserite non coincidono.", "Errore")
            return None

        # 2. Flusso alternativo A: Verifica se l'email è già associata a un account
        utente_esistente = self._repo_utente.ottieni_per_email(email)
        if utente_esistente:
            self._notifica = Notifica("Email già registrata. Accedi o usa un'altra email.", "Errore")
            return None

        # 3. Creazione dell'oggetto Modello Utente (CDU3 - Punto 3)
        nuovo_utente = Utente(
            nome=nome,
            cognome=cognome,
            eta=int(eta),
            email=email,
            password=password
        )

        # 4. Salvataggio nel database tramite Repository
        successo = self._repo_utente.aggiungi_utente(nuovo_utente)
        
        if successo:
            # 5. Il sistema restituisce un codice identificativo (Requisito 1.1.2)
            codice_id = self.genera_codice_identificativo()
            self._notifica = Notifica(f"Registrazione completata! Il tuo codice è: {codice_id}", "Successo")
            print(f"Utente {email} registrato con successo. Codice: {codice_id}")
            return codice_id
        
        self._notifica = Notifica("Errore tecnico durante il salvataggio dei dati.", "Errore")
        return None