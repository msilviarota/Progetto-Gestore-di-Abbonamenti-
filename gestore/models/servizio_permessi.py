class ServizioPermessi:
    """Verifica le abilitazioni e la validità d'accesso degli utenti ai contenuti."""
    def _init_(self):
        self.mappa_accessi = {}  # email -> lista codici abbonamenti

    def verifica_accesso_utente(self, email: str, codice_abb: str) -> bool:
        """Controlla se l'utente possiede l'abbonamento specifico per riprodurre il contenuto."""
        return email in self.mappa_accessi and codice_abb in self.mappa_accessi[email]