from models import abbonamento

class RepositoryAbbonamenti:
    def __init__(self):
        self.attivi = {}   # email -> lista oggetti Abbonamento
        self.scaduti = {}  # email -> lista oggetti Abbonamento

    def salva_abbonamento(self, email: str, abbonamento: abbonamento):
        if email not in self.attivi: 
            self.attivi[email] = []
            self.attivi[email].append(abbonamento)
        else:
            self.attivi[email].append(abbonamento)

    def getAbbonamentiAttivi(self, email):
        return self.attivi.get(email, [])