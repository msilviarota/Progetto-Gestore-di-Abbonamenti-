import os
import sys
import webbrowser
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox,QFrame,QHBoxLayout,QScrollArea,QWidget
from PyQt6.QtCore import Qt, QSize
from models.piattaforma import CATALOGO_PIATTAFORME
# Configurazione del path per permettere l'importazione dei moduli del progetto
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.dirname(cartella_corrente)
if radice_progetto not in sys.path:
    sys.path.insert(0, radice_progetto)

from intefaccia.stile import *
from intefaccia.utils import scarica_logo
from models.abbonamento import Abbonamento
class SchedaCategoria(QDialog):
    """Mostra le piattaforme di una categoria, permette l'avvio (CDU18) e l'acquisto (CDU1)."""
    def __init__(self, titolo, servizi, email_utente, gestore_abbonamenti, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titolo)
        self.setMinimumSize(400, 500)
        self.setStyleSheet(STILE_SCHEDA_CATEGORIA)
        self.gestore_abbonamenti = gestore_abbonamenti

        layout = QVBoxLayout(self)
        for nome, piattaforma in servizi.items():
            riga = QHBoxLayout()

            btn = QPushButton(nome.capitalize())
            icona = scarica_logo(piattaforma.logo)
            if icona:
                btn.setIcon(icona)
                btn.setIconSize(QSize(100, 30))
            btn.clicked.connect(lambda ch, p=piattaforma: webbrowser.open(p.link_login))
            riga.addWidget(btn)

            btn_acquista = QPushButton("🛒 Acquista")
            btn_acquista.clicked.connect(lambda ch, p=piattaforma: self.apri_acquisto(p))
            riga.addWidget(btn_acquista)

            layout.addLayout(riga)

    def apri_acquisto(self, piattaforma):
        if not self.gestore_abbonamenti:
            QMessageBox.warning(self, "Errore", "Servizio abbonamenti non disponibile.")
            return
        self.gestore_abbonamenti._piattaforma = piattaforma
        finestra = FinestraAcquisto(self.gestore_abbonamenti, self)
        finestra.exec()
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
    def __init__(self, testo, finestra_principale, parent=None):
        super().__init__(parent)

        self.testo = testo
        self.finestra_principale = finestra_principale

        self.setWindowTitle(f"Risultati per: {testo}")
        self.setFixedSize(520, 650)
        self.setStyleSheet("""
            QDialog {
                background-color: #F2F7FF;
            }
            QLabel#titolo {
                font-size: 22px;
                font-weight: bold;
                color: #1A3E73;
            }
            QFrame#card {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #D0D7E2;
            }
            QFrame#card:hover {
                border: 1px solid #4A90E2;
                background-color: #F7FAFF;
            }
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border-radius: 8px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QScrollArea {
                background-color: white;
            }

            QWidget {
                background-color: white;
                }

        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        titolo = QLabel(f"Risultati trovati per '{testo}':")
        titolo.setObjectName("titolo")
        layout.addWidget(titolo)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        contenitore = QWidget()
        layout_scroll = QVBoxLayout(contenitore)
        layout_scroll.setSpacing(15)

        risultati = self.esegui_ricerca_globale(testo)

        if not risultati:
            nessuno = QLabel("Nessun risultato trovato.")
            nessuno.setStyleSheet("font-size: 16px; color: #444;")
            layout_scroll.addWidget(nessuno)
        else:
            for r in risultati:
                card = QFrame()
                card.setObjectName("card")
                card_layout = QHBoxLayout(card)
                card_layout.setContentsMargins(15, 15, 15, 15)
                card_layout.setSpacing(15)

                # Icona piattaforma
                icona = QLabel()
                icona.setPixmap(
                    QPixmap(r["logo"]).scaled(
                      60,
                     60,
                     Qt.AspectRatioMode.KeepAspectRatio,
                     Qt.TransformationMode.SmoothTransformation ))

                card_layout.addWidget(icona)

                # Testo
                testo_box = QVBoxLayout()
                titolo_lbl = QLabel(f"{r['titolo']}")
                titolo_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #1A3E73;")
                testo_box.addWidget(titolo_lbl)

                categoria_lbl = QLabel(f"Categoria: {r['categoria']}")
                categoria_lbl.setStyleSheet("font-size: 14px; color: #555;")
                testo_box.addWidget(categoria_lbl)

                card_layout.addLayout(testo_box)

                # Pulsante apri
                btn = QPushButton("Apri")
                btn.clicked.connect(lambda ch, link=r["link"]: webbrowser.open(link))
                card_layout.addWidget(btn)

                layout_scroll.addWidget(card)

        scroll.setWidget(contenitore)
        layout.addWidget(scroll)
    def esegui_ricerca_globale(self, testo):
        testo = testo.lower()
        risultati = []

        for piattaforma in CATALOGO_PIATTAFORME.values():

         # 1. Cerca per categoria
            if testo in piattaforma.categoria.lower():
                risultati.append({
                "titolo": piattaforma.nome,
                "piattaforma": piattaforma.nome,
                "link": piattaforma.link_login,
                "logo": piattaforma.logo,
                "categoria": piattaforma.categoria
            })
                continue

         # 2. Cerca per nome piattaforma
            if testo in piattaforma.nome.lower():
                risultati.append({
                "titolo": piattaforma.nome,
                "piattaforma": piattaforma.nome,
                "link": piattaforma.link_login,
                "logo": piattaforma.logo,
                "categoria": piattaforma.categoria
            })

        return risultati


    def carica_consigli(self):
        preferenze = self.gestore_preferenze.ottieni_preferenze(self.email_utente)
        if not preferenze:
            return []

        risultati = []
        for piattaforma in CATALOGO_PIATTAFORME.values():
            if piattaforma.categoria in [p.replace("🎵 ", "").replace("🎬 ", "").replace("📚 ", "").replace("📡 ", "").replace("⚽ ", "") for p in preferenze]:
                risultati.append(piattaforma)

        return risultati


        
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
class FinestraScaduti(QDialog):
    """Mostra gli abbonamenti scaduti e permette di rimuoverli (CDU14)."""
    def __init__(self, gestore_abbonamenti, parent=None):
        super().__init__(parent)
        self.gestore_abbonamenti = gestore_abbonamenti

        self.setWindowTitle("Abbonamenti Scaduti")
        self.setFixedSize(450, 450)
        self.setStyleSheet("""
            QDialog { background-color: #e8f5e9; }
            QLabel { color: black; font-size: 14px; }
            QPushButton {
                color: black;
                background-color: #dcdcdc;
                border: 1px solid #555;
                padding: 6px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c8c8c8; }
        """)

        layout_principale = QVBoxLayout(self)
        layout_principale.setContentsMargins(20, 20, 20, 20)
        layout_principale.setSpacing(12)

        titolo = QLabel("⏰ Abbonamenti Scaduti")
        titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout_principale.addWidget(sep)
        self.area_scroll = QScrollArea()
        self.area_scroll.setWidgetResizable(True)
        self.area_scroll.setStyleSheet("QScrollArea { border: none; background-color: #e8f5e9; }")

        self.contenitore = QWidget()
        self.contenitore.setStyleSheet("background-color: #e8f5e9;")
        self.layout_lista = QVBoxLayout(self.contenitore)
        self.area_scroll.setWidget(self.contenitore)
        layout_principale.addWidget(self.area_scroll)

        self.carica_scaduti()

    def carica_scaduti(self):
        while self.layout_lista.count():
            item = self.layout_lista.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not self.gestore_abbonamenti:
            self.layout_lista.addWidget(QLabel("Servizio abbonamenti non disponibile."))
            return

        scaduti = self.gestore_abbonamenti.ottieni_scaduti()

        if not scaduti:
            self.layout_lista.addWidget(QLabel("Nessun abbonamento scaduto al momento."))
            return

        for abb in scaduti:
            riga = QFrame()
            riga.setStyleSheet("background-color: white; border-radius: 8px; padding: 8px;")
            riga_layout = QHBoxLayout(riga)

            testo = QLabel(f"{abb['piattaforma'].capitalize()}\nScaduto il {abb['data_scadenza']}")
            riga_layout.addWidget(testo)

            btn_rimuovi = QPushButton("🗑️ Rimuovi")
            btn_rimuovi.clicked.connect(lambda ch, id_abb=abb["id_abbonamento"]: self.rimuovi(id_abb))
            riga_layout.addWidget(btn_rimuovi)

            self.layout_lista.addWidget(riga)

    def rimuovi(self, id_abbonamento):
        successo = self.gestore_abbonamenti.elimina_scaduto(id_abbonamento)
        if successo:
            QMessageBox.information(self, "Rimosso", "Abbonamento rimosso dalla cronologia.")
            self.carica_scaduti()
        else:
            QMessageBox.warning(self, "Errore", "Impossibile rimuovere l'abbonamento.")

class FinestraAbbonamenti(QDialog):
    """Mostra tutti gli abbonamenti dell'utente, attivi e scaduti, e permette la disdetta (CDU13, CDU2)."""
    def __init__(self, gestore_abbonamenti, parent=None):
        super().__init__(parent)
        self.gestore_abbonamenti = gestore_abbonamenti

        self.setWindowTitle("I miei Abbonamenti")
        self.setFixedSize(450, 450)
        self.setStyleSheet("""
            QDialog { background-color: #e8f5e9; }
            QLabel { color: black; font-size: 14px; }
            QPushButton {
                color: black;
                background-color: #dcdcdc;
                border: 1px solid #555;
                padding: 6px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c8c8c8; }
        """)

        layout_principale = QVBoxLayout(self)
        layout_principale.setContentsMargins(20, 20, 20, 20)
        layout_principale.setSpacing(12)

        titolo = QLabel("📋 I miei Abbonamenti")
        titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principale.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout_principale.addWidget(sep)

        self.area_scroll = QScrollArea()
        self.area_scroll.setWidgetResizable(True)
        self.area_scroll.setStyleSheet("QScrollArea { border: none; background-color: #e8f5e9; }")

        self.contenitore = QWidget()
        self.contenitore.setStyleSheet("background-color: #e8f5e9;")
        self.layout_lista = QVBoxLayout(self.contenitore)
        self.area_scroll.setWidget(self.contenitore)
        layout_principale.addWidget(self.area_scroll)

        self.carica_abbonamenti()

    def carica_abbonamenti(self):
        while self.layout_lista.count():
            item = self.layout_lista.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not self.gestore_abbonamenti:
            self.layout_lista.addWidget(QLabel("Servizio abbonamenti non disponibile."))
            return

        abbonamenti = self.gestore_abbonamenti.ottieni_tutti()

        if not abbonamenti:
            self.layout_lista.addWidget(QLabel("Non hai ancora nessun abbonamento."))
            return

        for abb in abbonamenti:
            riga = QFrame()
            riga.setStyleSheet("background-color: white; border-radius: 8px; padding: 8px;")
            riga_layout = QHBoxLayout(riga)

            testo = QLabel(
                f"{abb['piattaforma'].capitalize()}  —  {abb['stato']}\n"
                f"Scadenza: {abb['data_scadenza']}"
            )
            riga_layout.addWidget(testo)

            if abb["stato"] == "Attivo":
                btn_disdici = QPushButton("Disdici")
                btn_disdici.clicked.connect(lambda ch, id_abb=abb["id_abbonamento"]: self.disdici(id_abb))
                riga_layout.addWidget(btn_disdici)

            self.layout_lista.addWidget(riga)

    def disdici(self, id_abbonamento):
        successo = self.gestore_abbonamenti.disdisci_abbonamento(id_abbonamento)
        if successo:
            QMessageBox.information(self, "Disdetto", "Rinnovo automatico interrotto.")
            self.carica_abbonamenti()
        else:
            QMessageBox.warning(self, "Errore", "Impossibile disdire l'abbonamento.")

class FinestraPrestitoAbbonamento(QDialog):
    """Permette di prestare un abbonamento a un amico (CDU11)."""
    def __init__(self, gestore_abbonamenti, parent=None):
        super().__init__(parent)

        self.gestore_abbonamenti = gestore_abbonamenti

        self.setWindowTitle("Presta Abbonamento")
        self.setFixedSize(420, 350)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("🤝 Presta un abbonamento")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 20px; font-weight: bold; color: #222;")
        layout.addWidget(titolo)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        # Lista abbonamenti attivi
        layout.addWidget(QLabel("Seleziona un abbonamento da prestare:"))

        self.lista_abbonamenti = self.gestore_abbonamenti._repo_Abbonamento.ottieni_per_utente(
            self.gestore_abbonamenti.email
        )

        if not self.lista_abbonamenti:
            layout.addWidget(QLabel("Nessun abbonamento attivo."))
            return

        self.btns = []
        for abb in self.lista_abbonamenti:
            btn = QPushButton(f"{abb._piattaforma} ({abb._piano})")
            btn.clicked.connect(lambda ch, a=abb: self.seleziona_abbonamento(a))
            layout.addWidget(btn)
            self.btns.append(btn)

        # Campo email amico
        layout.addWidget(QLabel("Email dell'amico:"))
        self.input_email = QLineEdit()
        layout.addWidget(self.input_email)

        # Pulsante conferma
        self.btn_conferma = QPushButton("Condividi accesso")
        self.btn_conferma.clicked.connect(self.conferma)
        layout.addWidget(self.btn_conferma)

        self.abbonamento_scelto = None

    def seleziona_abbonamento(self, abb):
        self.abbonamento_scelto = abb
        QMessageBox.information(self, "Selezionato", f"Hai scelto {abb._piattaforma}.")

    def conferma(self):
        if not self.abbonamento_scelto:
            QMessageBox.warning(self, "Errore", "Seleziona un abbonamento.")
            return

        email_amico = self.input_email.text()
        if not email_amico:
            QMessageBox.warning(self, "Errore", "Inserisci l'email dell'amico.")
            return

        successo = self.gestore_abbonamenti.presta_abbonamento(
            self.abbonamento_scelto._id_abbonamento,
            email_amico
        )

        if successo:
            QMessageBox.information(self, "Successo", "Accesso condiviso correttamente!")
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "Impossibile prestare l'abbonamento.")
