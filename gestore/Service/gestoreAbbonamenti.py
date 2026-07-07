import os
import sys
import json
from datetime import datetime

# Calcolo del percorso radice del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__)) 
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path: 
    sys.path.append(radice_progetto)

# Importazioni dai modelli e repository (coerenti con la struttura cartelle)
from repository.repositoryAbbonamento import RepositoryAbbonamento
from repository.repositoryDatiPagamento import RepositoryDatiPagamento
from Service.gestorePortafoglio import GestorePortafoglio
from models.notifica import Notifica
from models.utente import Utente
from models.abbonamento import Abbonamento
from models.piattaforma import Piattaforma

class GestoreAbbonamenti:
    """
    Rappresenta il «control» Gestore Abbonamenti.
    Gestisce il ciclo di vita degli abbonamenti (CDU1, CDU2, CDU11, CDU12, CDU14).
    """
    
    def __init__(self, utente: Utente, repoAbbonamento: RepositoryAbbonamento, 
                 repoDatiPagamento: RepositoryDatiPagamento, 
                 piattaforma: Piattaforma, notifica: Notifica,gestorePortafoglio: GestorePortafoglio = None):
        """Inizializza il gestore con i dati dell'utente e le repository [5]."""
        self._utente = utente
        self._email_utente = utente._email 
        self.email = utente._email
        self.utente = utente
        self._repo_Abbonamento = repoAbbonamento
        self._repo_DatiPagamento = repoDatiPagamento
        self._piattaforma = piattaforma
        self._notifica = notifica
        self.repoDatiPagamento = repoDatiPagamento
        self._gestore_portafoglio = gestorePortafoglio

    def acquista_abbonamento(self, abbonamento: Abbonamento, importo: float = 0.0):
        """
        CDU1: Consente l'acquisto di un abbonamento inserendo i dati necessari [4, 7].
        Verifica se già acquistato (Flusso alternativo A), controlla il credito
        disponibile e lo scala, poi salva l'abbonamento nel profilo [8, 9].
        """
        # Verifica se l'abbonamento per questa piattaforma è già attivo
        if self._repo_Abbonamento.esiste_abbonamento_attivo(self._email_utente, self._piattaforma.nome):
            self._notifica = Notifica("Abbonamento già acquistato per questa piattaforma.", "Errore") 
            return False

        # Verifica e scala il credito (finto) dell'utente, se il gestore è disponibile
        if self._gestore_portafoglio:
            successo_pagamento = self._gestore_portafoglio.scala_credito(self._email_utente, importo)
            if not successo_pagamento:
                self._notifica = self._gestore_portafoglio._notifica
                return False

        abbonamento._validita = True
        self._repo_Abbonamento.salva_nuovo_abbonamento(abbonamento)
        self._notifica = Notifica("Acquisto completato con successo!", "Successo") 
        return True

    def disdisci_abbonamento(self, id_abbonamento: str):
        """
        CDU2: Interrompe il rinnovo automatico e aggiorna lo stato come 'Disdetto' [9, 11].
        """
        successo = self._repo_Abbonamento.aggiorna_stato(id_abbonamento, "Disdetto")
        if successo:
            self._notifica = Notifica("Abbonamento disdetto correttamente.", "Info")
        return successo

    def presta_abbonamento(self, id_abbonamento: str, email_amico: str):
        """ CDU11: Permette di prestare un abbonamento a un amico registrato [12, 13].
        """
        successo = self._repo_Abbonamento.presta_a_amico(id_abbonamento, email_amico)
        if successo:
            self._notifica = Notifica(f"Accesso condiviso con {email_amico}.", "Info")
        else:
            self._notifica = Notifica("Impossibile registrare il prestito.", "Errore")
        return successo

    def sposta_in_scaduti(self, id_abbonamento: str):
        """
        CDU19: Sposta automaticamente gli abbonamenti non più validi nella sezione 'Scaduti' [14].
        """
        self._repo_Abbonamento.cambia_sezione(id_abbonamento, "Scaduti") 

    def elimina_scaduto(self, id_abbonamento: str):
        """
        CDU14: Consente all'utente di rimuovere i record dalla sezione scaduti [15, 16].
        """
        return self._repo_Abbonamento.rimuovi_record(id_abbonamento) 

    def verifica_tutte_scadenze(self):
        """
        CDU20/21: Il sistema invalida l'accesso passata la data di scadenza.
        """
        lista_abbonamenti = self._repo_Abbonamento.ottieni_per_utente(self._email_utente)
        data_attuale = datetime.now()

        for abb in lista_abbonamenti:
            if abb.get("sezione") == "Scaduti":
                continue
            data_scadenza = datetime.strptime(abb["data_scadenza"], "%Y-%m-%d")
            if data_attuale > data_scadenza:
                self.sposta_in_scaduti(abb["id_abbonamento"])
                self._notifica = Notifica(f"L'abbonamento {abb['piattaforma']} è scaduto.", "Avviso")
    def ottieni_scaduti(self):
        """CDU14/CDU19: Restituisce solo gli abbonamenti nella sezione 'Scaduti' dell'utente."""
        tutti = self._repo_Abbonamento.ottieni_per_utente(self._email_utente)
        return [abb for abb in tutti if abb.get("sezione") == "Scaduti"] 
    def ottieni_tutti(self):
        """CDU13: Restituisce tutti gli abbonamenti (attivi e scaduti) dell'utente."""
        return self._repo_Abbonamento.ottieni_per_utente(self._email_utente)           