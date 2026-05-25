class Usuario:
    def __init__(self, id=None, nome="", email="", senha=""):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    def __str__(self):
        return f"{self.nome} - {self.email}"
