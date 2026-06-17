import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QMessageBox
)
from PyQt6.QtGui import QFont, QDesktopServices, QPixmap, QIcon
from PyQt6.QtCore import Qt, QUrl

from stile import STILE_BTN_LINK
from utils import BASE_DIR


class RegisterWindow(QWidget):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window  # Memorizziamo il riferimento del login
        self.setWindowTitle("Registrazione")
        self.showMaximized()
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
        self.nome_input.setPlaceholderText("Es. Silvia")
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
        self.eta_input.setPlaceholderText("Es. 20")
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
        from Service.registrazione import GestoreRegistrazione
        from database.repositoryUtente import RepositoryUtente 
        from database.repositoryPreferenze import RepositoryPreferenze

        nome = self.nome_input.text()
        cognome = self.cognome_input.text()
        eta = self.eta_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        conferma = self.conferma_input.text()

        if not nome or not cognome or not eta or not email or not password or not conferma:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi!")
            return
        if password != conferma:
            QMessageBox.warning(self, "Errore", "Le password non coincidono!")
            return
        repo_utente = RepositoryUtente()
        repo_preferenze = RepositoryPreferenze()
        gestore = GestoreRegistrazione(repo_utente, repo_preferenze)
        gestore.inviaModulo(nome,cognome,eta,email,password)
        if gestore.valida():
            QMessageBox.information(self,"Successo", f"Account creato per {email}")
            self.torna_login()
        else:
            QMessageBox.warning(self, "Errore", "Email già registrata!")

    def torna_login(self):
        if self.login_window:
            self.login_window.show()  # Mostra la finestra di login esistente
        self.close()  # Chiude la finestra di registrazione


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, "logo5.1.png")))
        self.showMaximized()
        self.setStyleSheet("QWidget { background-color: #e8f5e9; }")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(14)

        # CORRETTO: rimosso il refuso 'Benvenutti'
        titolo = QLabel("Benvenuti in RelaxApp!")
        titolo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = QLabel()
        pixmap = QPixmap(os.path.join(BASE_DIR, "logo5.1.png"))
        logo.setPixmap(
            pixmap.scaled(220, 220, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        )
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
        from database.repositoryUtente import RepositoryUtente 
        from database.repositoryAbbonamento import RepositoryAbbonamento 
        from database.repositoryLog import RepositoryLog
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Errore", "Inserisci email e password!")
            return
        
        repo_utente = RepositoryUtente()
        repo_abbonamento = RepositoryAbbonamento()
        repo_log = RepositoryLog()
        gestore = GestoreAccessi (repo_utente, repo_abbonamento,repo_log)
        esito = gestore.inviaCredenziali(email,password)
        if esito:
            self.main_window = FinestraPrincipale(email)
            self.main_window.login_window = self 
            self.main_window.show()
            self.hide()
        else: 
            QMessageBox.warning(self, "Errore", "Email o password errati!")
    def password_dimenticata(self):
        QDesktopServices.openUrl(QUrl("https://tuosito.com/reset-password"))

    def apri_registrazione(self):
        # Passiamo 'self' (LoginWindow) a RegisterWindow così sa dove tornare
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()  # Nascondiamo il login invece di chiuderlo bruscamente