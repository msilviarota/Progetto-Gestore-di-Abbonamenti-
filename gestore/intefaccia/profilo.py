from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QFormLayout, QFrame, QScrollArea, QWidget,QMessageBox
)
from PyQt6.QtCore import Qt

from intefaccia.stile import (
    STILE_DIALOGO_PROFILO, STILE_BTN_ESCI, STILE_BTN_CHIUDI,
    STILE_TITOLO_PROFILO, STILE_LABEL_PROFILO, STILE_BTN_SERVIZIO
)
from intefaccia.dialoghi import FinestraCambiaPassword, FinestraModificaPagamento
from intefaccia.dialoghi import FinestraModificaPagamento

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
        scroll.setStyleSheet("QScrollArea { border: none; }")

        contenuto = QWidget()
        contenuto.setStyleSheet("background-color: #F7F4EF;")
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

        self.campo_piano = QLineEdit("Non ancora disponibile")
        self.campo_piano.setReadOnly(True)

        self.campo_pagamento = QLineEdit("Non ancora disponibile")
        self.campo_pagamento.setReadOnly(True)

        form.addRow(crea_label("Nome:"), self.campo_nome)
        form.addRow(crea_label("Email:"), self.campo_email)
        form.addRow(crea_label("Password:"), self.campo_password)
        form.addRow(crea_label("Piano:"), self.campo_piano)
        form.addRow(crea_label("Pagamento:"), self.campo_pagamento)
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
        btn_pagamento.clicked.connect(self.apri_pagamento)
        layout.addWidget(btn_pagamento)

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
        FinestraModificaPagamento(self).exec()

    def apri_abbonamenti(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self, "In arrivo",
            "La sezione 'I miei abbonamenti' sarà collegata al backend a breve."
        )

    def apri_presta(self):
        from intefaccia.dialoghi import FinestraModificaPagamento
        QMessageBox.information(
            self, "In arrivo",
            "La funzione 'Presta abbonamento' sarà collegata al backend a breve."
        )
  

    def apri_modifica_pagamento(self):
        finestra = FinestraModificaPagamento(
        email_utente=self.campo_email.text(),
        gestore_profilo=self.finestra_principale.gestore_profilo,
        parent=self
    )
        finestra.exec()
