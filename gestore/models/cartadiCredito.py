import os
import sys

cartella_corrente = os.path.dirname(os.path.abspath(__file__))
radice_progetto = os.path.abspath(os.path.join(cartella_corrente, ".."))
if radice_progetto not in sys.path:
    sys.path.append(radice_progetto)

from models.datiPagamento import DatiPagamento


class CartaDiCredito(DatiPagamento):
    """
    Estende DatiPagamento aggiungendo CVV e tipo carta (rilevato
    automaticamente dal numero, secondo i prefissi standard dei circuiti).
    """

    def __init__(self, numero_carta: str, scadenza_carta: str,
                 nome_titolare: str, cognome_titolare: str, cvv: str = ""):
        super().__init__(numero_carta, scadenza_carta, nome_titolare, cognome_titolare)
        self._cvv = cvv
        self._tipo_carta = self._rileva_tipo_carta(numero_carta)

    @staticmethod
    def _rileva_tipo_carta(numero_carta: str) -> str:
        """Determina il circuito della carta in base al prefisso del numero."""
        if not numero_carta:
            return "Sconosciuta"

        numero_pulito = numero_carta.replace(" ", "")

        if numero_pulito.startswith("4"):
            return "Visa"
        elif numero_pulito[:2] in ("51", "52", "53", "54", "55"):
            return "Mastercard"
        elif numero_pulito[:2] in ("34", "37"):
            return "American Express"
        else:
            return "Sconosciuta"

    def ottieni_dati_carta(self) -> dict:
        """Estende i dati base includendo CVV e tipo carta."""
        dati_base = super().ottieni_dati_carta()
        dati_base["cvv"] = self._cvv
        dati_base["tipo_carta"] = self._tipo_carta
        return dati_base