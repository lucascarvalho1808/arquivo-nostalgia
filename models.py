from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, username, created_at=None):
        """
        Inicializa um novo usuário.

        id (str/int): Identificador único do usuário.
        email (str): E-mail do usuário.
        username (str): Nome de usuário (apelido).
        created_at (str/datetime): Data de criação do usuário.
        """
        self.id = id
        self.email = email
        self.username = username
        self.created_at = created_at