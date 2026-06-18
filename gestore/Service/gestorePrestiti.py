from database.repositoryUtente import RepositoryUtente
from database.repositoryLog import RepositoryLog
from database.repositoryAbbonamento import RepositoryAbbonamento
from models.notifica import Notifica


class GestorePrestiti:
    def __init__(self, repoUtente: RepositoryUtente,
                 repoAbbonamento: RepositoryAbbonamento,
                 notifica: Notifica):
        self._repo_Utente = repoUtente
        self._email_Utente = RepositoryLog.recuperaUltimoLog()
        self._repo_Abbonamneto = repoAbbonamento
        self._notifica = notifica
    
    def avviaPrestito(self, emailAmico, IDAbbonamento):
        if self._repo_Utente.verifica(emailAmico):
            self._repo_Abbonamneto.duplicaPermessiAccesso(self._email_Utente, emailAmico, IDAbbonamento)
            notificaDiRitorno =self._notifica.invia("Abbonamento condiviso correttamente")
            return notificaDiRitorno
        else:
            self._notifica.inviaErrore("Il tuo amico/a deve avere un account Gestore")
            return