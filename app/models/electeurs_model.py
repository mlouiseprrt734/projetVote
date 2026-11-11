from app import db  # Importez l'instance de db définie dans votre app

class Electeur(db.Model):
    __tablename__ = 'electeur'  # Nom de la table dans le schéma "Vote"

    idelecteur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)

    def __repr__(self):
        return f"<Electeur {self.nom} {self.prenom}>"