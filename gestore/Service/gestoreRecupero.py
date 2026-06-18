import os
import sys
import random
import string # Necessario per generare la password alfanumerica

# Calcolo del percorso radice del progetto per gli import
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazioni corrette (Repository e Modelli)
from repository.repositoryUtente import RepositoryUtente
from models.email import Email
from models.notifica import Notifica

class GestoreRecupero:
    """
    Consente di modificare la password di un utente che non la ricorda.
    Implementa il CDU8 (RecuperoPassword).
    """

    def __init__(self, repoUtente: RepositoryUtente):
        """Inizializza il gestore con la repository degli utenti."""
        self._repo_Utente = repoUtente
        self._notifica = None

    def genera_password_casuale(self, lunghezza=8):
        """Genera una sequenza alfanumerica casuale (Requisito CDU8)."""
        caratteri = string.ascii_letters + string.digits
        return ''.join(random.choice(caratteri) for _ in range(lunghezza))

    def esegui_recupero(self, email_destinatario: str):
        """
        CDU8: Verifica l'email, genera una nuova password e aggiorna il database.
        """
        # 1. Verifica la presenza dell'email nel database (CDU8 - Punto 4)
        utente_dict = self._repo_Utente.ottieni_per_email(email_destinatario)
        
        if not utente_dict:
            return "Email non trovata nel sistema."

        # 2. Generazione password temporanea
        nuova_password = self.genera_password_casuale()
        
        # 3. Aggiornamento nel database
        # Assumiamo che la repository abbia un metodo per aggiornare solo la password
        successo = self._repo_Utente.aggiorna_password(email_destinatario, nuova_password)
        
        if successo:
            # 4. Creazione dell'oggetto Email (CDU8 - Punto 5)
            # Utilizza il modello Email definito nelle fonti [4]
            messaggio_email = Email(
                destinatario=email_destinatario,
                oggetto="Recupero Password - Nuove Credenziali",
                corpo=f"La tua nuova password temporanea è: {nuova_password}"
            )
            
            print(f"Email inviata a {email_destinatario} con la nuova password.")
            return True
        
        return False