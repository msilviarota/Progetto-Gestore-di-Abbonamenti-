import os
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

# Definizione della directory di base dell'interfaccia [2]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def scarica_logo(percorso):
    """
    Carica e scala l'immagine di un logo per restituire un QIcon [2].
    Utilizzato per visualizzare i loghi nel catalogo piattaforme [3].
    """
    try:
        percorso_assoluto = os.path.join(BASE_DIR, percorso)
        pixmap = QPixmap(percorso_assoluto)
        if not pixmap.isNull():
            # Scalatura mantenendo l'aspect ratio per una resa ottimale [2]
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
        print(f"Errore nel caricamento del logo: {e}")
    return None
