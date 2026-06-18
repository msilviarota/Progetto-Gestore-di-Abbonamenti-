import os
import sys
import webbrowser
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
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

class FinestraRicerca(QDialog):
    """Visualizza i risultati della ricerca globale (CDU4) [4]."""
    def __init__(self, testo, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Risultati per: {testo}")
        self.setFixedSize(400, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Risultati trovati per '{testo}':"))

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