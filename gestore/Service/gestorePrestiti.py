from database.repositoryUtente import RepositoryUtente
from database.repositoryLog import RepositoryLog
from database.repositoryAbbonamento import RepositoryAbbonamento
from models.notifica import Notifica


class GestorePrestiti:
    def __init__(self, 
                 repo_utente: RepositoryUtente,
                 repo_abbonamento: RepositoryAbbonamento,
                 repo_log: RepositoryLog,  # Iniettato per una migliore testabilità
                 notifica: Notifica):
        
        self._repo_utente = repo_utente
        self._repo_abbonamento = repo_abbonamento
        self._repo_log = repo_log
        self._notifica = notifica
        
       
        self._email_utente = self._repo_log.recuperaUltimoLog()
    
    def avvia_prestito(self, email_amico: str, id_abbonamento: int):
        """
        Avvia la procedura di condivisione di un abbonamento con un amico.
        """
        # 1. Verifica se l'amico esiste nel sistema
        if not self._repo_utente.verifica(email_amico):
            self._notifica.inviaErrore("Il tuo amico/a deve avere un account Gestore")
            return None

        # 2. Condivide l'abbonamento duplicando i permessi
        self._repo_abbonamento.duplicaPermessiAccesso(
            self._email_utente, 
            email_amico, 
            id_abbonamento
        )
        
        # 3. Invia la notifica di successo e la restituisce
        notifica_ritorno = self._notifica.invia("Abbonamento condiviso correttamente")
        return notifica_ritorno