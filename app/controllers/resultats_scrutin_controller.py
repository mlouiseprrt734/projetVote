
from flask import render_template, abort, session, redirect, url_for

from app import db
from app.models.organisation_model import Scrutin
from app.models.scrutin_model import Bulletin, Choix, Participation


def afficher_mes_scrutins():
    idelecteur = session.get("idelecteur")

    if idelecteur is None:
        return redirect(url_for("main.loginpage"))

    scrutins = (
        db.session.query(Scrutin)
        .join(Participation, Participation.idscrutin == Scrutin.idscrutin)
        .filter(
            Participation.idelecteur == idelecteur,
            Participation.avote.is_(True)
        )
        .order_by(Scrutin.dateouverture.desc())
        .all()
    )

    return render_template(
        "pages/scrutins_perso.html",
        scrutins=scrutins
    )


def afficher_resultats_scrutin(idscrutin):
    idelecteur = session.get("idelecteur")

    if idelecteur is None:
        return redirect(url_for("main.loginpage"))

    scrutin = db.session.get(Scrutin, idscrutin)

    if scrutin is None:
        abort(404)

    participation = db.session.get(
        Participation,
        (idelecteur, idscrutin)
    )

    if participation is None or not participation.avote:
        abort(403)

    total_inscrits = Participation.query.filter_by(
        idscrutin=idscrutin
    ).count()

    nb_votants = Participation.query.filter_by(
        idscrutin=idscrutin,
        avote=True
    ).count()

    taux_participation = (
        round(nb_votants / total_inscrits * 100, 1)
        if total_inscrits else 0
    )

    resultats = []
    total_bulletins = 0

    if scrutin.statut == "Terminé":
        choix_comptes = (
            db.session.query(
                Choix.idchoix,
                Choix.libelle,
                db.func.count(Bulletin.idbulletin).label("voix")
            )
            .outerjoin(Bulletin, db.and_(
                Bulletin.idchoix == Choix.idchoix,
                Bulletin.idscrutin == Choix.idscrutin
            ))
            .filter(Choix.idscrutin == idscrutin)
            .group_by(Choix.idchoix, Choix.libelle)
            .order_by(Choix.idchoix)
            .all()
        )

        total_bulletins = sum(voix for _, _, voix in choix_comptes)

        for idchoix, libelle, voix in choix_comptes:
            pourcentage = (
                round(voix / total_bulletins * 100, 1)
                if total_bulletins else 0
            )

            resultats.append({
                "libelle": libelle,
                "voix": voix,
                "pourcentage": pourcentage
            })

    return render_template(
        "pages/resultats_scrutin.html",
        scrutin=scrutin,
        resultats=resultats,
        total_bulletins=total_bulletins,
        total_inscrits=total_inscrits,
        nb_votants=nb_votants,
        taux_participation=taux_participation,
        url_retour=url_for("main.resultspage")
    )


def afficher_resultats_organisateur(idscrutin):
    scrutin = db.session.get(Scrutin, idscrutin)

    if scrutin is None:
        abort(404)

    total_inscrits = Participation.query.filter_by(
        idscrutin=idscrutin
    ).count()

    nb_votants = Participation.query.filter_by(
        idscrutin=idscrutin,
        avote=True
    ).count()

    taux_participation = (
        round(nb_votants / total_inscrits * 100, 1)
        if total_inscrits else 0
    )

    choix_comptes = (
        db.session.query(
            Choix.idchoix,
            Choix.libelle,
            db.func.count(Bulletin.idbulletin).label("voix")
        )
        .outerjoin(Bulletin, db.and_(
            Bulletin.idchoix == Choix.idchoix,
            Bulletin.idscrutin == Choix.idscrutin
        ))
        .filter(Choix.idscrutin == idscrutin)
        .group_by(Choix.idchoix, Choix.libelle)
        .order_by(Choix.idchoix)
        .all()
    )

    total_bulletins = sum(voix for _, _, voix in choix_comptes)

    resultats = []

    for idchoix, libelle, voix in choix_comptes:
        pourcentage = (
            round(voix / total_bulletins * 100, 1)
            if total_bulletins else 0
        )

        resultats.append({
            "libelle": libelle,
            "voix": voix,
            "pourcentage": pourcentage
        })

    return render_template(
        "pages/resultats_scrutin.html",
        scrutin=scrutin,
        resultats=resultats,
        total_bulletins=total_bulletins,
        total_inscrits=total_inscrits,
        nb_votants=nb_votants,
        taux_participation=taux_participation,
        url_retour=url_for("main.detailscrutin", idscrutin=idscrutin)
    )
