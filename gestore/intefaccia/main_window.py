import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFrame, QScrollArea, QMessageBox
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from intefaccia.profilo import ProfiloDialog
from intefaccia.dialoghi import FinestraRicerca, SchedaCategoria

cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from intefaccia.stile import (
    STILE_FINESTRA_PRINCIPALE, STILE_BTN_PROFILO, STILE_BTN_CATEGORIA,
    STILE_CAMPO_RICERCA, STILE_SALUTO, STILE_BTN_EXTRA
)
from intefaccia.utils import BASE_DIR
from models.piattaforma import CATALOGO_PIATTAFORME


class FinestraPrincipale(QWidget):
    """
    Rappresenta l'interfaccia principale del gestore (Home Page).
    Gestisce navigazione, ricerca, suggerimenti e notifiche (CDU4, CDU7, CDU17, CDU18, CDU21, CDU22).
    """

    def __init__(self, gestore_profilo,nome="Utente", email="utente@email.com", gestore_preferenze=None, parent=None):
        super().__init__()
        self.nome_utente = nome
        self.email_utente = email
        self.gestore_preferenze = gestore_preferenze
        self.gestore_profilo = gestore_profilo

        self.setWindowTitle("RelaxApp")
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, "logo5.1.png")))
        self.showMaximized()
        self.setStyleSheet(STILE_FINESTRA_PRINCIPALE)

        # Mappatura categorie -> piattaforme reali del catalogo (Requisito 1.4)
        self.mappa_categorie = {
            "🎵 Musica": "Musica",
            "📡 Streaming": "Streaming",
            "📚 Libri": "Libri",
            "🎬 Video": "Video",
            "⚽ Sport": "Sport"
        }
        self.link_categorie = {
            etichetta: {
                p.nome: p for p in CATALOGO_PIATTAFORME.values()
                if p.categoria == nome_reale
            }
            for etichetta, nome_reale in self.mappa_categorie.items()
        }

        self._build_ui()
        self.carica_suggerimenti()
        
    def _build_ui(self):
        layout_principale = QVBoxLayout(self)
        layout_principale.setContentsMargins(20, 20, 20, 20)
        layout_principale.setSpacing(15)

        # Barra superiore: solo il profilo, in alto a destra
        barra_top = QHBoxLayout()
        barra_top.addStretch()
        btn_profilo = QPushButton("👤")
        btn_profilo.setFixedSize(50, 50)
        btn_profilo.setStyleSheet(STILE_BTN_PROFILO)
        btn_profilo.clicked.connect(self.apri_profilo)
        barra_top.addWidget(btn_profilo)
        layout_principale.addLayout(barra_top)

        # Logo centrato
        logo = QLabel()
        percorso_logo = os.path.join(BASE_DIR, "logo5.1.png")
        if os.path.exists(percorso_logo):
            pixmap = QPixmap(percorso_logo)
            logo.setPixmap(
                pixmap.scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
            )
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(logo)

        # Saluto centrato
        saluto = QLabel(f"Ciao, {self.nome_utente}!")
        saluto.setStyleSheet(STILE_SALUTO)
        saluto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(saluto)

        # Barra di ricerca centrata
        barra_ricerca = QHBoxLayout()
        barra_ricerca.addStretch()
        self.campo_ricerca = QLineEdit()
        self.campo_ricerca.setPlaceholderText("🔍  Cerca un film, una serie o un brano...")
        self.campo_ricerca.setFixedWidth(400)
        self.campo_ricerca.setFixedHeight(40)
        self.campo_ricerca.setStyleSheet(STILE_CAMPO_RICERCA)
        self.campo_ricerca.returnPressed.connect(self.esegui_ricerca)
        barra_ricerca.addWidget(self.campo_ricerca)
        barra_ricerca.addStretch()
        layout_principale.addLayout(barra_ricerca)

        layout_principale.addStretch()

        # Pulsanti categoria, emoji sopra + testo sotto
        layout_categorie = QHBoxLayout()
        layout_categorie.setSpacing(12)
        for etichetta in self.link_categorie.keys():
            emoji, nome = etichetta.split(" ", 1)
            btn = QPushButton(f"{emoji}\n{nome}")
            btn.setFixedHeight(110)
            btn.setStyleSheet(STILE_BTN_CATEGORIA)
            btn.clicked.connect(lambda ch, c=etichetta: self.apri_categoria(c))
            layout_categorie.addWidget(btn)
        layout_principale.addLayout(layout_categorie)

        # Riga extra: Preferenze, Acquista, Scaduti
        layout_extra = QHBoxLayout()
        layout_extra.setSpacing(12)
        extra = [
            ("⭐  Preferenze", self.apri_preferenze),
            ("🛒  Acquista", self.apri_acquista),
            ("⏰  Scaduti", self.apri_scaduti),
        ]
        for nome, callback in extra:
            btn = QPushButton(nome)
            btn.setFixedHeight(70)
            btn.setStyleSheet(STILE_BTN_EXTRA)
            btn.clicked.connect(callback)
            layout_extra.addWidget(btn)
        layout_principale.addLayout(layout_extra)

        # Area Suggerimenti (CDU17)
        # Area Suggerimenti (CDU17)
        titolo_suggerimenti = QLabel("Contenuti Consigliati per Te")
        titolo_suggerimenti.setStyleSheet("color: #222222; font-size: 16px; font-weight: bold;")
        layout_principale.addWidget(titolo_suggerimenti)
        self.scroll_suggerimenti = QScrollArea()
        self.container_suggerimenti = QWidget()
        self.layout_suggerimenti = QHBoxLayout(self.container_suggerimenti)
        self.scroll_suggerimenti.setWidget(self.container_suggerimenti)
        self.scroll_suggerimenti.setWidgetResizable(True)
        layout_principale.addWidget(self.scroll_suggerimenti)

        layout_principale.addStretch()

    def apri_profilo(self):
        """CDU7: Apre il pannello di gestione del profilo."""
        dialogo = ProfiloDialog(self)
        dialogo.exec()

    def esegui_ricerca(self):
        """CDU4: Avvia la ricerca globale interrogando le piattaforme."""
        testo = self.campo_ricerca.text()
        if testo:
            dialogo = FinestraRicerca(testo, self)
            dialogo.exec()

    def apri_categoria(self, nome_categoria):
        """CDU18: Mostra le piattaforme per avviare la riproduzione."""
        servizi = self.link_categorie.get(nome_categoria, {})
        dialogo = SchedaCategoria(nome_categoria, servizi, self.email_utente, self)
        dialogo.exec()

    def apri_preferenze(self):
        """CDU5: Apre la finestra per impostare le categorie preferite."""
        from intefaccia.preferenze import FinestraPreferenze
        finestra = FinestraPreferenze(self.gestore_preferenze, self.email_utente, self)
        finestra.exec()

    def apri_acquista(self):
        """CDU1: Acquisto abbonamento (collegamento al backend in arrivo)."""
        QMessageBox.information(
            self, "In arrivo",
            "La schermata di acquisto sarà collegata al backend abbonamenti a breve."
        )

    def apri_scaduti(self):
        """CDU14/CDU19: Gestione abbonamenti scaduti (collegamento al backend in arrivo)."""
        QMessageBox.information(
            self, "In arrivo",
            "La schermata degli abbonamenti scaduti sarà collegata al backend a breve."
        )

    def carica_suggerimenti(self):
        """CDU17: Incrocia preferenze e disponibilità per mostrare i consigliati."""
        if not self.gestore_preferenze:
            label_vuoto = QLabel("Imposta le tue preferenze nel profilo per ricevere consigli!")
            label_vuoto.setStyleSheet("color: #555555; font-size: 13px;")
            self.layout_suggerimenti.addWidget(label_vuoto)
            return

        suggerimenti = self.gestore_preferenze.genera_suggerimenti(self.email_utente)
        if not suggerimenti:
            label_vuoto = QLabel("Imposta le tue preferenze per ricevere consigli personalizzati!")
            label_vuoto.setStyleSheet("color: #555555; font-size: 13px;")
            self.layout_suggerimenti.addWidget(label_vuoto)
            return

    def controlla_notifiche(self):
        """CDU21/CDU22: Invia avvisi per scadenze o aggiornamento preferenze."""
        messaggio = "È trascorsa una settimana! Desideri aggiornare le tue preferenze?"
        QMessageBox.information(self, "Avviso di Sistema", messaggio)