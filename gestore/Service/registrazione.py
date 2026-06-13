import json
import os
from models import utente

class GestoreRegistrazione:

    def __init__(self):
        self._nome = None
        self._cognome = None
        self._email = None
        self._password = None
        self._passwordValida = None
        return
    """Rappresenta il «control» Gestore Registrazione"""
    
    def getModulo(self):
        return ["nome", "email", "password"] # In un caso reale, questo potrebbe essere un oggetto più complesso o un template HTML
    
    def inviaModulo(self, nome, email, password):
        self._nome = nome
        self._email = email
        self._password = password
        print(f"[Control] Ricevuti dati: {nome}, {email}. Validazione in corso...")
        return
    
    def inviaDati(self, metodo, titolare, carta):
        print(f"[Control] Ricevuti dati per {metodo}. Salvo i dati...")
        # Qui potremmo avere la logica per salvare i dati nel database o fare altre operazioni
        self._registrazione_repo.salvaDati(titolare, carta)

    def bloccaRegistrazione(self):
        print("[Control] Registrazione bloccata a causa di errori.")
        # Qui potremmo avere la logica per bloccare ulteriori tentativi di registrazione

    def valida(self, validità: bool):
        if validità:
            print("[Control] Dati validi. Procedo con la registrazione.")
        else:
            print("[Control] Dati non validi. Registrazione interrotta.")
            self.bloccaRegistrazione()
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

