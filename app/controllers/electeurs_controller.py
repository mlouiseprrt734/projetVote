from flask import jsonify
from app.models.electeurs_model import Electeur

#récupère tous les élécteurs de la base de données et les renvoie en JSON
def get_electeurs():
    electeurs = Electeur.query.all()
    result = [{"id": u.idelecteur, "nom": u.nom, "prenom": u.prenom, "email": u.email} for u in electeurs]
    return jsonify(result)