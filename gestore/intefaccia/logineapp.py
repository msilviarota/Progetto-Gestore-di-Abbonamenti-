import sys
import os
import webbrowser
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QDialog, QFormLayout, QLineEdit,
    QFrame, QMessageBox, QComboBox, QCheckBox
)
from PyQt6.QtGui import QFont, QDesktopServices, QPixmap, QIcon
from PyQt6.QtCore import Qt, QUrl, QSize

from stile import (
    STILE_DIALOGO_PROFILO, STILE_SCHEDA_CATEGORIA, STILE_FINESTRA_PRINCIPALE,
    STILE_BTN_PROFILO, STILE_BTN_CATEGORIA, STILE_BTN_EXTRA, STILE_BTN_SERVIZIO,
    STILE_BTN_ESCI, STILE_BTN_CHIUDI, STILE_CAMPO_RICERCA,
    STILE_LABEL_PROFILO, STILE_TITOLO_PROFILO, STILE_SALUTO, STILE_BTN_LINK,
    STILE_COMBO
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def scarica_logo(percorso):
    try:
        percorso_assoluto = os.path.join(BASE_DIR, percorso)
        pixmap = QPixmap(percorso_assoluto)
        if not pixmap.isNull():
            return QIcon(
                pixmap.scaled(
                    120, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            print(f"Immagine nulla: {percorso_assoluto}")
    except Exception as e:
        print(f"Errore: {e}")
    return None


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registrazione")
        self.setFixedSize(450, 380)
        self.setStyleSheet("QWidget { background-color: #e8f5e9; }")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(14)

        titolo = QLabel("Crea un account")
        titolo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        riga_nome = QHBoxLayout()
        label_nome = QLabel("Nome:")
        label_nome.setFixedWidth(100)
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Es. Silvia Rota")
        self.nome_input.setFixedHeight(36)
        riga_nome.addWidget(label_nome)
        riga_nome.addWidget(self.nome_input)
        riga_cognome = QHBoxLayout()
        label_cognome = QLabel("Cognome:")
        label_cognome.setFixedWidth(100)
        self.cognome_input = QLineEdit()
        self.cognome_input.setPlaceholderText("Es. Rota")
        self.cognome_input.setFixedHeight(36)
        riga_cognome.addWidget(label_cognome)
        riga_cognome.addWidget(self.cognome_input)
        riga_eta = QHBoxLayout()
        label_eta = QLabel("Età:")
        label_eta.setFixedWidth(100)
        self.eta_input = QLineEdit()
        self.eta_input.setPlaceholderText("Es. 25")
        self.eta_input.setFixedHeight(36)
        riga_eta.addWidget(label_eta)
        riga_eta.addWidget(self.eta_input)
        riga_email = QHBoxLayout()
        label_email = QLabel("Email:")
        label_email.setFixedWidth(100)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Es. silvia@email.com")
        self.email_input.setFixedHeight(36)
        riga_email.addWidget(label_email)
        riga_email.addWidget(self.email_input)

        riga_password = QHBoxLayout()
        label_password = QLabel("Password:")
        label_password.setFixedWidth(100)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Inserisci password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(36)
        riga_password.addWidget(label_password)
        riga_password.addWidget(self.password_input)

        riga_conferma = QHBoxLayout()
        label_conferma = QLabel("Conferma:")
        label_conferma.setFixedWidth(100)
        self.conferma_input = QLineEdit()
        self.conferma_input.setPlaceholderText("Ripeti password")
        self.conferma_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.conferma_input.setFixedHeight(36)
        riga_conferma.addWidget(label_conferma)
        riga_conferma.addWidget(self.conferma_input)

        btn_registrati = QPushButton("Registrati")
        btn_registrati.setFixedHeight(38)
        btn_registrati.clicked.connect(self.registrati)

        btn_torna = QPushButton("Hai già un account? Accedi")
        btn_torna.setFlat(True)
        btn_torna.setStyleSheet(STILE_BTN_LINK)
        btn_torna.clicked.connect(self.torna_login)

        layout.addWidget(titolo)
        layout.addSpacing(10)
        layout.addLayout(riga_nome)
        layout.addLayout(riga_cognome)
        layout.addLayout(riga_eta)
        layout.addLayout(riga_email)
        layout.addLayout(riga_password)
        layout.addLayout(riga_conferma)
        layout.addWidget(btn_registrati)
        layout.addWidget(btn_torna, alignment=Qt.AlignmentFlag.AlignCenter)

    def registrati(self):
        nome = self.nome_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        conferma = self.conferma_input.text()

        if not nome or not email or not password or not conferma:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi!")
            return
        if password != conferma:
            QMessageBox.warning(self, "Errore", "Le password non coincidono!")
            return

        QMessageBox.information(self, "Successo", f"Account creato per {email}!")
        self.torna_login()

    def torna_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
class FinestraCambiaPassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cambia Password")
        self.setFixedSize(400, 300)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("🔑 Cambia Password")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        riga_vecchia = QHBoxLayout()
        label_vecchia = QLabel("Vecchia:")
        label_vecchia.setFixedWidth(110)
        self.vecchia_input = QLineEdit()
        self.vecchia_input.setPlaceholderText("Vecchia password")
        self.vecchia_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.vecchia_input.setFixedHeight(36)
        riga_vecchia.addWidget(label_vecchia)
        riga_vecchia.addWidget(self.vecchia_input)
        layout.addLayout(riga_vecchia)

        riga_nuova = QHBoxLayout()
        label_nuova = QLabel("Nuova:")
        label_nuova.setFixedWidth(110)
        self.nuova_input = QLineEdit()
        self.nuova_input.setPlaceholderText("Nuova password")
        self.nuova_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.nuova_input.setFixedHeight(36)
        riga_nuova.addWidget(label_nuova)
        riga_nuova.addWidget(self.nuova_input)
        layout.addLayout(riga_nuova)

        riga_conferma = QHBoxLayout()
        label_conferma = QLabel("Conferma:")
        label_conferma.setFixedWidth(110)
        self.conferma_input = QLineEdit()
        self.conferma_input.setPlaceholderText("Ripeti nuova password")
        self.conferma_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.conferma_input.setFixedHeight(36)
        riga_conferma.addWidget(label_conferma)
        riga_conferma.addWidget(self.conferma_input)
        layout.addLayout(riga_conferma)

        btn_salva = QPushButton("Salva")
        btn_salva.setFixedHeight(38)
        btn_salva.setStyleSheet(STILE_BTN_CHIUDI)
        btn_salva.clicked.connect(self.salva)
        layout.addWidget(btn_salva)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setFixedHeight(38)
        btn_annulla.setStyleSheet(STILE_BTN_ESCI)
        btn_annulla.clicked.connect(self.close)
        layout.addWidget(btn_annulla)

    def salva(self):
        vecchia = self.vecchia_input.text()
        nuova = self.nuova_input.text()
        conferma = self.conferma_input.text()

        if not vecchia or not nuova or not conferma:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi!")
            return
        if nuova != conferma:
            QMessageBox.warning(self, "Errore", "Le password non coincidono!")
            return

        QMessageBox.information(self, "Successo", "Password cambiata con successo!")
        self.close()


class FinestraAbbonamenti(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("I miei Abbonamenti")
        self.setFixedSize(450, 400)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("📋 I miei Abbonamenti")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        # abbonamenti di esempio
        abbonamenti = [
            ("Netflix", "Mensile", "Scade: 01/07/2026"),
            ("Spotify", "Annuale", "Scade: 15/12/2026"),
            ("Disney+", "Mensile", "Scade: 10/07/2026"),
        ]

        for nome, piano, scadenza in abbonamenti:
            riga = QHBoxLayout()
            lbl = QLabel(f"{nome}  —  {piano}  —  {scadenza}")
            lbl.setStyleSheet("font-size: 13px; color: #222222;")
            riga.addWidget(lbl)

            btn_disdici = QPushButton("Disdici")
            btn_disdici.setFixedHeight(30)
            btn_disdici.setStyleSheet(STILE_BTN_ESCI)
            btn_disdici.clicked.connect(lambda checked, n=nome: self.disdici(n))
            riga.addWidget(btn_disdici)
            layout.addLayout(riga)

        layout.addStretch()

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setFixedHeight(38)
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
        layout.addWidget(btn_chiudi, alignment=Qt.AlignmentFlag.AlignCenter)

    def disdici(self, nome):
        risposta = QMessageBox.question(
            self, "Conferma",
            f"Vuoi disdire {nome}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if risposta == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Disdetto", f"{nome} disdetto con successo!")


class FinestraPresta(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Presta Abbonamento")
        self.setFixedSize(400, 300)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("🤝 Presta Abbonamento")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        layout.addWidget(QLabel("Seleziona abbonamento da prestare:"))
        self.combo = QComboBox()
        self.combo.addItems(["Netflix", "Spotify", "Disney+"])
        self.combo.setFixedHeight(36)
        self.combo.setStyleSheet(STILE_COMBO)
        layout.addWidget(self.combo)

        riga_email = QHBoxLayout()
        label_email = QLabel("Email amico:")
        label_email.setFixedWidth(110)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Es. amico@email.com")
        self.email_input.setFixedHeight(36)
        riga_email.addWidget(label_email)
        riga_email.addWidget(self.email_input)
        layout.addLayout(riga_email)

        btn_presta = QPushButton("Presta")
        btn_presta.setFixedHeight(38)
        btn_presta.setStyleSheet(STILE_BTN_CHIUDI)
        btn_presta.clicked.connect(self.presta)
        layout.addWidget(btn_presta)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setFixedHeight(38)
        btn_annulla.setStyleSheet(STILE_BTN_ESCI)
        btn_annulla.clicked.connect(self.close)
        layout.addWidget(btn_annulla)

    def presta(self):
        abbonamento = self.combo.currentText()
        email = self.email_input.text()

        if not email:
            QMessageBox.warning(self, "Errore", "Inserisci l'email dell'amico!")
            return

        QMessageBox.information(
            self, "Inviato",
            f"{abbonamento} prestato a {email} con successo!"
        )
        self.close()


class FinestraModificaPagamento(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifica Pagamento")
        self.setFixedSize(400, 350)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("💳 Modifica Pagamento")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        riga_carta = QHBoxLayout()
        label_carta = QLabel("N° Carta:")
        label_carta.setFixedWidth(110)
        self.carta_input = QLineEdit()
        self.carta_input.setPlaceholderText("Es. 1234 5678 9012 3456")
        self.carta_input.setFixedHeight(36)
        riga_carta.addWidget(label_carta)
        riga_carta.addWidget(self.carta_input)
        layout.addLayout(riga_carta)

        riga_scadenza = QHBoxLayout()
        label_scadenza = QLabel("Scadenza:")
        label_scadenza.setFixedWidth(110)
        self.scadenza_input = QLineEdit()
        self.scadenza_input.setPlaceholderText("MM/AA")
        self.scadenza_input.setFixedHeight(36)
        riga_scadenza.addWidget(label_scadenza)
        riga_scadenza.addWidget(self.scadenza_input)
        layout.addLayout(riga_scadenza)

        riga_titolare = QHBoxLayout()
        label_titolare = QLabel("Titolare:")
        label_titolare.setFixedWidth(110)
        self.titolare_input = QLineEdit()
        self.titolare_input.setPlaceholderText("Es. Silvia Rota")
        self.titolare_input.setFixedHeight(36)
        riga_titolare.addWidget(label_titolare)
        riga_titolare.addWidget(self.titolare_input)
        layout.addLayout(riga_titolare)

        riga_cvv = QHBoxLayout()
        label_cvv = QLabel("CVV:")
        label_cvv.setFixedWidth(110)
        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("Es. 123")
        self.cvv_input.setFixedHeight(36)
        self.cvv_input.setMaxLength(3)
        riga_cvv.addWidget(label_cvv)
        riga_cvv.addWidget(self.cvv_input)
        layout.addLayout(riga_cvv)

        btn_salva = QPushButton("Salva")
        btn_salva.setFixedHeight(38)
        btn_salva.setStyleSheet(STILE_BTN_CHIUDI)
        btn_salva.clicked.connect(self.salva)
        layout.addWidget(btn_salva)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setFixedHeight(38)
        btn_annulla.setStyleSheet(STILE_BTN_ESCI)
        btn_annulla.clicked.connect(self.close)
        layout.addWidget(btn_annulla)

    def salva(self):
        carta = self.carta_input.text()
        scadenza = self.scadenza_input.text()
        titolare = self.titolare_input.text()
        cvv = self.cvv_input.text()

        if not carta or not scadenza or not titolare or not cvv:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi!")
            return

        QMessageBox.information(self, "Salvato", "Dati di pagamento aggiornati!")
        self.close()

class ProfiloDialog(QDialog):
    def __init__(self, finestra_principale, parent=None):
        super().__init__(parent)
        self.finestra_principale = finestra_principale
        self.setWindowTitle("Il mio Account")
        self.setFixedSize(430, 600)
        self.setStyleSheet(STILE_DIALOGO_PROFILO)

        # layout esterno
        layout_esterno = QVBoxLayout(self)
        layout_esterno.setContentsMargins(0, 0, 0, 0)

        # area scorrevole
        from PyQt6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        # widget interno con tutto il contenuto
        contenuto = QWidget()
        layout = QVBoxLayout(contenuto)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        titolo = QLabel("Profilo Utente")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        form = QFormLayout()
        form.setSpacing(14)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        def crea_label(testo):
            l = QLabel(testo)
            l.setStyleSheet(STILE_LABEL_PROFILO)
            return l

        self.campo_nome = QLineEdit("Silvia Rota")
        self.campo_email = QLineEdit("silvia@email.com")
        self.campo_password = QLineEdit("ciao")
        self.campo_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.campo_piano = QLineEdit("Premium")
        self.campo_piano.setReadOnly(True)
        self.campo_pagamento = QLineEdit("Visa **** 1234")
        self.campo_assistenza = QLineEdit("assistenza@servizio.com")
        self.campo_assistenza.setReadOnly(True)

        form.addRow(crea_label("Nome:"), self.campo_nome)
        form.addRow(crea_label("Email:"), self.campo_email)
        form.addRow(crea_label("Password:"), self.campo_password)
        form.addRow(crea_label("Piano:"), self.campo_piano)
        form.addRow(crea_label("Pagamento:"), self.campo_pagamento)
        form.addRow(crea_label("Assistenza:"), self.campo_assistenza)
        layout.addLayout(form)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep2)

        btn_cambia_password = QPushButton("🔑 Cambia password")
        btn_cambia_password.setFixedHeight(38)
        btn_cambia_password.setStyleSheet(STILE_BTN_SERVIZIO)
        btn_cambia_password.clicked.connect(self.apri_cambia_password)
        layout.addWidget(btn_cambia_password)

        btn_abbonamenti = QPushButton("📋 I miei abbonamenti")
        btn_abbonamenti.setFixedHeight(38)
        btn_abbonamenti.setStyleSheet(STILE_BTN_SERVIZIO)
        btn_abbonamenti.clicked.connect(self.apri_abbonamenti)
        layout.addWidget(btn_abbonamenti)

        btn_presta = QPushButton("🤝 Presta abbonamento")
        btn_presta.setFixedHeight(38)
        btn_presta.setStyleSheet(STILE_BTN_SERVIZIO)
        btn_presta.clicked.connect(self.apri_presta)
        layout.addWidget(btn_presta)

        btn_pagamento = QPushButton("💳 Modifica pagamento")
        btn_pagamento.setFixedHeight(38)
        btn_pagamento.setStyleSheet(STILE_BTN_SERVIZIO)
        btn_pagamento.clicked.connect(self.apri_pagamento)
        layout.addWidget(btn_pagamento)

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.Shape.HLine)
        sep3.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep3)

        btn_esci = QPushButton("Esci")
        btn_esci.setStyleSheet(STILE_BTN_ESCI)
        btn_esci.clicked.connect(self.esci)
        layout.addWidget(btn_esci, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
        layout.addWidget(btn_chiudi, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll.setWidget(contenuto)
        layout_esterno.addWidget(scroll)

    def esci(self):
        self.close()
        self.finestra_principale.login_window.show()
        self.finestra_principale.close()

    def apri_cambia_password(self):
        finestra = FinestraCambiaPassword(self)
        finestra.exec()

    def apri_abbonamenti(self):
        finestra = FinestraAbbonamenti(self)
        finestra.exec()

    def apri_presta(self):
        finestra = FinestraPresta(self)
        finestra.exec()

    def apri_pagamento(self):
        finestra = FinestraModificaPagamento(self)
        finestra.exec()
class FinestraAcquista(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acquista Abbonamento")
        self.setFixedSize(450, 520)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("Acquista Abbonamento")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        layout.addWidget(QLabel("Seleziona piattaforma:"))
        self.combo_piattaforma = QComboBox()
        self.combo_piattaforma.addItems([
            "Netflix", "Disney+", "Spotify", "Apple Music",
            "Amazon Music", "Prime Video", "RaiPlay",
            "Mediaset Infinity", "Kobo", "Kindle",
            "YouTube", "Sky Sport", "Now TV"
        ])
        self.combo_piattaforma.setFixedHeight(36)
        self.combo_piattaforma.setStyleSheet(STILE_COMBO)
        layout.addWidget(self.combo_piattaforma)

        layout.addWidget(QLabel("Seleziona piano:"))
        self.combo_piano = QComboBox()
        self.combo_piano.addItems(["Mensile", "Stagionale", "Annuale"])
        self.combo_piano.setFixedHeight(36)
        self.combo_piano.setStyleSheet(STILE_COMBO)
        layout.addWidget(self.combo_piano)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep2)

        layout.addWidget(QLabel("Dati di pagamento:"))

        riga_carta = QHBoxLayout()
        label_carta = QLabel("N° Carta:")
        label_carta.setFixedWidth(100)
        self.carta_input = QLineEdit()
        self.carta_input.setPlaceholderText("Es. 1234 5678 9012 3456")
        self.carta_input.setFixedHeight(36)
        riga_carta.addWidget(label_carta)
        riga_carta.addWidget(self.carta_input)
        layout.addLayout(riga_carta)

        riga_scadenza = QHBoxLayout()
        label_scadenza = QLabel("Scadenza:")
        label_scadenza.setFixedWidth(100)
        self.scadenza_input = QLineEdit()
        self.scadenza_input.setPlaceholderText("MM/AA")
        self.scadenza_input.setFixedHeight(36)
        riga_scadenza.addWidget(label_scadenza)
        riga_scadenza.addWidget(self.scadenza_input)
        layout.addLayout(riga_scadenza)

        riga_titolare = QHBoxLayout()
        label_titolare = QLabel("Titolare:")
        label_titolare.setFixedWidth(100)
        self.titolare_input = QLineEdit()
        self.titolare_input.setPlaceholderText("Es. Silvia Rota")
        self.titolare_input.setFixedHeight(36)
        riga_titolare.addWidget(label_titolare)
        riga_titolare.addWidget(self.titolare_input)
        layout.addLayout(riga_titolare)

        riga_cvv = QHBoxLayout()
        label_cvv = QLabel("CVV:")
        label_cvv.setFixedWidth(100)
        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("Es. 123")
        self.cvv_input.setFixedHeight(36)
        self.cvv_input.setMaxLength(3)
        riga_cvv.addWidget(label_cvv)
        riga_cvv.addWidget(self.cvv_input)
        layout.addLayout(riga_cvv)

        btn_acquista = QPushButton("Conferma acquisto")
        btn_acquista.setFixedHeight(40)
        btn_acquista.setStyleSheet(STILE_BTN_CHIUDI)
        btn_acquista.clicked.connect(self.conferma_acquisto)
        layout.addWidget(btn_acquista)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setFixedHeight(40)
        btn_annulla.setStyleSheet(STILE_BTN_ESCI)
        btn_annulla.clicked.connect(self.close)
        layout.addWidget(btn_annulla)

    def conferma_acquisto(self):
        piattaforma = self.combo_piattaforma.currentText()
        piano = self.combo_piano.currentText()
        carta = self.carta_input.text()
        scadenza = self.scadenza_input.text()
        titolare = self.titolare_input.text()
        cvv = self.cvv_input.text()

        if not carta or not scadenza or not titolare or not cvv:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi!")
            return

        QMessageBox.information(
            self, "Successo",
            f"Abbonamento {piano} a {piattaforma} acquistato con successo!"
        )
        self.close()


class FinestraRicerca(QDialog):
    def __init__(self, risultati, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Risultati ricerca")
        self.setFixedSize(350, 400)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        titolo = QLabel("Risultati trovati:")
        titolo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titolo)

        if not risultati:
            lbl = QLabel("Nessun risultato trovato.")
            lbl.setStyleSheet("font-size: 14px; color: #888888;")
            layout.addWidget(lbl)
        else:
            for nome, link in risultati:
                btn = QPushButton(nome)
                btn.setFixedHeight(45)
                btn.setStyleSheet(STILE_BTN_SERVIZIO)
                btn.clicked.connect(lambda checked, l=link: webbrowser.open(l))
                layout.addWidget(btn)

        layout.addStretch()

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
        layout.addWidget(btn_chiudi, alignment=Qt.AlignmentFlag.AlignCenter)


class SchedaCategoria(QDialog):
    def __init__(self, titolo, pulsanti, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titolo)
        self.setMinimumWidth(350)
        self.setMinimumHeight(400)
        self.setStyleSheet(STILE_SCHEDA_CATEGORIA)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        titolo_label = QLabel(titolo)
        titolo_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #222222;")
        titolo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo_label)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        layout.addStretch()

        for nome, link, logo_url in pulsanti:
            btn = QPushButton(nome)
            btn.setFixedHeight(50)
            btn.setFixedWidth(250)
            btn.setStyleSheet(STILE_BTN_SERVIZIO)
            btn.clicked.connect(lambda checked, l=link: webbrowser.open(l))

            if logo_url:
                icon = scarica_logo(logo_url)
                if icon:
                    btn.setIcon(icon)
                    btn.setIconSize(QSize(120, 40))
                    btn.setText("")

            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setFixedWidth(150)
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
        layout.addWidget(btn_chiudi, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

class FinestraPreferenze(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preferenze")
        self.setFixedSize(450, 550)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("Le mie Preferenze")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        sottotitolo = QLabel("Seleziona le categorie che ti interessano:")
        sottotitolo.setStyleSheet("font-size: 13px; color: #555555;")
        layout.addWidget(sottotitolo)

        self.checkboxes = []
        categorie = [
            "🎵 Musica", "🎬 Video", "📚 Libri",
            "📡 Streaming", "⚽ Sport"
        ]

        for cat in categorie:
            cb = QCheckBox(cat)
            cb.setStyleSheet("""
                QCheckBox {
                    font-size: 15px;
                    color: #222222;
                    padding: 6px;
                    spacing:10px;
                }
                
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #aaaaaa;
                    border-radius: 4px;
                    background-color: white;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #222222;
                    border-radius: 4px;
                    background-color: #4caf50;
                }
            """)
            layout.addWidget(cb)
            self.checkboxes.append(cb)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep2)

        btn_salva = QPushButton("Salva preferenze")
        btn_salva.setFixedHeight(40)
        btn_salva.setStyleSheet(STILE_BTN_CHIUDI)
        btn_salva.clicked.connect(self.salva)
        layout.addWidget(btn_salva)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setFixedHeight(40)
        btn_annulla.setStyleSheet(STILE_BTN_ESCI)
        btn_annulla.clicked.connect(self.close)
        layout.addWidget(btn_annulla)

    def salva(self):
        selezionate = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        if not selezionate:
            QMessageBox.warning(self, "Attenzione", "Seleziona almeno una categoria!")
            return
        QMessageBox.information(
            self, "Salvato",
            "Preferenze salvate:\n" + "\n".join(selezionate)
        )
        self.close()
class FinestraScaduti(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Abbonamenti Scaduti")
        self.setFixedSize(450, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("⏰ Abbonamenti Scaduti")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        # lista abbonamenti scaduti di esempio
        self.abbonamenti = [
            ("Netflix", "Scaduto il 01/05/2026"),
            ("Spotify", "Scaduto il 15/04/2026"),
            ("Disney+", "Scaduto il 10/03/2026"),
        ]

        self.righe = []

        for nome, data in self.abbonamenti:
            riga = QHBoxLayout()

            lbl = QLabel(f"{nome}  —  {data}")
            lbl.setStyleSheet("font-size: 13px; color: #222222;")
            riga.addWidget(lbl)

            btn_elimina = QPushButton("Elimina")
            btn_elimina.setFixedHeight(30)
            btn_elimina.setStyleSheet(STILE_BTN_ESCI)
            btn_elimina.clicked.connect(lambda checked, n=nome: self.elimina(n))
            riga.addWidget(btn_elimina)
            btn_rinnova = QPushButton("Rinnova")
            btn_rinnova.setFixedHeight(30)
            btn_rinnova.setStyleSheet(STILE_BTN_CHIUDI)
            btn_rinnova.clicked.connect(lambda checked,n=nome: self.rinnova(n))
            riga.addWidget(btn_rinnova)

            layout.addLayout(riga)
            self.righe.append((nome, riga))

        layout.addStretch()

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setFixedHeight(40)
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
        layout.addWidget(btn_chiudi, alignment=Qt.AlignmentFlag.AlignCenter)

    def elimina(self, nome):
        risposta = QMessageBox.question(
            self, "Conferma",
            f"Vuoi eliminare {nome} dagli scaduti?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if risposta == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Eliminato", f"{nome} eliminato!")

    def rinnova(self, nome):
        risposta = QMessageBox.question(
            self,"Rinnova",f"Vuoi rinnova{nome}?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
        
        if risposta == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self,"Rinnovato", f"{nome} rinnovato con successo!")     
class FinestraPrincipale(QWidget):
    def __init__(self, nome="Utente"):
        super().__init__()
        self.setWindowTitle("RelaxApp")
        self.setWindowIcon(
            QIcon(os.path.join(BASE_DIR,"logo/logo5.1.png"))
        )
        self.setMinimumSize(700, 500)
        self.nome_utente = nome
        self.setStyleSheet(STILE_FINESTRA_PRINCIPALE)
        self.showMaximized()
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
        pixmap = QPixmap(os.path.join(BASE_DIR,"logo/logo5.1.png))"))
        percorso_logo = os.path.join(BASE_DIR,"logo/logo5.1.png")
        print("LOGO:", percorso_logo)
        print("ESISTE?",os.path.exists(percorso_logo))
        pixmap = QPixmap(percorso_logo)
        logo.setPixmap(
            pixmap.scaled(140,1410,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
        
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(logo)
        saluto = QLabel (f"Buongiorno, {self.nome_utente}!")
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

        layout_extra = QHBoxLayout()
        layout_extra.setSpacing(12)

        extra = ["⭐  Preferenze", "🛒  Acquista", "⏰  Scaduti"]
        for nome in extra:
            btn = QPushButton(nome)
            btn.setFixedHeight(70)
            btn.setStyleSheet(STILE_BTN_EXTRA)
            if "Acquista" in nome:
                btn.clicked.connect(self.apri_acquista)
            elif "Preferenze" in nome :
                btn.clicked.connect(self.apri_preferenze)
            elif "Scaduti" in nome:
                btn.clicked.connect(self.apri_scaduti)
            layout_extra.addWidget(btn)
        layout_principale.addLayout(layout_extra)  
        layout_principale.addStretch()
        self.setLayout(layout_principale)  
    
            
    def apri_profilo(self):
        dialogo = ProfiloDialog(self, self)
        dialogo.exec()

    def apri_categoria(self, chiave):
        pulsanti = self.link_categorie[chiave]
        scheda = SchedaCategoria(chiave, pulsanti, self)
        scheda.exec()

    def apri_preferenze(self):
     finestra = FinestraPreferenze(self)
     finestra.exec()
    def apri_acquista(self):
        finestra = FinestraAcquista(self)
        finestra.exec()

    def apri_scaduti(self):
     finestra = FinestraScaduti(self)
     finestra.exec()

    def filtra_categorie(self):
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


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR,"logo/logo5.1.png")))
        self.showMaximized()
        self.setStyleSheet("QWidget { background-color: #e8f5e9; }")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(14)

        titolo = QLabel("Benvenutti in RelaxApp!")
        titolo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo = QLabel()
        pixmap = QPixmap(os.path.join(BASE_DIR,"logo/logo5.1.png"))
        logo.setPixmap(
            pixmap.scaled(220,220,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
        
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        riga_email = QHBoxLayout()
        label_email = QLabel("Email:")
        label_email.setFixedWidth(80)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Es. silvia@email.com")
        self.email_input.setFixedHeight(36)
        riga_email.addWidget(label_email)
        riga_email.addWidget(self.email_input)

        riga_password = QHBoxLayout()
        label_password = QLabel("Password:")
        label_password.setFixedWidth(80)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Inserisci password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(36)
        riga_password.addWidget(label_password)
        riga_password.addWidget(self.password_input)

        btn_login = QPushButton("Accedi")
        btn_login.setFixedHeight(38)
        btn_login.clicked.connect(self.login)

        btn_forgot = QPushButton("Hai dimenticato la password?")
        btn_forgot.setFlat(True)
        btn_forgot.setStyleSheet(STILE_BTN_LINK)
        btn_forgot.clicked.connect(self.password_dimenticata)

        btn_register = QPushButton("Non hai un account? Registrati")
        btn_register.setFlat(True)
        btn_register.setStyleSheet(STILE_BTN_LINK)
        btn_register.clicked.connect(self.apri_registrazione)
        layout.addWidget(logo)
        layout.addWidget(titolo)
        layout.addSpacing(10)
        layout.addLayout(riga_email)
        layout.addLayout(riga_password)
        layout.addWidget(btn_login)
        layout.addWidget(btn_forgot, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_register, alignment=Qt.AlignmentFlag.AlignCenter)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Errore", "Inserisci email e password!")
            return

        self.main_window = FinestraPrincipale("Silvia")
        self.main_window.login_window = self
        self.main_window.show()
        self.hide()

    def password_dimenticata(self):
        QDesktopServices.openUrl(QUrl("https://tuosito.com/reset-password"))

    def apri_registrazione(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    finestra = LoginWindow()
    finestra.show()
    sys.exit(app.exec())
