from PyQt6.QtWidgets import ( QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QLineEdit, QFrame, QMessageBox )
from PyQt6.QtCore import Qt

# Importazione degli stili definiti nel progetto [11-14]
from intefaccia.stile import ( 
    STILE_DIALOGO_PROFILO, STILE_BTN_ESCI, STILE_BTN_CHIUDI, 
    STILE_LABEL_PROFILO, STILE_TITOLO_PROFILO 
)
# Importazione delle finestre correlate [15-17]
from intefaccia.dialoghi import FinestraCambiaPassword, FinestraModificaPagamento

class ProfiloDialog(QDialog):
    """
    Hub centrale per la gestione dell'account utente (CDU7, CDU9, CDU15, CDU16) [8, 9].
    """
    def __init__(self, finestra_principale, parent=None):
        super().__init__(parent)
        self.finestra_principale = finestra_principale
        self.setWindowTitle("Il mio Account")
        self.setFixedSize(430, 650) # Dimensioni coerenti con le specifiche [9, 10]
        self.setStyleSheet(STILE_DIALOGO_PROFILO)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        
        titolo = QLabel("Gestione Profilo")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        layout.addWidget(titolo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Pulsanti per le operazioni sul profilo [16-19]
        btn_cambia_pw = QPushButton("Cambia Password")
        btn_cambia_pw.clicked.connect(self.apri_cambia_password)
        layout.addWidget(btn_cambia_pw)

        btn_modifica_pagamento = QPushButton("Modifica Dati Pagamento")
        btn_modifica_pagamento.clicked.connect(self.apri_modifica_pagamento)
        layout.addWidget(btn_modifica_pagamento)

        # Pulsanti di chiusura e logout [9, 11, 20, 21]
        layout.addStretch()
        btn_logout = QPushButton("Logout")
        btn_logout.setStyleSheet(STILE_BTN_ESCI)
        btn_logout.clicked.connect(self.esegui_logout)
        layout.addWidget(btn_logout)

    def apri_cambia_password(self):
        """CDU9: Avvia la procedura di cambio password [16, 18]."""
        dialogo = FinestraCambiaPassword(self)
        dialogo.exec()

    def apri_modifica_pagamento(self):
        """CDU16: Permette di aggiornare i dati della carta [17, 19]."""
        dialogo = FinestraModificaPagamento(self)
        dialogo.exec()

    def esegui_logout(self):
        """CDU15: Chiude la sessione e torna al login [20]."""
        self.close()
        self.finestra_principale.close()
        # Logica di reindirizzamento al login gestita dal sistema [6, 20]