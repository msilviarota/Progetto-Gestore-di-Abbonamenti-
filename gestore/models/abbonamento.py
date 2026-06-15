from datetime import datetime, timedelta

class Abbonamento:
    def __init__(self, email : str, nome_utente: str, cognome_utente: str, piattaforma_nome: str):
        self._email = email
        self._nome_utente = nome_utente
        self._cognome_utente = cognome_utente
        self.piattaforma = piattaforma_nome
        self._data_scadenza = datetime.now() + timedelta(days=365)  # Scadenza dopo 365 giorni
        self._valido = True
        self._stato = "Attivo"

    def get_email(self): return self._email

    def get_nome_utente(self): return self._nome_utente

    def get_cognome_utente(self): return self._cognome_utente

    def get_piattaforma(self): return self.piattaforma_nome

    def get_data_scadenza(self): return self._data_scadenza

    def get_valido(self): return self._valido

    def get_stato(self): return self._stato

    def to_dict(self):
        return{
            "email": self._email,
            "nome": self._nome_utente,
            "cognome": self._cognome_utente,
            "dataScadenza": self._data_scadenza,
            "validità": self._valido,
            "stato": self._stato
        }