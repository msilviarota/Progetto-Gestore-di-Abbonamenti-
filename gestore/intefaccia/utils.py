import os
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
from intefaccia.stile import STILE_MESSAGEBOX
# Corretto l'uso di __file__ per identificare la cartella dell'interfaccia [1]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def scarica_logo(percorso):
    """Carica e scala il logo di una piattaforma per le schede (CDU18) [1]."""
    try:
        # Costruisce il percorso partendo dalla radice dell'interfaccia
        percorso_assoluto = os.path.join(BASE_DIR, percorso)
        pixmap = QPixmap(percorso_assoluto)
        if not pixmap.isNull():
            return QIcon(
                pixmap.scaled(
                    120, 40, 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            print(f"Immagine nulla: {percorso_assoluto}")
    except Exception as e:
        print(f"Errore nel caricamento logo: {e}")
    return None

def mostra_messaggio(parent, titolo, testo, icona=QMessageBox.Icon.Warning):
    """Mostra un popup con lo stile scuro applicato direttamente sull'istanza."""
    msg = QMessageBox(parent)
    msg.setIcon(icona)
    msg.setWindowTitle(titolo)
    msg.setText(testo)
    msg.setStyleSheet(STILE_MESSAGEBOX)
    msg.exec()