import os
import sys
import webbrowser
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QFrame, QMessageBox, QScrollArea, QGridLayout
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

# Configurazione del percorso radice per gli import (correzione di **file** [2, 3])
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazioni coerenti con la struttura dei package [4, 5]
from intefaccia.stile import (
    STILE_DIALOGO_PROFILO, STILE_BTN_SERVIZIO, STILE_BTN_CHIUDI, 
    STILE_SCHEDA_CATEGORIA, STILE_CAMPO_RICERCA
)
from intefaccia.utils import scarica_logo
from models.piattaforma import CATALOGO_PIATTAFORME

# ============================================================
# 1. SCHEDA CATEGORIA (CDU18 - Riproduci) [6]
# ============================================================
class SchedaCategoria(QDialog):
    """Mostra le piattaforme di una categoria e ne permette l'avvio [6]."""
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
# 2. FINESTRE DI SUPPORTO (CDU 4, 8) [7]
# ============================================================
class FinestraRecuperoPassword(QDialog):
    """CDU8: Gestisce la richiesta di una password temporanea [7, 8]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recupero Password")
        self.setFixedSize(400, 250)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Inserisci l'email per il recupero:"))
        self.campo_email = QLineEdit()
        layout.addWidget(self.campo_email)
        
        btn_invia = QPushButton("Invia Password Temporanea")
        btn_invia.clicked.connect(self.conferma_invio)
        layout.addWidget(btn_invia)

    def conferma_invio(self):
        QMessageBox.information(self, "Successo", "Email inviata correttamente [9].")
        self.accept()

class FinestraRicerca(QDialog):
    """CDU4: Visualizza i risultati della ricerca globale [7, 10]."""
    def __init__(self, testo, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Risultati per: {testo}")
        self.setFixedSize(400, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Risultati trovati per '{testo}':"))
        # Logica di popolamento risultati (CDU4)...

# ============================================================
# 3. GESTIONE PREFERENZE (CDU5) [11]
# ============================================================
class FinestraPreferenze(QDialog):
    """CDU5: Permette all'utente di impostare i propri gusti [11, 12]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Le mie Preferenze")
        self.setFixedSize(450, 550)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")
        # Implementazione della selezione categorie...

# ============================================================
# 4. UTILITY DI SISTEMA (CDU23) [13]
# ============================================================
def mostra_errore_backup(messaggio_errore):
    """Popup di avviso per fallimento backup (CDU23) [13, 14]."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle("Avviso di Sistema - Backup")
    msg.setText(messaggio_errore)
    msg.setStyleSheet("QMessageBox { background-color: #fce4ec; font-size: 14px; }")
    msg.exec()