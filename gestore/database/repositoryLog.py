from datetime import datetime 
class RepositoryLog:
    def __init__(self): 
        self.logs = []
    def aggiungi_log(self, evento: str): 
        self.logs.append((datetime.now(), evento))

