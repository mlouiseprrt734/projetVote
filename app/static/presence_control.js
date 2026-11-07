document.getElementById('presence-control-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const codeValue = document.getElementById('code').value;
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = '';

    if (!navigator.geolocation) {
        errorDiv.textContent = "L'accès à la localisation n'est pas supportée par votre navigateur.";
        return;
    }

    //envoi de la lagitude, longitude et du code au controller pour vérification
    navigator.geolocation.getCurrentPosition(async function(position) {
        try {
            const response = await fetch("/verify-presence", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: codeValue,
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                })
            });

            const result = await response.json();

            if (response.ok && result.message) {
                alert("Succès : " + result.message);
                //à modifier pour rediriger vers la page de vote
                //window.location.href = "/ballotpage";
            } else {
                errorDiv.textContent = result.error || "Votre présence ne peut pas être confirmée.";
            }

        } catch (err) {
            console.error(err);
            errorDiv.textContent = "Une erreur est survenue lors de la communication avec le serveur.";
        }
    }, function(error) {
        errorDiv.textContent = "Impossible de récupérer votre position. Veuillez activer votre localisation.";
    }, { timeout: 10000 });
});