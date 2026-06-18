import os
import sys
import webbrowser
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt, QSize

# Setup path per i modelli
percorso_attuale = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.dirname(percorso_attuale)
if radice_progetto not in sys.path:
    sys.path.insert(0, radice_progetto)

# Import dagli altri file dell'interfaccia
from intefaccia.stile import *
from intefaccia.utils import scarica_logo
from models.piattaforma import CATALOGO_PIATTAFORME

# IMPORTANTE: Se abbiamo spostato ProfiloDialog in profilo.py, 
# dobbiamo importarlo qui affinché main_window lo trovi
try:
    from intefaccia.profilo import ProfiloDialog
except ImportError:
    ProfiloDialog = None # Fallback se il file non esiste ancora

# --- AGGIUNTA RegisterWindow (richiesta da login.py [4]) ---
class RegisterWindow(QDialog):
    """CDU3: Gestisce la registrazione di un nuovo utente [5, 6]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrazione Nuovo Utente")
        self.setFixedSize(400, 500)
        self.setStyleSheet(STILE_DIALOGO_PROFILO)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Nome:"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(QLineEdit())
        btn = QPushButton("Registrati")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

# --- Altri dialoghi necessari ---
class FinestraRecuperoPassword(QDialog):
    """CDU8: Recupero password [7, 8]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recupero Password")
        self.setFixedSize(400, 250)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Inserisci la tua email:"))
        self.email = QLineEdit()
        layout.addWidget(self.email)
        btn = QPushButton("Invia Password Temporanea")
        btn.clicked.connect(lambda: QMessageBox.information(self, "Info", "Email inviata"))
        layout.addWidget(btn)

class FinestraRicerca(QDialog):
    """CDU4: Risultati ricerca globale [8, 9]."""
    def __init__(self, testo, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Risultati: {testo}")
        self.setFixedSize(400, 400)