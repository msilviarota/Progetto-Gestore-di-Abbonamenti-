class Utente:
    def __init__(self, nome: str, cognome: str, eta: int, email: str, password: str, codice_identificativo: str):
        self._nome = nome
        self._cognome = cognome
        self._eta = eta
        self._email = email
        self._password = password
        self._codice_identificativo = codice_identificativo
        self._preferenze = []

    # L'UNICA FUNZIONE: Recupera tutti i dati dell'utente in un colpo solo
    def ottieni_profilo_completo(self) -> dict:
        return {
            "nome": self._nome,
            "cognome": self._cognome,
            "eta": self._eta,
            "email": self._email,
            "codice": self._codice_identificativo,
            "preferenze": self._preferenze
        }
