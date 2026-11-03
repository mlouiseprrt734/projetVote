
# Générateur adapté du projet github MinTOTP: https://github.com/susam/mintotp
# Adaptations : HMAC-SHA256, validité de 15 secondes et code à 6 chiffres

import os
import time
import hmac
import hashlib
from flask import jsonify, request


# Générer un code TOTP à 6 chiffres
def generate_totp(secret, current_time=None):

    if current_time is None:
        current_time = int(time.time())

    # Calcul de la période de 15 secondes
    counter = current_time // 15
    message = counter.to_bytes(8, "big")

    # Génération avec HMAC-SHA256
    result = hmac.new(secret, message, hashlib.sha256).digest()

    # Extraction du nombre
    offset = result[-1] & 15
    number = int.from_bytes(result[offset:offset + 4], "big")
    number = number & 0x7fffffff

    return str(number % 1000000).zfill(6)


# Récupérer le code TOTP pour l'affichage
def get_totp():

    # Vérifier que le mode test est activé
    if os.environ.get("TOTP_LOCAL_DEMO") != "1":
        return jsonify({"error": "Mode démonstration désactivé"}), 403

    if request.remote_addr not in ("127.0.0.1", "::1"):
        return jsonify({"error": "Accès local uniquement"}), 403

    # Récupérer la clé secrète
    try:
        secret = bytes.fromhex(os.environ.get("TOTP_SECRET_HEX", ""))
    except ValueError:
        return jsonify({"error": "Clé secrète invalide"}), 503

    if len(secret) < 32:
        return jsonify({"error": "Clé secrète non configurée"}), 503

    # Générer le code et calculer le temps restant
    now = int(time.time())
    code = generate_totp(secret, now)
    remaining = 15 - (now % 15)

    response = jsonify({"code": code, "remaining": remaining})
    response.headers["Cache-Control"] = "no-store"

    return response
