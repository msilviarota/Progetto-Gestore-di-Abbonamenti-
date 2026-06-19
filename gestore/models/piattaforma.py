# Import necessari per eventuali implementazioni future di automazione
import time
# Nota: Questi import sono presenti nelle fonti originali del modello
# sebbene il metodo trasmettiDati attualmente esegua solo una stampa.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.contenuto import Contenuto
class Piattaforma:
    """
    Rappresenta una piattaforma (Netflix, Prime Video, Spotify, ecc.)
    con un catalogo di contenuti ricercabili.
    """

    def __init__(self, nome: str, logo: str, link_login: str, categoria: str):
        self._nome = nome
        self._logo = logo
        self._link_login = link_login
        self._categoria = categoria
    @property
    def nome(self):
        return self._nome

    @property
    def logo(self):
        return self._logo

    @property
    def link_login(self):
        return self._link_login

    @property
    def categoria(self):
        return self._categoria

    def trasmettiDati(self, nome_contenuto, dati_abbonamento):
        """
        Simula la trasmissione dei dati alla piattaforma esterna 
        per l'avvio della riproduzione (CDU18).
        """
        print(f"[Piattaforma] Avvio {nome_contenuto}...")
        return True
 

# ====================================================================
# CATALOGO COMPLETO DELLE PIATTAFORME SUPPORTATE
# ====================================================================
CATALOGO_PIATTAFORME = {
    "netflix": Piattaforma(
        nome="Netflix",
         link_login="https://www.netflix.com/login",
        logo="loghi/netflix.png",
        categoria="Streaming",
         catalogo=[
            Contenuto("n1", "Stranger Things", "Netflix", "Serie"),
            Contenuto("n2", "The Witcher", "Netflix", "Serie"),
            Contenuto("n3", "Red Notice", "Netflix", "Film"),
        ]
    ),
    "prime video": Piattaforma(
        nome="Prime Video",
        link_login="https://www.primevideo.com",
        logo="loghi/primevideo.png",
        categoria="Streaming"
    ),
    "youtube": Piattaforma(
        nome="YouTube",
        link_login="https://www.youtube.com",
        logo="loghi/youtube.png",
        categoria="Video"
    ),
    "disney +": Piattaforma(
        nome="Disney+",
        link_login="https://www.disneyplus.com/it-it",
        logo="loghi/disney.png",
        categoria="Streaming"
    ),
    "applemusic": Piattaforma(
        nome="Apple Music",
        link_login="https://www.apple.com/it/apple-music/",
        logo="loghi/appmusic.png",
        categoria="Musica"
    ),
    "spotify": Piattaforma(
        nome="Spotify",
        link_login="https://open.spotify.com/intl-it",
        logo="loghi/spotify.png",
        categoria="Musica"
    ),
    "amazon music": Piattaforma(
        nome="Amazon Music",
        link_login="https://music.amazon.it/",
        logo="loghi/amazonmusic.png",
        categoria="Musica"
    ),
    "mediaset infinity": Piattaforma(
        nome="Mediaset Infinity",
        link_login="https://www.mediasetplay.mediaset.it/",
        logo="loghi/mediasetinfinity.png",
        categoria="Streaming"
    ),
    "raiplay": Piattaforma(
        nome="RaiPlay",
        link_login="https://www.raiplay.it/",
        logo="loghi/raiplay.png",
        categoria="Streaming"
    ),
    "kobo": Piattaforma(
        nome="Kobo",
        link_login="https://www.kobo.com/it/it",
        logo="loghi/kobo.png",
        categoria="Libri"
    ),
    "kindle": Piattaforma(
        nome="Kindle",
        link_login="https://leggi.amazon.it/landing",
        logo="loghi/kindle.png",
        categoria="Libri"
    ),
    "sky sport": Piattaforma(
        nome="Sky Sport",
        link_login="https://sport.sky.it/",
        logo="loghi/skysport.png",
        categoria="Sport"
    ),
    "now tv": Piattaforma(
        nome="Now TV",
        link_login="https://www.nowtv.it/sport",
        logo="loghi/nowtv.png",
        categoria="Sport"
    ),
}