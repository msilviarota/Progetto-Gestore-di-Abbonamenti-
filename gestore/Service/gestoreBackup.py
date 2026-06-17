import os
import time
import json
import logging
from datetime import datetime

# Configurazione del Logging (Requisito CDU23 - Flusso principale 4)
logging.basicConfig(
    filename='backup_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Percorsi simulati dei dati del database e della cartella di stoccaggio
DB_ABBONAMENTI = "db_abbonamenti.json"
DB_PREFERENZE = "db_preferenze.json"
CARTELLA_BACKUP = "stoccaggio_backup"

# Creazione della cartella di backup se non esiste
if not os.path.exists(CARTELLA_BACKUP):
    os.makedirs(CARTELLA_BACKUP)

def crea_dati_simulati_se_assenti():
    """Crea file di database fittizi se non esistono, per testare lo script."""
    if not os.path.exists(DB_ABBONAMENTI):
        conf_iniziale = {"utente_id_1": {"abbonamenti": ["Netflix", "Spotify"]}}
        with open(DB_ABBONAMENTI, 'w') as f:
            json.dump(conf_iniziale, f)
    if not os.path.exists(DB_PREFERENZE):
        pref_iniziali = {"utente_id_1": {"generi": ["Cinema", "Musica"]}}
        with open(DB_PREFERENZE, 'w') as f:
            json.dump(pref_iniziali, f)

def esegui_backup():
    """Esegue la copia di sicurezza dei dati (CDU23 - Flusso principale)."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cartella_istanza = os.path.join(CARTELLA_BACKUP, f"backup_{timestamp}")
    
    try:
        # Simulazione di un possibile errore casuale per testare il flusso alternativo
        # (Es. mancanza di permessi o file occupati)
        if not os.path.exists(DB_ABBONAMENTI) or not os.path.exists(DB_PREFERENZE):
            raise FileNotFoundError("Database non trovati per il backup.")
            
        os.makedirs(cartella_istanza)
        
        # 1. Copia dei dati degli abbonamenti (Flusso principale 2)
        with open(DB_ABBONAMENTI, 'r') as f_in:
            dati_abb = json.load(f_in)
        with open(os.path.join(cartella_istanza, "backup_abbonamenti.json"), 'w') as f_out:
            json.dump(dati_abb, f_out, indent=4)
            
        # 2. Copia delle preferenze utente (Flusso principale 3)
        with open(DB_PREFERENZE, 'r') as f_in:
            dati_pref = json.load(f_in)
        with open(os.path.join(cartella_istanza, "backup_preferenze.json"), 'w') as f_out:
            json.dump(dati_pref, f_out, indent=4)
            
        # Successo: Scrittura log (Flusso principale 4)
        info_successo = f"Backup completato con successo in: {cartella_istanza}"
        print(info_successo)
        logging.info(info_successo)
        return True

    except Exception as e:
        # Fallimento: Scrittura log ed errore (Flusso alternativo)
        info_errore = f"FALLIMENTO BACKUP: {str(e)}"
        print(info_errore)
        logging.error(info_errore)
        return False

def avvia_pianificazione():
    """Controlla l'orario e attiva il backup alle 23:30 (Attore Tempo)."""
    print("Gestore Backup avviato. In attesa delle ore 23:30...")
    logging.info("Servizio di pianificazione backup avviato.")
    
    crea_dati_simulati_se_assenti()
    
    while True:
        ora_attuale = datetime.now().strftime("%H:%M")
        
        # Condizione di attivazione: ore 23:30 (Requisito 2.5)
        if ora_attuale == "23:30":
            successo = esegui_backup()
            
            if not successo:
                # Flusso alternativo: riprova dopo 10 minuti (600 secondi)
                msg_riprovo = "Il sistema riproverà l'operazione tra 10 minuti."
                print(msg_riprovo)
                logging.warning(msg_riprovo)
                
                time.sleep(600) 
                print("Esecuzione del tentativo di recupero backup...")
                esegui_backup()
            
            # Evita che il ciclo riesegua il backup più volte nello stesso minuto delle 23:30
            time.sleep(60)
            
        # Controllo dell'ora ogni 30 secondi per non sovraccaricare la CPU
        time.sleep(30)

if __name__ == "__main__":
    # Per testare IMMEDIATAMENTE il funzionamento senza aspettare le 23:30,
    # puoi decommentare la riga successiva:
    # esegui_backup()
    
    avvia_pianificazione()
