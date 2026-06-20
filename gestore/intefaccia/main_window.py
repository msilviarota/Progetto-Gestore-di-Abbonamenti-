import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFrame, QScrollArea, QMessageBox,QDialog
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from intefaccia.profilo import ProfiloDialog
from intefaccia.dialoghi import FinestraRicerca, SchedaCategoria
from intefaccia.dialoghi import FinestraAcquisto

cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from intefaccia.stile import (
    STILE_FINESTRA_PRINCIPALE, STILE_BTN_PROFILO, STILE_BTN_CATEGORIA,
    STILE_CAMPO_RICERCA, STILE_SALUTO, STILE_BTN_EXTRA,
    STILE_TITOLO_SEZIONE, STILE_SCROLL_TRASPARENTE, STILE_TESTO_VUOTO,
    STILE_DIALOGO_VERDE, STILE_TITOLO_DIALOGO, STILE_SEPARATORE,
    STILE_FINESTRA_REGISTRAZIONE
)
from intefaccia.utils import BASE_DIR
from models.piattaforma import CATALOGO_PIATTAFORME

class FinestraPrincipale(QWidget):
    """
    Rappresenta l'interfaccia principale del gestore (Home Page).
    Gestisce navigazione, ricerca, suggerimenti e notifiche (CDU4, CDU7, CDU17, CDU18, CDU21, CDU22).
    """

    def __init__(self, gestore_profilo, gestore_abbonamenti, nome="Utente", email="utente@email.com",
                 gestore_preferenze=None, parent=None):
        super().__init__()
        self.nome_utente = nome
        self.email_utente = email
        self.gestore_preferenze = gestore_preferenze
        self.gestore_profilo = gestore_profilo
        self.gestore_abbonamenti = gestore_abbonamenti

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
        self.categoria_to_etichetta = {v: k for k, v in self.mappa_categorie.items()}
        self.link_categorie = {
            etichetta: {
                p.nome: p for p in CATALOGO_PIATTAFORME.values()
                if p.categoria == nome_reale
            }
            for etichetta, nome_reale in self.mappa_categorie.items()
        }

        self._build_ui()
        self.popola_consigliati()

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

        # Pulsanti categoria, emoji sopra + testo sotto, con stellina se consigliata
        layout_categorie = QHBoxLayout()
        layout_categorie.setSpacing(12)
        self.bottoni_categoria = []
        for etichetta in self.link_categorie.keys():
            emoji, nome = etichetta.split(" ", 1)
            btn = QPushButton()
            btn.setFixedHeight(110)
            btn.setStyleSheet(STILE_BTN_CATEGORIA)
            btn.clicked.connect(lambda ch, c=etichetta: self.apri_categoria(c))
            layout_categorie.addWidget(btn)
            self.bottoni_categoria.append((btn, emoji, nome))
        layout_principale.addLayout(layout_categorie)
        self.aggiorna_stelle_categorie()

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

        # Unica sezione "Consigliati per te" — una fila orizzontale scorrevole
        titolo_suggerimenti = QLabel("✨ Consigliati per te")
        titolo_suggerimenti.setStyleSheet(STILE_TITOLO_SEZIONE)
        layout_principale.addWidget(titolo_suggerimenti)

        self.scroll_suggerimenti = QScrollArea()
        self.scroll_suggerimenti.setWidgetResizable(True)
        self.scroll_suggerimenti.setFixedHeight(90)
        self.scroll_suggerimenti.setStyleSheet(STILE_SCROLL_TRASPARENTE)
        self.container_suggerimenti = QWidget()
        self.layout_suggerimenti = QHBoxLayout(self.container_suggerimenti)
        self.layout_suggerimenti.setSpacing(10)
        self.scroll_suggerimenti.setWidget(self.container_suggerimenti)
        layout_principale.addWidget(self.scroll_suggerimenti)

        layout_principale.addStretch()

    def popola_consigliati(self):
        """CDU17: Mostra le piattaforme consigliate in base alle preferenze, in un'unica fila."""
        while self.layout_suggerimenti.count():
            item = self.layout_suggerimenti.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not self.gestore_preferenze:
            label_vuoto = QLabel("Imposta le tue preferenze nel profilo per ricevere consigli!")
            label_vuoto.setStyleSheet(STILE_TESTO_VUOTO)
            self.layout_suggerimenti.addWidget(label_vuoto)
            return

        preferenze = self.gestore_preferenze.ottieni_preferenze(self.email_utente)
        if not preferenze:
            label_vuoto = QLabel("Imposta le tue preferenze per ricevere consigli personalizzati!")
            label_vuoto.setStyleSheet(STILE_TESTO_VUOTO)
            self.layout_suggerimenti.addWidget(label_vuoto)
            return

        categorie_pulite = [p.split(" ", 1)[1] if " " in p else p for p in preferenze]
        trovate = False
        for piattaforma in CATALOGO_PIATTAFORME.values():
            if piattaforma.categoria.lower() in [c.lower() for c in categorie_pulite]:
                trovate = True
                chip = QPushButton(f"{piattaforma.nome}\n{piattaforma.categoria}")
                chip.setFixedSize(140, 60)
                chip.setStyleSheet(STILE_BTN_EXTRA)
                etichetta_cat = self.categoria_to_etichetta.get(piattaforma.categoria)
                if etichetta_cat:
                    chip.clicked.connect(lambda ch, c=etichetta_cat: self.apri_categoria(c))
                self.layout_suggerimenti.addWidget(chip)

        if not trovate:
            label_vuoto = QLabel("Nessun consiglio disponibile per le categorie selezionate.")
            label_vuoto.setStyleSheet(STILE_TESTO_VUOTO)
            self.layout_suggerimenti.addWidget(label_vuoto)

    def apri_profilo(self):
        """CDU7: Apre il pannello di gestione del profilo."""
        dialogo = ProfiloDialog(self)
        dialogo.exec()

    def esegui_ricerca(self):
        testo = self.campo_ricerca.text().strip()
        if not testo:
            QMessageBox.warning(self, "Errore", "Inserisci un testo da cercare.")
            return
        finestra = FinestraRicerca(testo, self)
        finestra.exec()

    def apri_categoria(self, nome_categoria):
        """CDU18: Mostra le piattaforme per avviare la riproduzione."""
        servizi = self.link_categorie.get(nome_categoria, {})
        dialogo = SchedaCategoria(nome_categoria, servizi, self.email_utente, self.gestore_abbonamenti, self)
        dialogo.exec()

    def apri_preferenze(self):
        """CDU5: Apre la finestra per impostare le categorie preferite."""
        from intefaccia.preferenze import FinestraPreferenze
        finestra = FinestraPreferenze(self.gestore_preferenze, self.email_utente, self)
        finestra.exec()
        self.popola_consigliati()
        self.aggiorna_stelle_categorie()  # aggiorna i consigli dopo eventuali modifiche

    def apri_acquista(self):
        """CDU1: L'acquisto si avvia dalla scheda di una categoria/piattaforma."""
        QMessageBox.information(
            self, "Seleziona una piattaforma",
            "Per acquistare un abbonamento, apri una categoria (es. 🎵 Musica, 📡 Streaming...) "
            "e clicca su 'Acquista' accanto alla piattaforma che vuoi."
        )

    def apri_scaduti(self):
        """CDU14/CDU19: Mostra gli abbonamenti scaduti e permette di rimuoverli."""
        from intefaccia.dialoghi import FinestraScaduti
        dialogo = FinestraScaduti(self.gestore_abbonamenti, self)
        dialogo.exec()

    def categorie_consigliate(self):
        """Restituisce l'elenco delle categorie con almeno una piattaforma consigliata."""
        if not self.gestore_preferenze:
            return []
        preferenze = self.gestore_preferenze.ottieni_preferenze(self.email_utente)
        if not preferenze:
            return []
        categorie_pulite = [p.split(" ", 1)[1] if " " in p else p for p in preferenze]
        categorie_trovate = set()
        for piattaforma in CATALOGO_PIATTAFORME.values():
            if piattaforma.categoria.lower() in [c.lower() for c in categorie_pulite]:
                categorie_trovate.add(piattaforma.categoria)
        return list(categorie_trovate)
    def aggiorna_stelle_categorie(self):
        """Aggiorna la stellina sui pulsanti categoria in base alle preferenze correnti."""
        categorie_star = self.categorie_consigliate()
        for btn, emoji, nome in self.bottoni_categoria:
            nome_visualizzato = f"⭐ {nome}" if nome in categorie_star else nome
            btn.setText(f"{emoji}\n{nome_visualizzato}")


class FinestraCambiaCarta(QDialog):
    """Modulo completo per cambiare il numero della carta (simile al cambio password).

    NOTA: questa classe sembra un doppione di FinestraModificaPagamento in dialoghi.py.
    Valuta se eliminarla per evitare di mantenere due copie della stessa logica.
    """
    def __init__(self, email_utente, gestore_profilo, parent=None):
        super().__init__(parent)

        self.email_utente = email_utente
        self.gestore_profilo = gestore_profilo

        self.setWindowTitle("Modifica Carta")
        self.setFixedSize(420, 320)
        self.setStyleSheet(STILE_DIALOGO_VERDE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("💳 Modifica Carta")
        titolo.setStyleSheet(STILE_TITOLO_DIALOGO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(STILE_SEPARATORE)
        layout.addWidget(sep)

        # Vecchio numero carta
        layout.addWidget(QLabel("Vecchio numero carta:"))
        self.vecchia_input = QLineEdit()
        self.vecchia_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.vecchia_input)

        # Nuovo numero carta
        layout.addWidget(QLabel("Nuovo numero carta:"))
        self.nuova_input = QLineEdit()
        self.nuova_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.nuova_input)

        # Conferma nuovo numero carta
        layout.addWidget(QLabel("Conferma nuovo numero:"))
        self.conferma_input = QLineEdit()
        self.conferma_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.conferma_input)

        btn_salva = QPushButton("Salva")
        btn_salva.clicked.connect(self.salva)
        layout.addWidget(btn_salva)

    def salva(self):
        vecchia = self.vecchia_input.text()
        nuova = self.nuova_input.text()
        conferma = self.conferma_input.text()

        if not vecchia or not nuova or not conferma:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi.")
            return

        if nuova != conferma:
            QMessageBox.warning(self, "Errore", "I numeri non coincidono.")
            return

        if len(nuova) < 12:
            QMessageBox.warning(self, "Errore", "Il numero carta deve avere almeno 12 cifre.")
            return

        # Qui chiami il tuo gestore (devi aggiungere il metodo)
        successo = self.gestore_profilo.cambia_carta_utente(
            self.email_utente,
            vecchia,
            nuova
        )

        if successo:
            QMessageBox.information(self, "Successo", "Carta aggiornata correttamente.")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "Il vecchio numero carta non è corretto.")


class FinestraRegistrazione(QDialog):
    """NOTA: questa classe sembra un doppione (versione semplificata) di FinestraRegistrazione
    in dialoghi.py, che ha più campi (cognome, età, conferma password). Valuta se serve davvero
    o se è codice rimasto da una versione precedente."""
    def __init__(self, gestore_login, parent=None):
        super().__init__(parent)

        self.gestore_login = gestore_login

        self.setWindowTitle("Crea un nuovo account")
        self.setFixedSize(420, 380)
        self.setStyleSheet(STILE_DIALOGO_VERDE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("📝 Registrazione")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet(STILE_TITOLO_DIALOGO)
        layout.addWidget(titolo)

        # Campi
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome")
        layout.addWidget(self.input_nome)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")
        layout.addWidget(self.input_email)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_password)

        btn_registra = QPushButton("Crea account")
        btn_registra.clicked.connect(self.registra)
        layout.addWidget(btn_registra)

    def registra(self):
        nome = self.input_nome.text()
        email = self.input_email.text()
        password = self.input_password.text()

        if not nome or not email or not password:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi.")
            return

        successo = self.gestore_login.registra_utente(nome, email, password)

        if successo:
            QMessageBox.information(self, "Successo", "Account creato!")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "Email già registrata.")
            
class FinestraRecupero(QDialog):
    """NOTA: questa classe sembra un doppione di FinestraRecuperoPassword in dialoghi.py."""
    def __init__(self, gestore_login, parent=None):
        super().__init__(parent)

        self.gestore_login = gestore_login

        self.setWindowTitle("Recupero Password")
        self.setFixedSize(420, 250)
        self.setStyleSheet(STILE_DIALOGO_VERDE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("🔑 Recupero Password")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet(STILE_TITOLO_DIALOGO)
        layout.addWidget(titolo)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Inserisci la tua email")
        layout.addWidget(self.input_email)

        btn_invia = QPushButton("Invia nuova password")
        btn_invia.clicked.connect(self.recupera)
        layout.addWidget(btn_invia)

    def recupera(self):
        email = self.input_email.text()

        if not email:
            QMessageBox.warning(self, "Errore", "Inserisci un'email.")
            return

        successo = self.gestore_login.recupera_password(email)

        if successo:
            QMessageBox.information(self, "Successo", "Nuova password inviata!")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "Email non trovata.")