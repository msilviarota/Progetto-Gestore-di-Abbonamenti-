from datetime import datetime

# =====================================================================
# ═══════════════════════ SECTION 1: ENTITY ═══════════════════════════
# =====================================================================



class Abbonamento:
    def __init__(self, email : str, nome_utente: str, cognome_utente: str, piattaforma_nome: str):
        self._email = email
        self._nome_utente = nome_utente
        self._cognome_utente = cognome_utente
        self.piattaforma = piattaforma_nome
        self._data_scadenza = datetime.now()
        self._valido = True
        self._stato = "Attivo"

    # L'UNICA FUNZIONE: Recupera lo stato completo dell'abbonamento
    def ottieni_stato_abbonamento(self) -> dict:
        return {
            "email": self._email,
            "piattaforma": self.piattaforma,
            "scadenza": self._data_scadenza,
            "valido": self._valido,
            "stato": self._stato
        }


















