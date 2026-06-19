class Contenuto:
    """
    Rappresenta un contenuto audiovisivo (film, serie tv, ecc.) delle piattaforme.
    """

    def __init__(self, id_contenuto: str, titolo: str, piattaforma: str, tipologia: str):
        self._id_contenuto = id_contenuto
        self._titolo = titolo
        self._piattaforma = piattaforma
        self._tipologia = tipologia

    @property
    def titolo(self):
        return self._titolo

    @property
    def piattaforma(self):
        return self._piattaforma

    @property
    def tipologia(self):
        return self._tipologia
