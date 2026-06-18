import os
import sys
import json

# Calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Assicurati che il modello Contenuto esista nella cartella models
# from models.contenuto import Contenuto 


class RepositoryDati:
    def __init__(self, percorsoFile="catalogo.json"):
        self._percorsoFile = percorsoFile

  
    def caricaFile(self):
        try:
            with open(self._percorsoFile, "r", encoding="utf-8") as file:
                return json.load(file)        
        except FileNotFoundError:
            # Se il file non esiste, restituiamo un catalogo di esempio per non far crashare la grafica
            return [
                {"id": 1, "nome": "Netflix", "tipo": "Piattaforma"},
                {"id": 2, "nome": "Spotify", "tipo": "Piattaforma"},
                {"id": 3, "nome": "Disney+", "tipo": "Piattaforma"}
            ]

   
    def salvaFile(self, catalogo):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(catalogo, file, indent=4)

    
    def ottieni_catalogo_completo(self) -> list: 
        return self.caricaFile()