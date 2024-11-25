from app import db
import hashlib


class UserProfile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=True)
    password = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()