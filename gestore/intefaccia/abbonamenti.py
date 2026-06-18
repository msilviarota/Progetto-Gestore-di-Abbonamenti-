from PyQt6.QtWidgets import ( QVBoxLayout, QPushButton, QLabel, QDialog, QScrollArea, QFrame )
from PyQt6.QtCore import Qt

# Importazione dei servizi e modelli necessari [23, 24]
from Service.gestoreAbbonamenti import GestoreAbbonamenti
from Service.gestorePrestiti import GestorePrestiti

class FinestraAbbonamenti(QDialog):
    """CDU13: Visualizza la lista degli abbonamenti attivi dell'utente [11, 16, 25]."""
    def __init__(self, parent=None, email="", gestore_abbonamenti=None):
        super().__init__(parent)
        self.email_utente = email
        self.gestore = gestore_abbonamenti
        self.setWindowTitle("I miei Abbonamenti")
        self.setFixedSize(500, 400)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

class FinestraAcquista(QDialog):
    """CDU1: Gestisce la selezione dell'offerta e l'acquisto di un nuovo abbonamento [22, 26]."""
    def __init__(self, parent=None, email="", gestore_abbonamenti=None):
        super().__init__(parent)
        self.email_utente = email
        self.gestore = gestore_abbonamenti
        self.setWindowTitle("Acquista Abbonamento")
        self.setFixedSize(450, 520)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

class FinestraPresta(QDialog):
    """CDU11: Permette di condividere un abbonamento con un amico registrato [11, 27, 28]."""
    def __init__(self, parent=None, email_utente="", gestore_prestiti=None):
        super().__init__(parent)
        self.email_utente_corrente = email_utente
        self.gestore = gestore_prestiti
        self.setWindowTitle("Presta Abbonamento")
        self.setFixedSize(400, 300)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

class FinestraScaduti(QDialog):
    """CDU14: Gestione e rimozione degli abbonamenti non più validi [17, 22, 29]."""
    def __init__(self, parent=None, email="", gestore_abbonamenti=None):
        super().__init__(parent)
        self.email_utente = email
        self.gestore = gestore_abbonamenti
        self.setWindowTitle("Abbonamenti Scaduti")
        self.setFixedSize(500, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")