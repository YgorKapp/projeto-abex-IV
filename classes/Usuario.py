# classes/Usuario.py
class Usuario:
    def __init__(self, nome, username, email, telefone, senha):
        self.nome = nome
        self.username = username
        self.email = email
        self.telefone = telefone
        self.senha = senha

    def to_tuple(self):
        return (self.nome, self.username, self.email, self.telefone, self.senha)
