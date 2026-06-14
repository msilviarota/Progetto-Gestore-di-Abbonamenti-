class GestoreLogin():

    def __init__(self, db):
        self.db = db

    def getModulo(self):
        return ["email", "password"] # In un caso reale, questo potrebbe essere un oggetto più complesso o un template HTML
    
    def inviaCredenziali(self, email, password):
        print(f"[Control] Ricevuti dati: {email}. Verifica in corso...")
        return self.login(email, password)

    def login(self, email, password):
        user = self.db.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None
