from app import db 

class Lieu(db.Model):
    __tablename__ = 'lieu' 

    idlieu = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    codepostal = db.Column(db.String(50), db.ForeignKey('Vote.ville.codepostal'), nullable=False)
    longitude = db.Column(db.Numeric(9,6), nullable=True)
    latitude = db.Column(db.Numeric(9,6), nullable=True)

    ville = db.relationship('Ville', backref=db.backref('lieux_liees', lazy=True))

    def __repr__(self):
        return f"<Lieu {self.nom} {self.codepostal} >"