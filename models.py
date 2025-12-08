from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, username):
        self.id = id
        self.email = email
        self.username = username