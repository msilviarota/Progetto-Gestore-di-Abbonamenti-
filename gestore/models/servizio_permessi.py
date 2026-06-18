class ServizioPermessi:
    """
    Verifica le abilitazioni e la validità d'accesso degli utenti ai contenuti.
    Gestisce la mappatura tra gli utenti e i codici degli abbonamenti validi (CDU18, CDU20).
    """

    # Corretto: rinominato da *init* a __init__ per la corretta inizializzazione
    def __init__(self):
        """
        Inizializza il servizio con una mappa degli accessi.
        La struttura è: email dell'utente -> lista di codici abbonamento autorizzati.
        """
        self.mappa_accessi = {} # [1]

    def verifica_permesso(self, email: str, id_abbonamento: str):
        """
        CDU18: Controlla se un utente specifico ha il permesso di accedere 
        a un determinato abbonamento prima dell'avvio della piattaforma [2, 3].
        """
        accessi_utente = self.mappa_accessi.get(email, [])
        return id_abbonamento in accessi_utente

    def aggiungi_permesso(self, email: str, id_abbonamento: str):
        """
        Aggiunge un nuovo abbonamento alla lista dei permessi dell'utente.
        Viene utilizzato al momento dell'acquisto (CDU1) o della ricezione 
        di un prestito da un amico (CDU11) [4-6].
        """
        if email not in self.mappa_accessi:
            self.mappa_accessi[email] = []
        
        if id_abbonamento not in self.mappa_accessi[email]:
            self.mappa_accessi[email].append(id_abbonamento)
            return True
        return False

    def revoca_permesso(self, email: str, id_abbonamento: str):
        """
        CDU20: Revoca i permessi di accesso dell'utente per quello specifico 
        abbonamento quando giunge a scadenza [7].
        """
        if email in self.mappa_accessi and id_abbonamento in self.mappa_accessi[email]:
            self.mappa_accessi[email].remove(id_abbonamento)
            return True
        return False