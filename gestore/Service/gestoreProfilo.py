import os
import json

DB_PROFILO = "db_profilo.json"
DB_PREFERENZE = "db_preferenze.json"

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
    """Salva le preferenze (es. ['🎵 Musica', '🎬 Video']) nel file delle preferenze."""
    # Carichiamo il file esistente se c'è, altrimenti creiamo un dizionario vuoto
    if os.path.exists(DB_PREFERENZE):
        with open(DB_PREFERENZE, 'r', encoding='utf-8') as f:
            dati_pref = json.load(f)
    else:
        dati_pref = {}

    # Associamo le preferenze all'utente corrente (usiamo un id simulato o l'email)
    profilo = carica_profilo()
    email_utente = profilo.get("email", "utente_generico")
    
    dati_pref[email_utente] = {"categorie": lista_preferenze}

    with open(DB_PREFERENZE, 'w', encoding='utf-8') as f:
        json.dump(dati_pref, f, indent=4, ensure_ascii=False)
