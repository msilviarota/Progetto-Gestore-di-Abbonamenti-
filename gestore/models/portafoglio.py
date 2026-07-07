import os
import sys

cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)


class Portafoglio:
    """Rappresenta il credito (finto) disponibile per un utente,
    usato per acquistare abbonamenti all'interno dell'app."""

    def __init__(self, email_utente: str, saldo: float = 0.0):
        self._email_utente = email_utente
        self._saldo = saldo

    def ha_fondi_sufficienti(self, importo: float) -> bool:
        """Verifica se il saldo copre l'importo richiesto."""
        return self._saldo >= importo

    def aggiungi(self, importo: float):
        """Aumenta il saldo (ricarica credito). Rifiuta importi non positivi."""
        if importo <= 0:
            raise ValueError("L'importo da aggiungere deve essere positivo.")
        self._saldo += importo

    def scala(self, importo: float):
        """Diminuisce il saldo (acquisto). Solleva errore se i fondi non bastano."""
        if importo <= 0:
            raise ValueError("L'importo da scalare deve essere positivo.")
        if not self.ha_fondi_sufficienti(importo):
            raise ValueError("Credito insufficiente.")
        self._saldo -= importo

    def ottieni_saldo(self) -> float:
        return self._saldo