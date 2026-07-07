import os
import sys

cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from repository.repositoryPortafoglio import RepositoryPortafoglio
from models.notifica import Notifica


class GestorePortafoglio:
    """
    Gestisce il credito (finto) dell'utente: consultazione saldo,
    ricariche e scalo per gli acquisti di abbonamenti.
    """

    def __init__(self, repoPortafoglio: RepositoryPortafoglio, notifica: Notifica):
        self._repo_Portafoglio = repoPortafoglio
        self._notifica = notifica

    def ottieni_saldo(self, email: str) -> float:
        """Restituisce il saldo attuale dell'utente."""
        portafoglio = self._repo_Portafoglio.ottieni_portafoglio(email)
        return portafoglio.ottieni_saldo()

    def aggiungi_credito(self, email: str, importo: float) -> bool:
        """Ricarica il portafoglio dell'utente con l'importo indicato."""
        try:
            portafoglio = self._repo_Portafoglio.ottieni_portafoglio(email)
            portafoglio.aggiungi(importo)
            self._repo_Portafoglio.salva_portafoglio(portafoglio)
            self._notifica = Notifica(f"Credito ricaricato: +{importo:.2f}€.", "Successo")
            return True
        except ValueError as e:
            self._notifica = Notifica(str(e), "Errore")
            return False

    def scala_credito(self, email: str, importo: float) -> bool:
        """
        Scala l'importo dal portafoglio dell'utente, se i fondi bastano.
        Restituisce False (senza modificare nulla) se il credito è insufficiente.
        """
        portafoglio = self._repo_Portafoglio.ottieni_portafoglio(email)

        if not portafoglio.ha_fondi_sufficienti(importo):
            self._notifica = Notifica("Credito insufficiente per completare l'acquisto.", "Errore")
            return False

        portafoglio.scala(importo)
        self._repo_Portafoglio.salva_portafoglio(portafoglio)
        self._notifica = Notifica(f"Addebitati {importo:.2f}€ dal credito.", "Info")
        return True