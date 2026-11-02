import os
import time
from flask import jsonify, request
from app.models.generator_TOTP import generate_totp


# Route de démonstration locale avec "1"
def get_totp():
    if os.environ.get("TOTP_LOCAL_DEMO") != "1":
        return jsonify({"error": "Mode démonstration désactivé"}), 403

    if request.remote_addr not in ("127.0.0.1", "::1"):
        return jsonify({"error": "Accès local uniquement"}), 403

    # La clé secrète est fournie par le serveur(powershell)
    try:
        secret = bytes.fromhex(os.environ.get("TOTP_SECRET_HEX", ""))
    except ValueError:
        return jsonify({"error": "Clé secrète invalide"}), 503

    if len(secret) < 32:
        return jsonify({"error": "Clé secrète non configurée"}), 503

    now = int(time.time())
    code = generate_totp(secret, now)
    remaining = 15 - (now % 15)

    response = jsonify({"code": code, "remaining": remaining})
    response.headers["Cache-Control"] = "no-store"
    return response
