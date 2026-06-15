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
from models import utente
from database import repositoryUtente


class GestoreRegistrazione:

    def __init__(self):
        self._nome = None
        self._cognome = None
        self._eta = None
        self._email = None
        self._password = None
        self._passwordValida = None
        return
    """Rappresenta il «control» Gestore Registrazione"""


    def getModulo(self):
        return ["nome", "cognome", "eta", "email", "password"] # In un caso reale, questo potrebbe essere un oggetto più complesso o un template HTML


    def inviaModulo(self, nome, cognome, eta, email, password):
        self._nome = nome
        self._cognome = cognome
        self._eta = eta
        self._email = email
        self._password = password
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
        validità = repositoryUtente.verifica(self._email)
        if validità:
            print("[Control] Dati non validi. Registrazione interrotta.")
            self.bloccaRegistrazione()
            return False
            # Questo metodo gestirà la logica di business (es. creare l'Utente nel DB)
            print(f"[Control] Elaborazione dati per l'utente: {self._nome} ({self._email})")
        else:
            repositoryUtente.salva_utente(utente(self._nome, self._cognome, self._eta, self._email, self._password))
            print("[Control] Dati validi. Procedo con la registrazione.")
            return True
            # Questo metodo gestirà la logica di business (es. creare l'Utente nel DB)