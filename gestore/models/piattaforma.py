class Piattaforma:
     def __init__(self,nome, link_ricerca, link_login, logo, categoria):
          self.nome = nome
          self.link_ricerca = link_ricerca
          self.link_login = link_login
          self.logo = logo
          self.categoria = categoria
     def get_nome(self):
          return self.nome
     def get_link_ricerca(self):
          return self.link_ricerca
     def get_link_login(self):
          return self.link_login
     def get_logo(self):
          return self.logo
     def get_categoria(self):
          return self.categoria

CATALOGO_PIATTAFORME ={
     "netflix": Piattaforma(
          nome="Netflix",
          link_ricerca="https://www.netflix.com/search?q={}",
          link_login="https://www.netflix.com/login",
          logo="loghi/netflix.png",
          categoria="Streaming"
     ),
     "prime video": Piattaforma(     
          nome="Prime Video",
          link_ricerca="https://www.primevideo.com/search/ref=atv_nb_sr?phrase={}", # CORRETTO: Aggiunta virgola
          link_login="https://www.primevideo.com",
          logo="loghi/primevideo.png", 
          categoria="Streaming"
     ),
     "youtube": Piattaforma(
        nome="YouTube",
        link_ricerca="https://www.youtube.com/results?search_query={}",
        link_login="https://www.youtube.com",
        logo="loghi/youtube.png",
        categoria="Video"
    ),
    "disney +": Piattaforma(
        nome="Disney+",
        link_ricerca="https://www.disneyplus.com/search/{}",
        link_login="https://www.disneyplus.com/it-it",
        logo="loghi/disney.png",
        categoria="Streaming"
    ),
     "applemusic": Piattaforma(
        nome="Apple Music",
        link_ricerca="https://music.apple.com/search?term={}",
        link_login="https://www.apple.com/it/apple-music/",
        logo="loghi/appmusic.png",
        categoria="Musica"
    ),
     "spotify": Piattaforma(
        nome="Spotify",
        link_ricerca="https://open.spotify.com/search/{}",
        link_login="https://open.spotify.com/intl-it",
        logo="loghi/spotify.png",
        categoria="Musica"
    ),
     "amazon music": Piattaforma(
        nome="Amazon Music",
        link_ricerca="https://music.amazon.it/search/{}",
        link_login="https://music.amazon.it/",
        logo="loghi/amazonmusic.png",
        categoria="Musica"
    ),
     "mediaset infinity": Piattaforma(
        nome="Mediaset Infinity",
        link_ricerca="https://www.mediasetinfinity.mediaset.it/ricerca/{}",
        link_login="https://www.mediasetplay.mediaset.it/",
        logo="loghi/mediasetinfinity.png",
        categoria="Streaming"
    ),
     "raiplay": Piattaforma(
        nome="RaiPlay",
        link_ricerca="https://www.raiplay.it/cerca?q={}",
        link_login="https://www.raiplay.it/",
        logo="loghi/raiplay.png",
        categoria="Streaming"
    ),
    "kobo": Piattaforma(
        nome="Kobo",
        link_ricerca="https://www.kobo.com/it/it/search?query={}",
        link_login="https://www.kobo.com/it/it",
        logo="loghi/kobo.png",
        categoria="Libri"
    ),
    "kindle": Piattaforma(
        nome="Kindle",
        link_ricerca="https://www.amazon.it/s?k={}",
        link_login="https://leggi.amazon.it/landing",
        logo="loghi/kindle.png",
        categoria="Libri"
    ),
    "sky sport": Piattaforma(
        nome="Sky Sport",
        link_ricerca="https://sport.sky.it/ricerca?q={}",
        link_login="https://sport.sky.it/",
        logo="loghi/skysport.png",
        categoria="Sport"
    ),
     "now tv": Piattaforma(
        nome="Now TV",
        link_ricerca="https://www.nowtv.it/cerca?q={}",
        link_login="https://www.nowtv.it/sport",
        logo="loghi/nowtv.png",
        categoria="Sport"
    ),
}