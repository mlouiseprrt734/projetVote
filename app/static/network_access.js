function checkNetwork() {
    const statusText = document.getElementById("network-status");
    statusText.innerHTML = "Checking network connection...";

    fetch("/verify-network")
        .then(response => response.json())
        .then(data => {
            if (data.connected) {
                statusText.innerHTML = "Go";
            } else {
                statusText.innerHTML = "Vous n'êtes pas connecté au réseau de la salle de vote. Veuillez vous connecter pour pouvoir voter.";
            }
        })
        .catch(err => {
            console.error("Erreur:", err);
            statusText.innerHTML = "Une erreur s'est produite lors de la vérification de votre connexion.";
        });
}