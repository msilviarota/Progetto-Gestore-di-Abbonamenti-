from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QDialog, QLineEdit,
    QFrame, QMessageBox, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt
from Service.gestoreAbbonamenti import GestoreAbbonamenti
from repository.repositoryAbbonamento import RepositoryAbbonamento
from repository.repositoryDatiPagamento import RepositoryDatiPagamento
from repository.repositoryUtente import RepositoryUtente
from Service.gestorePrestiti import GestorePrestiti
from repository.repositoryLog import RepositoryLog
from models.piattaforma import Piattaforma
from models.notifica import Notifica

from stile import (
    STILE_BTN_ESCI, STILE_BTN_CHIUDI, STILE_TITOLO_PROFILO, STILE_COMBO
)


class FinestraAbbonamenti(QDialog):
    def __init__(self, parent=None, email="",gestore_abbonamenti=None):
        super().__init__(parent)
        self.email_utente=email
        self.gestore = gestore_abbonamenti
        self.setWindowTitle("I miei Abbonamenti")
        self.setFixedSize(450, 400)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("📋 I miei Abbonamenti")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        abbonamenti = [
            ("Netflix", "Mensile", "Scade: 01/07/2026"),
            ("Spotify", "Annuale", "Scade: 15/12/2026"),
            ("Disney+", "Mensile", "Scade: 10/07/2026"),
        ]

        for nome, piano, scadenza in abbonamenti:
            riga = QHBoxLayout()
            lbl = QLabel(f"{nome}  —  {piano}  —  {scadenza}")
            lbl.setStyleSheet("font-size: 13px; color: #222222;")
            riga.addWidget(lbl)

            btn_disdici = QPushButton("Disdici")
            btn_disdici.setFixedHeight(30)
            btn_disdici.setStyleSheet(STILE_BTN_ESCI)
            btn_disdici.clicked.connect(lambda checked, n=nome: self.disdici(n))
            riga.addWidget(btn_disdici)
            layout.addLayout(riga)

        layout.addStretch()

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setFixedHeight(38)
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
        layout.addWidget(btn_chiudi, alignment=Qt.AlignmentFlag.AlignCenter)

    def disdici(self, nome):
        risposta = QMessageBox.question(...)
        if risposta == QMessageBox.StandardButton.Yes:
            self.gestore.eseguiDisdetta(nome)
            QMessageBox.information(self, "Disdetto",f"{nome} disdetto!")

       
class FinestraPresta(QDialog):
    def __init__(self, parent=None, email_utente="", gestore_prestiti=None):
        super().__init__(parent)
        self.email_utente_corrente = email_utente
        self.gestore = gestore_prestiti
        self.setWindowTitle("Presta Abbonamento")
        self.setFixedSize(400, 300)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("🤝 Presta Abbonamento")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        layout.addWidget(QLabel("Seleziona abbonamento da prestare:"))
        self.combo = QComboBox()
        self.combo.addItems(["Netflix", "Spotify", "Disney+"])
        self.combo.setFixedHeight(36)
        self.combo.setStyleSheet(STILE_COMBO)
        layout.addWidget(self.combo)

        riga_email = QHBoxLayout()
        label_email = QLabel("Email amico:")
        label_email.setFixedWidth(110)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Es. amico@email.com")
        self.email_input.setFixedHeight(36)
        riga_email.addWidget(label_email)
        riga_email.addWidget(self.email_input)
        layout.addLayout(riga_email)

        btn_presta = QPushButton("Presta")
        btn_presta.setFixedHeight(38)
        btn_presta.setStyleSheet(STILE_BTN_CHIUDI)
        btn_presta.clicked.connect(self.presta)
        layout.addWidget(btn_presta)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setFixedHeight(38)
        btn_annulla.setStyleSheet(STILE_BTN_ESCI)
        btn_annulla.clicked.connect(self.close)
        layout.addWidget(btn_annulla)

    def presta(self):
        nome_piattaforma = self.combo.currentText()
        email_amico = self.email_input.text().strip()

        if not email_amico:
            QMessageBox.warning(self, "Errore", "Inserisci l'email dell'amico!")
            return

        # LA MODIFICA: Passa il nome della piattaforma (stringa) al gestore.
        # È compito del GestorePrestiti trovare l'ID corrispondente.
        risultato = self.gestore.avvia_prestito(email_amico, nome_piattaforma)
        
        if risultato:
            QMessageBox.information(self, "Inviato", f"{nome_piattaforma} prestato a {email_amico}!")
            self.close()
        else:
            QMessageBox.critical(self, "Errore", "Impossibile prestare l'abbonamento.\nL'amico deve avere un account registrato!")
class FinestraAcquista(QDialog):
    def __init__(self, parent=None, email="", gestore_abbonamenti=None):
        super().__init__(parent)
        self.gestore = gestore_abbonamenti
        self.email_utente = email
        self.setWindowTitle("Acquista Abbonamento")
        self.setFixedSize(450, 520)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("Acquista Abbonamento")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        layout.addWidget(QLabel("Seleziona piattaforma:"))
        self.combo_piattaforma = QComboBox()
        self.combo_piattaforma.addItems([
            "Netflix", "Disney+", "Spotify", "Apple Music",
            "Amazon Music", "Prime Video", "RaiPlay",
            "Mediaset Infinity", "Kobo", "Kindle",
            "YouTube", "Sky Sport", "Now TV"
        ])
        self.combo_piattaforma.setFixedHeight(36)
        self.combo_piattaforma.setStyleSheet(STILE_COMBO)
        layout.addWidget(self.combo_piattaforma)

        layout.addWidget(QLabel("Seleziona piano:"))
        self.combo_piano = QComboBox()
        self.combo_piano.addItems(["Mensile", "Stagionale", "Annuale"])
        self.combo_piano.setFixedHeight(36)
        self.combo_piano.setStyleSheet(STILE_COMBO)
        layout.addWidget(self.combo_piano)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep2)

        layout.addWidget(QLabel("Dati di pagamento:"))

        riga_carta = QHBoxLayout()
        label_carta = QLabel("N° Carta:")
        label_carta.setFixedWidth(100)
        self.carta_input = QLineEdit()
        self.carta_input.setPlaceholderText("Es. 1234 5678 9012 3456")
        self.carta_input.setFixedHeight(36)
        riga_carta.addWidget(label_carta)
        riga_carta.addWidget(self.carta_input)
        layout.addLayout(riga_carta)

        riga_scadenza = QHBoxLayout()
        label_scadenza = QLabel("Scadenza:")
        label_scadenza.setFixedWidth(100)
        self.scadenza_input = QLineEdit()
        self.scadenza_input.setPlaceholderText("MM/AA")
        self.scadenza_input.setFixedHeight(36)
        riga_scadenza.addWidget(label_scadenza)
        riga_scadenza.addWidget(self.scadenza_input)
        layout.addLayout(riga_scadenza)

        riga_titolare = QHBoxLayout()
        label_titolare = QLabel("Titolare:")
        label_titolare.setFixedWidth(100)
        self.titolare_input = QLineEdit()
        self.titolare_input.setPlaceholderText("Es. Silvia Rota")
        self.titolare_input.setFixedHeight(36)
        riga_titolare.addWidget(label_titolare)
        riga_titolare.addWidget(self.titolare_input)
        layout.addLayout(riga_titolare)

        riga_cvv = QHBoxLayout()
        label_cvv = QLabel("CVV:")
        label_cvv.setFixedWidth(100)
        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("Es. 123")
        self.cvv_input.setFixedHeight(36)
        self.cvv_input.setMaxLength(3)
        riga_cvv.addWidget(label_cvv)
        riga_cvv.addWidget(self.cvv_input)
        layout.addLayout(riga_cvv)

        btn_acquista = QPushButton("Conferma acquisto")
        btn_acquista.setFixedHeight(40)
        btn_acquista.setStyleSheet(STILE_BTN_CHIUDI)
        btn_acquista.clicked.connect(self.conferma_acquisto)
        layout.addWidget(btn_acquista)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setFixedHeight(40)
        btn_annulla.setStyleSheet(STILE_BTN_ESCI)
        btn_annulla.clicked.connect(self.close)
        layout.addWidget(btn_annulla)

    def conferma_acquisto(self):
        piattaforma = self.combo_piattaforma.currentText()
        piano = self.combo_piano.currentText()
        carta = self.carta_input.text()
        scadenza = self.scadenza_input.text()
        titolare = self.titolare_input.text()
        cvv = self.cvv_input.text()

        if not carta or not scadenza or not titolare or not cvv:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi!")
            return
        
        repo_utente = RepositoryUtente()
        utente= repo_utente.getInformazioni(self.email_utente)
        repo_abb = RepositoryAbbonamento()
        repo_pag = RepositoryDatiPagamento()
        piattaforma_obj = Piattaforma()
        notifica_obj = Notifica()
        gestore = GestoreAbbonamenti (utente, repo_abb, repo_pag ,piattaforma_obj, notifica_obj)
        esito_notifica = gestore.inviaScelta (f"{piattaforma}-{piano}")
        QMessageBox.information(self, "Successo", f"Abbonamento {piano} a {piattaforma} acquistato con successo!")
        self.close()


class FinestraScaduti(QDialog):
    def __init__(self, parent=None, email="", gestore_abbonamenti=None):
        super().__init__(parent)
        self.gestore = gestore_abbonamenti
        self.email_utente = email
        self.setWindowTitle("Abbonamenti Scaduti")
        self.setFixedSize(500, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("⏰ Abbonamenti Scaduti")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        self.abbonamenti = [
            ("Netflix", "Scaduto il 01/05/2026"),
            ("Spotify", "Scaduto il 15/04/2026"),
            ("Disney+", "Scaduto il 10/03/2026"),
        ]

        for nome, data in self.abbonamenti:
            riga = QHBoxLayout()

            lbl = QLabel(f"{nome}  —  {data}")
            lbl.setStyleSheet("font-size: 13px; color: #222222;")
            riga.addWidget(lbl)

            btn_rinnova = QPushButton("Rinnova")
            btn_rinnova.setFixedHeight(30)
            btn_rinnova.setStyleSheet(STILE_BTN_CHIUDI)
            btn_rinnova.clicked.connect(lambda checked, n=nome: self.rinnova(n))
            riga.addWidget(btn_rinnova)

            btn_elimina = QPushButton("Elimina")
            btn_elimina.setFixedHeight(30)
            btn_elimina.setStyleSheet(STILE_BTN_ESCI)
            btn_elimina.clicked.connect(lambda checked, n=nome: self.elimina(n))
            riga.addWidget(btn_elimina)

            layout.addLayout(riga)

        layout.addStretch()

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setFixedHeight(40)
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
       
        repo_utente = RepositoryUtente()
        utente_obj = repo_utente.getInformazioni(self.email_utente)
        
        if not utente_obj:
            from models.utente import Utente
            utente_obj = Utente(email=self.email_utente)

        gestore_scadenze = GestoreAbbonamenti(
            utente_obj, 
            RepositoryAbbonamento(), 
            RepositoryDatiPagamento(), 
            Piattaforma(), 
            Notifica()
        )
        
        esito_scadenza = gestore_scadenze.ricordaScadenza()
        if esito_scadenza:
            QMessageBox.warning(self, "Controllo Scadenze", esito_scadenza)
        
        layout.addWidget(btn_chiudi, alignment=Qt.AlignmentFlag.AlignCenter)

    def rinnova(self, nome):
        risposta = QMessageBox.question(
            self, "Rinnova",
            f"Vuoi rinnovare {nome}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if risposta == QMessageBox.StandardButton.Yes:
        
            repo_utente = RepositoryUtente()
            utente_obj = repo_utente.getInformazioni(self.email_utente)
            if not utente_obj:
                from models.utente import Utente
                utente_obj = Utente(email=self.email_utente)

            gestore = GestoreAbbonamenti(
                utente_obj, 
                RepositoryAbbonamento(), 
                RepositoryDatiPagamento(), 
                Piattaforma(), 
                Notifica()
            )

            # Creiamo il dizionario fittizio con i dati dell'abbonamento da passare alla funzione
            abbonamento_da_rinnovare = {
                "nome": utente_obj.get_nome() if hasattr(utente_obj, 'get_nome') else "Utente",
                "cognome": utente_obj.get_cognome() if hasattr(utente_obj, 'get_cognome') else "Registrato",
                "piattaforma": nome
            }

            # Lanciamo il rinnovo sul backend
            gestore.avviaProceduraRinnovo(abbonamento_da_rinnovare)

            QMessageBox.information(self, "Rinnovato", f"{nome} rinnovato con successo nel sistema!")

    def elimina(self, nome):
        risposta = QMessageBox.question(
            self, "Conferma",
            f"Vuoi eliminare {nome} dagli scaduti?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if risposta == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Eliminato", f"{nome} eliminato!")