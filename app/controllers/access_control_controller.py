import math
from flask import has_request_context, request, jsonify

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

def verify_location():
    #récupère la localisation de l'électeur
    data = request.get_json()

    if (not data) or ('latitude' not in data) or ('longitude' not in data):
        return jsonify({"allowed": False, "message": "Coordonnées manquantes."}), 400

    user_lat = data['latitude']
    user_lng = data['longitude']

    print(f"User Latitude: {user_lat}, User Longitude: {user_lng}")

    distance = get_distance(
        user_lat, user_lng,
        #à remplacer quand la bdd sera connectée
        VOTING_SITE["latitude"], VOTING_SITE["longitude"]
    )

    if(distance<=VOTING_SITE["max_radius"]):
        is_allowed = True
    else:
        is_allowed = False

    return jsonify({
        "allowed": is_allowed,
        "distanceMeters": round(distance)
    })

##Connexion réseau
def is_connected_to_site_network():
    user_ip = request.remote_addr

    #adresse IP localhost
    if user_ip == "127.0.0.1" :
        is_connected = True
    else:
        is_connected = False

    return jsonify({
        "connected": is_connected
    })

