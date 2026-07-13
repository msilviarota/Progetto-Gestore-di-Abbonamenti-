import os
import sys
import webbrowser # Necessario per aprire i link delle piattaforme
from models.notifica import Notifica
from models.piattaforma import Piattaforma
from models.contenuto import Contenuto
from repository.repositoryAbbonamento import RepositoryAbbonamento
from repository.repositoryDati import RepositoryDati

# Calcolo del percorso radice del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__)) 
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path: 
    sys.path.append(radice_progetto)

class GestoreStreaming:
    """
    Rappresenta il gestore che interfaccia l'utente con le piattaforme esterne.
    Implementa il CDU18 (Riproduci).
    """

    def __init__(self, repoDati: RepositoryDati, repoAbb: RepositoryAbbonamento, 
                 piattaforma: Piattaforma, notifica: Notifica):
        """Inizializza il gestore con le repository e la piattaforma di riferimento."""
        self._repo_Dati = repoDati
        self._repo_Abb = repoAbb
        self._piattaforma_esterna = piattaforma
        self._notifica = notifica

    def avvia_riproduzione(self, contenuto: Contenuto, email_utente: str):
        """
        CDU18: Verifica l'abbonamento e avvia la piattaforma esterna.
        """
        # 1. Verifica validità abbonamento (CDU18 - Punto 2 del flusso principale)
        abbonamento = self._repo_Abb.ottieni_abbonamento_attivo(email_utente, contenuto._piattaforma)

        if not abbonamento or not abbonamento['validita']:
            self._notifica = Notifica("Abbonamento non valido o scaduto. Impossibile riprodurre.", "Errore")
            return False

        # 2. Recupero URL di ricerca/riproduzione dalla piattaforma
        # Formatta il link di ricerca con il titolo del contenuto
        url_finale = self._piattaforma_esterna.link_ricerca.format(contenuto._titolo)
        try:
            # 3. Avvio interfaccia piattaforma (CDU18 - Punto 4)
            print(f"Trasmissione dati a {self._piattaforma_esterna.nome} per: {contenuto._titolo}")
            webbrowser.open(url_finale)

            # 4. Notifica di successo
            self._notifica = Notifica(f"Apertura di {contenuto._titolo} su {self._piattaforma_esterna.nome}...", "Successo")
            return True
        except Exception as e:
            self._notifica = Notifica(f"Errore nell'avvio della piattaforma: {str(e)}", "Errore")
            return False