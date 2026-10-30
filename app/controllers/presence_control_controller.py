import math
from flask import has_request_context, request, jsonify

##Contrôle de présence##
def verify_presence():
    if not has_request_context():
        return jsonify({"error": "Erreur"}), 400

    if not is_code_valid():
        return jsonify({
            "success": False, 
            "error": "Code invalide."
        }), 400

    if not is_within_voting_radius():
        return jsonify({
            "success": False, 
            "error": "Votre localisation ne correspond pas à celle de votre lieu de vote."
        }), 400

    # 3. Vérification du réseau
    if not is_connected_to_site_network():
        return jsonify({
            "success": False, 
            "error": "Vous n'êtes pas connecté au réseau Wifi de votre lieu de vote."
        }), 400

    if is_code_valid() and is_within_voting_radius() and is_connected_to_site_network():
        return jsonify({"message": "Votre présence a bien été confirmée."}), 200



##Code TOTP##
def is_code_valid():
    data = request.get_json()

    if (not data) or ('code' not in data):
        return False

    user_code = data['code']

    #à remplacer quand la bdd sera connectée
    expected_code = "1234"

    if(user_code == expected_code):
        return True
    else:
        return False



##Localisation##
##à supprimer quand la bdd sera connectée
VOTING_SITE = {
    "latitude": 44.8075,   
    "longitude": -0.6026,  
    "max_radius": 100  
}

#calcule la distance entre la position de l'électeur et celle du site avec la Haversine Formula
def get_distance(lat_user, lon_user, lat_site, lon_site):
    R = 6371e3 
    phi1 = math.radians(lat_user)
    phi2 = math.radians(lat_site)
    d_phi = math.radians(lat_site - lat_user)
    d_lambda = math.radians(lon_site - lon_user)

    a = (math.sin(d_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def is_within_voting_radius():
    data = request.get_json()

    if (not data) or ('latitude' not in data) or ('longitude' not in data):
        return False

    user_lat = data['latitude']
    user_lng = data['longitude']

    distance = get_distance(
        user_lat, user_lng,
        #à remplacer quand la bdd sera connectée
        VOTING_SITE["latitude"], VOTING_SITE["longitude"]
    )

    if(distance<=VOTING_SITE["max_radius"]):
        return True
    else:
        return False


##Connexion réseau
def is_connected_to_site_network():
    user_ip = request.remote_addr

    #adresse IP localhost
    if user_ip == "127.0.0.1" :
        return True
    else:
        return False

