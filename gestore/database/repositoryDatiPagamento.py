import sys
import os
import json
from models.datiPagamento import DatiPagamento

class RepositoryDatiPagamento:
    def __init__(self, percorsoFile = "datiPagamento.json"):
        self._percorsoFile = percorsoFile
    
    # Scarichiamo tutte le informazioni dalla repository e carichiamole nel file
    def caricaFile(self):
        try:
            with open(self._percorsoFile, "r", encoding="utf-8") as file:
                return json.load(file)        
        except FileNotFoundError:
            return {}

    # Salviamo il file con le nuove informazioni nella repository
    def salvaFile(self, dati_totali):
        with open(self._percorsoFile, "w", encoding="utf-8") as file:
            json.dump(dati_totali, file, indent=4)

    # Salviamo il metodo di pagamento deciso dall'utente
    def salva_metodo(self, email: str, dati: DatiPagamento): 
        metodoPagamento = self.caricaFile()
        
        
        # Usiamo to_dict() o ottieni_dati_carta() a seconda di cosa restituisce il tuo modello
        if hasattr(dati, 'to_dict'):
            metodoPagamento[email] = dati.to_dict()
        else:
            metodoPagamento[email] = dati.ottieni_dati_carta()
            
        self.salvaFile(metodoPagamento)

  
    def getMetodoPagamento(self, emailUtente):
        metodoPagamento = self.caricaFile()
        return metodoPagamento.get(emailUtente, None)