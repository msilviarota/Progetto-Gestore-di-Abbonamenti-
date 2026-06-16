import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from models.piattaforma import Piattaforma

#================================================================================================================
# Rappresenta il <<control>> GestoreRicerca
class GestoreRicerca():
    def __init__(self, piattaforma: Piattaforma):
        self._piattaforma = piattaforma


    def filtra_categorie(self):
        from dialoghi import FinestraRicerca
        testo = self.campo_ricerca.text().lower().strip()

        if not testo:
            return

        risultati = []
        for chiave, servizi in self.link_categorie.items():
            if testo in chiave.lower():
                for nome, link, _ in servizi:
                    risultati.append((f"{chiave} → {nome}", link))
            else:
                for nome, link, _ in servizi:
                    if testo in nome.lower():
                        risultati.append((nome, link))

        finestra = FinestraRicerca(risultati, self)
        finestra.exec()

    def inviaCerca(self, parolaChiave: str):
        self._piattaforma.getRicerca(parolaChiave)
        return
