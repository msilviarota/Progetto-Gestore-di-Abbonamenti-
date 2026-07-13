import os
import sys

# Calcolo del percorso radice del progetto per gestire gli import e i file
# Corretto l'uso di __file__ (doppio underscore) [4]
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

class RepositoryLog:
    """
    Gestisce la persistenza del log di sessione.
    Memorizza l'email dell'ultimo utente che ha effettuato l'accesso.
    """

    def __init__(self, nome_file="log"):
        # Percorso robusto verso repository2/log (visto in imagine2) [5]
        self._cartella_dati = os.path.join(radice_progetto, "repository2")
        self._percorso_file = os.path.join(self._cartella_dati, nome_file)
        
        # Assicura che la cartella repository2 esista [5]
        if not os.path.exists(self._cartella_dati):
            os.makedirs(self._cartella_dati)

    def salvaLog(self, email: str):
        """
        Salva l'email dell'utente loggato nel file di log.
        Viene chiamato dal GestoreLogin dopo un accesso riuscito.
        """
        try:
            with open(self._percorso_file, "w", encoding="utf-8") as f:
                f.write(email)
            return True
        except Exception as e:
            print(f"Errore durante il salvataggio del log: {e}")
            return False

    def recuperaUltimoLog(self):
        """
        Legge il file di log e restituisce l'email dell'utente attivo.
        Se il file non esiste o è vuoto, restituisce None.
        """
        if not os.path.exists(self._percorso_file):
            return None
            
        try:
            with open(self._percorso_file, "r", encoding="utf-8") as f:
                email = f.read().strip()
                return email if email else None
        except Exception as e:
            print(f"Errore durante la lettura del log: {e}")
            return None

    def cancellaLog(self):
        """
        Rimuove l'email dal file di log (Logout).
        """
        if os.path.exists(self._percorso_file):
            os.remove(self._percorso_file)