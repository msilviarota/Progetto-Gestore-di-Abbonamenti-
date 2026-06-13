def filtra_categorie(self):
        from dialoghi import FinestraRicerca
        testo = self.campo_ricerca.text().lower().strip()

        if not testo:
            return

        risultati = []
        for chiave, servizi in self.link_categorie.items():
            if testo in chiave.lower():
                for nome, link, _ in servizi:
                    risultati.append((f"{chiave} → {nome}", link))
            else:
                for nome, link, _ in servizi:
                    if testo in nome.lower():
                        risultati.append((nome, link))

        finestra = FinestraRicerca(risultati, self)
        finestra.exec()