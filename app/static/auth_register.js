//conversion Base64URL <-> ArrayBuffer
function bufferEncode(value) {
    return btoa(String.fromCharCode.apply(null, new Uint8Array(value)))
        .replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
}

function bufferDecode(value) {
    value = value.replace(/-/g, "+").replace(/_/g, "/");
    while (value.length % 4) { value += "="; }
    const binary = atob(value);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
    }
    return bytes.buffer;
}

async function registerWithPasskey() {
    const email = document.getElementById("email").value;
    const errorElement = document.getElementById("error-message");
    errorElement.innerText = "";

    if (!email) {
        errorElement.innerText = "Veuillez entrer une adresse email.";
        return;
    }

    try {
        //initialise l'enregistrement auprès du serveur
        let res = await fetch("/register/begin", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });
        
        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            errorElement.innerText = errorData.error || "Erreur lors de votre enregistrement";
            return;
        }

        let options = await res.json();

        // Adaptation des types pour l'API du navigateur
        options.challenge = bufferDecode(options.challenge);
        options.user.id = bufferDecode(options.user.id);
        if (options.excludeCredentials) {
            options.excludeCredentials.forEach(c => c.id = bufferDecode(c.id));
        }

        //demande au navigateur de créer la passkey
        let credential = await navigator.credentials.create({ publicKey: options });

        //formate la réponse de la clé
        const credentialPayload = {
            id: credential.id,
            rawId: bufferEncode(credential.rawId),
            type: credential.type,
            response: {
                attestationObject: bufferEncode(credential.response.attestationObject),
                clientDataJSON: bufferEncode(credential.response.clientDataJSON),
            }
        };

        //envoyer au serveur pour vérification et stockage
        let verifyRes = await fetch("/register/complete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(credentialPayload)
        });

        let result = await verifyRes.json();

        if (result.verified) {
            alert("Inscription réussie ! Vous pouvez maintenant vous connecter.");
            window.location.href = "/loginpage";
        } else {
            errorElement.innerText = "Échec : " + (result.error || "Inconnue");
        }

    } catch (err) {
        errorElement.innerText = "Action annulée ou erreur technique";
    }
}