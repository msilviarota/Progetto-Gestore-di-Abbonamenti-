import os
import sys
import json

# Calcolo del percorso radice del progetto per gli import
# Corretto: uso di __file__ invece di **file**
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from models.datiPagamento import DatiPagamento

class RepositoryDatiPagamento:
    """
    Gestisce il salvataggio e il recupero dei dati di pagamento (CDU16).
    I dati risiedono in repository2/pagamenti.
    """

    # Corretto: rinominato da **init** a __init__
    def __init__(self, nome_file="pagamenti"):
        # Percorso robusto verso repository2/pagamenti (visto in imagine2)
        self._percorso_file = os.path.join(radice_progetto, "repository2", nome_file)
        
        # Assicura che la cartella repository2 esista
        cartella = os.path.dirname(self._percorso_file)
        if not os.path.exists(cartella):
            os.makedirs(cartella)
            
        # Carica il database locale in memoria
        self._database = self._carica_file()

    def _carica_file(self):
        """Legge il file JSON dei pagamenti."""
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

    def ottieni_per_utente(self, email):
        """Recupera i dati di pagamento associati a una specifica email."""
        return self._database.get(email)

    def aggiornaDatiPagamento(self, email, dati: DatiPagamento):
        """
        CDU16: Modifica i dati di pagamento sovrascrivendo i precedenti.
        Nota: i dati dovrebbero essere cifrati prima del salvataggio (Requisito 2).
        """
        # Creazione della struttura dati (Simulazione cifratura)
        self._database[email] = {
            "numero_carta": dati._numero_carta, # Qui andrebbe applicata la cifratura
            "scadenza": dati._scadenza_carta,
            "nome_titolare": dati._nome_titolare,
            "cognome_titolare": dati._cognome_titolare
        }
        
        self._salva_su_disco()
        print(f"Dati di pagamento aggiornati per {email}.")
        return True