import os
import sys
import json

# Calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from models.abbonamento import Abbonamento


class RepositoryAbbonamento:
    def __init__(self, percorsoFile = "abbonamenti.json"):
        self._percorsoFile = percorsoFile
    
    def caricaFile(self):
        try:
            with open(self._percorsoFile, "r", encoding="utf-8") as file:
                return json.load(file)        
        except FileNotFoundError:
            return {}

    def salvaFile(self, abbonamenti):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(abbonamenti, file, indent=4)

    def salva_abbonamento(self, email: str, abbonamento: Abbonamento):
        abbonamenti = self.caricaFile()
      
        if email not in abbonamenti:
            abbonamenti[email] = []
        abbonamenti[email].append(abbonamento.to_dict())
        self.salvaFile(abbonamenti)
    
    def elimina_abbonamento(self, abbonamento: Abbonamento):
        abbonamenti = self.caricaFile()
        email = abbonamento.get_email()
        if email in abbonamenti:
            datiDaEliminare = abbonamento.to_dict()
            abbonamenti[email] = [abb for abb in abbonamenti[email] if abb != datiDaEliminare]
            self.salvaFile(abbonamenti)
            return True 
        return False


    def duplicaPermessiAccesso(self, emailUtente, emailAmico, IDAbbonamento):
        """Sposta o copia i permessi nel file JSON."""
        tutti_abbonamenti = self.caricaFile()
        abbonamento_da_condividere = None

        if emailUtente in tutti_abbonamenti:
            for abb in tutti_abbonamenti[emailUtente]:
                if abb.get("codiceID") == IDAbbonamento or abb.get("id") == IDAbbonamento:
                    abbonamento_da_condividere = abb
                    break

        if abbonamento_da_condividere:
            print(f"[Repository] Abbonamento trovato. Duplico l'accesso per {emailAmico}")
            if emailAmico not in tutti_abbonamenti:
                tutti_abbonamenti[emailAmico] = []
            
            if abbonamento_da_condividere not in tutti_abbonamenti[emailAmico]:
                tutti_abbonamenti[emailAmico].append(abbonamento_da_condividere)
            
            self.salvaFile(tutti_abbonamenti)
            print("[Repository] File JSON aggiornato con i nuovi permessi.")
        else:
            print("[Repository] Errore: Impossibile trovare l'abbonamento da condividere.")
    
 
    def getAbbonamentiAttivi(self, email):
        tutti = self.caricaFile()
        # Restituisce gli abbonamenti dell'utente che non sono scaduti (puoi filtrare per campo 'stato' se presente)
        lista_utente = tutti.get(email, [])
        return [abb for abb in lista_utente if abb.get("stato", "attivo") == "attivo"]
    
    def getAbbonamentiScaduti(self, email):
        tutti = self.caricaFile()
        lista_utente = tutti.get(email, [])
        return [abb for abb in lista_utente if abb.get("stato") == "scaduto"]
    
    def getAbbonamentiPossibili(self, email):
        tutti = self.caricaFile()
        return tutti.get(email, [])