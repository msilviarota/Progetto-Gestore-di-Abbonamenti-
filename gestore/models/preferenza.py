from models.utente import Utente

class Preferenza:
    def __init__(self):
        self._preferenze = []

    def getCategorie(self):
        return self._preferenze
    
    def 