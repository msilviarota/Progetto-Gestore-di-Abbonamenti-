import os
import sys
import json

# Calcolo del percorso radice del progetto per gestire gli import
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

class RepositoryPreferenze:
    """
    Gestisce la lettura e scrittura delle preferenze degli utenti (CDU5, CDU17).
    I dati sono salvati in repository2/preferenze.json.
    """

    def __init__(self, nome_file="preferenze.json"):
        # Percorso robusto verso la cartella repository2
        self._percorso_file = os.path.join(radice_progetto, "repository2", nome_file)
        
        # Assicura che la cartella esista
        cartella = os.path.dirname(self._percorso_file)
        if not os.path.exists(cartella):
            os.makedirs(cartella)
            
        # Carica il database locale in memoria
        self._database = self.carica_file()

    def carica_file(self):
        """Carica l'intero dizionario delle preferenze dal file JSON."""
        if not os.path.exists(self._percorso_file):
            return {}
        try:
            with open(self._percorso_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _salva_su_disco(self):
        """Salva lo stato attuale del dizionario sul file fisico."""
        with open(self._percorso_file, "w", encoding="utf-8") as f:
            json.dump(self._database, f, indent=4, ensure_ascii=False)

    def ottieni_per_utente(self, email):
        """
        Recupera le preferenze (categorie e data) associate a un utente.
        Se non presenti, restituisce None (CDU17 - Flusso Alt. A).
        """
        return self._database.get(email)

    def salva_per_utente(self, email, dati_preferenze):
        """
        CDU5: Aggiorna o crea il record delle preferenze per l'utente.
        'dati_preferenze' è un dizionario contenente la lista categorie e la data.
        """
        self._database[email] = dati_preferenze
        self._salva_su_disco()
        return True