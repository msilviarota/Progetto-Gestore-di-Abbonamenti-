from datetime import datetime
"""chiede al sistema operativo (anno, mese, giorno, ora, minuto, secondo) in cui viene eseguita quella riga di codice."""

class Notifica:
    """Gestisce l'invio e la generazione di notifiche, avvisi di errore ed email di sistema."""
    def _init_(self, messaggio: str = "", tipo: str = "Standard"):
        self._messaggio = messaggio
        self._timestamp = datetime.now()
        self._tipo = tipo

    # inviamoun messaggio di notifica relativo ad un successo
    def invia(self, messaggio):
        return "Conferma", messaggio

    # inviamoun messaggio di notifica relativo ad un errore
    def inviaErrore(self, messaggio_errore: str):
        """Metodo Richiesto: Configura e stampa una notifica di errore di sistema."""
        self._messaggio = messaggio_errore
        self._tipo = "Errore"
        self._timestamp = datetime.now()
        print(f"[{self._timestamp.strftime('%H:%M:%S')}] [NOTIFICA DI ERRORE]: {self._messaggio}")
        return "Errore", self._messaggio

    # comunichiamo l'invio di una Email
    def inviaEmail(self, email_destinatario: str,
                    oggetto: str, corpo_messaggio: str):
        """Metodo Richiesto: Simula l'invio di una notifica formale via Email all'utente."""
        self._messaggio = corpo_messaggio
        self._tipo = "Email"
        self._timestamp = datetime.now()
        print(f"--- EMAIL INVIATA A: {email_destinatario} ---")
        print(f"Oggetto: {oggetto}")
        print(f"Contenuto: {corpo_messaggio}")
        print(f"-------------------------------------------")
        return "Email", self._messaggio

    # inviamo un avviso all'utente sulla prossima scadena
    def inviaAvviso(self, messaggio):
        self._messaggio = messaggio
        self._tipo = "Avviso"
        return self._tipo, self._messaggio
    
    
    # Otteniamo informazioni sulla notifica
    def ottieni_info_notifica(self) -> dict:
        """Recupera le informazioni dell'ultima notifica generata."""
        return {
            "messaggio": self._messaggio, 
            "data": self._timestamp, 
            "tipo": self._tipo
        }