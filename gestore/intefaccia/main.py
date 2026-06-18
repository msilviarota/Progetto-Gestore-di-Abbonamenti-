import sys
import os
from PyQt6.QtWidgets import QApplication

# Configurazione del percorso radice (gestore) per gli import
# Se main.py è in gestore/intefaccia/, il padre è 'gestore'
percorso_attuale = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.dirname(percorso_attuale)
if radice_progetto not in sys.path:
    sys.path.insert(0, radice_progetto)

# Ora gli import funzioneranno correttamente con il prefisso del package
from intefaccia.login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Avvio della finestra di Login (CDU7)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())