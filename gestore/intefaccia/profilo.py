from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

from intefaccia.stile import ( 
    STILE_DIALOGO_PROFILO, STILE_BTN_ESCI, STILE_TITOLO_PROFILO 
)
# Importazione dei dialoghi specifici definiti in dialoghi.py
from intefaccia.dialoghi import FinestraCambiaPassword, FinestraModificaPagamento

class ProfiloDialog(QDialog):
    """Hub per la gestione dell'account (CDU7, CDU9, CDU15, CDU16) [10]."""
    def __init__(self, finestra_principale, parent=None):
        super().__init__(parent)
        self.finestra_principale = finestra_principale
        self.setWindowTitle("Il mio Account")
        self.setFixedSize(430, 650)
        self.setStyleSheet(STILE_DIALOGO_PROFILO)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        titolo = QLabel("Gestione Profilo")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        layout.addWidget(titolo, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_pw = QPushButton("Cambia Password")
        btn_pw.clicked.connect(lambda: FinestraCambiaPassword(self).exec())
        layout.addWidget(btn_pw)

        btn_pag = QPushButton("Modifica Dati Pagamento")
        btn_pag.clicked.connect(lambda: FinestraModificaPagamento(self).exec())
        layout.addWidget(btn_pag)

        layout.addStretch()
        btn_logout = QPushButton("Logout")
        btn_logout.setStyleSheet(STILE_BTN_ESCI)
        btn_logout.clicked.connect(self.accept) # Chiude tornando alla finestra login
        layout.addWidget(btn_logout)