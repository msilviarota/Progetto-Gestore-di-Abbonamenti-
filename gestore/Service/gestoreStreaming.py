import os
import sys

# Calcolo automatico della radice del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)
from repository.repositoryAbbonamento import RepositoryAbbonamento
from repository.repositoryDati import RepositoryDati
from models.piattaforma import Piattaforma
from models.notifica import Notifica

class GestoreStreaming:
    def __init__(self, repoDati: RepositoryDati, repoAbb: RepositoryAbbonamento, piattaforma: Piattaforma):
        self._repo_Dati = repoDati
        self._repo_Abb = repoAbb  
        self._piattaforma_esterna = piattaforma
        self._notifiche = Notifica()

    def avviaPiattaforma(self, email_utente: str, password_utente: str, nome_contenuto: str):
        abbonamenti = self._repo_Abb.getAbbonamentiAttivi(email_utente)
        if not abbonamenti:
            self._notifiche.inviaErrore("Abbonamento non valido o scaduto.")
            return "errore", "Abbonamento scaduto"
        self._piattaforma_esterna.trasmettiDati(nome_contenuto, "Dati_Abbonamento")
        return "successo", (nome_contenuto, "Piattaforma Pronta")
        