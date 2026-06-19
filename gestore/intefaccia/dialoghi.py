import os
import sys
import webbrowser
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox,QFrame
from PyQt6.QtCore import Qt, QSize

# Configurazione del path per permettere l'importazione dei moduli del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.dirname(cartella_corrente)
if radice_progetto not in sys.path:
    sys.path.insert(0, radice_progetto)

from intefaccia.stile import *
from intefaccia.utils import scarica_logo
from models.abbonamento import Abbonamento
class SchedaCategoria(QDialog):
    """Mostra le piattaforme di una categoria e permette l'avvio (CDU18) [3]."""
    def __init__(self, titolo, servizi, email_utente, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titolo)
        self.setMinimumSize(400, 500)
        self.setStyleSheet(STILE_SCHEDA_CATEGORIA)
        layout = QVBoxLayout(self)
        for nome, piattaforma in servizi.items():
            btn = QPushButton(nome.capitalize())
            icona = scarica_logo(piattaforma.logo)
            if icona:
                btn.setIcon(icona)
                btn.setIconSize(QSize(100, 30))
            btn.clicked.connect(lambda ch, p=piattaforma: webbrowser.open(p.link_login))
            layout.addWidget(btn)

class FinestraCambiaPassword(QDialog):
    """Modulo completo per cambiare la password (CDU9)."""
    def __init__(self, email_utente, gestore_profilo, parent=None):
        super().__init__(parent)

        self.email_utente = email_utente
        self.gestore_profilo = gestore_profilo

        self.setWindowTitle("Cambia Password")
        self.setFixedSize(420, 320)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("🔑 Cambia Password")
        titolo.setStyleSheet("font-size: 20px; font-weight: bold; color: #222;")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        # Vecchia password
        layout.addWidget(QLabel("Vecchia password:"))
        self.vecchia_input = QLineEdit()
        self.vecchia_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.vecchia_input)

        # Nuova password
        layout.addWidget(QLabel("Nuova password:"))
        self.nuova_input = QLineEdit()
        self.nuova_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.nuova_input)

        # Conferma
        layout.addWidget(QLabel("Conferma nuova password:"))
        self.conferma_input = QLineEdit()
        self.conferma_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.conferma_input)

        btn_salva = QPushButton("Salva")
        btn_salva.clicked.connect(self.salva)
        layout.addWidget(btn_salva)

    def salva(self):
        vecchia = self.vecchia_input.text()
        nuova = self.nuova_input.text()
        conferma = self.conferma_input.text()

        if not vecchia or not nuova or not conferma:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi.")
            return

        if nuova != conferma:
            QMessageBox.warning(self, "Errore", "Le password non coincidono.")
            return

        if len(nuova) < 6:
            QMessageBox.warning(self, "Errore", "La password deve avere almeno 6 caratteri.")
            return

        successo = self.gestore_profilo.cambia_password_utente(
            self.email_utente,
            vecchia,
            nuova
        )

        if successo:
            QMessageBox.information(self, "Successo", "Password cambiata correttamente.")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "La vecchia password non è corretta.")


class FinestraRecuperoPassword(QDialog):
    """Richiesta di una password temporanea (CDU8)."""
    def __init__(self, gestore_login, parent=None):
        super().__init__(parent)

        self.gestore_login = gestore_login

        self.setWindowTitle("Recupero Password")
        self.setFixedSize(420, 260)
        self.setStyleSheet("""
         QDialog { background-color: #e8f5e9; }
         QLabel {
         color: black !important;
         font-size: 14px;}
         QLineEdit {
         color: black !important;
         background-color: white !important;
         border: 1px solid #888;
         padding: 6px;
         border-radius: 6px;}
         QPushButton {
         color: black !important;
         background-color: #dcdcdc !important;
         border: 1px solid #555;
         padding: 8px;
         border-radius: 6px;
         font-weight: bold;}
         QPushButton:hover {
         background-color: #c8c8c8 !important;}""")


        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("🔑 Recupero Password")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 20px; font-weight: bold; color: #222;")
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        layout.addWidget(QLabel("Inserisci la tua email:"))
        self.input_email = QLineEdit()
        layout.addWidget(self.input_email)

        btn = QPushButton("Invia nuova password")
        btn.clicked.connect(self.invia)
        layout.addWidget(btn)

    def invia(self):
        email = self.input_email.text()

        if not email:
            QMessageBox.warning(self, "Errore", "Inserisci un'email.")
            return

        successo = self.gestore_login.recupera_password(email)

        if successo:
            QMessageBox.information(self, "Successo", "Una nuova password è stata inviata alla tua email.")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "Email non trovata.")



class FinestraModificaPagamento(QDialog):
    """Modulo completo per cambiare il numero della carta (CDU16)."""
    def __init__(self, email_utente, gestore_profilo, parent=None):
        super().__init__(parent)

        self.email_utente = email_utente
        self.gestore_profilo = gestore_profilo

        self.setWindowTitle("Modifica Carta")
        self.setFixedSize(420, 320)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("💳 Modifica Carta")
        titolo.setStyleSheet("font-size: 20px; font-weight: bold; color: #222;")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        # Vecchia carta
        layout.addWidget(QLabel("Vecchio numero carta:"))
        self.vecchia_input = QLineEdit()
        self.vecchia_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.vecchia_input)

        # Nuova carta
        layout.addWidget(QLabel("Nuovo numero carta:"))
        self.nuova_input = QLineEdit()
        self.nuova_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.nuova_input)

        # Conferma
        layout.addWidget(QLabel("Conferma nuovo numero:"))
        self.conferma_input = QLineEdit()
        self.conferma_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.conferma_input)

        btn_salva = QPushButton("Salva")
        btn_salva.clicked.connect(self.salva)
        layout.addWidget(btn_salva)

    def salva(self):
        vecchia = self.vecchia_input.text()
        nuova = self.nuova_input.text()
        conferma = self.conferma_input.text()

        if not vecchia or not nuova or not conferma:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi.")
            return

        if nuova != conferma:
            QMessageBox.warning(self, "Errore", "I numeri non coincidono.")
            return

        if len(nuova) < 12:
            QMessageBox.warning(self, "Errore", "Il numero carta deve avere almeno 12 cifre.")
            return

        successo = self.gestore_profilo.cambia_carta_utente(
            self.email_utente,
            vecchia,
            nuova
        )

        if successo:
            QMessageBox.information(self, "Successo", "Carta aggiornata correttamente.")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "Il vecchio numero carta non è corretto.")


class FinestraRicerca(QDialog):
    """Visualizza i risultati della ricerca globale (CDU4)."""
    def __init__(self, testo, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Risultati per: {testo}")
        self.setFixedSize(400, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Risultati trovati per '{testo}':"))
        layout.addStretch()
        
class FinestraRegistrazione(QDialog):
    def __init__(self, gestore_login, parent=None):
        super().__init__(parent)

        self.gestore_login = gestore_login

        self.setWindowTitle("Crea un nuovo account")
        self.setFixedSize(420, 380)
        self.setStyleSheet("""
         QDialog { background-color: #e8f5e9; }

         QLineEdit {
          color: black;
          background-color: white;
         border: 1px solid #888;
         padding: 6px;
         border-radius: 6px;}

         QPushButton {
         color: black;
         background-color: #dcdcdc;
         border: 1px solid #555;
         padding: 8px;
         border-radius: 6px;
         font-weight: bold;}

         QPushButton:hover {
         background-color: #c8c8c8;}""")


        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("📝 Registrazione")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 20px; font-weight: bold; color: #222;")
        layout.addWidget(titolo)

        # Campi
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome")
        layout.addWidget(self.input_nome)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")
        layout.addWidget(self.input_email)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_password)

        btn_registra = QPushButton("Crea account")
        btn_registra.clicked.connect(self.registra)
        layout.addWidget(btn_registra)


    def registra(self):
        nome = self.input_nome.text()
        email = self.input_email.text()
        password = self.input_password.text()

        if not nome or not email or not password:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi.")
            return

        successo = self.gestore_login.registra_utente(nome, email, password)

        if successo:
            QMessageBox.information(self, "Successo", "Account creato!")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "Email già registrata.")
class FinestraAcquisto(QDialog):
    """Schermata completa per acquistare un abbonamento (CDU15)."""
    def __init__(self, gestore_abbonamenti, parent=None):
        super().__init__(parent)

        self.gestore_abbonamenti = gestore_abbonamenti

        self.setWindowTitle("Acquista Abbonamento")
        self.setFixedSize(450, 420)
        self.setStyleSheet("""
            QDialog { background-color: #e8f5e9; }

            QLabel {
                color: black;
                font-size: 15px;
            }

            QLineEdit {
                color: black;
                background-color: white;
                border: 1px solid #888;
                padding: 6px;
                border-radius: 6px;
            }

            QPushButton {
                color: black;
                background-color: #dcdcdc;
                border: 1px solid #555;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #c8c8c8;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Titolo
        titolo = QLabel("🛒 Acquista Abbonamento")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(titolo)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        # Scelta piano
        layout.addWidget(QLabel("Seleziona il piano:"))

        self.btn_mensile = QPushButton("Mensile - 9,99€")
        self.btn_annuale = QPushButton("Annuale - 79,99€")

        self.btn_mensile.clicked.connect(lambda: self.seleziona_piano("mensile"))
        self.btn_annuale.clicked.connect(lambda: self.seleziona_piano("annuale"))

        layout.addWidget(self.btn_mensile)
        layout.addWidget(self.btn_annuale)

        # Metodo di pagamento
        layout.addWidget(QLabel("Metodo di pagamento registrato:"))

        carta = self.gestore_abbonamenti.repoDatiPagamento.ottieni_numero_carta(
            self.gestore_abbonamenti.email
        )

        if carta:
            carta_mascherata = "**** **** **** " + carta[-4:]
        else:
            carta_mascherata = "Nessuna carta registrata"

        self.label_carta = QLabel(carta_mascherata)
        layout.addWidget(self.label_carta)

        # Pulsante conferma
        self.btn_conferma = QPushButton("Conferma acquisto")
        self.btn_conferma.clicked.connect(self.conferma_acquisto)
        layout.addWidget(self.btn_conferma)

        self.piano_scelto = None

    def seleziona_piano(self, piano):
        self.piano_scelto = piano
        QMessageBox.information(self, "Piano selezionato", f"Hai scelto il piano {piano}.")

    def conferma_acquisto(self):
        if not self.piano_scelto:
            QMessageBox.warning(self, "Errore", "Seleziona un piano prima di continuare.")
            return

        abbonamento = Abbonamento( email_utente=self.gestore_abbonamenti.email,
                                   piattaforma=self.gestore_abbonamenti._piattaforma.get_nome(),
                                   piano=self.piano_scelto)
        successo= self.gestore_abbonamenti.acquista_abbonamento(abbonamento)
        if successo:
            QMessageBox.information(self, "Successo", "Abbonamento acquistato correttamente!")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "Impossibile completare l'acquisto.")
