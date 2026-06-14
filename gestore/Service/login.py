from gestore.models import notifica
from gestore.database import repositoryUtente
from gestore.database import repositoryAbbonamento

class GestoreAccessi():

    def __init__(self):
        self._email = None
        self._password = None
        return


    def getModulo(self, modulo):
        match modulo:
            case "login":
                return ["email", "password"]
            case "CambioPassword":
                return ["vecchia_password", "nuova_password", "conferma_nuova_password"]
            case _:
                return []


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


    def richiestaCambioPassword(self, vecchia_password, nuova_password, conferma_nuova_password):
        if nuova_password != conferma_nuova_password:
            self.bloccaOperazione("Le nuove password non corrispondono.")
            return False
        elif vecchia_password != repositoryUtente.getInformazioni[2]:
            self.bloccaOperazione("La vecchia password non corrisponde")
            return False
        elif nuova_password == vecchia_password:
            self.bloccaOperazione("La nuova password non può essere uguale alla vecchia.")
            return False
        else:
            repositoryUtente.aggiornaPassword(self.criptaPassword(nuova_password))
            self.mostra("passwordAggiornata")
            return True

# Da rivedere poiché non so come controllare la presenza o meno di un download
    def verificaDownloadAttivo(self, email):
        abbonamenti_attivi = repositoryAbbonamento.getAbbonamentiAttivi(email)
        if not abbonamenti_attivi:
            self.bloccaOperazione("Nessun abbonamento attivo trovato per l'utente.")
            return False
        return True
    
    def inviaCredenziali(self, email, password):
        self._email = email
        self._password = password
        print(f"[Control] Ricevuti dati: {email}. Verifica in corso...")
        return self.login(email, password)


    def login(self, email, password):
        if email in repositoryUtente.utenti and repositoryUtente.getInformazioni[2] == self.criptaPassword(password):
            return True
        return None


    def richiestaLogout(self, abbonamento):
        if abbonamento in repositoryAbbonamento.getAbbonamentiAttivi(email):
            del repositoryAbbonamento.abbonamenti[abbonamento]
        print("[Control] Logout richiesto. Procedo con il logout.")
        return True