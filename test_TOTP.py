##Afficher directement le code à la seconde precisée##

# from app.controllers.totp_controller import generate_totp
# # Clé secrète utilisée uniquement pour le test
# secret = b"12345678901234567890123456789012"

# # Générer des codes à différents instants
# print("Seconde 15 :", generate_totp(secret, 15))
# print("Seconde 29 :", generate_totp(secret, 29))
# print("Seconde 30 :", generate_totp(secret, 30))


# ##Afficher le code à chaque seconde... On peut remarquer que le code reste le même pdt 15 secondes et change après##
# import time
# from app.controllers.totp_controller import generate_totp
# # Clé publique utilisée uniquement pour les tests
# test_secret = b"12345678901234567890123456789012"

# while True:
#     code = generate_totp(test_secret)
#     print("Code actuel :", code)
#     time.sleep(1)

from app.controllers.totp_controller import generate_totp
test_secret = b"12345678901234567890123456789012"

assert generate_totp(test_secret, 15) == "119246"
assert generate_totp(test_secret, 29) == "119246"
assert generate_totp(test_secret, 30) == "882438"

print("Tous les tests TOTP sont réussis.")