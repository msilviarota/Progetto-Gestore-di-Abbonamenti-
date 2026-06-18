import json
from database.repositoryUtente import RepositoryUtente
from database.repositoryDatiPagamento import RepositoryDatiPagamento
from database.repositoryLog import RepositoryLog
from models.notifica import Notifica


class GestorePagamenti:
    def __init__(self, repoUtente: RepositoryUtente,
                  repoDatiPagamento: RepositoryDatiPagamento,
                  repoLog: RepositoryLog,
                  notifica: Notifica):
        self._email_Utente = repoLog.recuperaUltimoLog()
        self._repo_Utente = repoUtente
        self._repo_DatiPagamento = repoDatiPagamento
        self._notifica = notifica


    # Prendiamo tutti i metodi di pagamento salvati dall'utente
    def getMetodoPagamenti(self):
        if self._repo_Utente.verifica(self._email_Utente):
            metodiDiPagamento = self._repo_DatiPagamento.getMetodiPagamento(self._email_Utente)
            
            if len(metodiDiPagamento) == 0:
                self.bloccaOperazione()
                messaggio_notifica = self._notifica.inviaErrore("nessun metodo di pagamento salvato")
                return messaggio_notifica
            
            else:
                return metodiDiPagamento
            
    # Scelto un metodo di pagamento, utilizziamo quello per pagare
    def inviaSelezione(self, metodo):
        return metodo["numero"], metodo["scadenza"], metodo["titolare"]
    

    def inviaDati(self, datiPagamento):
        if not self.valida(datiPagamento):
            self.bloccaOperazione()
            notifica = self._notifica.inviaErrore("Dati non validi")
            return notifica
        else:
            self.valida(datiPagamento)
   #         self._repo_DatiPagamento.aggiornaDatiPagamento()
            notifica = self._notifica.invia("Pagamento avvenuto con successo.")
            return notifica