import os
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def scarica_logo(percorso):
    try:
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
        print(f"Errore: {e}")
    return None
