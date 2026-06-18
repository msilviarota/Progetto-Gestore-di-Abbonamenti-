import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Ora puoi importare utente direttamente senza usare i punti!
import json
import os
from models.utente import Utente
from repository.repositoryUtente import RepositoryUtente
from repository.repositoryPreferenze import RepositoryPreferenze


class GestoreRegistrazione:

    def __init__(self, repoUtente: RepositoryUtente,
                  repoPreferenze: RepositoryPreferenze):
        self._nome = None
        self._cognome = None
        self._eta = None
        self._email = None
        self._password = None
        self._passwordValida = None
        self._preferenze = None
        self._repo_Utente = repoUtente
        self._repo_Preferenze = repoPreferenze
        return
    """Rappresenta il «control» Gestore Registrazione"""


    def getModulo(self):
        return ["nome", "cognome", "eta", "email", "password", "preferenze"] # In un caso reale, questo potrebbe essere un oggetto più complesso o un template HTML


    def inviaModulo(self, nome, cognome, eta, email, password, preferenze):
        self._nome = nome
        self._cognome = cognome
        self._eta = eta
        self._email = email
        self._password = password
        self._preferenze = preferenze
        print(f"[Control] Ricevuti dati: {nome}, {cognome}, {eta}, {email}. Validazione in corso...")
        return


    def inviaDati(self, metodo, titolare, carta):
        print(f"[Control] Ricevuti dati per {metodo}. Salvo i dati...")
        # Qui potremmo avere la logica per salvare i dati nel database o fare altre operazioni
        self._registrazione_repo.salvaDati(titolare, carta)


    def bloccaRegistrazione(self):
        print("[Control] Registrazione bloccata a causa di errori.")
        # Qui potremmo avere la logica per bloccare ulteriori tentativi di registrazione


    def valida(self):
        # controllo se email esiste già 
        
        if self._repo_Utente.verifica(self._email):
            print("[Control] Errore : Utente già esistente .")
            self.bloccaRegistrazione()
            return False
        else:
            password_sicura = "hashed_"+ self._password
            nuovoUtente = Utente(self._nome, self._cognome,  self._eta, self._email, password_sicura)
            self._repo_Utente.salva_utente(nuovoUtente)
            self._repo_Preferenze.aggiornaPreferenze(self._preferenze)
            print("[Control]registrazione completata con successo")
            return True
           