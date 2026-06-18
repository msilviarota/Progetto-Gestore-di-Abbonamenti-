import sys
import os
from PyQt6.QtWidgets import QApplication

# Configurazione del percorso radice per permettere gli import dai vari package [4]
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import dei gestori di servizio e delle finestre di interfaccia [4-6]
from login import LoginWindow

if __name__ == "__main__":
    # Inizializzazione dell'applicazione PyQt6 [5]
    app = QApplication(sys.argv)
    
    # Avvio della finestra di Login (CDU7) [6, 7]
    finestra_login = LoginWindow()
    finestra_login.show()
    
    sys.exit(app.exec())