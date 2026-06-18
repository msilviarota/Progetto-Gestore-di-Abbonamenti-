from datetime import datetime, timedelta

class Abbonamento:
    """Rappresenta un abbonamento acquistato (CDU1)."""
    
    def __init__(self, email: str, nome_utente: str, cognome_utente: str, piattaforma_nome: str):
        self._email = email
        self._nome_utente = nome_utente
        self._cognome_utente = cognome_utente
        self.piattaforma = piattaforma_nome
        # La scadenza è impostata di default a 365 giorni (Stagionale)
        self._data_scadenza = datetime.now() + timedelta(days=365)
        self._validita = True
        self._stato = "Attivo"