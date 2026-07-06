import os
import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Calcolo del percorso della cartella principale del progetto
# Corretto l'uso di **file** in __file__ [1]
cartella_corrente = os.path.dirname(os.path.abspath(__file__)) 
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))

# Aggiunta della radice del progetto al sys.path per permettere gli import [2]
if radice_progetto not in sys.path: 
    sys.path.append(radice_progetto)

# Importazione corretta del modello Piattaforma [2]
from models.piattaforma import Piattaforma

class GestoreRicerca:
    """Rappresenta il gestore che si occupa di interfacciarsi con i siti esterni."""
    
    # Corretto il nome del costruttore da **init** a __init__ [2]
    def __init__(self, piattaforma: Piattaforma):
        """Inizializza il gestore con una specifica piattaforma di riferimento."""
        self._piattaforma = piattaforma
        self._driver = None # Sarà inizializzato quando serve la ricerca web



    def esegui_ricerca(self, termine_ricerca: str):
        """
        Esegue la ricerca sulla piattaforma impostata utilizzando il termine fornito.
        Sfrutta i link di ricerca definiti nel modello Piattaforma.
        """
        link_base = self._piattaforma.get_link_ricerca()
        url_finale = link_base.format(termine_ricerca)
        print(f"Ricerca in corso su {self._piattaforma.get_nome()} per: {termine_ricerca}")
        # Qui andrebbe la logica Selenium per navigare all'url_finale [3, 4]