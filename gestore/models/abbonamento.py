from datetime import datetime, timedelta

class Abbonamento:
    """Rappresenta un abbonamento acquistato (CDU1)."""
    
    def __init__(self, email: str, nome_utente: str, cognome_utente: str, 
                 piattaforma_nome: str, piano: str = "mensile"):
        self._email = email
        self._nome_utente = nome_utente
        self._cognome_utente = cognome_utente
        self.piattaforma = piattaforma_nome
        self._piano = piano

        # Scadenza calcolata in base al piano scelto
        giorni_validita = 365 if piano == "annuale" else 30
        self._data_scadenza = datetime.now() + timedelta(days=giorni_validita)

        self._validita = True
        self._stato = "Attivo"