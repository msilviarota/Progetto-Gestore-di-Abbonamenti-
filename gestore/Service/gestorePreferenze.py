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
from Service.gestoreRicerca import GestoreRicerca
from models.notifica import Notifica


# Ceazione del <<control>> GestorePreferenze
class GestorePreferenze:
    def __init__(self, repoUtente: RepositoryUtente,
                  repoPreferenze: RepositoryPreferenze,
                  gestRicerca: GestoreRicerca,
                  notifica: Notifica):
        self._repo_Utente = repoUtente
        self._repo_Preferenze = repoPreferenze
        self._gest_Ricerca = gestRicerca
        self._notifica = notifica
        self._risultati = []


    # Riprendiamo le categorie dalla RepositoryPreferenze
    def getPreferenze(self ):
        preferenze = self._repo_Preferenze.getCategorie()
        if preferenze is None:
            return self._notifica.inviaErrore("preferenze non impostate")

        paroleChiave = self._repo_Preferenze.getCategorie()
        
        for parola in paroleChiave:
            self._risultati.append(self._gest_Ricerca.inviaCerca(parola))
        return self._risultati
        

    # Dopo che l'utente ha deciso quale contenuto voluto,
    #  facciamo return del contenuto selezionato
    def inviaSelezione(self, contenutoSelezionato):
        return contenutoSelezionato
    