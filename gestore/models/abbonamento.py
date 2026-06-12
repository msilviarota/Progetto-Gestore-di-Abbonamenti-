from datetime import datetime

# =====================================================================
# ═══════════════════════ SECTION 1: ENTITY ═══════════════════════════
# =====================================================================



class Abbonamento:
    def __init__(self, codice_identificativo: str, nome_utente: str, cognome_utente: str, piattaforma_nome: str):
        self._codice_identificativo = codice_identificativo
        self._nome_utente = nome_utente
        self._cognome_utente = cognome_utente
        self.piattaforma = piattaforma_nome
        self._data_scadenza = datetime.now()
        self._valido = True
        self._stato = "Attivo"

    # L'UNICA FUNZIONE: Recupera lo stato completo dell'abbonamento
    def ottieni_stato_abbonamento(self) -> dict:
        return {
            "codice": self._codice_identificativo,
            "piattaforma": self.piattaforma,
            "scadenza": self._data_scadenza,
            "valido": self._valido,
            "stato": self._stato
        }



class RepositoryUtente:
    def __init__(self): 
        self.utenti = {} # email -> Oggetto Utente
    def salva_utente(self, utente: Utente): 
        self.utenti[utente.get_email() if hasattr(utente, 'get_email') else utente._email] = utente


class RepositoryAbbonamenti:
    def __init__(self):
        self.attivi = {}   # email -> lista oggetti Abbonamento
        self.scaduti = {}  # email -> lista oggetti Abbonamento
    def salva_abbonamento(self, email: str, abbonamento: Abbonamento):
        if email not in self.attivi: self.attivi[email] = []
        self.attivi[email].append(abbonamento)


class RepositoryAcquisti:
    def __init__(self): 
        self.storico = {} # email -> lista Abbonamenti passati
    def registra_acquisto(self, email: str, abbonamento: Abbonamento):
        if email not in self.storico: self.storico[email] = []
        self.storico[email].append(abbonamento)


class RepositoryPreferenze:
    def __init__(self):
        self.categorie = ["Cinema", "Sport", "Musica", "Serie TV"]
    def ottieni_tutte_categorie(self) -> list: 
        return self.categorie


class RepositoryDati:
    def __init__(self):
        self.catalogo = [] # Lista globale di oggetti Contenuto
    def ottieni_catalogo_completo(self) -> list: 
        return self.catalogo


class RepositoryPagamenti:
    def __init__(self): 
        self.metodi = {} # email -> DatiPagamento
    def salva_metodo(self, email: str, dati: DatiPagamento): 
        self.metodi[email] = dati


class RepositoryLog:
    def __init__(self): 
        self.logs = []
    def aggiungi_log(self, evento: str): 
        self.logs.append((datetime.now(), evento))

