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

async function loginWithPasskey() {
    const errorElement = document.getElementById("error-message");
    errorElement.innerText = "";

    try {
        //demande les options de login au serveur
        let res = await fetch("/login/begin", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });
        
        if (!res.ok) throw new Error("Erreur lors de l'initialisation de votre connexion");
        let options = await res.json();

        //adaptation des types pour l'API du navigateur
        options.challenge = bufferDecode(options.challenge);
        if (options.allowCredentials) {
            options.allowCredentials.forEach(c => c.id = bufferDecode(c.id));
        }

        //demande au navigateur de demander la passkey (empreinte, FaceID, Windows Hello...)
        let assertion = await navigator.credentials.get({ publicKey: options });

        //formate la réponse pour l'envoyer au serveur
        const assertionPayload = {
            id: assertion.id,
            rawId: bufferEncode(assertion.rawId),
            type: assertion.type,
            response: {
                authenticatorData: bufferEncode(assertion.response.authenticatorData),
                clientDataJSON: bufferEncode(assertion.response.clientDataJSON),
                signature: bufferEncode(assertion.response.signature),
                userHandle: assertion.response.userHandle ? bufferEncode(assertion.response.userHandle) : null
            }
        };

        //envoi la réponse au serveur pour vérification
        let verifyRes = await fetch("/login/complete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(assertionPayload)
        });

        let result = await verifyRes.json();

        if (result.verified) {
            window.location.href = "/ballotpage";
        } else {
            errorElement.innerText = "Échec de l'authentification : " + (result.error || "Inconnue");
        }

    } catch (err) {
        errorElement.innerText = "Action annulée ou erreur technique";
    }
}