class Contenuto:
    """Rappresenta un contenuto audiovisivo (film, serie tv, ecc.) delle piattaforme."""
    def _init_(self, id_contenuto: str, titolo: str, piattaforma: str, tipologia: str):
        self._id_contenuto = id_contenuto
        self._titolo = titolo
        self._piattaforma = piattaforma
        self._tipologia = tipologia

    def ottieni_dettagli_contenuto(self) -> dict:
        """Recupera i dettagli del contenuto multimediale."""
        return {
            "id": self._id_contenuto,
            "titolo": self._titolo,
            "piattaforma": self._piattaforma,
            "tipologia": self._tipologia
        }
