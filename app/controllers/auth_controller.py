import os
from flask import jsonify, request, session
from webauthn import generate_registration_options, options_to_json, generate_authentication_options, verify_authentication_response, verify_registration_response
from webauthn.helpers import bytes_to_base64url, base64url_to_bytes
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    ResidentKeyRequirement,
    UserVerificationRequirement,
    PublicKeyCredentialDescriptor,
)

# config
RP_ID = "localhost"
RP_NAME = "Application de vote"
ORIGIN = "http://localhost:5000"
users = {} # à remplacer par le modèle de bdd


def register_begin():
    data = request.get_json()
    if not data or "email" not in data:
        return {"error": "Email requis"}, 400
        
    email = data["email"]
    user = users.setdefault(email, {"id": os.urandom(16), "credentials": []})
    
    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_name=email,
        user_id=user["id"],
        user_display_name=email,
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.REQUIRED,
            user_verification=UserVerificationRequirement.PREFERRED,
        ),
        exclude_credentials=[
            PublicKeyCredentialDescriptor(id=c["id"]) for c in user["credentials"]
        ],
        timeout=60000,
    )
    
    session["reg_challenge"] = bytes_to_base64url(options.challenge)
    session["reg_email"] = email
    
    return options_to_json(options)


def register_complete():
    email = session["reg_email"]
    user = users[email]

    verification = verify_registration_response(
        credential=request.get_data(as_text=True),   # raw JSON from the browser
        expected_challenge=base64url_to_bytes(session["reg_challenge"]),
        expected_origin=ORIGIN,
        expected_rp_id=RP_ID,
        require_user_verification=False,
    )

    user["credentials"].append({
        "id": verification.credential_id,
        "public_key": verification.credential_public_key,
        "sign_count": verification.sign_count,
        "aaguid": verification.aaguid,
        "backup_eligible": verification.credential_device_type,   # "single_device" or "multi_device"
        "backed_up": verification.credential_backed_up,           # True once synced
    })

    session.pop("reg_challenge", None)
    session.pop("reg_email", None)

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
    for email, user in users.items():
        for cred in user["credentials"]:
            if cred["id"] == raw_id:
                return cred, email
    return None, None


def login_complete():
    body = request.get_json()
    cred, email = find_credential(base64url_to_bytes(body["rawId"]))
    if cred is None:
        return jsonify({"verified": False, "error": "Passkey non trouvée"}), 400

    verification = verify_authentication_response(
        credential=request.get_data(as_text=True),
        expected_challenge=base64url_to_bytes(session["auth_challenge"]),
        expected_origin=ORIGIN,
        expected_rp_id=RP_ID,
        credential_public_key=cred["public_key"],
        credential_current_sign_count=cred["sign_count"],
        require_user_verification=False,
    )

    cred["sign_count"] = verification.new_sign_count
    session["user"] = email

    session.pop("auth_challenge", None)
    
    return jsonify({"verified": True})