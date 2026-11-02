# Générateur adapté du projet github MinTOTP: https://github.com/susam/mintotp
# Adaptations : HMAC-SHA256, validité de 15 secondes et code à 6 chiffres

import time
import hmac
import hashlib


# Générer un code TOTP à 6 chiffres toutes les 15 secondes
def generate_totp(secret, current_time=None):

    if current_time is None:
        current_time = int(time.time())

    # Calcul de la période de 15 secondes
    counter = current_time // 15
    message = counter.to_bytes(8, "big")

    # Génération avec HMAC-SHA256
    result = hmac.new(secret, message, hashlib.sha256).digest()

    # Extraction d'un nombre à partir du résultat
    offset = result[-1] & 15
    number = int.from_bytes(result[offset:offset + 4], "big")
    number = number & 0x7fffffff

    # Conversion en code de 6 chiffres
    return str(number % 1000000).zfill(6)
