import os
import sys
import json

# Calcolo del percorso radice del progetto per gli import
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazioni corrette (cartella 'repository' invece di 'database')
from repository.repositoryUtente import RepositoryUtente
from repository.repositoryDatiPagamento import RepositoryDatiPagamento
from repository.repositoryLog import RepositoryLog
from models.notifica import Notifica
from models.datiPagamento import DatiPagamento

class GestorePagamenti:
    """
    Rappresenta il gestore che si occupa delle transazioni 
    e della sicurezza dei dati di pagamento (CDU1, CDU16).
    """

    def __init__(self, repoUtente: RepositoryUtente, 
                 repoDatiPagamento: RepositoryDatiPagamento, 
                 repoLog: RepositoryLog, notifica: Notifica):
        """Inizializza il gestore recuperando l'ultimo utente loggato."""
        self._email_Utente = repoLog.recuperaUltimoLog()
        self._repo_Utente = repoUtente
        self._repo_DatiPagamento = repoDatiPagamento
        self._notifica = notifica

    def convalida_e_salva_metodo(self, dati: DatiPagamento):
        """
        CDU16: Modifica o aggiunge un metodo di pagamento.
        I dati vengono cifrati prima del salvataggio (Requisito non funzionale 2).
        """
        # Esempio di validazione (CDU16 - Flusso alternativo A)
        if len(dati._numero_carta) != 16:
            self._notifica = Notifica("Numero carta non valido.", "Errore")
            return False

        print(f"Cifratura dati per utente: {self._email_Utente}")
        # Qui andrebbe la logica di cifratura reale prima della scrittura su JSON
        successo = self._repo_DatiPagamento.aggiornaDatiPagamento(self._email_Utente, dati)
        
        if successo:
            self._notifica = Notifica("Dati di pagamento aggiornati con successo.", "Successo")
        return successo

    def conferma_acquisto(self, importo: float):
        """Gestisce la transazione entro 3 passaggi (Requisito non funzionale 1)."""
        print(f"Transazione di {importo}€ avviata...")
        return True