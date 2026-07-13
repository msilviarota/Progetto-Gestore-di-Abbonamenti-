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
from repository.repositoryDatiPagamento import RepositoryDatiPagamento 
from repository.repositoryPortafoglio import RepositoryPortafoglio
from Service.gestorePortafoglio import GestorePortafoglio
from models.notifica import Notifica
from Service.gestoreLogin import GestoreLogin
from Service.gestorePreferenze import GestorePreferenze
from intefaccia.main_window import FinestraPrincipale
from Service.registrazione import GestoreRegistrazione
from intefaccia.stile import STILE_MESSAGEBOX

def avvia_applicazione():
    app = QApplication(sys.argv)
    app.setStyleSheet(STILE_MESSAGEBOX)

    # --- Creazione delle dipendenze di backend ---
    repo_utente = RepositoryUtente()
    repo_log = RepositoryLog()
    repo_preferenze = RepositoryPreferenze()
    repo_dati_pagamento = RepositoryDatiPagamento()
    repo_portafoglio = RepositoryPortafoglio()
    notifica = Notifica("", "")
    gestore_profilo = GestoreProfilo(repo_utente, notifica, repo_dati_pagamento)
    gestore_login = GestoreLogin(repo_utente, repo_log, notifica)
    gestore_preferenze = GestorePreferenze(repo_utente, repo_preferenze, repo_dati_pagamento, notifica)
    gestore_portafoglio = GestorePortafoglio(repo_portafoglio, notifica)
    gestore_registrazione = GestoreRegistrazione(repo_utente, notifica)

    window = LoginWindow(
        gestore_login=gestore_login,
        gestore_preferenze=gestore_preferenze,
        gestore_profilo=gestore_profilo,
        gestore_abbonamenti=None,
        gestore_registrazione=gestore_registrazione,
        repo_dati_pagamento=repo_dati_pagamento,
        gestore_portafoglio=gestore_portafoglio
    )
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    avvia_applicazione()

