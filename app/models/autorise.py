from app import db 

class Autorise(db.Model):
    __tablename__ = 'autorise'

    idscrutin = db.Column(
        db.Integer,
        db.ForeignKey('scrutin.idscrutin'),
        primary_key=True,
        nullable=False,
    )
    idlieu = db.Column(
        db.Integer,
        db.ForeignKey('lieu.idlieu'),
        primary_key=True,
        nullable=False,
    )