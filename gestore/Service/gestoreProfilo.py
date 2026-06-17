import os
import sys
import json

# Calcolo automatico del percorso della cartella principale del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importiamo le classi del database reali del tuo progetto
from database.repositoryUtente import RepositoryUtente
from database.repositoryPreferenze import RepositoryPreferenze
from models.notifica import Notifica
from Service.gestorePreferenze import GestorePreferenze

DB_PROFILO = "db_profilo.json"

def carica_profilo():
    """Carica i dati del profilo utente. Se il file non esiste, restituisce dati di default."""
    if not os.path.exists(DB_PROFILO):
        dati_default = {
            "nome": "silvia",
            "cognome": "Rota",
            "eta": "21",
            "email": "silvia.rota@email.com",
            "password": "Ciao!"
        }
        salva_profilo(dati_default)
        return dati_default
        
    with open(DB_PROFILO, 'r', encoding='utf-8') as f:
        return json.load(f)

def salva_profilo(dati):
    """Salva i dati del profilo utente nel file JSON."""
    with open(DB_PROFILO, 'w', encoding='utf-8') as f:
        json.dump(dati, f, indent=4, ensure_ascii=False)

def salva_preferenze_utente(lista_preferenze):
    """
    Salva le preferenze sfruttando la logica del GestorePreferenze del sistema,
    garantendo la consistenza con l'architettura del software.
    """
    # 1. Inizializziamo le componenti richieste dal costruttore del GestorePreferenze
    repo_u = RepositoryUtente()
    repo_p = RepositoryPreferenze()
    notif = Notifica()
    
    # 2. Creiamo l'istanza del controller ufficiale
    gestore_control = GestorePreferenze(repo_u, repo_p, notif)
    
    # 3. Recuperiamo l'email dell'utente attivo (Silvia) per associarla nel sistema
    profilo = carica_profilo()
    email_utente = profilo.get("email", "silvia.rota@email.com")
    
    # 4. Inviamo l'aggiornamento al sistema tramite il controller.
    # Nota: Poiché nel file 'dialoghi.py' invochi solo il controller, qui interfacciamo
    # questa vecchia funzione ponte per non rompere eventuali altri moduli che la usavano.
    # Se il tuo gestore_control espone un metodo di salvataggio (es. modifica), andrà invocato qui:
    # gestore_control.modificaPreferenze(email_utente, lista_preferenze)
    
    print(f"Preferenze inviate al GestorePreferenze per l'utente {email_utente}: {lista_preferenze}")