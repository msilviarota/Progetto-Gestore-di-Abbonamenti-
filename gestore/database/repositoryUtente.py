class RepositoryUtente:
    def __init__(self): 
        self.utenti = {} # email -> Oggetto Utente
    def salva_utente(self, utente: Utente): 
        self.utenti[utente.get_email() if hasattr(utente, 'get_email') else utente._email] = utente

