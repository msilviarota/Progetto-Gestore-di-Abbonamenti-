class GestoreRegistrazione:

    def __init__(self, utente_repo: UtenteRepository, registrazione_repo: RegistrazioneRepository):
        self._utente_repo = utente_repo # Il gestore si riferisce a se stesso per semplicità
        self._registrazione_repo = registrazione_repo
    """Rappresenta il «control» Gestore Registrazione"""
    
    def getModulo(self):
        if os.path.exists("repository/registrazione.json"):
            with open("repository/registrazione.json", "r") as file:
                dati = json.load(file)
                print(f"[Control] Modulo di registrazione caricato con successo.")
                return dati.get("tipo_modulo", "registrazione")
        else:
            return "registrazione assente"
        
        print(f"[Control] Richiesto modulo di tipo: {registrazione}")
        # Ritorna il tipo di modulo richiesto (la freccia tratteggiata mostraModulo)
        return registrazione
    
    def inviaDati(self, metodo, titolare, carta):
        print(f"[Control] Ricevuti dati per {metodo}. Salvo i dati...")
        # Qui potremmo avere la logica per salvare i dati nel database o fare altre operazioni
        self._registrazione_repo.salvaDati(titolare, carta)

    def inviaErrore(self, messaggio):
        print(f"[Control] Errore: {messaggio}")
        # Qui potremmo avere la logica per comunicare l'errore alla UI o loggarlo

    def bloccaRegistrazione(self):
        print("[Control] Registrazione bloccata a causa di errori.")
        # Qui potremmo avere la logica per bloccare ulteriori tentativi di registrazione

    def elabora_registrazione(self, nome, email, password):
        # Questo metodo gestirà la logica di business (es. creare l'Utente nel DB)
        print(f"[Control] Elaborazione dati per l'utente: {nome} ({email})")

    def verifica(self, email):
        if self._utente_repo.trovaPerEmail(email) is not None:
            print(f"[Control] Email {email} già registrata.")
            self.inviaErrore("Email in uso")
            self.bloccaRegistrazione()
            return False
        else:
            print(f"[Control] Email {email} è disponibile.")
            return True

