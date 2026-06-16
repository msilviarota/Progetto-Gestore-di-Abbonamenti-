from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QDialog, QLineEdit,
    QFrame, QMessageBox, QComboBox, QScrollArea
)
from PyQt6.QtCore import Qt

from stile import (
    STILE_DIALOGO_PROFILO, STILE_BTN_SERVIZIO, STILE_BTN_ESCI,
    STILE_BTN_CHIUDI, STILE_LABEL_PROFILO, STILE_TITOLO_PROFILO, STILE_COMBO
)


class FinestraCambiaPassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cambia Password")
        self.setFixedSize(400, 300)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("🔑 Cambia Password")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        riga_vecchia = QHBoxLayout()
        label_vecchia = QLabel("Vecchia:")
        label_vecchia.setFixedWidth(110)
        self.vecchia_input = QLineEdit()
        self.vecchia_input.setPlaceholderText("Vecchia password")
        self.vecchia_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.vecchia_input.setFixedHeight(36)
        riga_vecchia.addWidget(label_vecchia)
        riga_vecchia.addWidget(self.vecchia_input)
        layout.addLayout(riga_vecchia)

        riga_nuova = QHBoxLayout()
        label_nuova = QLabel("Nuova:")
        label_nuova.setFixedWidth(110)
        self.nuova_input = QLineEdit()
        self.nuova_input.setPlaceholderText("Nuova password")
        self.nuova_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.nuova_input.setFixedHeight(36)
        riga_nuova.addWidget(label_nuova)
        riga_nuova.addWidget(self.nuova_input)
        layout.addLayout(riga_nuova)

        riga_conferma = QHBoxLayout()
        label_conferma = QLabel("Conferma:")
        label_conferma.setFixedWidth(110)
        self.conferma_input = QLineEdit()
        self.conferma_input.setPlaceholderText("Ripeti nuova password")
        self.conferma_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.conferma_input.setFixedHeight(36)
        riga_conferma.addWidget(label_conferma)
        riga_conferma.addWidget(self.conferma_input)
        layout.addLayout(riga_conferma)

        btn_salva = QPushButton("Salva")
        btn_salva.setFixedHeight(38)
        btn_salva.setStyleSheet(STILE_BTN_CHIUDI)
        btn_salva.clicked.connect(self.salva)
        layout.addWidget(btn_salva)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setFixedHeight(38)
        btn_annulla.setStyleSheet(STILE_BTN_ESCI)
        btn_annulla.clicked.connect(self.close)
        layout.addWidget(btn_annulla)

    def salva(self):
        from Service.gestoreAccessi import GestoreAccessi 
        from database.repositoryUtente import RepositoryUtente 
        from database.repositoryAbbonamento import RepositoryAbbonamento 
        vecchia = self.vecchia_impurt.text()
        nuova= self.nuova_imput.text()
        conferma = self.conferma_input.text()
        if not vecchia or not nuova or not conferma :
            QMessageBox.warning(self, "Errore", "Compila tutti i campi!")
            return
        repo_utente = RepositoryUtente()
        repo_abbonamento = RepositoryAbbonamento()
        gestore = GestoreAccessi(repo_utente, repo_abbonamento)
        esito = gestore.richiestaCambioPassword(vecchia, nuova,conferma)
        if esito:
            QMessageBox.information(self,"Successo","Password cambiata con successo!")
            self.close()
        else:
            QMessageBox.warning(self,"Errore","Operazione non riuscita. Controlla i dati inseriti.")


class FinestraModificaPagamento(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifica Pagamento")
        self.setFixedSize(400, 350)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("💳 Modifica Pagamento")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        riga_carta = QHBoxLayout()
        label_carta = QLabel("N° Carta:")
        label_carta.setFixedWidth(110)
        self.carta_input = QLineEdit()
        self.carta_input.setPlaceholderText("Es. 1234 5678 9012 3456")
        self.carta_input.setFixedHeight(36)
        riga_carta.addWidget(label_carta)
        riga_carta.addWidget(self.carta_input)
        layout.addLayout(riga_carta)

        riga_scadenza = QHBoxLayout()
        label_scadenza = QLabel("Scadenza:")
        label_scadenza.setFixedWidth(110)
        self.scadenza_input = QLineEdit()
        self.scadenza_input.setPlaceholderText("MM/AA")
        self.scadenza_input.setFixedHeight(36)
        riga_scadenza.addWidget(label_scadenza)
        riga_scadenza.addWidget(self.scadenza_input)
        layout.addLayout(riga_scadenza)

        riga_titolare = QHBoxLayout()
        label_titolare = QLabel("Titolare:")
        label_titolare.setFixedWidth(110)
        self.titolare_input = QLineEdit()
        self.titolare_input.setPlaceholderText("Es. Silvia Rota")
        self.titolare_input.setFixedHeight(36)
        riga_titolare.addWidget(label_titolare)
        riga_titolare.addWidget(self.titolare_input)
        layout.addLayout(riga_titolare)

        riga_cvv = QHBoxLayout()
        label_cvv = QLabel("CVV:")
        label_cvv.setFixedWidth(110)
        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("Es. 123")
        self.cvv_input.setFixedHeight(36)
        self.cvv_input.setMaxLength(3)
        riga_cvv.addWidget(label_cvv)
        riga_cvv.addWidget(self.cvv_input)
        layout.addLayout(riga_cvv)

        btn_salva = QPushButton("Salva")
        btn_salva.setFixedHeight(38)
        btn_salva.setStyleSheet(STILE_BTN_CHIUDI)
        btn_salva.clicked.connect(self.salva)
        layout.addWidget(btn_salva)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setFixedHeight(38)
        btn_annulla.setStyleSheet(STILE_BTN_ESCI)
        btn_annulla.clicked.connect(self.close)
        layout.addWidget(btn_annulla)

    def salva(self):
        carta = self.carta_input.text()
        scadenza = self.scadenza_input.text()
        titolare = self.titolare_input.text()
        cvv = self.cvv_input.text()

        if not carta or not scadenza or not titolare or not cvv:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi!")
            return

        QMessageBox.information(self, "Salvato", "Dati di pagamento aggiornati!")
        self.close()


class ProfiloDialog(QDialog):
    def __init__(self, finestra_principale, parent=None):
        super().__init__(parent)
        self.finestra_principale = finestra_principale
        self.setWindowTitle("Il mio Account")
        self.setFixedSize(430, 600)
        self.setStyleSheet(STILE_DIALOGO_PROFILO)

        layout_esterno = QVBoxLayout(self)
        layout_esterno.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        contenuto = QWidget()
        layout = QVBoxLayout(contenuto)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        titolo = QLabel("Profilo Utente")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        from PyQt6.QtWidgets import QFormLayout
        form = QFormLayout()
        form.setSpacing(14)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        def crea_label(testo):
            l = QLabel(testo)
            l.setStyleSheet(STILE_LABEL_PROFILO)
            return l

        self.campo_nome = QLineEdit("Silvia Rota")
        self.campo_email = QLineEdit("silvia@email.com")
        self.campo_password = QLineEdit("ciao")
        self.campo_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.campo_piano = QLineEdit("Premium")
        self.campo_piano.setReadOnly(True)
        self.campo_pagamento = QLineEdit("Visa **** 1234")
        self.campo_assistenza = QLineEdit("assistenza@servizio.com")
        self.campo_assistenza.setReadOnly(True)

        form.addRow(crea_label("Nome:"), self.campo_nome)
        form.addRow(crea_label("Email:"), self.campo_email)
        form.addRow(crea_label("Password:"), self.campo_password)
        form.addRow(crea_label("Piano:"), self.campo_piano)
        form.addRow(crea_label("Pagamento:"), self.campo_pagamento)
        form.addRow(crea_label("Assistenza:"), self.campo_assistenza)
        layout.addLayout(form)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep2)

        btn_cambia_password = QPushButton("🔑 Cambia password")
        btn_cambia_password.setFixedHeight(38)
        btn_cambia_password.setStyleSheet(STILE_BTN_SERVIZIO)
        btn_cambia_password.clicked.connect(self.apri_cambia_password)
        layout.addWidget(btn_cambia_password)

        btn_abbonamenti = QPushButton("📋 I miei abbonamenti")
        btn_abbonamenti.setFixedHeight(38)
        btn_abbonamenti.setStyleSheet(STILE_BTN_SERVIZIO)
        btn_abbonamenti.clicked.connect(self.apri_abbonamenti)
        layout.addWidget(btn_abbonamenti)

        btn_presta = QPushButton("🤝 Presta abbonamento")
        btn_presta.setFixedHeight(38)
        btn_presta.setStyleSheet(STILE_BTN_SERVIZIO)
        btn_presta.clicked.connect(self.apri_presta)
        layout.addWidget(btn_presta)

        btn_pagamento = QPushButton("💳 Modifica pagamento")
        btn_pagamento.setFixedHeight(38)
        btn_pagamento.setStyleSheet(STILE_BTN_SERVIZIO)
        btn_pagamento.clicked.connect(self.apri_pagamento)
        layout.addWidget(btn_pagamento)

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.Shape.HLine)
        sep3.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep3)

        btn_esci = QPushButton("Esci")
        btn_esci.setStyleSheet(STILE_BTN_ESCI)
        btn_esci.clicked.connect(self.esci)
        layout.addWidget(btn_esci, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
        layout.addWidget(btn_chiudi, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll.setWidget(contenuto)
        layout_esterno.addWidget(scroll)

    def esci(self):
        self.close()
        self.finestra_principale.login_window.show()
        self.finestra_principale.close()

    def apri_cambia_password(self):
        finestra = FinestraCambiaPassword(self)
        finestra.exec()

    def apri_abbonamenti(self):
        from abbonamenti import FinestraAbbonamenti
        finestra = FinestraAbbonamenti(self)
        finestra.exec()

    def apri_presta(self):
        from abbonamenti import FinestraPresta
        finestra = FinestraPresta(self)
        finestra.exec()

    def apri_pagamento(self):
        finestra = FinestraModificaPagamento(self)
        finestra.exec()
