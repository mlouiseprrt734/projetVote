// Récupère le code TOTP calculé par le serveur
async function update_code() {
    try {
        const response = await fetch("/totp", {cache: "no-store"});
        if (!response.ok) throw new Error("Code indisponible");

        const data = await response.json();
        const code = data.code;

        document.getElementById("code").textContent = code.slice(0, 3) + " " + code.slice(3);
        document.getElementById("timer").textContent =
            "Expire dans 00:" + String(data.remaining).padStart(2, "0");
    } catch (error) {
        document.getElementById("code").textContent = "Indisponible";
        document.getElementById("timer").textContent = "Erreur de connexion au serveur";
    }
}

// Mise à jour toutes les secondes, sans générer de code dans le navigateur
window.onload = function() {
    update_code();
    setInterval(update_code, 1000);
};
