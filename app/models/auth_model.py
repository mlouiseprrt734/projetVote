from datetime import datetime
from app import db
from app.models.electeurs_model import Electeur

class WebAuthnCredential(db.Model):
    __tablename__ = "webauthn_credentials"
    
    id = db.Column(db.Integer, primary_key=True)

    #clé étrangère
    idelecteur = db.Column(
        db.Integer,
        db.ForeignKey("electeur.idelecteur", ondelete="CASCADE"),
        nullable=False,
    )

    #binaire
    credential_id = db.Column(db.LargeBinary, unique=True, nullable=False)
    public_key = db.Column(db.LargeBinary, nullable=False)

    sign_count = db.Column(db.Integer, nullable=False, default=0)
 
    #timestamps
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow
    )
    last_used_at = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow
    )

    #liaison electeur et auth
    electeur = db.relationship(
        "Electeur",
        backref=db.backref(
            "credentials", cascade="all, delete-orphan", lazy=True
        ),
    )

    def __repr__(self):
        return f"<WebAuthnCredential {self.name} (Electeur ID: {self.idelecteur})>"