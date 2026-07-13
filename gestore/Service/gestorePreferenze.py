import os
import sys
from datetime import datetime, timedelta

# Calcolo del percorso radice del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__)) 
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path: 
    sys.path.append(radice_progetto)

# Importazioni corrette dai moduli del progetto
from repository.repositoryUtente import RepositoryUtente
from repository.repositoryPreferenze import RepositoryPreferenze
from Service.gestoreRicerca import GestoreRicerca
from models.notifica import Notifica

class GestorePreferenze:
    """
    Gestisce le preferenze dell'utente e i suggerimenti personalizzati 
    (CDU5, CDU10, CDU17, CDU22).
    """

    def __init__(self, repoUtente: RepositoryUtente, repoPreferenze: RepositoryPreferenze, 
                 gestRicerca: GestoreRicerca, notifica: Notifica):
        """Inizializza il gestore con le repository e il sistema di ricerca."""
        self._repo_Utente = repoUtente
        self._repo_Preferenze = repoPreferenze
        self._gest_Ricerca = gestRicerca
        self._notifica = notifica
        self._risultati_suggeriti = []

    def salva_preferenze(self, email_utente: str, nuove_categorie: list):
        """
        CDU5: Aggiorna le preferenze dell'utente (es. Cinema, Musica, Sport).
        Salva la data corrente per monitorare il tempo trascorso (CDU22).
        """
        dati_preferenze = {
            "categorie": nuove_categorie,
            "ultima_modifica": datetime.now().strftime("%Y-%m-%d")
        }
        successo = self._repo_Preferenze.salva_per_utente(email_utente, dati_preferenze)
        if successo:
            self._notifica = Notifica("Preferenze aggiornate con successo.", "Successo")
        return successo


    def ottieni_preferenze(self, email_utente: str):
        """
        Restituisce la lista delle categorie preferite dell'utente.
        Se non esistono preferenze salvate, restituisce una lista vuota.
        """
        dati = self._repo_Preferenze.ottieni_per_utente(email_utente)

        if not dati:
            return []

        # Il repository salva un dizionario: {"categorie": [...], "ultima_modifica": "..."}
        return dati.get("categorie", [])


    def genera_suggerimenti(self, email_utente: str):
        """
        CDU17: Incrocia le preferenze salvate con i database delle piattaforme.
        Se le preferenze sono assenti, non restituisce nulla (Flusso alternativo A).
        """
        preferenze = self._repo_Preferenze.ottieni_per_utente(email_utente)
        
        if not preferenze or not preferenze.get("categorie"):
            self._notifica = Notifica("Nessuna preferenza impostata. Impostale per vedere i consigli.", "Avviso")
            return []

        # Logica di matching: interroga il gestore ricerca per ogni categoria scelta
        self._risultati_suggeriti = []
        
        return self._risultati_suggeriti

    def controlla_sollecitazione_settimanale(self, email_utente: str):
        """
        CDU22: Invia una notifica se è trascorsa una settimana dall'ultima modifica.
        """
        preferenze = self._repo_Preferenze.ottieni_per_utente(email_utente)
        if preferenze and "ultima_modifica" in preferenze:
            ultima_data = datetime.strptime(preferenze["ultima_modifica"], "%Y-%m-%d")
            if datetime.now() > ultima_data + timedelta(days=7):
                self._notifica = Notifica("È passata una settimana: vuoi aggiornare le tue preferenze?", "Suggerimento")
                return True
        return False
