import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from repository.repositoryUtente import RepositoryUtente
from repository.repositoryPreferenze import RepositoryPreferenze
from Service.gestoreRicerca import GestoreRicerca 
from Service.gestorePreferenze import GestorePreferenze
from models.notifica import Notifica 
from login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    repo_u = RepositoryUtente()
    repo_p = RepositoryPreferenze()
    notifica = Notifica()
    gest_ricerca = GestoreRicerca(None)
    gestore_preferenze = GestorePreferenze(repo_u,repo_p, gest_ricerca , notifica)
    finestra = LoginWindow(gestore_preferenze)
    finestra.show()
    sys.exit(app.exec())