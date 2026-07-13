from PyQt6.QtWidgets import QDialog

from intefaccia.stile import STILE_DIALOGO_VERDE
class FinestraAbbonamenti(QDialog):
    """Visualizza gli abbonamenti acquistati (CDU13) [11]."""
    def __init__(self, parent=None, email="", gestore_abbonamenti=None):
        super().__init__(parent)
        self.setWindowTitle("I miei Abbonamenti")
        self.setFixedSize(450, 400)
        self.setStyleSheet(STILE_DIALOGO_VERDE)

class FinestraAcquista(QDialog):
    """Gestisce l'acquisto di un nuovo abbonamento (CDU1) [12]."""
    def __init__(self, parent=None, email="", gestore_abbonamenti=None):
        super().__init__(parent)
        self.setWindowTitle("Acquista Abbonamento")
        self.setFixedSize(450, 520)
        self.setStyleSheet(STILE_DIALOGO_VERDE)

class FinestraPresta(QDialog):
    """Permette di prestare un abbonamento (CDU11) [11]."""
    def __init__(self, parent=None, email_utente="", gestore_prestiti=None):
        super().__init__(parent)
        self.setWindowTitle("Presta Abbonamento")
        self.setFixedSize(400, 300)
        self.setStyleSheet(STILE_DIALOGO_VERDE) 

class FinestraScaduti(QDialog):
    """Gestione abbonamenti scaduti (CDU14, CDU19) [12]."""
    def __init__(self, parent=None, email="", gestore_abbonamenti=None):
        super().__init__(parent)
        self.setWindowTitle("Abbonamenti Scaduti")
        self.setFixedSize(500, 500)
        self.setStyleSheet(STILE_DIALOGO_VERDE)