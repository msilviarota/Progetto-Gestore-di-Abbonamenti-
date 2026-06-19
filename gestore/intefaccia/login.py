import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt

# Configurazione dei percorsi per gestire gli import dal progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazione degli stili e delle utility
from intefaccia.stile import STILE_BTN_LINK, STILE_CAMPO_RICERCA
from intefaccia.utils import BASE_DIR
from intefaccia.main_window import FinestraPrincipale
# Nota: RegisterWindow e FinestraRecuperoPassword devono essere definite o importate
from intefaccia.dialoghi import RegisterWindow, FinestraRecuperoPassword

class LoginWindow(QWidget):
    """
    Gestisce l'interfaccia di accesso dell'utente (CDU7).
    Permette il login, il reindirizzamento alla registrazione (CDU3) 
    e al recupero password (CDU8).
    """

    def __init__(self, gestore_login=None, gestore_preferenze=None):
        super().__init__()
        self.gestore_login = gestore_login
        self.gestore_preferenze = gestore_preferenze
        
        # Configurazione Finestra (Requisito Mockup)
        self.setWindowTitle("Login - RelaxApp")
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, "logo5.1.png")))
        self.showMaximized()
        self.setStyleSheet("QWidget { background-color: #e8f5e9; }")
        
        self._build_ui()

    def _build_ui(self):
        """Costruisce l'interfaccia grafica del modulo di login."""
        layout_principale = QVBoxLayout(self)
        layout_principale.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 1. Logo del Progetto
        label_logo = QLabel()
        percorso_logo = os.path.join(BASE_DIR, "logo5.1.png")
        if os.path.exists(percorso_logo):
            pixmap = QPixmap(percorso_logo).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            label_logo.setPixmap(pixmap)
        label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(label_logo)

        # 2. Titolo
        titolo = QLabel("Bentornato!")
        titolo.setStyleSheet("font-size: 28px; font-weight: bold; color: #222222; margin-bottom: 20px;")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(titolo)

        # 3. Campi Input (CDU7 - Flusso principale)
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Inserisci la tua Email")
        self.input_email.setFixedWidth(350)
        self.input_email.setStyleSheet(STILE_CAMPO_RICERCA)
        layout_principale.addWidget(self.input_email, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Inserisci la tua Password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setFixedWidth(350)
        self.input_password.setStyleSheet(STILE_CAMPO_RICERCA)
        layout_principale.addWidget(self.input_password, alignment=Qt.AlignmentFlag.AlignCenter)

        # 4. Pulsante Accedi
        btn_accedi = QPushButton("Accedi")
        btn_accedi.setFixedWidth(350)
        btn_accedi.setStyleSheet("""
            QPushButton { background-color: #222222; color: white; padding: 12px; border-radius: 10px; font-weight: bold; }
            QPushButton:hover { background-color: #444444; }
        """)
        btn_accedi.clicked.connect(self.esegui_login)
        layout_principale.addWidget(btn_accedi, alignment=Qt.AlignmentFlag.AlignCenter)

        # 5. Collegamenti Extra (CDU3 e CDU8)
        layout_link = QHBoxLayout()
        layout_link.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_registrati = QPushButton("Registrati ora")
        btn_registrati.setStyleSheet(STILE_BTN_LINK)
        btn_registrati.clicked.connect(self.apri_registrazione)

        btn_forgot = QPushButton("Password dimenticata?")
        btn_forgot.setStyleSheet(STILE_BTN_LINK)
        btn_forgot.clicked.connect(self.apri_recupero)

        layout_link.addWidget(btn_registrati)
        layout_link.addWidget(QLabel("|"))
        layout_link.addWidget(btn_forgot)
        layout_principale.addLayout(layout_link)

    def esegui_login(self):
        """Implementa la logica di verifica credenziali (CDU7)."""
        email = self.input_email.text()
        password = self.input_password.text()

        if not email or not password:
            QMessageBox.warning(self, "Errore", "Credenziali non valide o mancanti.")
            return

        if self.gestore_login:
            risultato = self.gestore_login.verifica_accesso(email, password)
            if not risultato:
                QMessageBox.warning(self, "Errore", "Email o password errati.")
                return
            nome_utente = risultato.get("nome", "Utente")
        else:
            nome_utente = "Utente"

        print(f"Tentativo di accesso per: {email}")
        self.home = FinestraPrincipale(nome=nome_utente, email=email, gestore_preferenze=self.gestore_preferenze)
        self.home.show()
        self.close()

    def apri_registrazione(self):
        """CDU3: Apre la finestra di registrazione."""
        self.reg = RegisterWindow()
        self.reg.show()

    def apri_recupero(self):
        """CDU8: Apre la finestra per il recupero password."""
        self.rec = FinestraRecuperoPassword()
        self.rec.show()