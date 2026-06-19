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


class RegisterWindow(QDialog):
    """Gestisce la creazione di un nuovo account (CDU3) [5]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrazione")
        self.setFixedSize(400, 550)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Inserisci Nome, Email e Password:"))
        layout.addWidget(QLineEdit())
        btn = QPushButton("Registrati")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

class FinestraRecuperoPassword(QDialog):
    """Richiesta di una password temporanea (CDU8) [4]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recupero Password")
        self.setFixedSize(400, 250)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Inserisci la tua email:"))
        layout.addWidget(QLineEdit())
        btn = QPushButton("Invia")
        btn.clicked.connect(lambda: QMessageBox.information(self, "Info", "Email inviata"))
        layout.addWidget(btn)

class FinestraCambiaPassword(QDialog):
    """Modulo per impostare una nuova password (CDU9) [6]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cambia Password")
        self.setFixedSize(400, 350)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Nuova Password:"))
        layout.addWidget(QLineEdit())
        btn = QPushButton("Conferma")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

class FinestraModificaPagamento(QDialog):
    """Modifica i dati della carta (CDU16) [7]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifica Pagamento")
        self.setFixedSize(400, 400)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Nuovo Numero Carta:"))
        layout.addWidget(QLineEdit())
        btn = QPushButton("Salva")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
        
class FinestraRicerca(QDialog):
    """Visualizza i risultati della ricerca globale (CDU4)."""
    def __init__(self, testo, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Risultati per: {testo}")
        self.setFixedSize(400, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Risultati trovati per '{testo}':"))
