from app import db 
from app.models.ville_model import Ville

class Lieu(db.Model):
    __tablename__ = 'lieu' 

    idlieu = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    codepostal = db.Column(db.String(50), db.ForeignKey('ville.codepostal'), nullable=False)
    longitude = db.Column(db.Numeric(9,6), nullable=True)
    latitude = db.Column(db.Numeric(9,6), nullable=True)

    ville = db.relationship(Ville, back_populates="lieux")

    def __repr__(self):
        return f"<Lieu {self.nom} {self.codepostal} >"