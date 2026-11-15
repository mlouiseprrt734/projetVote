from app import db 

class Ville(db.Model):
    __tablename__ = 'ville'

    codepostal = db.Column(db.String(50), primary_key=True)
    nomville = db.Column(db.String(50))
    
    lieux = db.relationship("Lieu", back_populates="ville", lazy=True)