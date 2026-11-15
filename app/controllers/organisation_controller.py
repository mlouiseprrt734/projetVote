from flask import render_template, abort
from app import db
from app.models.organisation_model import Scrutin

def organisationpage():
    scrutins = Scrutin.query.order_by(Scrutin.dateouverture.desc()).all()
    return render_template("pages/organisationpage.html", scrutins=scrutins)

def detailscrutin(idscrutin):
    scrutin = db.session.get(Scrutin, idscrutin)
    if scrutin is None:
        abort(404)
    return render_template("pages/detailscrutin.html", scrutin=scrutin)