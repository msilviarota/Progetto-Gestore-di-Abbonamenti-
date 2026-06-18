import sys
import os

# Configurazione path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QMessageBox, QDialog
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt

from stile import STILE_BTN_LINK
from utils import BASE_DIR

# --- Classi RegisterWindow e FinestraRecuperoPassword devono stare sopra LoginWindow ---
# Se le tieni nello stesso file, assicuratevi che le definizioni siano qui sopra.
# Se sono in file separati, assicurati di avere gli import corretti in cima.

class LoginWindow(QWidget):
    def __init__(self, gest_pref):
        super().__init__()
        self.gest_pref = gest_pref
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, "logo5.1.png")))
        self.showMaximized()
        self.setStyleSheet("QWidget { background-color: #e8f5e9; }")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(14)

        titolo = QLabel("Benvenuti in RelaxApp!")
        titolo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = QLabel()
        pixmap = QPixmap(os.path.join(BASE_DIR, "logo5.1.png"))
        logo.setPixmap(pixmap.scaled(220, 220, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
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
        from main_window import FinestraPrincipale
        from Service.gestoreLogin import GestoreAccessi 
        from repository.repositoryUtente import RepositoryUtente 
        from repository.repositoryAbbonamento import RepositoryAbbonamento 
        from repository.repositoryLog import RepositoryLog
        
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Errore", "Inserisci email e password!")
            return
        
        # Inizializzazioni singole
        repo_utente = RepositoryUtente()
        repo_abbonamento = RepositoryAbbonamento()
        repo_log = RepositoryLog()
        
        gestore = GestoreAccessi(repo_utente, repo_abbonamento, repo_log)
        esito = gestore.inviaCredenziali(email, password)

        if esito:
            dati_utente = repo_utente.getUtente(email)
            nome_reale = dati_utente.get("nome", "Utente") if dati_utente else "Utente"
            
            # CORRETTO: nome parametro "gestore_preferenze"
            self.main_window = FinestraPrincipale(
                nome=nome_reale,
                email=email,
                gestore_preferenze=self.gest_pref
            )
            self.main_window.show()
            self.hide()
        else: 
            QMessageBox.warning(self, "Errore", "Email o password errati!")

    def password_dimenticata(self):
        finestra = FinestraRecuperoPassword(self)
        finestra.exec()

    def apri_registrazione(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()