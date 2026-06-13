import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Ora puoi importare utente direttamente senza usare i punti!
from models import utente
#from models import registrazione
#from models import RegistrazioneRepository



class InterfacciaUtente:
    """Rappresenta la «boundary» Interfaccia Utente"""
    
    def __init__(self, gestore_registrazione):
        self.gestore = gestore_registrazione

    def registrazione(self):
        # 1. L'utente clicca o avvia la registrazione
        # 2. L'interfaccia chiede il modulo al gestore (control)
        modulo = self.gestore.getModulo("registrazione")
        
        # 3. Ricevuto il modulo, l'interfaccia lo mostra all'utente
        self.mostraModulo(modulo)

    def mostraModulo(self, tipo_modulo):
        print(f"[UI] Mostro a schermo il modulo di: {tipo_modulo}")

    def inviaModulo(self, nome, email, password):
        print(f"[UI] Ricevuti dati dall'utente. Invio al gestore...")
        # Nota: Nel diagramma l'invio si ferma alla UI, ma realisticamente 
        # qui la UI passerà i dati al GestoreRegistrazione per salvarli.
        self.GestoreRegistrazione.elabora_registrazione(nome, email, password)






class Notifiche:
    def __init__(self):
        pass
    def Notifica(self, messaggio):
        print(f"[Notifica] {messaggio}")
        return messaggio
    


# --- SIMULAZIONE DEL FLUSSO (L'Attore 'Utente' interagisce con il sistema) ---
if __name__ == "__main__":
    # Inizializziamo i componenti del sistema
    gestore_control = GestoreRegistrazione()
    interfaccia_ui = InterfacciaUtente(gestore_control)

    print("--- INIZIO FLUSSO DIAGRAMMA DI SEQUENZA ---")
    
    # Freccia 1: Utente -> registrazione() sulla Interfaccia Utente
    interfaccia_ui.registrazione()
    
    print("\n--- L'UTENTE COMPILA I CAMPI ---")
    
    # Freccia 5: Utente -> inviaModulo(nome, email, password) sulla Interfaccia Utente
    interfaccia_ui.inviaModulo(nome="Mario Rossi", email="mario@example.com", password="password123")



class InterfacciaUtente:
    """Rappresenta la «boundary» Interfaccia Utente"""
    
    def __init__(self, gestore_autenticazione):
        self.gestore = gestore_autenticazione

    def logout(self):
        print("\n[UI] L'utente ha cliccato su 'Disconnetti'.")
        # Comunica al gestore (control) di effettuare il logout
        successo = self.gestore.disconnetti_utente()
        
        if successo:
            self.mostra_schermata_login()
        else:
            print("[UI] Errore: Nessun utente era loggato.")

    def mostra_schermata_login(self):
        print("[UI] Schermata di Login mostrata con successo. Arrivederci!")


class GestoreAutenticazione:
    """Rappresenta il «control» Gestore Autenticazione / Registrazione"""
    
    def __init__(self):
        # Simuliamo una sessione attiva memorizzando l'utente corrente
        # Se è None, significa che nessun utente è loggato
        self.utente_corrente = "Mario Rossi" 

    def disconnetti_utente(self):
        if self.utente_corrente is not None:
            print(f"[Control] Rimozione della sessione per l'utente: {self.utente_corrente}")
            # Resettiamo l'utente corrente a None (Logout)
            self.utente_corrente = None
            print("[Control] Logout effettuato nel sistema.")
            return True
        else:
            return False


# --- SIMULAZIONE DEL FLUSSO ---
if __name__ == "__main__":
    gestore_control = GestoreAutenticazione()
    interfaccia_ui = InterfacciaUtente(gestore_control)

    print("--- STATO INIZIALE ---")
    print(f"Utente connesso nel sistema: {gestore_control.utente_corrente}")

    # L'utente avvia il processo di logout dalla UI
    interfaccia_ui.logout()

    print("\n--- STATO FINALE ---")
    print(f"Utente connesso nel sistema: {gestore_control.utente_corrente}")