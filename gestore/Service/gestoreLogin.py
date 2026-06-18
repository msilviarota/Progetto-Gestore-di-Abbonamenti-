import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Ora puoi importare utente direttamente senza usare i punti!
from models.notifica import Notifica
from repository.repositoryUtente import RepositoryUtente
from repository.repositoryAbbonamento import RepositoryAbbonamento
from repository.repositoryLog import RepositoryLog

class GestoreAccessi():

    def __init__(self, repoUtente: RepositoryUtente,
                 repoAbbonamento: RepositoryAbbonamento,
                 repoLog: RepositoryLog):
        self._email = None
        self._password = None
        self._repo_Utente = repoUtente
        self._repo_Abbonamento = repoAbbonamento
        self._repo_Log = repoLog
        self._notifica = Notifica()
        return


    def getModulo(self, modulo):
        match modulo:
            case "login":
                return ["email", "password"]
            case "CambioPassword":
                return ["email", "vecchia_password", "nuova_password", "conferma_nuova_password"]
            case _:
                return []


    # Criptiamo la password inserita dall'utente
    def criptaPassword(self, password):
        passwordCriptata = "hashed_" + password  # Simulazione di hashing
        return passwordCriptata


    def bloccaOperazione(self, errore: str):
        self._notifica.inviaErrore(errore)
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


    # Effettuiamo il login all'app
    def login(self, email, password):
        utente =  self._repo_Utente.getInformazioni(email)
        if utente is not None and utente.get_password() == self.criptaPassword(password):
            self._repo_Log.aggiungi_log("Login effettuato da :" +  email)
            self._email = email 
            return True 
        return False


    # Permettimao all'utente di cambiare password, se lo desidera, una volta fatto l'accesso
    def richiestaCambioPassword(self, vecchia_password, nuova_password, conferma_nuova_password):
        utente = self._repo_Utente.getInformazioni(self._email)

        if nuova_password != conferma_nuova_password:
            self.bloccaOperazione("Le nuove password non corrispondono.")
            return False
        elif self.criptaPassword(vecchia_password) != utente.get_password():
             self.bloccaOperazione("La vecchia password non corrisponde")
             return False
        elif vecchia_password != self._repo_Utente.getInformazioni(self._email)["password"]:
            self.bloccaOperazione("La vecchia password non corrisponde")
            return False
        elif nuova_password == vecchia_password:
            self.bloccaOperazione("La nuova password non può essere uguale alla vecchia.")
            return False
        else:
            self._repo_Utente.aggiornaPassword(self._email, self.criptaPassword(nuova_password))
            self.mostra("passwordAggiornata")
            return True

# Da rivedere poiché non so come controllare la presenza o meno di un download
    def verificaDownloadAttivo(self, email):
        abbonamenti_attivi = self._repo_Abbonamento.getAbbonamentiAttivi(email)
        if not abbonamenti_attivi:
            self.bloccaOperazione("Nessun abbonamento attivo trovato per l'utente.")
            return False
        return True
    
    def inviaCredenziali(self, email, password):
        self._email = email
        self._password = password
        print(f"[Control] Ricevuti dati: {email}. Verifica in corso...")
        return self.login(email, password)


    def richiestaLogout(self):
       self._email= None
       self._password = None
       print ("[Control]Logout effettuato.")
       return True 