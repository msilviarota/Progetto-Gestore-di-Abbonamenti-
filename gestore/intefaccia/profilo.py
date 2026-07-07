from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QFormLayout, QFrame, QScrollArea, QWidget,QMessageBox
)
from PyQt6.QtCore import Qt

from intefaccia.stile import (
    STILE_DIALOGO_PROFILO, STILE_BTN_ESCI, STILE_BTN_CHIUDI,
    STILE_TITOLO_PROFILO, STILE_LABEL_PROFILO, STILE_BTN_SERVIZIO,STILE_SCROLL_TRASPARENTE,
    STILE_CONTENITORE_PROFILO
)
from intefaccia.dialoghi import FinestraCambiaPassword, FinestraModificaPagamento
from intefaccia.dialoghi import FinestraModificaPagamento
from intefaccia.dialoghi import FinestraAbbonamenti
from intefaccia.dialoghi import FinestraPrestitoAbbonamento

class ProfiloDialog(QDialog):
    """Hub per la gestione dell'account (CDU7, CDU9, CDU15, CDU16)."""

    def __init__(self, finestra_principale, parent=None):
        super().__init__(parent)
        self.finestra_principale = finestra_principale
        self.setWindowTitle("Il mio Account")
        self.setFixedSize(430, 650)
        self.setStyleSheet(STILE_DIALOGO_PROFILO)
        self._build_ui()

    def _build_ui(self):
        layout_esterno = QVBoxLayout(self)
        layout_esterno.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(STILE_SCROLL_TRASPARENTE)

        contenuto = QWidget()
        contenuto.setStyleSheet(STILE_CONTENITORE_PROFILO)
        layout = QVBoxLayout(contenuto)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        titolo = QLabel("Profilo Utente")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        form = QFormLayout()
        form.setSpacing(14)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        def crea_label(testo):
            l = QLabel(testo)
            l.setStyleSheet(STILE_LABEL_PROFILO)
            return l

        nome_utente = getattr(self.finestra_principale, "nome_utente", "Utente")
        email_utente = getattr(self.finestra_principale, "email_utente", "")

        self.campo_nome = QLineEdit(nome_utente)
        self.campo_nome.setReadOnly(True)

        self.campo_email = QLineEdit(email_utente)
        self.campo_email.setReadOnly(True)

        self.campo_password = QLineEdit("••••••••")
        self.campo_password.setReadOnly(True)
        self.campo_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.campo_piano = QLabel(self._ottieni_testo_piano())
        self.campo_piano.setStyleSheet(STILE_LABEL_PROFILO)
        self.campo_piano.setWordWrap(True)
        self.campo_pagamento = QLabel(self._ottieni_testo_pagamento(email_utente))

        form.addRow(crea_label("Nome:"), self.campo_nome)
        form.addRow(crea_label("Email:"), self.campo_email)
        form.addRow(crea_label("Password:"), self.campo_password)
        form.addRow(crea_label("Piano:"), self.campo_piano)
        form.addRow(crea_label("Pagamento:"), self.campo_pagamento)
        self.campo_credito = QLabel(self._ottieni_testo_credito(email_utente))
        form.addRow(crea_label("Credito:"), self.campo_credito)
        layout.addLayout(form)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
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
        btn_pagamento.clicked.connect(self.apri_modifica_pagamento)
        layout.addWidget(btn_pagamento)

        btn_credito = QPushButton("💰 Ricarica credito")
        btn_credito.setFixedHeight(38)
        btn_credito.setStyleSheet(STILE_BTN_SERVIZIO)
        btn_credito.clicked.connect(self.apri_ricarica_credito)
        layout.addWidget(btn_credito)

        sep3 = QFrame()
        sep3.setFrameShape(QFrame.Shape.HLine)
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
        """CDU15: Chiude la sessione e torna al login."""
        self.close()
        login_window = getattr(self.finestra_principale, "login_window", None)
        if login_window:
            login_window.show()
        self.finestra_principale.close()

    def apri_cambia_password(self):
     finestra = FinestraCambiaPassword(
      email_utente=self.campo_email.text(),
        gestore_profilo=self.finestra_principale.gestore_profilo,
        parent=self
    )
     finestra.exec()

    def apri_pagamento(self):
      FinestraModificaPagamento(
        email_utente=self.campo_email.text(),
        gestore_profilo=self.finestra_principale.gestore_profilo,
        parent=self
     ).exec()


    def apri_abbonamenti(self):
       
        gestore_abbonamenti = getattr(self.finestra_principale, "gestore_abbonamenti", None)
        finestra = FinestraAbbonamenti(gestore_abbonamenti, parent=self)
        finestra.exec()

    def apri_presta(self):
        gestore_abbonamenti = getattr(self.finestra_principale, "gestore_abbonamenti", None)
        finestra = FinestraPrestitoAbbonamento(gestore_abbonamenti, self)
        finestra.exec()


    def apri_modifica_pagamento(self):
        finestra = FinestraModificaPagamento(
            email_utente=self.campo_email.text(),
            gestore_profilo=self.finestra_principale.gestore_profilo,
            parent=self
        )
        finestra.exec()
        # Aggiorna subito il campo "Pagamento" con i nuovi dati, senza dover riaprire il profilo
        self.campo_pagamento.setText(self._ottieni_testo_pagamento(self.campo_email.text()))
   
    def apri_ricarica_credito(self):
        from intefaccia.dialoghi import FinestraRicaricaCredito
        gestore_portafoglio = getattr(self.finestra_principale, "gestore_portafoglio", None)
        finestra = FinestraRicaricaCredito(
            email_utente=self.campo_email.text(),
            gestore_portafoglio=gestore_portafoglio,
            parent=self
        )
        finestra.exec()
        # Aggiorna subito il saldo mostrato, dopo la ricarica
        self.campo_credito.setText(self._ottieni_testo_credito(self.campo_email.text()))
    
    def _ottieni_testo_pagamento(self, email_utente):
        """Recupera numero (mascherato) e tipo carta dal repository dati pagamento."""
        gestore_profilo = getattr(self.finestra_principale, "gestore_profilo", None)
        repo_pagamento = getattr(gestore_profilo, "_repo_DatiPagamento", None)

        if not repo_pagamento:
            return "Non ancora disponibile"

        dati = repo_pagamento.ottieni_per_utente(email_utente)
        numero = dati.get("numero_carta", "")
        tipo = dati.get("tipo_carta", "Sconosciuta")

        if not numero:
            return "Nessuna carta registrata"

        numero_mascherato = "**** **** **** " + numero[-4:]
        return f"{tipo}  {numero_mascherato}"
    def _ottieni_testo_credito(self, email_utente):
        """Recupera il saldo attuale dal gestore portafoglio."""
        gestore_portafoglio = getattr(self.finestra_principale, "gestore_portafoglio", None)

        if not gestore_portafoglio:
            return "Non ancora disponibile"

        saldo = gestore_portafoglio.ottieni_saldo(email_utente)
        return f"{saldo:.2f} €"
    
    def _ottieni_testo_piano(self):
        """Mostra tutti gli abbonamenti attivi, divisi per tipo di piano (Mensile/Annuale)."""
        
        gestore_abbonamenti = getattr(self.finestra_principale, "gestore_abbonamenti", None)

        if not gestore_abbonamenti:
            return "Nessun piano attivo"

        abbonamenti = gestore_abbonamenti.ottieni_tutti()
        attivi = [abb for abb in abbonamenti if abb.get("stato") == "Attivo"]

        if not attivi:
            return "Nessun piano attivo"

        mensili = [abb["piattaforma"].capitalize() for abb in attivi if abb.get("piano", "mensile") == "mensile"]
        annuali = [abb["piattaforma"].capitalize() for abb in attivi if abb.get("piano") == "annuale"]

        righe = []
        if mensili:
            righe.append("Mensile: " + ", ".join(mensili))
        if annuali:
            righe.append("Annuale: " + ", ".join(annuali))

        return "\n".join(righe)