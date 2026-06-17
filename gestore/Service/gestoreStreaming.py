import os
import sys
import webbrowser

# Calcolo automatico della radice del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importiamo le repository necessarie per verificare l'abbonamento dell'utente
from database.repositoryUtente import RepositoryUtente

class GestoreStreaming:
    def __init__(self, repoUtente: RepositoryUtente):
        self._repo_Utente = repoUtente

    def avviaPiattaforma(self, email_utente: str, nome_piattaforma: str, url_piattaforma: str):
        """
        Controlla se l'utente possiede un abbonamento attivo per la piattaforma selezionata.
        Se attivo, apre il browser sul contenuto richiesto. Altrimenti restituisce False.
        """
        # Recuperiamo la lista degli abbonamenti attivi dell'utente dalla Repository
        # Nota: adatta il metodo in base a come è strutturata la tua repositoryUtente
        abbonamenti_attivi = self._repo_Utente.getAbbonamentiAttivi(email_utente)
        
        # Se la piattaforma è tra gli abbonamenti attivi dell'utente
        if nome_piattaforma in abbonamenti_attivi:
            # Il maggiordomo avvia la piattaforma aprendo il link nel browser
            webbrowser.open(url_piattaforma)
            return True, "Avvio della piattaforma in corso..."
        else:
            # L'utente non ha l'abbonamento acquistato o attivo
            return False, f"Accesso negato. Non possiedi un abbonamento attivo per {nome_piattaforma}."
