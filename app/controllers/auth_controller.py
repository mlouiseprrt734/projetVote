from flask import jsonify, request, session
from webauthn import generate_registration_options, options_to_json, generate_authentication_options, verify_authentication_response, verify_registration_response
from webauthn.helpers import bytes_to_base64url, base64url_to_bytes
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    ResidentKeyRequirement,
    UserVerificationRequirement,
    PublicKeyCredentialDescriptor,
)
from datetime import datetime, timezone

from app.models.auth_model import WebAuthnCredential
from app.models.electeurs_model import Electeur
from app import db

# config
RP_ID = "localhost"
RP_NAME = "Application de vote"
ORIGIN = "http://localhost:5000"

def register_begin():
    data = request.get_json()
    if not data or "email" not in data:
        return {"error": "Email requis"}, 400
        
    email = data["email"]

    electeur = Electeur.query.filter_by(email=email).first()
    if not electeur:
        return {"error": "Aucun électeur trouvé avec cet email"}, 404

    user_id_bytes = electeur.idelecteur.to_bytes(16, byteorder="big")

    exclude_creds = [
        PublicKeyCredentialDescriptor(id=c.credential_id)
        for c in electeur.credentials
    ]
    
    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_name=electeur.email,
        user_id=user_id_bytes,
        user_display_name=electeur.email,
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.REQUIRED,
            user_verification=UserVerificationRequirement.PREFERRED,
        ),
        exclude_credentials=exclude_creds,
        timeout=60000,
    )
    
    session["reg_challenge"] = bytes_to_base64url(options.challenge)
    session["reg_idelecteur"] = electeur.idelecteur
    
    return options_to_json(options)


def register_complete():
    idelecteur = session.get("reg_idelecteur")
    if not idelecteur:
        return jsonify({"verified": False, "error": "Session d'enregistrement expirée"}), 400

    electeur = Electeur.query.get(idelecteur)
    if not electeur:
        return jsonify({"verified": False, "error": "Électeur introuvable"}), 404

    verification = verify_registration_response(
        credential=request.get_data(as_text=True),   # raw JSON from the browser
        expected_challenge=base64url_to_bytes(session["reg_challenge"]),
        expected_origin=ORIGIN,
        expected_rp_id=RP_ID,
        require_user_verification=False,
    )

    new_credential = WebAuthnCredential(
        idelecteur=electeur.idelecteur,
        credential_id=verification.credential_id,
        public_key=verification.credential_public_key,
        sign_count=verification.sign_count,
    )

    db.session.add(new_credential)
    db.session.commit()

    session.pop("reg_challenge", None)
    session.pop("reg_idelecteur", None)

    return jsonify({"verified": True})


def login_begin():
    options = generate_authentication_options(
        rp_id=RP_ID,
        user_verification=UserVerificationRequirement.PREFERRED,
        # allow_credentials omitted => discoverable credentials, no username needed
    )
    session["auth_challenge"] = bytes_to_base64url(options.challenge)
    return options_to_json(options)


def find_credential(raw_id):
    return WebAuthnCredential.query.filter_by(credential_id=raw_id).first()


def login_complete():
    body = request.get_json()
    cred = find_credential(base64url_to_bytes(body["rawId"]))
    if cred is None:
        return jsonify({"verified": False, "error": "Passkey non trouvée"}), 400

    verification = verify_authentication_response(
        credential=request.get_data(as_text=True),
        expected_challenge=base64url_to_bytes(session["auth_challenge"]),
        expected_origin=ORIGIN,
        expected_rp_id=RP_ID,
        credential_public_key=cred.public_key,
        credential_current_sign_count=cred.sign_count,
        require_user_verification=False,
    )

    cred.sign_count = verification.new_sign_count
    cred.last_used_at = datetime.now(timezone.utc)
    db.session.commit()

    session["idelecteur"] = cred.idelecteur

    session.pop("auth_challenge", None)
    
    return jsonify({"verified": True})