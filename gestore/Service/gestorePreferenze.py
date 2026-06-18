import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from repository.repositoryUtente import RepositoryUtente
from repository.repositoryPreferenze import RepositoryPreferenze
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
    def getPreferenze(self,emailUtente):
        # 1. Reset dei risultati per evitare duplicazioni
        self._risultati = []
        
        # 2. Recupero categorie una sola volta
        paroleChiave = self._repo_Preferenze.getCategorie(emailUtente)
        
        if not paroleChiave: # Verifica se la lista è vuota o None
            self._notifica.inviaErrore("Preferenze non impostate")
            return [] # Restituiamo una lista vuota per evitare crash dell'interfaccia
        
        # 3. Ciclo di ricerca
        for parola in paroleChiave:
            risultato = self._gest_Ricerca.inviaCerca(parola,"youtube")
            if risultato: # Aggiungiamo solo se la ricerca ha dato esito positivo
                self._risultati.append(risultato)
                
        return self._risultati
    def inviaSelezione(self, contenutoSelezionato):
        return contenutoSelezionato
    