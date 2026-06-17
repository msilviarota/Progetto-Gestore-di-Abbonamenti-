from models.utente import Utente

class Preferenza:
    def __init__(self, utente: Utente):
        self._preferenze = utente.get_preferenze()

    def getCategorie(self):
        return self._preferenze