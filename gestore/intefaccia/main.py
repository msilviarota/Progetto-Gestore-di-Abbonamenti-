import sys
import os
from PyQt6.QtWidgets import QApplication

# Configura il path in modo che 'gestore' sia la radice [13]
percorso_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.dirname(percorso_corrente)
if radice_progetto not in sys.path:
    sys.path.insert(0, radice_progetto)

# Importazione della finestra di Login (CDU7)
from intefaccia.login import LoginWindow

def avvia_applicazione():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    avvia_applicazione()