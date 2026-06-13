class RepositoryAbbonamenti:
    def __init__(self):
        self.attivi = {}   # email -> lista oggetti Abbonamento
        self.scaduti = {}  # email -> lista oggetti Abbonamento
    def salva_abbonamento(self, email: str, abbonamento: Abbonamento):
        if email not in self.attivi: self.attivi[email] = []
        self.attivi[email].append(abbonamento)
