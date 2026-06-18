class Contenuto:
    """
    Rappresenta un contenuto audiovisivo (film, serie tv, ecc.) delle piattaforme.
    """
    
    # Corretto: rinominato da *init* a __init__ per la corretta inizializzazione
    def __init__(self, id_contenuto: str, titolo: str, piattaforma: str, tipologia: str):
        """
        Inizializza un oggetto Contenuto con i dati provenienti dal catalogo.
        """
        self._id_contenuto = id_contenuto
        self._titolo = titolo
        self._piattaforma = piattaforma
        self._tipologia = tipologia
