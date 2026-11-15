from flask import render_template, request, redirect, url_for, abort
from app import db
from app.models.organisation_model import Scrutin
from datetime import date

def organisationpage():
    scrutins = Scrutin.query.order_by(Scrutin.dateouverture.desc()).all()
    return render_template("pages/organisationpage.html", scrutins=scrutins)

def detailscrutin(idscrutin):
    scrutin = db.session.get(Scrutin, idscrutin)
    if scrutin is None:
        abort(404)
    return render_template("pages/detailscrutin.html", scrutin=scrutin)

def parametrescrutin(idscrutin):
    scrutin = db.session.get(Scrutin, idscrutin)
    if scrutin is None:
        abort(404)
    
    if request.method == "POST":
        dateouverture = date.fromisoformat(request.form["dateouverture"])
        datecloture = date.fromisoformat(request.form["datecloture"])

        if dateouverture > datecloture :
            return render_template("pages/parametrescrutin.html", scrutin=scrutin, erreur="La date d'ouverture doit précéder la date de clôture.")
        elif datecloture < dateouverture :
            return render_template("pages/parametrescrutin.html", scrutin=scrutin, erreur="La date de clôture doit être postérieure à la date d'ouverture.")

        scrutin.type = request.form["type"]
        scrutin.dateouverture = dateouverture
        scrutin.datecloture = datecloture
        scrutin.statut = request.form["statut"]
        db.session.commit()
        return redirect(url_for("main.parametrescrutin", idscrutin=scrutin.idscrutin))
    
    return render_template("pages/parametrescrutin.html", scrutin=scrutin) 