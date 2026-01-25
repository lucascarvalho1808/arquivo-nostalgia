from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, username):
        """
        Inicializa um novo usuário.

        id (str/int): Identificador único do usuário.
        email (str): E-mail do usuário.
        username (str): Nome de usuário (apelido).
        """
        self.id = id
        self.email = email
        self.username = username