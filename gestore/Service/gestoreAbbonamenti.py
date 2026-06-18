import os
import sys
import json

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Ora puoi importare utente direttamente senza usare i punti!
from database.repositoryAbbonamento import RepositoryAbbonamento
from database import repositoryUtente
from database.repositoryDatiPagamento import RepositoryDatiPagamento
from models.notifica import Notifica
from models.utente import Utente
from models.abbonamento import Abbonamento
from models import piattaforma
from datetime import datetime


#==================================================================== 
# Rappresenta il «control» Gestore Abbonamenti
class GestoreAbbonamenti:
    def __init__(self, utente: Utente, repoAbbonamento: RepositoryAbbonamento,
                 repoDatiPagamento: RepositoryDatiPagamento,
                 nomePiattaforma: piattaforma, notifica: Notifica):
        self._email = utente.get_email()
        self._repo_Abbonamento = repoAbbonamento
        self._repo_DatiPagamento = repoDatiPagamento
        self._notifica = notifica
        self._piattaforma = nomePiattaforma
        self._abbonamentoScelto = None
        return
    

    # Restituisce una lista di scelta degli abbonamenti
    def getLista(self):
        return self._repo_Abbonamento.getAbbonamentiPossibili(self._email)


    # Riceve la scelta dell'utente e la elabora
    def inviaScelta(self, abbonamentoScelto):
        print(f"[Control] Ricevuto abbonamento: {abbonamentoScelto}. Elaborazione in corso...")
        self._repo_Abbonamento.getAbbonamentiPossibili(self._email)
        self._repo_DatiPagamento.getiDatiPagamaneto(self._email)
        self._notifica.inviaNotifica("Abbonamento scelto: " + Abbonamento + "Dati di Pagamento" + self._repo_DatiPagamento.getiDatiPagamaneto(self._email))
        self._piattaforma.inviaSceltaAbbonamento(self._piattaforma.getPiattaformaScelta())        
        self._piattaforma.inviaDatiPagamento(self._piattaforma.getPiattaformaScelta(), self._repo_DatiPagamento.getiDatiPagamaneto(self._email))
        nuovoAbbonamento = Abbonamento(self._email, repositoryUtente.getInformazioni(self._email).get_nome(),
                                       repositoryUtente.getInformazioni(self._email).get_cognome(),
                                       abbonamentoScelto, datetime.now(), True, "Attivo")
        self._repo_Abbonamento.salva_abbonamento(self._email, nuovoAbbonamento)
        return self._notifica.inviaConferma()


    # Blocca l'operazione in caso di errori o dati non validi
    def bloccaOperazione(self, errore: str):
     self._notifica.inviaErrore(errore)
     print("[Control] Operazione bloccata per motivi di sicurezza.")
     return False


    # ===========================================================================================================================================================
    # Qui scriviamo il codice per il caso d'uso 2 in cui si affronta il caso in cui l'utente vuole disdire un abbonamento tra quelli comprati
    
    # recuperiamo gli abbonamenti attivi dalla self._repo_Abbonamento
    def recuperaAbbonamenti(self):
        return self._repo_Abbonamento.getAbbonamentiPossibili()
    
    # inviamo una notifica all'utente per accertarci che voglia disdire l'abbonamento
    def inviaSeleziona(self, abbonamentoScelto):
        self._abbonamentoScelto = abbonamentoScelto
        self._notifica.invia("Vuoi disdire?")
        return
    
    # Richiamiamo la funzione elimina_abbonamento per scorrere gli abbonamenti ed elimnare quello voluto
    # se presente
    def esguiDisdetta(self, abbonamentoScelto ):
        self._repo_Abbonamento.elimina_abbonamento(abbonamentoScelto)
        return
    

    #===================================================================================================================================================
    # Qui scrviamo il codice per il caso d'uso 12
    def ricordaScadenza(self):
        print("[Control] Avvio il calcolo delle date di scadenza...")
        
        tutti_abbonamenti = self._repo_Abbonamento.caricaFile()

        # 2. Prendi la data di oggi (senza ore e minuti, solo Anno-Mese-Giorno)
        oggi = datetime.now().date()
        print(f"[Control] Data di oggi: {oggi}")

        # 3. Cicla tutti gli utenti e i loro abbonamenti
        for email, lista_abbonamenti in tutti_abbonamenti.items():
            for abb in lista_abbonamenti:
                data_scadenza_abb = abb["scadenza"]
                
                if data_scadenza_abb:
                    # Converte la stringa del JSON "AAAA-MM-GG" in una vera data Python
                    data_scadenza = datetime.strptime(data_scadenza_abb, "%Y-%m-%d").date()
                    
                    # Calcola la differenza (data_scadenza - oggi)
                    differenza = data_scadenza - oggi
                    giorni_rimasti = differenza.days
                    
                    print(f"Abbonamento '{abb['tipo']}' di {email}: mancano {giorni_rimasti} giorni alla scadenza.")

                    # --- CONDIZIONE PER FAR SCATTARE IL TIMER/NOTIFICA ---
                    # Se i giorni rimasti sono 0 (scade oggi) o negativi (è già scaduto)
                    if giorni_rimasti == 1:
                        print(f"🚨 ATTENZIONE: L'abbonamento '{abb['tipo']}' sta per scadere! Attivo la notifica.")
                        self._notifica.inviaAvviso("L'abbonamento" + str(abb) + "sta per scadere")

                    elif giorni_rimasti <= 0:
                        print(f"🚨 ATTENZIONE: L'abbonamento '{abb['tipo']}' è scaduto! Attivo la notifica.")
                        self._notifica.inviaAvviso("L'abbonamento" + str(abb) + "è scaduto.")
                        # Ritorna il messaggio di errore che salirà fino all'interfaccia
                        return f"Il tuo abbonamento a {abb['tipo']} è scaduto il {data_scadenza_abb}!"
                        
        # Se nessun abbonamento è scaduto, ritorna None e il timer non farà nulla
        return None

    def getAbbonamento(self, abbonamento):
        return(abbonamento)
    
    def avviaProceduraRinnovo(self, abbonamento_da_rinnovare):
        nuovoAbbonamento = Abbonamento(self._email, abbonamento_da_rinnovare["nome"],
                                       abbonamento_da_rinnovare["cognome"],
                                       abbonamento_da_rinnovare["piattaforma"])
        self._repo_Abbonamento.elimina_abbonamento(abbonamento_da_rinnovare)
        self._repo_Abbonamento.salva_abbonamento(nuovoAbbonamento)
        return