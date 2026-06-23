class DatiPagamento:
    """Rappresenta i dati della carta di pagamento dell'utente."""
    def __init__(self, numero_carta: str, scadenza_carta: str, nome_titolare: str, cognome_titolare: str):
        self._numero_carta = numero_carta
        self._scadenza_carta = scadenza_carta
        self._nome_titolare = nome_titolare
        self._cognome_titolare = cognome_titolare

    def ottieni_dati_carta(self) -> dict:
        """Recupera i dati della carta per le transazioni cifrate."""
        return {
            "numero": self._numero_carta,
            "scadenza": self._scadenza_carta,
            "titolare": f"{self._nome_titolare} {self._cognome_titolare}"
        }
