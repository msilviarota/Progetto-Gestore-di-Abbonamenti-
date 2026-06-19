import os
import sys

cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QCheckBox, QFrame, QMessageBox
from PyQt6.QtCore import Qt

from intefaccia.stile import STILE_TITOLO_PROFILO, STILE_BTN_CHIUDI, STILE_BTN_ESCI


class FinestraPreferenze(QDialog):
    """CDU5: Permette all'utente di scegliere le categorie di interesse."""

    CATEGORIE = ["🎵 Musica", "🎬 Video", "📚 Libri", "📡 Streaming", "⚽ Sport"]

    def __init__(self, gestore_preferenze, email_utente, parent=None):
        super().__init__(parent)
        self.gestore_preferenze = gestore_preferenze
        self.email_utente = email_utente
        self.setWindowTitle("Le mie Preferenze")
        self.setFixedSize(420, 480)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        self.setStyleSheet("""
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid black;
                border-radius: 4px;
                background: white;
            }

            QCheckBox::indicator:hover {
                border: 2px solid #333;
            }

            QCheckBox::indicator:checked {
                background-color: black;
                image: none;
            }
            """)


        titolo = QLabel("Le mie Preferenze")
        titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        layout.addWidget(QLabel("Seleziona le categorie che ti interessano:"))

        self.checkboxes = []
        for cat in self.CATEGORIE:
            cb = QCheckBox(cat)
            layout.addWidget(cb)
            self.checkboxes.append(cb)

        layout.addStretch()

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
        if self.gestore_preferenze:
            self.gestore_preferenze.salva_preferenze(self.email_utente, selezionate)
        QMessageBox.information(self, "Salvato", "Preferenze salvate con successo!")
        self.close()