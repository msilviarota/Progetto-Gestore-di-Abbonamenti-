import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Ora puoi importare utente direttamente senza usare i punti!
from models.abbonamento import Abbonamento


class RepositoryAbbonamento:
    def __init__(self, percorsoFile = "abbonamenti.json"):
        self.attivi = {}   # email -> lista oggetti Abbonamento
        self.scaduti = {}  # email -> lista oggetti Abbonamento
        self._percorsoFile = percorsoFile


    
    def caricaFile(self):
        try:
            with open(self._percorsoFile, "r", encoding="utf-8") as file:
                return json.load(file)        
        except FileNotFoundError:
            return {}


    # Salviamo il file con le nuove informazioni nella repository
    def salvaFile(self, abbonamenti):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(abbonamenti, file, indent=4)


    def salva_abbonamento(self, email: str, abbonamento: Abbonamento):
        abbonamenti = self.caricaFile()
        if abbonamento.get_email() not in abbonamenti:
            abbonamenti[email] = []
        abbonamenti[email].append(abbonamento.to_dict())
        self.salvaFile(abbonamenti)
    
    # Scorriamo i vari abbonamenti contenuti nella lista relativa alla specifica email
    # dell'utente e se corrisponde lo eliminiamo 
    def elimina_abbonamento(self, abbonamento: Abbonamento):
        abbonamenti = self.caricaFile()
        email = abbonamento.get_email()
        if email in abbonamenti:
            datiDaEliminare = abbonamento.to_dict()

            abbonamenti[email] = [abb for abb in abbonamenti[email] if abb != datiDaEliminare]

            self.salvaFile(abbonamenti)
            return True # eliminazione riuscita


    def duplicaPermessiAccesso(self, emailUtente, emailAmico, IDAbbonamento):
        """Sposta o copia i permessi nel file JSON secondo la tua descrizione."""
        # 1. Carica il dizionario degli abbonamenti dal PC
        tutti_abbonamenti = self.caricaFile()
        abbonamento_da_condividere = None

        # 2. Cerca l'abbonamento specifico all'interno della lista dell'utente proprietario
        if emailUtente in tutti_abbonamenti:
            for abb in tutti_abbonamenti[emailUtente]:
                if abb["codiceID"] == IDAbbonamento:
                    abbonamento_da_condividere = abb
                    break

        # 3. Se l'abbonamento è stato trovato, duplica il permesso per l'amico
        if abbonamento_da_condividere:
            print(f"[Repository] Abbonamento trovato. Duplico l'accesso per {emailAmico}")
            
            # Se l'amico non ha ancora nessun abbonamento nel JSON, crea una lista vuota
            if emailAmico not in tutti_abbonamenti:
                tutti_abbonamenti[emailAmico] = []
            
            # Controlla per sicurezza che l'amico non abbia già quell'abbonamento
            if abbonamento_da_condividere not in tutti_abbonamenti[emailAmico]:
                # Aggiunge l'abbonamento alla lista dell'amico
                tutti_abbonamenti[emailAmico].append(abbonamento_da_condividere)
            
            # 4. Salva il file JSON aggiornato in locale
            self.salvaFile(tutti_abbonamenti)
            print("[Repository] File JSON aggiornato con i nuovi permessi.")
        else:
            print("[Repository] Errore: Impossibile trovare l'abbonamento da condividere.")
    
    def getAbbonamentiAttivi(self, email):
        return self.attivi.get(email, [])
    
    def getAbbonamentiScaduti(self, email):
        return self.scaduti.get(email, [])
    
    def getAbbonamentiPossibili(self, email):
        return self.attivi.get(email, []) + self.scaduti.get(email, [])
    
