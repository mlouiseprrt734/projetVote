from app import db

class Scrutin(db.Model):
    __tablename__ = "scrutin"

    idscrutin = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    dateouverture = db.Column(db.Date)
    datecloture = db.Column(db.Date)
    statut = db.Column(db.String(50))

    lieux = db.relationship("Lieu", secondary="autorise", lazy="select")