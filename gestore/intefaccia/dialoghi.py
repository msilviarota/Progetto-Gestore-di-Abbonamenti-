import os
import sys
import webbrowser
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QFrame, QMessageBox, QComboBox, 
    QCheckBox, QScrollArea, QFormLayout, QSpinBox
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

# Configurazione robusta dei percorsi per gestire gli import
cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

# Importazione degli stili e delle utilità [5, 6]
from intefaccia.stile import *
from intefaccia.utils import BASE_DIR, scarica_logo
from models.piattaforma import CATALOGO_PIATTAFORME

# ============================================================
# 1. SCHEDA CATEGORIA (CDU18 - Riproduci)
# ============================================================
class SchedaCategoria(QDialog):
    """Mostra le piattaforme di una categoria e ne permette l'avvio [7, 8]."""
    def __init__(self, titolo, servizi, email_utente, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titolo)
        self.setMinimumSize(400, 500)
        self.setStyleSheet(STILE_SCHEDA_CATEGORIA)
        self.email_utente = email_utente
        
        layout = QVBoxLayout(self)
        label_titolo = QLabel(f"Servizi per {titolo}")
        label_titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        layout.addWidget(label_titolo)

        # Creazione dinamica dei pulsanti per ogni servizio della categoria [4, 9]
        for nome, link, logo_path in servizi:
            btn_servizio = QPushButton(f"  {nome}")
            # Caricamento del logo con ridimensionamento 120x40 [3, 10]
            icona = scarica_logo(logo_path)
            if icona:
                btn_servizio.setIcon(icona)
                btn_servizio.setIconSize(QSize(100, 30))
            
            btn_servizio.setStyleSheet(STILE_BTN_SERVIZIO)
            # Implementazione del CDU18: avvio della piattaforma esterna
            btn_servizio.clicked.connect(lambda ch, n=nome, l=link: self.avvia_piattaforma(n, l))
            layout.addWidget(btn_servizio)

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setStyleSheet(STILE_BTN_CHIUDI)
        btn_chiudi.clicked.connect(self.close)
        layout.addWidget(btn_chiudi)

    def avvia_piattaforma(self, nome, link):
        """Simula la trasmissione dei dati e apre il browser [11, 12]."""
        print(f"[Sistema] Verifico abbonamento per {nome}...")
        webbrowser.open(link)

# ============================================================
# 2. PROFILO DIALOG (CDU7, CDU15, CDU16)
# ============================================================
class ProfiloDialog(QDialog):
    """Hub centrale per la gestione dell'account utente [2, 13]."""
    def __init__(self, finestra_principale, parent=None):
        super().__init__(parent)
        self.finestra_principale = finestra_principale
        self.setWindowTitle("Il mio Account")
        self.setFixedSize(430, 650)
        self.setStyleSheet(STILE_DIALOGO_PROFILO)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        
        # Info Utente basate sulla registrazione [14, 15]
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)
        label_titolo = QLabel("Dati Utente")
        label_titolo.setStyleSheet(STILE_TITOLO_PROFILO)
        
        label_nome = QLabel(f"Nome: {self.finestra_principale.nome_utente}")
        label_email = QLabel(f"Email: {self.finestra_principale.email_utente}")
        label_nome.setStyleSheet(STILE_LABEL_PROFILO)
        label_email.setStyleSheet(STILE_LABEL_PROFILO)
        
        info_layout.addWidget(label_titolo)
        info_layout.addWidget(label_nome)
        info_layout.addWidget(label_email)
        layout.addWidget(info_frame)

        # Pulsanti di gestione per i vari Casi d'Uso [16-18]
        azioni = [
            ("💳 Metodi di Pagamento", self.apri_pagamento), # CDU16
            ("📜 I miei Abbonamenti", self.apri_abbonamenti), # CDU13
            ("🤝 Presta Abbonamento", self.apri_presta),     # CDU11
            ("⭐ Preferenze", self.apri_preferenze),         # CDU5
            ("🗑️ Abbonamenti Scaduti", self.apri_scaduti),   # CDU14
            ("🔑 Cambia Password", self.apri_cambia_password) # CDU9
        ]

        for testo, funzione in azioni:
            btn = QPushButton(testo)
            btn.setStyleSheet(STILE_BTN_EXTRA)
            btn.clicked.connect(funzione)
            layout.addWidget(btn)

        # Logout (CDU15) [19]
        btn_logout = QPushButton("Esci dal Gestore")
        btn_logout.setStyleSheet(STILE_BTN_ESCI)
        btn_logout.clicked.connect(self.finestra_principale.close)
        layout.addWidget(btn_logout)

    # Metodi per l'apertura delle sotto-finestre [7, 13, 20]
    def apri_pagamento(self): FinestraModificaPagamento(self).exec()
    def apri_abbonamenti(self): FinestraAbbonamenti(self).exec()
    def apri_presta(self): FinestraPresta(self).exec()
    def apri_preferenze(self): FinestraPreferenze(self).exec()
    def apri_scaduti(self): FinestraScaduti(self).exec()
    def apri_cambia_password(self): FinestraCambiaPassword(self).exec()

# ============================================================
# 3. FINESTRE DI SUPPORTO (CDU 1, 4, 8, 9)
# ============================================================

class FinestraRecuperoPassword(QDialog):
    """CDU8: Gestisce la richiesta di una password temporanea [21]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recupero Password")
        self.setFixedSize(400, 250)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Inserisci l'email associata al tuo account:"))
        self.input_email = QLineEdit()
        self.input_email.setStyleSheet(STILE_CAMPO_RICERCA)
        layout.addWidget(self.input_email)
        
        btn_invia = QPushButton("Invia Password Temporanea")
        btn_invia.setStyleSheet(STILE_BTN_CHIUDI)
        btn_invia.clicked.connect(self.conferma_invio)
        layout.addWidget(btn_invia)

    def conferma_invio(self):
        if self.input_email.text():
            QMessageBox.information(self, "Email Inviata", "Controlla la tua casella di posta per la password temporanea.")
            self.close()

class FinestraRicerca(QDialog):
    """CDU4: Visualizza i risultati della ricerca globale [7, 22]."""
    def __init__(self, testo, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Risultati per: {testo}")
        self.setFixedSize(400, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Risultati aggregati per '{testo}':"))
        
        scroll = QScrollArea()
        container = QWidget()
        layout_risultati = QVBoxLayout(container)
        
        # Simulazione aggregazione risultati [23]
        piattaforme = ["Netflix", "Spotify", "Disney+", "Prime Video"]
        for p in piattaforme:
            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.StyledPanel)
            h_layout = QHBoxLayout(frame)
            h_layout.addWidget(QLabel(f"Contenuto trovato su {p}"))
            btn_vai = QPushButton("Vedi")
            btn_vai.setFixedWidth(60)
            h_layout.addWidget(btn_vai)
            layout_risultati.addWidget(frame)
            
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

class FinestraCambiaPassword(QDialog):
    """CDU9: Modulo per impostare una nuova password [1, 20, 24]."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cambia Password")
        self.setFixedSize(400, 350)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")
        
        layout = QFormLayout(self)
        self.old_pass = QLineEdit()
        self.new_pass = QLineEdit()
        self.conf_pass = QLineEdit()
        
        for p in [self.old_pass, self.new_pass, self.conf_pass]:
            p.setEchoMode(QLineEdit.EchoMode.Password)
            p.setStyleSheet(STILE_CAMPO_RICERCA)
            
        layout.addRow("Vecchia Password:", self.old_pass)
        layout.addRow("Nuova Password:", self.new_pass)
        layout.addRow("Conferma Password:", self.conf_pass)
        
        btn_salva = QPushButton("Aggiorna Password")
        btn_salva.setStyleSheet(STILE_BTN_CHIUDI)
        layout.addWidget(btn_salva)

# ============================================================
# 4. ALTRE FINESTRE DI GESTIONE [7, 9, 13, 20, 25, 26]
# ============================================================

class FinestraAbbonamenti(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("I miei Abbonamenti")
        self.setFixedSize(500, 400)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

class FinestraModificaPagamento(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifica Pagamento")
        self.setFixedSize(400, 400)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

class FinestraPreferenze(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preferenze")
        self.setFixedSize(450, 550)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

class FinestraScaduti(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Abbonamenti Scaduti")
        self.setFixedSize(450, 500)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

class FinestraPresta(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Presta Abbonamento")
        self.setFixedSize(400, 300)
        self.setStyleSheet("QDialog { background-color: #e8f5e9; }")

# ============================================================
# 5. UTILITY DI SISTEMA (CDU23)
# ============================================================
def mostra_errore_backup(messaggio_errore):
    """Popup di avviso per fallimento backup alle 23:30 [27, 28]."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle("Avviso di Sistema - Backup")
    msg.setText(messaggio_errore)
    msg.setStyleSheet("QMessageBox { background-color: #fce4ec; font-size: 14px; }")
    msg.exec()