import os
import sys

# Calcolo automatico della radice del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from database.repositoryDati import RepositoryDati
from models.piattaforma import Piattaforma
from models.notifica import Notifica

class GestoreStreaming:
    """Colonna centrale 'GestoreStreaming'."""
    def __init__(self, repoDati: RepositoryDati, piattaforma: Piattaforma):
        self._repo_Dati = repoDati
        self._piattaforma_esterna = piattaforma
        self._notifiche = Notifica()

    def avviaPiattaforma(self, email_utente: str, password_utente: str, nome_contenuto: str):
        """
        Esegue l'intero flusso del diagramma di sequenza.
        """
        print(f"\n[Control] riproduzione({nome_contenuto}) avviata.")
        
        # --- 1. BLOCCO: Verifica Abbonamento ---
        # Freccia verso la repository
        stato = self._repo_Dati.verificaAbbonamento(email_utente, password_utente)
        print(f"[Control] Risposta ricevuta: statoAbbonamento() -> {stato}")
        
        # --- 2. BLOCCO CONDIZIONALE (alt) ---
        
        # CASO A: ABBONAMENTO SCADUTO (Flusso Alternativo)
        if stato == "scaduto":
            # Chiama l'entità notifiche
            self._notifiche.inviaNotificaScadenza(nome_contenuto)
            # Fa risalire la notifica verso l'interfaccia (Catena di return)
            return "errore", "Abbonamento scaduto"
            
        # CASO B: ABBONAMENTO VALIDO
        elif stato == "valido":
            
            # --- 3. BLOCCO: Recupero Dati di Accesso ---
            # Richiede le credenziali alla repository
            email_acc, pass_acc = self._repo_Dati.getDati(email_utente, password_utente)
            print(f"[Control] Ricevuto messaggio di ritorno: mostra({email_acc}, ****** )")
            
            # --- 4. BLOCCO: Avvio Piattaforma Esterna ---
            # Trasmette i dati all'Entity esterna (Spostato qui webbrowser/selenium per SOLID)
            self._piattaforma_esterna.trasmettiDati(nome_contenuto, "Dati_Abbonamento")
            
            # Restituisce il successo all'interfaccia per mostrare il video (mostra(piattaforma, contenuto))
            return "successo", (nome_contenuto, "Piattaforma Pronta")

