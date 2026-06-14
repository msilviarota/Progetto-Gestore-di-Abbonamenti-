class Utente:
    def __init__(self, nome: str, cognome: str, eta: int, email: str, password: str):
        self._nome = nome
        self._cognome = cognome
        self._eta = eta
        self._email = email
        self._password = password
        self._preferenze = []

    def get_nome(self): return self._nome

    def get_cognome(self): return self._cognome

    def get_eta(self): return self._eta

    def get_email(self): return self._email

    def get_password(self): return self._password

    def get_preferenze(self): return self._preferenze
