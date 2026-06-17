import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

from stile import (
    STILE_FINESTRA_PRINCIPALE, STILE_BTN_PROFILO, STILE_BTN_CATEGORIA,
    STILE_BTN_EXTRA, STILE_CAMPO_RICERCA, STILE_SALUTO
)
from utils import BASE_DIR


class FinestraPrincipale(QWidget):
    def __init__(self, nome="Utente"):
        super().__init__()
        self.setWindowTitle("RelaxApp")
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, "logo5.1.png")))
        self.showMaximized()
        self.nome_utente = nome
        self.email_utente = nome 
        self.setStyleSheet(STILE_FINESTRA_PRINCIPALE)

        self.link_categorie = {
            "🎵 Musica": [
                ("Apple Music", "https://www.apple.com/it/apple-music/", "loghi/appmusic.png"),
                ("Spotify", "https://open.spotify.com/intl-it", "loghi/spotify.png"),
                ("Amazon Music", "https://music.amazon.it/", "loghi/amazonmusic.png"),
            ],
            "📡 Streaming": [
                ("Netflix", "https://www.netflix.com/browse", "loghi/netflix.png"),
                ("Disney+", "https://www.disneyplus.com/it-it", "loghi/disney.png"),
                ("Mediaset Infinity", "https://www.mediasetplay.mediaset.it/", "loghi/mediasetinfinity.png"),
                ("RaiPlay", "https://www.raiplay.it/", "loghi/raiplay.png"),
                ("Prime Video", "https://www.primevideo.com/", "loghi/primevideo.png"),
            ],
            "📚 Libri": [
                ("Kobo", "https://www.kobo.com/it/it", "loghi/kobo.png"),
                ("Kindle", "https://leggi.amazon.it/landing", "loghi/kindle.png"),
            ],
            "🎬 Video": [
                ("YouTube", "https://www.youtube.com", "loghi/youtube.png"),
            ],
            "⚽ Sport": [
                ("Sky Sport", "https://sport.sky.it/", "loghi/skysport.png"),
                ("Now TV", "https://www.nowtv.it/sport", "loghi/nowtv.png"),
            ],
        }

        self._costruisci_ui()

    def _costruisci_ui(self):
        layout_principale = QVBoxLayout()
        layout_principale.setContentsMargins(20, 20, 20, 20)
        layout_principale.setSpacing(15)

        barra_top = QHBoxLayout()
        barra_top.addStretch()

        btn_profilo = QPushButton("👤")
        btn_profilo.setFixedSize(50, 50)
        btn_profilo.setStyleSheet(STILE_BTN_PROFILO)
        btn_profilo.clicked.connect(self.apri_profilo)
        barra_top.addWidget(btn_profilo)
        layout_principale.addLayout(barra_top)

        logo = QLabel()
        percorso_logo = os.path.join(BASE_DIR, "logo5.1.png")
        pixmap = QPixmap(percorso_logo)
        logo.setPixmap(
            pixmap.scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        )
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(logo)

        saluto = QLabel(f"Buongiorno, {self.nome_utente}!")
        saluto.setStyleSheet(STILE_SALUTO)
        saluto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(saluto)

        barra_ricerca = QHBoxLayout()
        barra_ricerca.addStretch()
        self.campo_ricerca = QLineEdit()
        self.campo_ricerca.setPlaceholderText("🔍  Cerca...")
        self.campo_ricerca.setFixedWidth(400)
        self.campo_ricerca.setFixedHeight(40)
        self.campo_ricerca.setStyleSheet(STILE_CAMPO_RICERCA)
        self.campo_ricerca.returnPressed.connect(self.filtra_categorie)
        barra_ricerca.addWidget(self.campo_ricerca)
        barra_ricerca.addStretch()
        layout_principale.addLayout(barra_ricerca)

        layout_principale.addStretch()
        self.bottoni_categoria = []

        layout_categorie = QHBoxLayout()
        layout_categorie.setSpacing(12)

        categorie = [
            ("🎵", "Musica"),
            ("🎬", "Video"),
            ("📚", "Libri"),
            ("📡", "Streaming"),
            ("⚽", "Sport"),
        ]

        for emoji, nome in categorie:
            chiave = f"{emoji} {nome}"
            btn = QPushButton(f"{emoji}\n{nome}")
            btn.setFixedHeight(110)
            btn.setStyleSheet(STILE_BTN_CATEGORIA)
            btn.clicked.connect(lambda checked, k=chiave: self.apri_categoria(k))
            layout_categorie.addWidget(btn)
            self.bottoni_categoria.append((btn, nome.lower()))

        layout_principale.addLayout(layout_categorie)

        # Prima riga extra: Preferenze, Acquista, Scaduti
        layout_extra = QHBoxLayout()
        layout_extra.setSpacing(12)

        extra = ["⭐  Preferenze", "🛒  Acquista", "⏰  Scaduti"]
        for nome in extra:
            btn = QPushButton(nome)
            btn.setFixedHeight(70)
            btn.setStyleSheet(STILE_BTN_EXTRA)
            if "Acquista" in nome:
                btn.clicked.connect(self.apri_acquista)
            elif "Preferenze" in nome:
                btn.clicked.connect(self.apri_preferenze)
            elif "Scaduti" in nome:
                btn.clicked.connect(self.apri_scaduti)
            layout_extra.addWidget(btn)

        layout_principale.addLayout(layout_extra)

        # Seconda riga extra: I miei Abbonamenti, Presta Abbonamento
        layout_extra2 = QHBoxLayout()
        layout_extra2.setSpacing(12)

        btn_abbonamenti = QPushButton("📋  I miei Abbonamenti")
        btn_abbonamenti.setFixedHeight(70)
        btn_abbonamenti.setStyleSheet(STILE_BTN_EXTRA)
        btn_abbonamenti.clicked.connect(self.apri_abbonamenti)
        layout_extra2.addWidget(btn_abbonamenti)

        btn_presta = QPushButton("🤝  Presta Abbonamento")
        btn_presta.setFixedHeight(70)
        btn_presta.setStyleSheet(STILE_BTN_EXTRA)
        btn_presta.clicked.connect(self.apri_presta)
        layout_extra2.addWidget(btn_presta)

        layout_principale.addLayout(layout_extra2)

        layout_principale.addStretch()
        self.setLayout(layout_principale)

    def apri_profilo(self):
        from profilo import ProfiloDialog
        dialogo = ProfiloDialog(self, self)
        dialogo.exec()

    def apri_categoria(self, chiave):
        from dialoghi import SchedaCategoria
        pulsanti = self.link_categorie[chiave]
        scheda = SchedaCategoria(chiave, pulsanti, self)
        scheda.exec()

    def apri_preferenze(self):
        from dialoghi import FinestraPreferenze
        finestra = FinestraPreferenze(self)
        finestra.exec()

    def apri_acquista(self):
        from abbonamenti import FinestraAcquista
        finestra = FinestraAcquista(self, self.email_utente)
        finestra.exec()

    def apri_scaduti(self):
        from abbonamenti import FinestraScaduti
        finestra = FinestraScaduti(self, self.email_utente)
        finestra.exec()

    def apri_abbonamenti(self):
        from abbonamenti import FinestraAbbonamenti
        finestra = FinestraAbbonamenti(self, self.email_utente)
        finestra.exec()

    def apri_presta(self):
        from abbonamenti import FinestraPresta
        finestra = FinestraPresta(self)
        finestra.exec()

    def filtra_categorie(self):
        from dialoghi import FinestraRicerca
        testo = self.campo_ricerca.text().strip()
        finestra = FinestraRicerca (testo, self)
        finestra.exec()