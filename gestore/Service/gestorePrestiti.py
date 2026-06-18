from repository.repositoryUtente import RepositoryUtente
from repository.repositoryLog import RepositoryLog
from repository.repositoryAbbonamento import RepositoryAbbonamento
from models.notifica import Notifica


class GestorePrestiti:
    def __init__(self, 
                 repo_utente: RepositoryUtente,
                 repo_abbonamento: RepositoryAbbonamento,
                 repo_log: RepositoryLog,  
                 notifica: Notifica):
        
        self._repo_utente = repo_utente
        self._repo_abbonamento = repo_abbonamento
        self._repo_log = repo_log
        self._notifica = notifica
    
    def avvia_prestito(self, email_amico: str,nome_piattaforma: int):
        """
        Avvia la procedura di condivisione di un abbonamento con un amico.
        """
        # 1. Verifica se l'amico esiste nel sistema
        email_utente = self._repo_log.recuperaUltimoLog()
        if not email_utente:
            self._notifica.inviaErrore("Errore: sessione utente non trovata.")
            return None
      
        id_abbonamento = self._repo_abbonamento.get_id_by_nome(nome_piattaforma)
        
        if id_abbonamento is None:
            self._notifica.inviaErrore(f"Abbonamento {nome_piattaforma} non trovato.")
            return None

        # 3. Verifica se l'amico esiste
        if not self._repo_utente.verifica(email_amico):
            self._notifica.inviaErrore("Il tuo amico/a deve avere un account registrato.")
            return None

        # 4. Condivisione
        successo = self._repo_abbonamento.duplicaPermessiAccesso(
            email_utente, 
            email_amico, 
            id_abbonamento
        )
        
        if successo:
            return self._notifica.invia("Abbonamento condiviso correttamente")
        
        return None