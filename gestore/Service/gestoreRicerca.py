import os
import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Questo comando calcola automaticamente il percorso della cartella principale del tuo progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from models.piattaforma import Piattaforma

#================================================================================================================
# Rappresenta il <<control>> GestoreRicerca
class GestoreRicerca():
    def __init__(self, piattaforma: Piattaforma):
        self._piattaforma = piattaforma
 
    # Definiamo la funzione che ci consete di avere accesso almeno a i catologhi delle varie piattaforme
    # e che ci consente di cercare una parola Chiave precisa.
    def inviaCerca(self, parolaChiave: str, piattaforma):
        # 1. Dizionario con i link di ricerca delle varie piattaforme
        # Il simbolo {} serve per inserire la parola formattata dentro al link
        link_piattaforme = {
            "netflix": "https://netflix.com{}",
            "prime": "https://primevideo.com{}",
            "youtube": "https://youtube.com{}",
            "disney": "https://disneyplus.com{}"
        }
        
        # Trasformiamo il nome della piattaforma in minuscolo per evitare errori di scrittura
        piattaforma = piattaforma.lower()
        
        # 2. Controllo se la piattaforma inserita è supportata
        if piattaforma not in link_piattaforme:
            print(f"Errore: La piattaforma '{piattaforma}' non è ancora supportata.")
            return
        
        # 3. Formatta la parola per l'URL (sostituisce gli spazi con %20)
        parola_formattata = parolaChiave.replace(" ", "%20")
        
        # 4. Costruisce l'URL specifico per quella piattaforma
        url_ricerca = link_piattaforme[piattaforma].format(parola_formattata)
        
        # 5. Avvia il browser
        driver = webdriver.Chrome()
        
        try:
            driver.get(url_ricerca)
            attesa = WebDriverWait(driver, 10)
            
            # 6. Gestione dei Cookie generica (funziona per Netflix e YouTube)
            try:
                # Prova a cliccare il banner cookie se presente
                # Nota: ogni sito potrebbe richiedere ID differenti, questo è un tentativo base
                bottone_cookie = attesa.until(
                    EC.element_to_be_clickable((By.ID, "cookie-disclosure-accept"))
                )
                bottone_cookie.click()
            except Exception:
                pass

            print(f"Ricerca completata per '{parolaChiave}' su {piattaforma.upper()}.")
            time.sleep(10)
            
        finally:
            driver.quit()
        return