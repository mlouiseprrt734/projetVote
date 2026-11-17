from flask import Blueprint
from ..controllers import main_controller, presence_control_controller, totp_controller, electeurs_controller, auth_controller, organisation_controller, participants_scrutin_controller,resultats_scrutin_controller

bp = Blueprint("main",__name__)

bp.add_url_rule("/", "homepage", main_controller.homepage, methods=["GET", "POST"])
bp.add_url_rule("/loginpage", "loginpage", main_controller.loginpage)
bp.add_url_rule("/registerpage", "registerpage", main_controller.registerpage)
bp.add_url_rule("/navigation", "navigation", main_controller.navigation)
bp.add_url_rule("/ballotpage", "ballotpage", main_controller.ballotpage)
bp.add_url_rule("/resultspage", "resultspage",  resultats_scrutin_controller.afficher_mes_scrutins,methods=["GET"])
bp.add_url_rule("/organisationpage", "organisationpage", organisation_controller.organisationpage)
bp.add_url_rule("/detailscrutin/<int:idscrutin>", "detailscrutin", organisation_controller.detailscrutin)
bp.add_url_rule("/creationscrutin", "creationscrutin", main_controller.creationscrutin)
bp.add_url_rule("/RGPDpage", "RGPDpage", main_controller.RGPDpage)
bp.add_url_rule("/parametrescrutin/<int:idscrutin>", "parametrescrutin", organisation_controller.parametrescrutin, methods=["GET", "POST"])
bp.add_url_rule("/electeurs","electeurs", electeurs_controller.get_electeurs,methods=["GET"])

# Gestion des électeurs associés à un scrutin
bp.add_url_rule("/detailscrutin/<int:idscrutin>/electeurs/ajouter","ajouter_electeur", participants_scrutin_controller.ajouter_electeur,methods=["POST"])
bp.add_url_rule("/detailscrutin/<int:idscrutin>/electeurs/<int:idelecteur>/modifier","modifier_electeur", participants_scrutin_controller.modifier_electeur, methods=["POST"])
bp.add_url_rule("/detailscrutin/<int:idscrutin>/electeurs/<int:idelecteur>/supprimer", "supprimer_electeur",participants_scrutin_controller.supprimer_electeur,methods=["POST"])
bp.add_url_rule("/mes-scrutins-votes", "mes_scrutins_votes", resultats_scrutin_controller.afficher_mes_scrutins,methods=["GET"])

# Afficher la liste des électeurs d'un scrutin
bp.add_url_rule("/detailscrutin/<int:idscrutin>/electeurs", "afficher_participants_scrutin", participants_scrutin_controller.afficher_participants_scrutin, methods=["GET"])

# Afficher les résultats d'un scrutin
bp.add_url_rule("/detailscrutin/<int:idscrutin>/resultats","afficher_resultats_scrutin",resultats_scrutin_controller.afficher_resultats_organisateur,methods=["GET"])
bp.add_url_rule("/scrutins-perso/<int:idscrutin>/resultats","resultats_electeur",resultats_scrutin_controller.afficher_resultats_scrutin,methods=["GET"])

#contrôle de présence
bp.add_url_rule("/presence-control", "presence_control", main_controller.presence_control)
bp.add_url_rule("/verify-presence", "verify_presence", presence_control_controller.verify_presence, methods=["POST"])

#route pour l'affichage du code TOTP
bp.add_url_rule("/displayTOTP", "displayTOTP", main_controller.displayTOTP)

#routes pour l'authentification par passkey
bp.add_url_rule("/register/begin", "register_begin", auth_controller.register_begin, methods=["POST"])
bp.add_url_rule("/register/complete", "register_complete", auth_controller.register_complete, methods=["POST"])
bp.add_url_rule("/login/begin", "login_begin", auth_controller.login_begin, methods=["POST"])
bp.add_url_rule("/login/complete", "login_complete", auth_controller.login_complete, methods=["POST"])

#route pour le TOTP
bp.add_url_rule("/totp", "totp", totp_controller.get_totp)

#route pour récupérer les électeurs
bp.add_url_rule('/electeurs', "electeurs", electeurs_controller.get_electeurs, methods=["GET"])
