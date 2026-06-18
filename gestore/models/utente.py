class Utente:
    """Rappresenta l'utente registrato al gestore."""
    
    def __init__(self, nome: str, cognome: str, eta: int, email: str, password: str):
        self._nome = nome
        self._cognome = cognome
        self._eta = eta
        self._email = email
        self._password = password