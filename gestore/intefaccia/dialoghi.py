import webbrowser
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QDialog, QCheckBox, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QSize

from stile import (
    STILE_SCHEDA_CATEGORIA, STILE_BTN_SERVIZIO,
    STILE_BTN_CHIUDI, STILE_BTN_ESCI, STILE_TITOLO_PROFILO
)
from utils import scarica_logo


class SchedaCategoria(QDialog):
    def __init__(self, titolo, pulsanti, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titolo)
        self.setMinimumWidth(350)
        self.setMinimumHeight(400)
        self.setStyleSheet(STILE_SCHEDA_CATEGORIA)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        titolo_label = QLabel(titolo)
        titolo_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #222222;")
        titolo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo_label)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        layout.addStretch()

        for nome, link, logo_url in pulsanti:
            btn = QPushButton(nome)
            btn.setFixedHeight(50)
            btn.setFixedWidth(250)
            btn.setStyleSheet(STILE_BTN_SERVIZIO)
            btn.clicked.connect(lambda checked, l=link: webbrowser.open(l))

            if logo_url:
                icon = scarica_logo(logo_url)
                if icon:
                    btn.setIcon(icon)
                    btn.setIconSize(QSize(120, 40))
                    btn.setText("")

            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setFixedWidth(150)
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
        layout.addWidget(btn_chiudi, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)


class FinestraRicerca(QDialog):
    def __init__(self, risultati, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Risultati ricerca")
        self.setFixedSize(350, 400)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        titolo = QLabel("Risultati trovati:")
        titolo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titolo)

        if not risultati:
            lbl = QLabel("Nessun risultato trovato.")
            lbl.setStyleSheet("font-size: 14px; color: #888888;")
            layout.addWidget(lbl)
        else:
            for nome, link in risultati:
                btn = QPushButton(nome)
                btn.setFixedHeight(45)
                btn.setStyleSheet(STILE_BTN_SERVIZIO)
                btn.clicked.connect(lambda checked, l=link: webbrowser.open(l))
                layout.addWidget(btn)

        layout.addStretch()

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
        layout.addWidget(btn_chiudi, alignment=Qt.AlignmentFlag.AlignCenter)


class FinestraPreferenze(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preferenze")
        self.setFixedSize(450, 550)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        titolo = QLabel("Le mie Preferenze")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep)

        sottotitolo = QLabel("Seleziona le categorie che ti interessano:")
        sottotitolo.setStyleSheet("font-size: 13px; color: #555555;")
        layout.addWidget(sottotitolo)

        self.checkboxes = []
        categorie = ["🎵 Musica", "🎬 Video", "📚 Libri", "📡 Streaming", "⚽ Sport"]

        for cat in categorie:
            cb = QCheckBox(cat)
            cb.setStyleSheet("""
                QCheckBox {
                    font-size: 15px;
                    color: #222222;
                    padding: 6px;
                    spacing: 10px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #aaaaaa;
                    border-radius: 4px;
                    background-color: white;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #222222;
                    border-radius: 4px;
                    background-color: #4caf50;
                }
            """)
            layout.addWidget(cb)
            self.checkboxes.append(cb)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #cccccc;")
        layout.addWidget(sep2)

        btn_salva = QPushButton("Salva preferenze")
        btn_salva.setFixedHeight(40)
        btn_salva.setStyleSheet(STILE_BTN_CHIUDI)
        btn_salva.clicked.connect(self.salva)
        layout.addWidget(btn_salva)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setFixedHeight(40)
        btn_annulla.setStyleSheet(STILE_BTN_ESCI)
        btn_annulla.clicked.connect(self.close)
        layout.addWidget(btn_annulla)

    def salva(self):
        selezionate = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        if not selezionate:
            QMessageBox.warning(self, "Attenzione", "Seleziona almeno una categoria!")
            return
        QMessageBox.information(self, "Salvato", "Preferenze salvate:\n" + "\n".join(selezionate))
        self.close()
