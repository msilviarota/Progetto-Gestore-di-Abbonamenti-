import os
import sys
import webbrowser
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox,QFrame
from PyQt6.QtCore import Qt, QSize

# Configurazione del path per permettere l'importazione dei moduli del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.dirname(cartella_corrente)
if radice_progetto not in sys.path:
    sys.path.insert(0, radice_progetto)

from intefaccia.stile import *
from intefaccia.utils import scarica_logo

class SchedaCategoria(QDialog):
    """Mostra le piattaforme di una categoria e permette l'avvio (CDU18) [3]."""
    def __init__(self, titolo, servizi, email_utente, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titolo)
        self.setMinimumSize(400, 500)
        self.setStyleSheet(STILE_SCHEDA_CATEGORIA)
        layout = QVBoxLayout(self)
        for nome, piattaforma in servizi.items():
            btn = QPushButton(nome.capitalize())
            icona = scarica_logo(piattaforma.logo)
            if icona:
                btn.setIcon(icona)
                btn.setIconSize(QSize(100, 30))
            btn.clicked.connect(lambda ch, p=piattaforma: webbrowser.open(p.link_login))
            layout.addWidget(btn)

class FinestraCambiaPassword(QDialog):
    """Modulo completo per cambiare la password (CDU9)."""
    def __init__(self, email_utente, gestore_profilo, parent=None):
        super().__init__(parent)

        self.email_utente = email_utente
        self.gestore_profilo = gestore_profilo

        self.setWindowTitle("Cambia Password")
        self.setFixedSize(420, 320)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("🔑 Cambia Password")
        titolo.setStyleSheet("font-size: 20px; font-weight: bold; color: #222;")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        # Vecchia password
        layout.addWidget(QLabel("Vecchia password:"))
        self.vecchia_input = QLineEdit()
        self.vecchia_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.vecchia_input)

        # Nuova password
        layout.addWidget(QLabel("Nuova password:"))
        self.nuova_input = QLineEdit()
        self.nuova_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.nuova_input)

        # Conferma
        layout.addWidget(QLabel("Conferma nuova password:"))
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
            QMessageBox.warning(self, "Errore", "Le password non coincidono.")
            return

        if len(nuova) < 6:
            QMessageBox.warning(self, "Errore", "La password deve avere almeno 6 caratteri.")
            return

        successo = self.gestore_profilo.cambia_password_utente(
            self.email_utente,
            vecchia,
            nuova
        )

        if successo:
            QMessageBox.information(self, "Successo", "Password cambiata correttamente.")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "La vecchia password non è corretta.")


class FinestraRecuperoPassword(QDialog):
    """Richiesta di una password temporanea (CDU8)."""
    def __init__(self, gestore_login, parent=None):
        super().__init__(parent)

        self.gestore_login = gestore_login

        self.setWindowTitle("Recupero Password")
        self.setFixedSize(420, 260)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("🔑 Recupero Password")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 20px; font-weight: bold; color: #222;")
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        layout.addWidget(QLabel("Inserisci la tua email:"))
        self.input_email = QLineEdit()
        layout.addWidget(self.input_email)

        btn = QPushButton("Invia nuova password")
        btn.clicked.connect(self.invia)
        layout.addWidget(btn)

    def invia(self):
        email = self.input_email.text()

        if not email:
            QMessageBox.warning(self, "Errore", "Inserisci un'email.")
            return

        successo = self.gestore_login.recupera_password(email)

        if successo:
            QMessageBox.information(self, "Successo", "Una nuova password è stata inviata alla tua email.")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "Email non trovata.")



class FinestraModificaPagamento(QDialog):
    """Modulo completo per cambiare il numero della carta (CDU16)."""
    def __init__(self, email_utente, gestore_profilo, parent=None):
        super().__init__(parent)

        self.email_utente = email_utente
        self.gestore_profilo = gestore_profilo

        self.setWindowTitle("Modifica Carta")
        self.setFixedSize(420, 320)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("💳 Modifica Carta")
        titolo.setStyleSheet("font-size: 20px; font-weight: bold; color: #222;")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        # Vecchia carta
        layout.addWidget(QLabel("Vecchio numero carta:"))
        self.vecchia_input = QLineEdit()
        self.vecchia_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.vecchia_input)

        # Nuova carta
        layout.addWidget(QLabel("Nuovo numero carta:"))
        self.nuova_input = QLineEdit()
        self.nuova_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.nuova_input)

        # Conferma
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


class FinestraRicerca(QDialog):
    """Visualizza i risultati della ricerca globale (CDU4)."""
    def __init__(self, testo, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Risultati per: {testo}")
        self.setFixedSize(400, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Risultati trovati per '{testo}':"))
        layout.addStretch()
        
class FinestraRegistrazione(QDialog):
    def __init__(self, gestore_login, parent=None):
        super().__init__(parent)

        self.gestore_login = gestore_login

        self.setWindowTitle("Crea un nuovo account")
        self.setFixedSize(420, 380)
        self.setStyleSheet("""
          QDialog { background-color: #e8f5e9; }
         QLineEdit {
         color: black;
         background-color: white;
         border: 1px solid #888;
         padding: 6px;
         border-radius: 6px; }""")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("📝 Registrazione")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 20px; font-weight: bold; color: #222;")
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
