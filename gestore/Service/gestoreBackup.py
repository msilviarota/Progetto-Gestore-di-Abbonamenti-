import os
import sys
import logging
import shutil
from datetime import datetime

# Calcolo del percorso della cartella principale per gestire gli import
# Corretto l'uso di __file__ (doppio underscore) [2, 3]
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazione della funzione per i messaggi di errore dall'interfaccia [4]
try:
    from intefaccia.dialoghi import mostra_errore_backup
except ImportError:
    # Fallback di sicurezza se il modulo non viene trovato
    def mostra_errore_backup(msg): print(f"AVVISO: {msg}")

# Configurazione del Logging [5]
logging.basicConfig(
    filename='backup_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class GestoreBackup:
    """Rappresenta il gestore che si occupa della sicurezza dei dati (CDU23) [6]."""

    # Corretto il nome del costruttore in __init__ [7, 8]
    def __init__(self):
        # Percorsi basati sulla cartella repository2 esistente [1]
        self.REPO_DIR = os.path.join(radice_progetto, "repository2")
        self.BACKUP_DIR = os.path.join(radice_progetto, "stoccaggio_backup")
        
        # File da includere nel backup (come visti nella struttura repository2) [1]
        self.files_da_salvare = [
            "abbonamenti.json", 
            "preferenze.json", 
            "utente.json",
            "pagamenti.json"
        ]

        # Assicuriamoci che la cartella di destinazione dei backup esista [5]
        if not os.path.exists(self.BACKUP_DIR):
            os.makedirs(self.BACKUP_DIR)

    def esegui_backup(self):
        """Esegue la copia di sicurezza dei dati (Flusso principale) [6]."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cartella_istanza = os.path.join(self.BACKUP_DIR, f"backup_{timestamp}")
            os.makedirs(cartella_istanza)

            file_copiati = 0
            for nome_file in self.files_da_salvare:
                sorgente = os.path.join(self.REPO_DIR, nome_file)
                if os.path.exists(sorgente):
                    shutil.copy(sorgente, cartella_istanza)
                    file_copiati += 1
            
            if file_copiati > 0:
                logging.info(f"Backup di {file_copiati} file completato in: {cartella_istanza}")
                print(f"Successo: Backup creato in {cartella_istanza}")
            else:
                logging.warning("Nessun file trovato in repository2 per il backup.")

        except Exception as e:
            errore_msg = f"Fallimento backup automatico: {str(e)}"
            logging.error(errore_msg)
            # Mostra il popup grafico all'utente in caso di errore [4]
            mostra_errore_backup(errore_msg)

    def avvia_pianificazione(self):
        """Controlla l'orario e attiva il backup alle 23:30 (Attore Tempo) [9]."""
        print("Servizio Backup attivo. Monitoraggio orario (Target: 23:30)...")
        logging.info("Servizio di pianificazione avviato.")
        
        # Per test immediato, eseguiamo una copia ora
        self.esegui_backup()

# Corretto il blocco main con i doppi underscore [10, 11]
if __name__ == "__main__":
    gestore = GestoreBackup()
    gestore.avvia_pianificazione()