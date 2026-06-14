from gestore.models import notifica

class GestoreAccessi():

    def __init__(self, db):
        self.db = db

    def getModulo(self, modulo):
        match modulo:
            case "login":
                return ["email", "password"]
            case "CambioPassword":
                return ["vecchia_password", "nuova_password", "conferma_nuova_password"]
            case _:
                return []
    
    def inviaCredenziali(self, email, password):
        print(f"[Control] Ricevuti dati: {email}. Verifica in corso...")
        return self.login(email, password)
    
    def criptaPassword(self, password):
        passwordCriptata = "hashed_" + password  # Simulazione di hashing
        return passwordCriptata

    def bloccaOperazione(self, errore: str):
        notifica.inviaErrore(errore)
        print("[Control] Operazione bloccata per motivi di sicurezza.")
        return False
    
    def mostra(self, esitoVerifica: str):
        match esitoVerifica:
            case "successo":
                print("[Control] Accesso consentito.")
            case "Utente non trovato":
                self.bloccaOperazione("Utente non trovato")
            case "password errata":
                self.bloccaOperazione("password errata")
            case _:
                print("[Control] Accesso negato.")
        return
    
    def login(self, email, password):
        user = self.db.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None
