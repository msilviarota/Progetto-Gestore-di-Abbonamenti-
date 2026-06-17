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


    def filtra_categorie(self):
        from dialoghi import FinestraRicerca
        testo = self.campo_ricerca.text().lower().strip()

        if not testo:
            return

        risultati = []
        for chiave, servizi in self.link_categorie.items():
            if testo in chiave.lower():
                for nome, link, _ in servizi:
                    risultati.append((f"{chiave} → {nome}", link))
            else:
                for nome, link, _ in servizi:
                    if testo in nome.lower():
                        risultati.append((nome, link))

        finestra = FinestraRicerca(risultati, self)
        finestra.exec()


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

    # --- ESEMPI DI UTILIZZO ---
    # Ora puoi scegliere tu dove cercare cambiando semplicemente la parola finale:

        self.inviaCerca("Wednesday", "netflix")
        self.inviaCerca("The Boys", "prime")
        self.inviaCerca("Måneskin", "youtube")

        return






import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_e_cerca_netflix(email_utente, password_utente, film_da_cercare):
    # 1. Avvia il browser Chrome
    driver = webdriver.Chrome()
    attesa = WebDriverWait(driver, 10)
    
    try:
        # 2. Vai alla pagina di login di Netflix
        driver.get("https://www.netflix.com/it/login")
        
        # 3. Gestione dei Cookie (Clicca su Accetta se compare il banner)
        try:
            bottone_cookie = attesa.until(
                EC.element_to_be_clickable((By.ID, "cookie-disclosure-accept"))
            )
            bottone_cookie.click()
        except Exception:
            pass # Continua se il banner non appare
            
        # 4. Trova i campi di testo usando i loro attributi "name" HTML
        # Inserisce l'email e la password fornite
        campo_email = attesa.until(EC.presence_of_element_located((By.NAME, "userLoginId")))
        campo_email.send_keys(email_utente)
        
        campo_password = driver.find_element(By.NAME, "password")
        campo_password.send_keys(password_utente)
        
        # 5. Trova e clicca il pulsante di accesso (Sign In)
        # Netflix usa un pulsante con data-uia="login-submit-button"
        pulsante_accedi = driver.find_element(By.XPATH, '//button[@data-uia="login-submit-button"]')
        pulsante_accedi.click()
        
        # Aspetta che il login venga elaborato e la home si carichi
        time.sleep(5)
        
        # 6. Una volta dentro, naviga direttamente sulla ricerca del film
        parola_formattata = film_da_cercare.replace(" ", "%20")
        url_ricerca = f"https://netflix.com{parola_formattata}"
        driver.get(url_ricerca)
        
        print(f"Login effettuato e ricerca aperta per: {film_da_cercare}")
        
        # Lascia la pagina aperta per 15 secondi per goderti il film
        time.sleep(15)
        
    finally:
        # Chiude il browser controllato da Selenium
        driver.quit()

# --- COME USARE LA FUNZIONE ---
# Sostituisci con le tue vere credenziali di Netflix
MIA_EMAIL = "tuo_indirizzo@email.com"
MIA_PASSWORD = "la_tua_password_segreta"

login_e_cerca_netflix(MIA_EMAIL, MIA_PASSWORD, "Stranger Things")













import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_netflix_locale(film_da_cercare):
    # --- FASE 1: Leggi le credenziali dal file JSON locale ---
    print("Lettura delle credenziali dal file locale...")
    
    # Apriamo il file 'credenziali.json' presente nella stessa cartella del codice
    with open("credenziali.json", "r", encoding="utf-8") as file:
        dati_json = json.load(file)
    
    email_utente = dati_json.get("netflix_email")
    password_utente = dati_json.get("netflix_password")

    # --- FASE 2: Avvia Selenium e fai il login automatico ---
    print("Avvio del browser per il login automatico...")
    driver = webdriver.Chrome()
    attesa = WebDriverWait(driver, 10)
    
    try:
        driver.get("https://netflix.com")
        
        # Gestione dei Cookie
        try:
            bottone_cookie = attesa.until(
                EC.element_to_be_clickable((By.ID, "cookie-disclosure-accept"))
            )
            bottone_cookie.click()
        except Exception:
            pass
            
        # Inserimento Email e Password prese dal file locale
        campo_email = attesa.until(EC.presence_of_element_located((By.NAME, "userLoginId")))
        campo_email.send_keys(email_utente)
        
        campo_password = driver.find_element(By.NAME, "password")
        campo_password.send_keys(password_utente)
        
        # Clic sul pulsante Accedi
        pulsante_accedi = driver.find_element(By.XPATH, '//button[@data-uia="login-submit-button"]')
        pulsante_accedi.click()
        
        # Pausa per permettere il caricamento
        time.sleep(5)
        
        # Navigazione diretta sul film cercato
        parola_formattata = film_da_cercare.replace(" ", "%20")
        url_ricerca = f"https://netflix.com{parola_formattata}"
        driver.get(url_ricerca)
        
        print(f"Login completato per l'utente {email_utente}!")
        time.sleep(15)
        
    finally:
        driver.quit()

# --- COME USARE LA FUNZIONE ---
# Adesso basta solo passare il titolo del film!
login_netflix_locale("Wednesday")
