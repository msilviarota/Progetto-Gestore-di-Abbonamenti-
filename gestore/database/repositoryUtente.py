from models import utente

class RepositoryUtente:
    def __init__(self): 
        self.utenti = {} # email -> Oggetto Utente


    def salva_utente(self, utente: utente): 
        self.utenti[utente.get_email() if hasattr(utente, 'get_email') else utente._email] = utente


    def getInformazioni(self, email):
        if email in self.utenti:
            utente = self.utenti[email]
            return utente
        return None
    

    def aggiornaPassword(self, email, nuova_password):
        if email in self.utenti:
            self.utenti[email] = nuova_password
            return True
        return False
    