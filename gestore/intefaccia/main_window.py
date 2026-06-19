import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QFrame, QScrollArea, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from intefaccia.profilo import ProfiloDialog
from intefaccia.dialoghi import FinestraRicerca, SchedaCategoria
# Calcolo del percorso radice del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazione degli stili, utility e dialoghi
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

    def __init__(self, nome="Utente", email="utente@email.com", gestore_preferenze=None):
        super().__init__()
        self.nome_utente = nome
        self.email_utente = email
        self.gestore_preferenze = gestore_preferenze

        # Configurazione finestra
        self.setWindowTitle("RelaxApp")
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, "logo5.1.png")))
        self.showMaximized()
        self.setStyleSheet(STILE_FINESTRA_PRINCIPALE)

        # Mappatura delle categorie con etichetta -> nome categoria reale (Requisito 1.4)
        self.mappa_categorie = {
            "🎵 Musica": "Musica",
            "📡 Streaming": "Streaming",
            "📚 Libri": "Libri",
            "🎬 Video": "Video",
            "⚽ Sport": "Sport"
        }

        # Costruisce, per ogni categoria, un dizionario {nome: oggetto Piattaforma}
        self.link_categorie = {
            etichetta: {
                p.nome: p for p in CATALOGO_PIATTAFORME.values()
                if p.categoria == nome_reale
            }
            for etichetta, nome_reale in self.mappa_categorie.items()
        }

        self._build_ui()
        self.carica_suggerimenti() # Implementazione CDU17
        self.controlla_notifiche() # Implementazione CDU21/CDU22

    def _build_ui(self):
        """Costruisce il layout della Home Page."""
        self.layout_principale = QVBoxLayout(self)

        # 1. Barra Superiore: Saluto, Ricerca e Profilo
        top_bar = QHBoxLayout()
        label_saluto = QLabel(f"Ciao, {self.nome_utente}!")
        label_saluto.setStyleSheet(STILE_SALUTO)
        
        self.campo_ricerca = QLineEdit()
        self.campo_ricerca.setPlaceholderText("Cerca un film, una serie o un brano...")
        self.campo_ricerca.setStyleSheet(STILE_CAMPO_RICERCA)
        self.campo_ricerca.returnPressed.connect(self.esegui_ricerca)
        btn_profilo = QPushButton("👤")
        btn_profilo.setFixedSize(50, 50)
        btn_profilo.setStyleSheet(STILE_BTN_PROFILO)
        btn_profilo.clicked.connect(self.apri_profilo)

        top_bar.addWidget(label_saluto)
        top_bar.addStretch()
        top_bar.addWidget(self.campo_ricerca)
        top_bar.addWidget(btn_profilo)
        self.layout_principale.addLayout(top_bar)

        # 2. Sezione Categorie (CDU4)
        self.layout_principale.addWidget(QLabel("Esplora per Categoria"))
        layout_cat = QHBoxLayout()
        for cat_nome in self.link_categorie.keys():
            btn_cat = QPushButton(cat_nome)
            btn_cat.setStyleSheet(STILE_BTN_CATEGORIA)
            btn_cat.clicked.connect(lambda ch, c=cat_nome: self.apri_categoria(c))
            layout_cat.addWidget(btn_cat)
        self.layout_principale.addLayout(layout_cat)

        # 3. Area Suggerimenti (CDU17)
        self.layout_principale.addWidget(QLabel("Contenuti Consigliati per Te"))
        self.scroll_suggerimenti = QScrollArea()
        self.container_suggerimenti = QWidget()
        self.layout_suggerimenti = QHBoxLayout(self.container_suggerimenti)
        self.scroll_suggerimenti.setWidget(self.container_suggerimenti)
        self.scroll_suggerimenti.setWidgetResizable(True)
        self.layout_principale.addWidget(self.scroll_suggerimenti)

        self.layout_principale.addStretch()

    def apri_profilo(self):
        """CDU7: Apre il pannello di gestione del profilo."""
        dialogo = ProfiloDialog(self)
        dialogo.exec()

    def esegui_ricerca(self):
        """CDU4: Avvia la ricerca globale interrogando le piattaforme."""
        testo = self.campo_ricerca.text()
        if testo:
            # Aggrega i risultati e li mostra nella finestra dedicata
            dialogo = FinestraRicerca(testo, self)
            dialogo.exec()

    def apri_categoria(self, nome_categoria):
        """CDU18: Mostra le piattaforme per avviare la riproduzione."""
        servizi = self.link_categorie.get(nome_categoria, {})
        dialogo = SchedaCategoria(nome_categoria, servizi, self.email_utente, self)
        dialogo.exec()

    def carica_suggerimenti(self):
        """CDU17: Incrocia preferenze e disponibilità per mostrare i consigliati."""
        # Se le preferenze sono assenti, il sistema notifica l'assenza
        if not self.gestore_preferenze or not self.gestore_preferenze.ottieni_preferenze(self.email_utente):
            self.layout_suggerimenti.addWidget(QLabel("Imposta le tue preferenze nel profilo per ricevere consigli!"))
            return

        # Simula il caricamento dei suggerimenti basati sull'algoritmo di matching
        suggerimenti = ["Film d'Azione (Netflix)", "Pop Hits (Spotify)", "Documentari (Disney+)"]
        for s in suggerimenti:
            btn_sug = QPushButton(s)
            btn_sug.setStyleSheet(STILE_BTN_EXTRA)
            self.layout_suggerimenti.addWidget(btn_sug)

    def controlla_notifiche(self):
        """CDU21/CDU22: Invia avvisi per scadenze o aggiornamento preferenze."""
        # Esempio: Notifica periodica ogni settimana per le preferenze
        messaggio = "È trascorsa una settimana! Desideri aggiornare le tue preferenze?"
        QMessageBox.information(self, "Avviso di Sistema", messaggio)