class Email:
    """
    Modello per la struttura delle email di sistema.
    Utilizzato per comunicazioni automatiche come il recupero password (CDU8).
    """

    # Corretto: rinominato da *init* a __init__ per la corretta inizializzazione
    def __init__(self, destinatario: str, oggetto: str, corpo: str):
        """
        Inizializza un oggetto Email con mittente di sistema predefinito.
        """
        self._mittente = "sistema@gestore.it"
        self._destinatario = destinatario
        self._oggetto = oggetto
        self._corpo = corpo