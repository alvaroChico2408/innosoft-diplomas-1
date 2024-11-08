from app import db


class Diplomas(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'Diplomas<{self.id}>'
