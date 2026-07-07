import os
import sys
import json

cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from models.portafoglio import Portafoglio


class RepositoryPortafoglio:
    """
    Gestisce il salvataggio e il recupero del credito (finto) degli utenti.
    I dati risiedono in repository2/portafogli.
    """

    def __init__(self, nome_file="portafogli"):
        self._percorso_file = os.path.join(radice_progetto, "repository2", nome_file)

        cartella = os.path.dirname(self._percorso_file)
        if not os.path.exists(cartella):
            os.makedirs(cartella)

        self._database = self._carica_file()

    def _carica_file(self):
        """Legge il file JSON dei portafogli."""
        if not os.path.exists(self._percorso_file):
            return {}
        try:
            with open(self._percorso_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _salva_su_disco(self):
        """Scrive i dati aggiornati sul file JSON."""
        with open(self._percorso_file, "w", encoding="utf-8") as f:
            json.dump(self._database, f, indent=4, ensure_ascii=False)

    def ottieni_portafoglio(self, email: str) -> Portafoglio:
        """Recupera il portafoglio dell'utente. Se non esiste, ne crea
        uno nuovo con saldo a 0 (ma non lo salva finché non viene modificato)."""
        dati = self._database.get(email)

        if dati is None:
            return Portafoglio(email_utente=email, saldo=0.0)

        return Portafoglio(email_utente=email, saldo=dati.get("saldo", 0.0))

    def salva_portafoglio(self, portafoglio: Portafoglio):
        """Salva (o aggiorna) il saldo del portafoglio sul disco."""
        self._database[portafoglio._email_utente] = {
            "saldo": portafoglio._saldo
        }
        self._salva_su_disco()
        return True