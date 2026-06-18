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
class GestoreRicerca:
    def __init__(self, piattaforma: Piattaforma):
        self._piattaforma = piattaforma
    
    # Definiamo la funzione che ci consete di avere accesso almeno a i catologhi delle varie piattaforme
    # e che ci consente di cercare una parola Chiave precisa.


        

    def inviaCerca(self, parolaChiave: str, piattaforma_nome, email="", password=""):
          piattaforma_key = piattaforma_nome.lower()

          if piattaforma_key not in CATALOGO_PIATTAFORME:
               print(f"Errore: La piattaforma '{piattaforma_nome}' non è ancora supportata.")
               return

          piattaforma_obj = CATALOGO_PIATTAFORME[piattaforma_key]
          parola_formattata = parolaChiave.replace(" ", "%20")
          url_ricerca = piattaforma_obj.get_link_ricerca().format(parola_formattata)

          driver = webdriver.Chrome()

          try:
               if email and password:
                    print(f"[Demo] Tentativo di login su {piattaforma_obj.get_nome()} con {email}")

               driver.get(url_ricerca)
               attesa = WebDriverWait(driver, 10)

               try:
                    bottone_cookie = attesa.until(
                         EC.element_to_be_clickable((By.ID, "cookie-disclosure-accept"))
                    )
                    bottone_cookie.click()
               except Exception:
                    pass

               print(f"Ricerca completata per '{parolaChiave}' su {piattaforma_obj.get_nome().upper()}.")
               time.sleep(10)

          finally:
               driver.quit()
          return
