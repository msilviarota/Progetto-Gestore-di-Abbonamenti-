import os
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QMessageBox, QSpinBox
)
from PyQt6.QtCore import Qt

# Configurazione dei percorsi per gestire gli import dal progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from intefaccia.stile import (
    STILE_CAMPO_RICERCA, STILE_BTN_LINK, STILE_FINESTRA_LOGIN,
    STILE_TITOLO_REGISTRAZIONE, STILE_SPINBOX, STILE_BTN_ACCEDI
)

class RegisterWindow(QWidget):
    """
    Gestisce l'interfaccia di creazione di un nuovo account (CDU3).
    Richiede: nome, cognome, età, email, password e conferma [1].
    """

    def __init__(self, gestore_registrazione=None):
        super().__init__()
        self.gestore_registrazione = gestore_registrazione
        
        # Configurazione Finestra basata su Source [3]
        self.setWindowTitle("Registrazione - RelaxApp")
        self.setFixedSize(450, 550) # Leggermente aumentata per ospitare tutti i campi di [1]
        self.setStyleSheet(STILE_FINESTRA_LOGIN)
        
        self._build_ui()

    def _build_ui(self):
        """Costruisce il modulo di inserimento dati (Requisito 1.1.1)."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(10)

        # Titolo
        titolo = QLabel("Crea il tuo Account")
        titolo.setStyleSheet(STILE_TITOLO_REGISTRAZIONE)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        # Campi Input richiesti dai Requisiti [1]
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome")
        self.input_nome.setStyleSheet(STILE_CAMPO_RICERCA)
        layout.addWidget(self.input_nome)

        self.input_cognome = QLineEdit()
        self.input_cognome.setPlaceholderText("Cognome")
        self.input_cognome.setStyleSheet(STILE_CAMPO_RICERCA)
        layout.addWidget(self.input_cognome)

        layout_eta = QHBoxLayout()
        layout_eta.addWidget(QLabel("Età:"))
        self.input_eta = QSpinBox()
        self.input_eta.setRange(14, 120)
        self.input_eta.setStyleSheet(STILE_SPINBOX)
        layout_eta.addWidget(self.input_eta)
        layout.addLayout(layout_eta)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Indirizzo Email")
        self.input_email.setStyleSheet(STILE_CAMPO_RICERCA)
        layout.addWidget(self.input_email)

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Password")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setStyleSheet(STILE_CAMPO_RICERCA)
        layout.addWidget(self.input_pass)

        self.input_conf_pass = QLineEdit()
        self.input_conf_pass.setPlaceholderText("Conferma Password")
        self.input_conf_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_conf_pass.setStyleSheet(STILE_CAMPO_RICERCA)
        layout.addWidget(self.input_conf_pass)

        # Pulsante Registrati
        btn_register = QPushButton("Registrati")
        btn_register.setStyleSheet(STILE_BTN_ACCEDI)
        btn_register.clicked.connect(self.esegui_registrazione)
        layout.addWidget(btn_register)

        # Torna al Login
        btn_back = QPushButton("Hai già un account? Accedi")
        btn_back.setStyleSheet(STILE_BTN_LINK)
        btn_back.clicked.connect(self.close)
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    def esegui_registrazione(self):
        """Valida i dati e simula la creazione del profilo (CDU3)."""
        nome = self.input_nome.text()
        cognome = self.input_cognome.text()
        email = self.input_email.text()
        password = self.input_pass.text()
        conferma = self.input_conf_pass.text()

        # 1. Controllo campi vuoti
        if not all([nome, cognome, email, password, conferma]):
            QMessageBox.warning(self, "Errore", "Tutti i campi sono obbligatori.")
            return

        # 2. Verifica uguaglianza password (Requisito 1.1.1)
        if password != conferma:
            QMessageBox.warning(self, "Errore", "Le password non coincidono.")
            return

        # 3. Logica di registrazione (CDU3 - Flusso principale)
        print(f"Registrazione in corso per {email}...")
        
        # Simula il successo della registrazione e la generazione dell'ID [1]
        id_utente = "USR_7721" # Esempio di codice identificativo restituito [1]
        QMessageBox.information(self, "Successo", 
            f"Registrazione completata!\nIl tuo codice identificativo è: {id_utente}\n"
            "Controlla la tua email per confermare l'account.")
        self.close()