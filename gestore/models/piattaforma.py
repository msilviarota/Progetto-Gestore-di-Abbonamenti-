class Piattaforma:
    def __init__(self, nome: str):
        self._nome = nome


    def get_nome(self): return self._nome


    def inviaSceltaAbbonamento(self, email, nome_utente, cognome_utente):
        
        return {
            "email": email,
            "nome_utente": nome_utente,
            "cognome_utente": cognome_utente,
            "piattaforma_nome": self._nome
        }

    
    def getRicerca(self, parolaChiave: str):
        
        return