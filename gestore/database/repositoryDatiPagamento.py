from models.datiPagamento import DatiPagamento
class RepositoryDatiPagamento:
    def __init__(self): 
        self.metodi = {} # email -> DatiPagamento
    def salva_metodo(self, email: str, dati: DatiPagamento): 
        self.metodi[email] = dati
