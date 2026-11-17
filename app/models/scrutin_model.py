from app import db

class Participation(db.Model):
    __tablename__ = "participation"

    idelecteur = db.Column(db.Integer, db.ForeignKey("electeur.idelecteur"), primary_key=True)
    idscrutin = db.Column(db.Integer, db.ForeignKey("scrutin.idscrutin"), primary_key=True)
    avote = db.Column(db.Boolean)

    electeur = db.relationship("Electeur")


class Choix(db.Model):
    __tablename__ = "choix"

    idchoix = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50))
    idscrutin = db.Column(db.Integer, db.ForeignKey("scrutin.idscrutin"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("idchoix", "idscrutin", name="uq_choix_id_scrutin"),
    )


class Bulletin(db.Model):
    __tablename__ = "bulletin"

    idbulletin = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.String(50))
    idchoix = db.Column(db.Integer, nullable=False)
    idscrutin = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ["idchoix", "idscrutin"],
            ["choix.idchoix", "choix.idscrutin"],
            name="fk_bulletin_choix_scrutin"
        ),
    )