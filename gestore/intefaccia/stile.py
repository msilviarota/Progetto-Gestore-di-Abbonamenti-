### ==============================
### STILI - colori, font, pulsanti
### ==============================

# Stili per i contenitori e dialoghi principali [1]
STILE_DIALOGO_PROFILO = """
QDialog {
    background-color: #F7F4EF;
}

QLabel {
    color: #222222;
    font-size: 13px;
}

QLineEdit {
    background-color: #D6D6D6;
    color: #222222;
    border: 1px solid #cccccc;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
}
"""

STILE_SCHEDA_CATEGORIA = """ 
QDialog { background-color: #E8F5E9; } 
QLabel { color: #222222; } 
"""

STILE_FINESTRA_PRINCIPALE = "QWidget { background-color:#F7F4EF; color: #222222; } QLabel { color: #222222; }"

# Stili per i pulsanti della Home Page [2]
STILE_BTN_PROFILO = """ 
QPushButton { 
    background-color: #f0f0f0; 
    color: #222222; 
    border: 2px solid #222222; 
    border-radius: 25px; 
    font-size: 22px; 
} 
QPushButton:hover { 
    background-color: #222222; 
    color: white; 
} 
"""

STILE_BTN_CATEGORIA = """ 
QPushButton { 
    background-color: #D6D6D6; 
    color: #222222; 
    border: 1px solid #cccccc; 
    border-radius: 14px; 
    font-size: 17px; 
    font-weight: bold; 
    min-width: 180px;
    min-height: 70px;
    padding: 14px 20px;
} 

QPushButton:hover { 
    background-color: #222222; 
    color: white; 
} 
"""


STILE_BTN_EXTRA = """ 
QPushButton { 
    background-color: #D6D6D6; 
    color: #222222; 
    border: 1px solid #cccccc; 
    border-radius: 14px; 
    font-size: 17px; 
    font-weight: bold; 
    min-width: 180px;
    min-height: 70px;
    padding: 14px 20px;
} 

QPushButton:hover { 
    background-color: #222222; 
    color: white; 
} 
"""



# Stili per i pulsanti di servizio e chiusura [3]
STILE_BTN_SERVIZIO = """ 
QPushButton { 
    background-color: #D6D6D6; 
    color: #222222; 
    border: 1px solid #cccccc; 
    border-radius: 14px; 
    font-size: 17px; 
    font-weight: bold; 
    min-width: 180px;
    min-height: 70px;
    padding: 14px 20px;
} 

QPushButton:hover { 
    background-color: #222222; 
    color: white; 
} 
"""


STILE_BTN_ESCI = """ 
QPushButton { 
    background-color: #888888; 
    color: white; 
    border: none; 
    border-radius: 10px; 
    padding: 10px 30px; 
    font-size: 14px; 
    font-weight: bold; 
} 
QPushButton:hover { 
    background-color: #555555; 
} 
"""

STILE_BTN_CHIUDI = """ 
QPushButton { 
    background-color: #222222; 
    color: white; 
    border: none; 
    border-radius: 10px; 
    padding: 10px 30px; 
    font-size: 14px; 
    font-weight: bold; 
} 
QPushButton:hover { 
    background-color: #444444; 
} 
"""

# Stili per campi di input e testi informativi [4]
STILE_CAMPO_RICERCA = """ 
QLineEdit { 
    background-color: #D6D6D6; 
    color: #222222; 
    border: 1px solid #cccccc; 
    border-radius: 20px; 
    padding: 0px 20px; 
    font-size: 14px; 
} 
QLineEdit:focus { 
    border: 1px solid #222222; 
} 
"""

STILE_COMBO = """ 
QComboBox { 
    background-color: #D6D6D6; 
    color: #222222; 
    border: 1px solid #cccccc; 
    border-radius: 8px; 
    padding: 5px 12px; 
    font-size: 13px; 
} 
QComboBox:focus { 
    border: 1px solid #222222; 
} 
QComboBox::drop-down { 
    border: none; 
} 
"""

STILE_FINESTRA_REGISTRAZIONE = """
QDialog {
    background-color: #E8F5E9;
}

QLabel {
    color: black;
    font-size: 14px;
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
    padding: 8px;
    border-radius: 6px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #c8c8c8;
}
"""

STILE_FINESTRA_LOGIN = """
QWidget {
    background-color: #E8F5E9;
}
"""

STILE_TITOLO_LOGIN = """
font-size: 28px;
font-weight: bold;
color: #222222;
margin-bottom: 20px;
"""

STILE_BTN_ACCEDI = """
QPushButton {
    background-color: #222222;
    color: white;
    padding: 12px;
    border-radius: 10px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #444444;
}
"""

STILE_LABEL_PROFILO = "color: #555555; font-weight: bold;" 
STILE_TITOLO_PROFILO = "color: #222222; font-size: 20px; font-weight: bold;" 
STILE_SALUTO = "color: #222222; font-size: 22px; font-weight: bold;" 
STILE_BTN_LINK = "color: black; text-decoration: underline;"


### ==============================
### NUOVI STILI - centralizzati da finestre.py
### ==============================

STILE_DIALOGO_VERDE = "QDialog { background-color: #E8F5E9; }"
STILE_TITOLO_DIALOGO = "font-size: 20px; font-weight: bold; color: #222;"
STILE_SEPARATORE = "color: #cccccc;"
STILE_SCROLL_VERDE = "QScrollArea { border: none; background-color: #E8F5E9; }"
STILE_CONTENITORE_VERDE = "background-color: #E8F5E9;"
STILE_CARD_LISTA = "background-color: white; border-radius: 8px; padding: 8px;"

STILE_FINESTRA_RICERCA = """
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
"""

STILE_CHECKBOX = """
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
"""
STILE_MESSAGEBOX = """
QMessageBox {
    background-color: #2b2b2b !important;
}
QMessageBox QLabel {
    color: white !important;
    font-size: 13px;
    selection-background-color: #2b2b2b !important;
    selection-color: white !important;
}
QMessageBox QPushButton {
    background-color: #444444 !important;
    color: white !important;
    border: 1px solid #666;
    border-radius: 6px;
    padding: 6px 16px;
    font-weight: bold;
}
QMessageBox QPushButton:hover {
    background-color: #666666 !important;
}
"""

STILE_TITOLO_RICERCA_ITEM = "font-size: 18px; font-weight: bold; color: #1A3E73;"
STILE_LABEL_CATEGORIA_RICERCA = "font-size: 14px; color: #555;"
STILE_LABEL_NESSUN_RISULTATO = "font-size: 16px; color: #444;"

STILE_TITOLO_SEZIONE = "color: #222222; font-size: 16px; font-weight: bold;"
STILE_SCROLL_TRASPARENTE = "QScrollArea { border: none; }"
STILE_TESTO_VUOTO = "color: #555555; font-size: 13px;"
STILE_CONTENITORE_PROFILO = "background-color: #F7F4EF;"
STILE_TITOLO_REGISTRAZIONE = "font-size: 22px; font-weight: bold; color: #222222; margin-bottom: 10px;"
STILE_SPINBOX = "padding: 5px; border-radius: 5px; background: white;"
