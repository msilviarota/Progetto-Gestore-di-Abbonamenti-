import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
# Importa i gestori
from Service.gestoreAbbonamenti import GestoreAbbonamenti 
from Service.gestoreRicerca import GestoreRicerca 
from Service.gestorePreferenze import GestorePreferenze
# Importa le repository
from repository.repositoryUtente import RepositoryUtente
from repository.repositoryPreferenze import RepositoryPreferenze
from repository.repositoryAbbonamento import RepositoryAbbonamento
from repository.repositoryDatiPagamento import RepositoryDatiPagamento
# Importa modelli e altro
from models.notifica import Notifica 
from models import piattaforma
from login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Inizializzazione Repository
    repo_u = RepositoryUtente()
    repo_p = RepositoryPreferenze()
    repo_a = RepositoryAbbonamento()
    repo_d = RepositoryDatiPagamento()
    notifica = Notifica()
    
    # Inizializzazione Gestori
    gest_ricerca = GestoreRicerca(None)
    gestore_preferenze = GestorePreferenze(repo_u, repo_p, gest_ricerca, notifica)
    
    gestore_abbonamenti = GestoreAbbonamenti(
        utente=None, 
        repoAbbonamento=repo_a,
        repoDatiPagamento=repo_d,
        nomePiattaforma=piattaforma, 
        notifica=notifica # Corretto da 'notidica' a 'notifica'
    )
    
    # Avvio applicazione
    finestra = LoginWindow(gestore_preferenze, gestore_abbonamenti) # Passa entrambi
    finestra.show()
    sys.exit(app.exec())