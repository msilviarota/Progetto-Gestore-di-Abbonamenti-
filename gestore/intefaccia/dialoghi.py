import os
import sys
import webbrowser
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt, QSize

# Configurazione path per gli import
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.dirname(cartella_corrente)
if radice_progetto not in sys.path:
    sys.path.insert(0, radice_progetto)

from intefaccia.stile import *
from intefaccia.utils import scarica_logo
from models.piattaforma import CATALOGO_PIATTAFORME

# Importiamo ProfiloDialog dal nuovo file profilo.py per mantenere la compatibilità
try:
    from intefaccia.profilo import ProfiloDialog
except ImportError:
    # Se il file profilo.py non è ancora pronto, definiamo una classe vuota per evitare crash
    class ProfiloDialog(QDialog): pass

# ============================================================
# SCHEDA CATEGORIA (CDU18 - Riproduci) -> RICHIESTA DA main_window
# ============================================================
class SchedaCategoria(QDialog):
    """Mostra le piattaforme di una categoria e ne permette l'avvio [2]."""
    def __init__(self, titolo, servizi, email_utente, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titolo)
        self.setMinimumSize(400, 500)
        self.setStyleSheet(STILE_SCHEDA_CATEGORIA)
        self.email_utente = email_utente
        self._build_ui(servizi)

    def _build_ui(self, servizi):
        layout = QVBoxLayout(self)
        for nome, piattaforma in servizi.items():
            btn = QPushButton(nome.capitalize())
            icona = scarica_logo(piattaforma.logo)
            if icona:
                btn.setIcon(icona)
                btn.setIconSize(QSize(100, 30))
            btn.clicked.connect(lambda ch, p=piattaforma: webbrowser.open(p.link_login))
            layout.addWidget(btn)

# ============================================================
# FINESTRA RICERCA (CDU4) -> RICHIESTA DA main_window
# ============================================================
class FinestraRicerca(QDialog):
    def __init__(self, testo, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Risultati per: {testo}")
        self.setFixedSize(400, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Risultati della ricerca per '{testo}':"))

# ============================================================
# FINESTRE PER IL LOGIN (CDU3, CDU8) -> RICHIESTE DA login.py
# ============================================================
class RegisterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrazione")
        self.setFixedSize(400, 500)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Modulo di Registrazione"))

class FinestraRecuperoPassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recupero Password")
        self.setFixedSize(400, 250)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Inserisci Email:"))
        layout.addWidget(QLineEdit())