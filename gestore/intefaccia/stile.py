### ==============================
### STILI - colori, font, pulsanti
### ==============================

# Stili per i contenitori e dialoghi principali [1]
STILE_DIALOGO_PROFILO = """ 
QDialog { background-color: #e8f5e9; } 
QLabel { color: #222222; font-size: 13px; } 
QLineEdit { background-color: #f5f5f5; color: #222222; border: 1px solid #cccccc; border-radius: 8px; padding: 8px 12px; font-size: 13px; } 
QLineEdit:focus { border: 1px solid #222222; } 
"""

STILE_SCHEDA_CATEGORIA = """ 
QDialog { background-color: #e8f5e9; } 
QLabel { color: #222222; } 
"""

STILE_FINESTRA_PRINCIPALE = "QWidget { background-color:#F7F4EF ; }"

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
    background-color: #f5f5f5; 
    color: #222222; 
    border: 1px solid #cccccc; 
    border-radius: 14px; 
    font-size: 16px; 
    font-weight: bold; 
    padding: 10px; 
} 
QPushButton:hover { 
    background-color: #222222; 
    color: white; 
} 
"""

STILE_BTN_EXTRA = """ 
QPushButton { 
    background-color: #f5f5f5; 
    color: #222222; 
    border: 1px solid #cccccc; 
    border-radius: 14px; 
    font-size: 15px; 
    font-weight: bold; 
    padding: 10px; 
} 
QPushButton:hover { 
    background-color: #222222; 
    color: white; 
} 
"""

# Stili per i pulsanti di servizio e chiusura [3]
STILE_BTN_SERVIZIO = """ 
QPushButton { 
    background-color: #f5f5f5; 
    color: #222222; 
    border: 1px solid #cccccc; 
    border-radius: 10px; 
    font-size: 14px; 
    font-weight: bold; 
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
    background-color: #f5f5f5; 
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
    background-color: #f5f5f5; 
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

STILE_LABEL_PROFILO = "color: #555555; font-weight: bold;" 
STILE_TITOLO_PROFILO = "color: #222222; font-size: 20px; font-weight: bold;" 
STILE_SALUTO = "color: #222222; font-size: 22px; font-weight: bold;" 
STILE_BTN_LINK = "color: black; text-decoration: underline;"