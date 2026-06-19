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
                 piattaforma: Piattaforma, notifica: Notifica):
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
    def acquista_abbonamento(self, abbonamento: Abbonamento):
        """
        CDU1: Consente l'acquisto di un abbonamento inserendo i dati necessari [4, 7].
        Verifica se già acquistato (Flusso alternativo A) e salva nel profilo [8, 9].
        """
        # Verifica se l'abbonamento per questa piattaforma è già attivo
        if self._repo_Abbonamento.esiste_abbonamento_attivo(self._email_utente, self._piattaforma.get_nome()):
            self._notifica = Notifica("Abbonamento già acquistato per questa piattaforma.", "Errore") 
            return False

        # Simulazione transazione e generazione data scadenza [8]
        # In un'implementazione reale, qui si interagirebbe con repoDatiPagamento
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
        """
        CDU11: Permette di prestare un abbonamento a un amico registrato [12, 13].
        """
        # Verifica descritta nel PDF: l'amico deve avere un account sul gestore [12, 13]
        # (Qui si chiamerebbe una funzione di verifica su RepositoryUtente)
        print(f"Prestito abbonamento {id_abbonamento} a {email_amico} in corso...")
        self._notifica = Notifica(f"Accesso condiviso con {email_amico}.", "Info")
        return True

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
        CDU20/21: Il sistema invalida l'accesso passata la data di scadenza [17, 18].
        """
        lista_abbonamenti = self._repo_Abbonamento.ottieni_per_utente(self._email_utente)
        data_attuale = datetime.now()
        
        for abb in lista_abbonamenti:
            if data_attuale > abb._data_scadenza: # Confronto date [17, 19]
                abb._validita = False
                self.sposta_in_scaduti(abb._id_abbonamento)
                # Invia avviso di scadenza (CDU21) [18]
                self._notifica = Notifica(f"L'abbonamento {abb._piattaforma} è scaduto.", "Avviso")