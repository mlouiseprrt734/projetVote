from flask import Blueprint
from ..controllers import access_control_controller, main_controller

bp = Blueprint("main",__name__)

bp.add_url_rule("/", "homepage", main_controller.homepage, methods=["GET", "POST"])
bp.add_url_rule("/loginpage", "loginpage", main_controller.loginpage)
bp.add_url_rule("/navigation", "navigation", main_controller.navigation)
bp.add_url_rule("/ballotpage", "ballotpage", main_controller.ballotpage)
bp.add_url_rule("/resultspage", "resultspage", main_controller.resultspage)
bp.add_url_rule("/organisationpage", "organisationpage", main_controller.organisationpage)

bp.add_url_rule("/presence-control", "presence_control", main_controller.presence_control)

#contrôle de présence
bp.add_url_rule("/verify-location", "verify_location", access_control_controller.verify_location, methods=["POST"])