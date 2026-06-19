import sys
import os
from PyQt6.QtWidgets import QApplication

# Configura il path in modo che 'gestore' sia la radice
percorso_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.dirname(percorso_corrente)
if radice_progetto not in sys.path:
    sys.path.insert(0, radice_progetto)

from intefaccia.login import LoginWindow
from Service.gestoreProfilo import GestoreProfilo
from repository.repositoryUtente import RepositoryUtente
from repository.repositoryLog import RepositoryLog
from repository.repositoryPreferenze import RepositoryPreferenze
from models.notifica import Notifica
from Service.gestoreLogin import GestoreLogin
from Service.gestorePreferenze import GestorePreferenze
from intefaccia.main_window import FinestraPrincipale

def avvia_applicazione():
    app = QApplication(sys.argv)

    # --- Creazione delle dipendenze di backend ---
    repo_utente = RepositoryUtente()
    repo_log = RepositoryLog()
    repo_preferenze = RepositoryPreferenze()
    notifica = Notifica("", "")
    gestore_profilo = GestoreProfilo(repo_utente, notifica)
    gestore_login = GestoreLogin(repo_utente, repo_log, notifica)
    # Nota: GestorePreferenze richiede anche un GestoreRicerca; per ora None
    # (è usato solo in un punto non ancora implementato nel backend)
    gestore_preferenze = GestorePreferenze(repo_utente, repo_preferenze, None, notifica)
    finestra = FinestraPrincipale(gestore_profilo)
    window = LoginWindow(gestore_login=gestore_login, gestore_preferenze=gestore_preferenze)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    avvia_applicazione()