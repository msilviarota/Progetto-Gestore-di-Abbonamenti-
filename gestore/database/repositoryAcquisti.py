class RepositoryAcquisti:
    def __init__(self): 
        self.storico = {} # email -> lista Abbonamenti passati
    def registra_acquisto(self, email: str, abbonamento: Abbonamento):
        if email not in self.storico: self.storico[email] = []
        self.storico[email].append(abbonamento)

