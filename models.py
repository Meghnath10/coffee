from flask_login import UserMixin

class User(UserMixin):
    def __init__(self):
        self.id = None
        self.username = None
        self.email = None
        self.password_hash = None
