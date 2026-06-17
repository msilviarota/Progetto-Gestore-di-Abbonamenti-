import os
import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.piattaforma import CATALOGO_PIATTAFORME
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
            "netflix": "https://www.netflix.com/it/login?serverState=Bgi3uuvcAxK1Ac2GPyEBJXr89EhSDVBn4MShVY1lMLQOwYH5Xr6AAfpWtY5W5va3bSDF%2FHB%2B2EQkZYdciX7LSzcbYg%2FJKsLjHZNIt2G%2Frbv6JLiykpXFEShNbnfNJw8caP4DG8f1cY0xdIADXtDWnj9qoCmFrKBLS12K1oSrTriD5SIXyUf6qj%2FFOSS3IM87Djqmxd4R3Hcq3Ydpb%2Frka%2B%2BcMwmC2jk5INlRWV3vSq17YKB4uC0TVFGyUfAnX4QYBiIOCgydiKLowBcR91EZTrU%3D}",
            "prime video": "https://www.primevideo.com{}",
            "youtube": "https://www.youtube.com{}",
            "disney + ": "https://www.disneyplus.com/it-it{}",
            "apple music":"https://www.apple.com/it/apple-music/{}",
            "spotify": "https://open.spotify.com/intl-it{}",
            "amazon music": "https://music.amazon.it/{}",
            "mediaset infinity":"https://www.mediasetplay.mediaset.it/{}",
            "raiplay": "https://www.raiplay.it/{}",
            "kobo": "https://www.kobo.com/it/it{}",
            "kindle": "https://leggi.amazon.it/landing{}",
            "sky sport":"https://sport.sky.it/{}",
            "now tv":"https://www.nowtv.it/sport{}",
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