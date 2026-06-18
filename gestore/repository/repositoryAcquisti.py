import os
import sys
import json
from datetime import datetime

# Calcolo del percorso radice del progetto per gestire gli import e i file
# Corretto l'uso di __file__ rispetto al frammento originale [3]
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from models.abbonamento import Abbonamento

class RepositoryAcquisti:
    """
    Gestisce la persistenza della cronologia acquisti (CDU13).
    I dati sono salvati nel file repository2/acquisti [4].
    """

    # Corretto il nome del costruttore in __init__ [3]
    def __init__(self, nome_file="acquisti"):
        # Percorso robusto verso la cartella repository2 [4]
        self._percorso_file = os.path.join(radice_progetto, "repository2", nome_file)
        
        # Assicura che la cartella esista
        cartella = os.path.dirname(self._percorso_file)
        if not os.path.exists(cartella):
            os.makedirs(cartella)
            
        # Carica lo storico in memoria
        self._storico = self._carica_storico()

    def _carica_storico(self):
        """Legge il file JSON e restituisce la lista degli acquisti."""
        if not os.path.exists(self._percorso_file):
            return []
        try:
            with open(self._percorso_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _salva_su_disco(self):
        """Salva lo stato attuale dello storico sul file fisico."""
        with open(self._percorso_file, "w", encoding="utf-8") as f:
            json.dump(self._storico, f, indent=4, ensure_ascii=False)

    def aggiungi_acquisto(self, abbonamento: Abbonamento, prezzo: str):
        """
        Registra un nuovo acquisto nello storico (CDU1).
        Include dettagli come data di transazione e prezzo.
        """
        nuovo_acquisto = {
            "data_transazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "email_utente": abbonamento._email,
            "piattaforma": abbonamento.piattaforma,
            "prezzo": prezzo,
            "scadenza_prevista": abbonamento._data_scadenza.strftime("%Y-%m-%d")
        }
        self._storico.append(nuovo_acquisto)
        self._salva_su_disco()
        return True

    def ottieni_cronologia_utente(self, email: str):
        """
        CDU13: Recupera l'intera cronologia degli acquisti per un utente specifico.
        Restituisce i dati in ordine cronologico [2].
        """
        cronologia = [a for a in self._storico if a['email_utente'] == email]
        # Ordina per data decrescente (più recenti prima)
        cronologia.sort(key=lambda x: x['data_transazione'], reverse=True)
        return cronologia