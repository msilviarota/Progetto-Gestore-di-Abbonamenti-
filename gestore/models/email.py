class Email:
    """Modello per la struttura delle email di sistema."""
    def _init_(self, destinatario: str, oggetto: str, corpo: str):
        self._mittente = "sistema@gestore.it"
        self._destinatario = destinatario
        self._oggetto = oggetto
        self._corpo = corpo

    def ottieni_dati_email(self) -> dict:
        """Restituisce i dati dell'email pronti per il server di posta."""
        return {
            "da": self._mittente, 
            "a": self._destinatario, 
            "oggetto": self._oggetto, 
            "corpo": self._corpo
        }