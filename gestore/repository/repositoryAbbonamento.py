import os
import sys
import json
from datetime import datetime

# Calcolo del percorso radice del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from models.abbonamento import Abbonamento

class RepositoryAbbonamento:
    """
    Gestisce la persistenza degli abbonamenti nel file JSON (CDU1, CDU2, CDU13, CDU14).
    """

    def __init__(self):
        # Percorso robusto verso repository2/abbonamenti.json
        self._percorso_file = os.path.join(radice_progetto, "repository2", "abbonamenti.json")
        self._assicura_cartella()
        self._abbonamenti = self._carica_dati()

    def _assicura_cartella(self):
        """Crea la cartella repository2 se non esiste."""
        cartella = os.path.dirname(self._percorso_file)
        if not os.path.exists(cartella):
            os.makedirs(cartella)

    def _carica_dati(self):
        """Carica la lista degli abbonamenti dal file JSON."""
        if not os.path.exists(self._percorso_file):
            return []
        try:
            with open(self._percorso_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _salva_dati(self):
        """Salva l'intera lista abbonamenti su disco."""
        with open(self._percorso_file, "w", encoding="utf-8") as f:
            json.dump(self._abbonamenti, f, indent=4, ensure_ascii=False)

    def salva_nuovo_abbonamento(self, abb: Abbonamento):
        """CDU1: Aggiunge un nuovo abbonamento calcolando i dati necessari."""
        nuovo_record = {
            "id_abbonamento": f"ABB_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "email": abb._email,
            "piattaforma": abb.piattaforma,
            "piano": abb._piano,
            "data_emissione": datetime.now().strftime("%Y-%m-%d"),
            "data_scadenza": abb._data_scadenza.strftime("%Y-%m-%d"),
            "validita": True,
            "sezione": "Attivi",
            "stato": "Attivo"
        }
        self._abbonamenti.append(nuovo_record)
        self._salva_dati()
        return True

    def esiste_abbonamento_attivo(self, email, piattaforma):
        """Verifica se l'utente ha già un abbonamento valido per la piattaforma (CDU1 - Flusso Alt. A)."""
        for abb in self._abbonamenti:
            if abb['email'] == email and abb['piattaforma'] == piattaforma and abb['validita']:
                return True
        return False

    def ottieni_per_utente(self, email):
        """CDU13: Recupera tutti gli abbonamenti (attivi e scaduti) di un utente."""
        return [abb for abb in self._abbonamenti if abb['email'] == email]

    def ottieni_per_id(self, id_abbonamento):
        """Recupera un singolo abbonamento tramite il suo id, se esiste."""
        for abb in self._abbonamenti:
            if abb['id_abbonamento'] == id_abbonamento:
                return abb
        return None

    def ottieni_abbonamento_attivo(self, email, piattaforma):
        """Recupera l'abbonamento attivo e valido di un utente per una data piattaforma."""
        for abb in self._abbonamenti:
            if abb['email'] == email and abb['piattaforma'] == piattaforma and abb['validita']:
                return abb
        return None


    def aggiorna_stato(self, id_abb, nuovo_stato):
        """CDU2: Cambia lo stato dell'abbonamento (es. 'Disdetto')."""
        for abb in self._abbonamenti:
            if abb['id_abbonamento'] == id_abb:
                abb['stato'] = nuovo_stato
                self._salva_dati()
                return True
        return False

    def cambia_sezione(self, id_abb, nuova_sezione):
        """CDU19: Sposta l'abbonamento (es. nella sezione 'Scaduti')."""
        for abb in self._abbonamenti:
            if abb['id_abbonamento'] == id_abb:
                abb['sezione'] = nuova_sezione
                abb['validita'] = False if nuova_sezione == "Scaduti" else abb['validita']
                self._salva_dati()
                return True
        return False
    def presta_a_amico(self, id_abb, email_amico):
        """Registra a chi è stato prestato l'abbonamento."""
        for abb in self._abbonamenti:
            if abb['id_abbonamento'] == id_abb:
                abb['prestato_a'] = email_amico
                self._salva_dati()
                return True
        return False

    def rimuovi_record(self, id_abb):
        """CDU14: Elimina definitivamente un record dalla cronologia."""
        self._abbonamenti = [abb for abb in self._abbonamenti if abb['id_abbonamento'] != id_abb]
        self._salva_dati()
        return True