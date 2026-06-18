from datetime import datetime

class Notifica:
    """Gestisce la generazione di notifiche e avvisi di sistema."""
    
    def __init__(self, messaggio: str = "", tipo: str = "Standard"):
        self._messaggio = messaggio
        self._timestamp = datetime.now()
        self._tipo = tipo