from flask import render_template, request, redirect, url_for, abort, flash

from app import db
from app.models.electeurs_model import Electeur
from app.models.organisation_model import Scrutin
from app.models.scrutin_model import Participation


def afficher_participants_scrutin(idscrutin):
    """Affiche les électeurs inscrits à un scrutin précis."""
    scrutin = db.session.get(Scrutin, idscrutin)
    if scrutin is None:
        abort(404)

    participations = (
        Participation.query
        .join(Electeur)
        .filter(Participation.idscrutin == idscrutin)
        .order_by(Electeur.nom, Electeur.prenom)
        .all()
    )

    return render_template(
        "pages/participants_scrutin.html",
        scrutin=scrutin,
        participations=participations
    )


def ajouter_electeur(idscrutin):
    """Crée l'électeur dans electeur s'il n'existe pas, puis l'inscrit au scrutin."""
    scrutin = db.session.get(Scrutin, idscrutin)
    if scrutin is None:
        abort(404)

    nom = request.form.get("nom", "").strip()
    prenom = request.form.get("prenom", "").strip()
    email = request.form.get("email", "").strip().lower() or None

    if not nom or not prenom:
        flash("Le nom et le prénom sont obligatoires.", "warning")
        return redirect(url_for("main.afficher_participants_scrutin", idscrutin=idscrutin))

    # Si un email existe déjà, on réutilise cet électeur au lieu de créer un doublon.
    electeur = None
    if email:
        electeur = Electeur.query.filter(
            db.func.lower(Electeur.email) == email
        ).first()

    # Sinon, on crée une ligne dans la table electeur.
    if electeur is None:
        electeur = Electeur(nom=nom, prenom=prenom, email=email)
        db.session.add(electeur)
        db.session.flush()  # Récupère idelecteur avant de créer la participation.

    # Vérifie que cet électeur n'est pas déjà inscrit à ce scrutin.
    participation_existante = Participation.query.filter_by(
        idelecteur=electeur.idelecteur,
        idscrutin=idscrutin
    ).first()

    if participation_existante is not None:
        flash("Cet électeur est déjà inscrit à ce scrutin.", "warning")
    else:
        participation = Participation(
            idelecteur=electeur.idelecteur,
            idscrutin=idscrutin,
            avote=False
        )
        db.session.add(participation)
        db.session.commit()
        flash("Électeur ajouté à la liste du scrutin.", "success")

    return redirect(url_for("main.afficher_participants_scrutin", idscrutin=idscrutin))


def modifier_electeur(idscrutin, idelecteur):
    """Modifie les informations de l'électeur associé à ce scrutin."""
    participation = db.session.get(Participation, (idelecteur, idscrutin))
    if participation is None:
        abort(404)

    electeur = participation.electeur
    nom = request.form.get("nom", "").strip()
    prenom = request.form.get("prenom", "").strip()
    email = request.form.get("email", "").strip().lower() or None

    if not nom or not prenom:
        flash("Le nom et le prénom sont obligatoires.", "warning")
        return redirect(url_for("main.afficher_participants_scrutin", idscrutin=idscrutin))

    if email:
        autre_electeur = Electeur.query.filter(
            db.func.lower(Electeur.email) == email,
            Electeur.idelecteur != idelecteur
        ).first()
        if autre_electeur is not None:
            flash("Cette adresse email est déjà utilisée par un autre électeur.", "warning")
            return redirect(url_for("main.afficher_participants_scrutin", idscrutin=idscrutin))

    electeur.nom = nom
    electeur.prenom = prenom
    electeur.email = email
    db.session.commit()

    flash("Électeur modifié avec succès.", "success")
    return redirect(url_for("main.afficher_participants_scrutin", idscrutin=idscrutin))


def supprimer_electeur(idscrutin, idelecteur):
    """Retire l'électeur de ce scrutin sans supprimer sa fiche electeur."""
    participation = db.session.get(Participation, (idelecteur, idscrutin))
    if participation is None:
        abort(404)

    # On ne retire pas une participation si le vote a déjà été effectué.
    if participation.avote:
        flash("Impossible de retirer un électeur qui a déjà voté.", "warning")
    else:
        db.session.delete(participation)
        db.session.commit()
        flash("Électeur retiré de ce scrutin.", "success")

    return redirect(url_for("main.afficher_participants_scrutin", idscrutin=idscrutin))
