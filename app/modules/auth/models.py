from datetime import datetime


from flask_login import UserMixin
import pytz
import hashlib

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(256), unique=True, nullable=True)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.utc))

    profile = db.relationship('UserProfile', backref='user', uselist=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if 'password' in kwargs:
            self.set_password(kwargs['password'])

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        password_introduced = hashlib.sha256(password.encode()).hexdigest()
        password2 = hashlib.sha256(password_introduced.encode()).hexdigest()
        return self.password == password_introduced

    def temp_folder(self) -> str:
        from app.modules.auth.services import AuthenticationService
        return AuthenticationService().temp_folder_by_user(self)
