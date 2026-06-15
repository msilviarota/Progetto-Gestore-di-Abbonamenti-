import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Ora puoi importare utente direttamente senza usare i punti!
from database import repositoryAbbonamento
from database import repositoryUtente
from database import repositoryDatiPagamento
from models import notifica
from models import utente
from models import abbonamento
from models import piattaforma
from datetime import datetime


#==================================================================== 
# Rappresenta il «control» Gestore Abbonamenti
class GestoreAbbonamenti:
    def __init__(self):
        self._email = utente.get_email()
        return
    

    # Restituisce una lista di scelta degli abbonamenti
    def getLista(self):
        return repositoryAbbonamento.getAbbonamentiAttivi(self._email)


    # Riceve la scelta dell'utente e la elabora
    def inviaScelta(self, abbonamentoScelto):
        print(f"[Control] Ricevuto abbonamento: {abbonamentoScelto}. Elaborazione in corso...")
        repositoryUtente.controlloProfilo(self._email)
        repositoryDatiPagamento.getiDatiPagamaneto(self._email)
        notifica.inviaNotifica("Abbonamento scelto: " + abbonamento + "Dati di Pagamento" + repositoryDatiPagamento.getiDatiPagamaneto(self._email))
        piattaforma.inviaSceltaAbbonamento(piattaforma.getPiattaformaScelta(), abbonamento)        
        piattaforma.inviaDatiPagamento(piattaforma.getPiattaformaScelta(), repositoryDatiPagamento.getiDatiPagamaneto(self._email))
        nuovoAbbonamento = abbonamento(self._email, repositoryUtente.getInformazioni(self._email).get_nome(),
                                       repositoryUtente.getInformazioni(self._email).get_cognome(),
                                       abbonamentoScelto, datetime.now(), True, "Attivo")
        repositoryAbbonamento.salva_abbonamento(self._email, nuovoAbbonamento)
        return repositoryUtente.getInformazioni(self._email) is not None and notifica.inviaConferma()


    # Blocca l'operazione in caso di errori o dati non validi
    def bloccaOperazione(self, errore: str):
        notifica.inviaErrore(errore)
        print("[Control] Operazione bloccata per motivi di sicurezza.")
        return False