import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from database.repositoryUtente import RepositoryUtente
from database.repositoryPreferenze import RepositoryPreferenze
from models.notifica import Notifica


# Ceazione del <<control>> GestorePreferenze
class GestorePreferenze:
    def __init__(self, repoUtente: RepositoryUtente,
                  repoPreferenze: RepositoryPreferenze,
                  notifica: Notifica):
        self._repo_Utente = repoUtente
        self._repo_Preferenze = repoPreferenze
        self._notifica = notifica


    # Riprendiamo le categorie dalla RepositoryPreferenze
    def getPreferenze(self, ):
