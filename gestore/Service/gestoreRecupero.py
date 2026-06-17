import os
import random

from database.repositoryUtente import RepositoryUtente
from database.repositoryLog import RepositoryLog
from models.email import Email


# Creaimo il gestore di recupero che consente di modificare la password
# di un utente, che non ricordandosela, ne riceverà un'altra
# generata randomicamente via email e che sarà la stessa con 
# abbiamo aggiornato la RepositoryUtente.
class GestoreRecupero:
    def __init__(self, repoUtente: RepositoryUtente,
                  email: Email):
        self._repo_Utente = repoUtente
        self._email_Utente = None
        self._email = email

    def getModulo(self):
        return ["eamil"]
    

    # Inviamo un mail all'utente con la nuova password randomicamente generata
    def inviaEmail(self, emailUtente):
        self._repo_Utente.verifica(emailUtente)
        nuovaPassword = self.generaPasswordRandomica()
        self._email.inviaEmail(emailUtente, nuovaPassword)
        self._repo_Utente.aggiornaPassword(emailUtente, nuovaPassword)
        return True
    
    
    # Generiamo una nuova password utilizzando la libreria random
    def generaPasswordRandomica(self):
        sequenzaRandomica = [random.randint(0, 10) for r in range(6)]
        nuovaPasswordRandomica = "".join(str(n) for n in sequenzaRandomica)
        return nuovaPasswordRandomica
