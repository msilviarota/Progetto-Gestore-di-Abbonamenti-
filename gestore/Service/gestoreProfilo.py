import os
import sys

cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from repository.repositoryUtente import RepositoryUtente
from repository.repositoryDatiPagamento import RepositoryDatiPagamento
from models.datiPagamento import DatiPagamento
from models.cartadiCredito import CartaDiCredito
from models.utente import Utente
from models.datiPagamento import DatiPagamento
from models.notifica import Notifica

class GestoreProfilo:
    """
    Gestisce le operazioni legate al profilo utente (CDU7, CDU9, CDU16).
    """

    def __init__(self, repoUtente: RepositoryUtente, notifica: Notifica,
                 repoDatiPagamento: RepositoryDatiPagamento = None):
        self._repo_Utente = repoUtente
        self._notifica = notifica
        self._repo_DatiPagamento = repoDatiPagamento or RepositoryDatiPagamento

    def ottieni_dati_utente(self, email: str):
        utente_dict = self._repo_Utente.ottieni_per_email(email)
        if utente_dict:
            return Utente(
                nome=utente_dict.get('nome'),
                cognome=utente_dict.get('cognome'),
                eta=utente_dict.get('eta'),
                email=utente_dict.get('email'),
                password=utente_dict.get('password')
            )
        return None

    def aggiorna_dati_personali(self, utente_aggiornato: Utente):
        successo = self._repo_Utente.aggiorna_utente(utente_aggiornato)
        if successo:
            self._notifica = Notifica("Profilo aggiornato con successo.", "Successo")
        else:
            self._notifica = Notifica("Errore durante l'aggiornamento del profilo.", "Errore")
        return successo

    def cambia_password_utente(self, email: str, vecchia_pass: str, nuova_pass: str):
        utente = self.ottieni_dati_utente(email)
        if utente and utente._password == vecchia_pass:
            utente._password = nuova_pass
            self._repo_Utente.aggiorna_utente(utente)
            self._notifica = Notifica("Password cambiata correttamente.", "Successo")
            return True

        self._notifica = Notifica("La vecchia password non è corretta.", "Errore")
        return False

    def cambia_carta_utente(self, email: str, vecchia: str, nuova: str, cvv: str = ""):
        carta_attuale = self._repo_DatiPagamento.ottieni_numero_carta(email)

        if carta_attuale != vecchia:
            self._notifica = Notifica("Il vecchio numero carta non è corretto.", "Errore")
            return False

        utente = self.ottieni_dati_utente(email)
        nome_titolare = utente._nome if utente else "Demo"
        cognome_titolare = utente._cognome if utente else "User"

        dati_precedenti = self._repo_DatiPagamento.ottieni_per_utente(email)
        scadenza = dati_precedenti.get("scadenza", "12/30")

        # NOTA: il CVV viene usato solo per la validazione del form (lato GUI),
        # ma non viene mai salvato su disco per motivi di sicurezza (standard PCI-DSS:
        # il CVV non va mai persistito dopo l'autorizzazione).
        nuovi_dati = CartaDiCredito(
            numero_carta=nuova,
            scadenza_carta=scadenza,
            nome_titolare=nome_titolare,
            cognome_titolare=cognome_titolare
            # cvv NON passato qui: resta "" di default, non verrà salvato
        )

        self._repo_DatiPagamento.aggiornaDatiPagamento(email, nuovi_dati)
        self._notifica = Notifica("Carta aggiornata correttamente.", "Successo")
        return True