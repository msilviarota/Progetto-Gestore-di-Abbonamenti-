import os
import sys
import json

# Calcolo del percorso radice del progetto per gestire gli import
# Corretto l'uso di __file__ (doppio underscore)
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazione del modello Contenuto
from models.contenuto import Contenuto

class RepositoryDati:
    """
    Gestisce il catalogo dei contenuti disponibili (film, serie, musica).
    Interagisce con il file repository2/dati (CDU4, CDU17).
    """

    # Corretto il nome del costruttore in __init__
    def __init__(self, nome_file="dati"):
        # Percorso robusto verso repository2/dati (come visto in imagine2)
        self._percorso_file = os.path.join(radice_progetto, "repository2", nome_file)
        
        # Carica il catalogo in memoria
        self._catalogo = self._carica_catalogo()

    def _carica_catalogo(self):
        """Legge il file JSON e restituisce la lista dei contenuti disponibili."""
        if not os.path.exists(self._percorso_file):
            # Se il file non esiste, restituisce un catalogo vuoto di base
            return []
        try:
            with open(self._percorso_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def ottieni_tutti(self):
        """Restituisce l'intera lista dei contenuti come oggetti Modello."""
        lista_oggetti = []
        for c in self._catalogo:
            lista_oggetti.append(Contenuto(
                id_contenuto=c.get('id'),
                titolo=c.get('titolo'),
                piattaforma=c.get('piattaforma'),
                tipologia=c.get('tipologia')
            ))
        return lista_oggetti

    def cerca_per_titolo(self, parola_chiave: str):
        """
        CDU4: Filtra il catalogo in base a una parola chiave inserita dall'utente.
        """
        risultati = []
        parola_chiave = parola_chiave.lower()
        for c in self.ottieni_tutti():
            if parola_chiave in c._titolo.lower():
                risultati.append(c)
        return risultati

    def filtra_per_categoria(self, categoria: str):
        """
        CDU17: Filtra i contenuti in base ai gusti (es. 'Musica', 'Cinema').
        """
        return [c for c in self.ottieni_tutti() if c._tipologia.lower() == categoria.lower()]

    def ottieni_per_piattaforma(self, nome_piattaforma: str):
        """Recupera tutti i contenuti di una specifica piattaforma (es. 'Netflix')."""
        return [c for c in self.ottieni_tutti() if c._piattaforma.lower() == nome_piattaforma.lower()]