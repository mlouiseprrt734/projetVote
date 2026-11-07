from flask import Blueprint
from ..controllers import main_controller, presence_control_controller, totp_controller, electeurs_controller

bp = Blueprint("main",__name__)

bp.add_url_rule("/", "homepage", main_controller.homepage, methods=["GET", "POST"])
bp.add_url_rule("/loginpage", "loginpage", main_controller.loginpage)
bp.add_url_rule("/navigation", "navigation", main_controller.navigation)
bp.add_url_rule("/ballotpage", "ballotpage", main_controller.ballotpage)
bp.add_url_rule("/resultspage", "resultspage", main_controller.resultspage)
bp.add_url_rule("/organisationpage", "organisationpage", main_controller.organisationpage)

#contrôle de présence
bp.add_url_rule("/presence-control", "presence_control", main_controller.presence_control)
bp.add_url_rule("/verify-presence", "verify_presence", presence_control_controller.verify_presence, methods=["POST"])

#route séparée pour l'affichage du code TOTP
bp.add_url_rule("/displayTOTP", "displayTOTP", main_controller.displayTOTP)

#route pour le TOTP
bp.add_url_rule("/totp", "totp", totp_controller.get_totp)

#route pour récupérer les électeurs
bp.add_url_rule('/electeurs', "electeurs", electeurs_controller.get_electeurs, methods=["GET"])