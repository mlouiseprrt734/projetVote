// Durée initiale en secondes (15 secondes)
let remainingTime = 15;

// Fonction pour générer un code aléatoire à 6 chiffres
function generate_new_code() {
  // Génère un nombre entre 100 000 et 999 999
  const newCode = Math.floor(100000 + Math.random() * 900000);
  
  // Sépare les chiffres par un espace pour faire joli (ex: 482 951)
  const formattedCode = newCode.toString().replace(/(\d{3})(?=\d)/g, "$1 ");
  
  // Met à jour l'élément HTML du code
  document.getElementById("code").textContent = formattedCode;
}

// Fonction pour démarrer le compte à rebours
function start_timer() {
  const timerElement = document.getElementById("timer");

  const interval = setInterval(() => {
    // Calcul des minutes et des secondes
    let minutes = Math.floor(remainingTime / 60);
    let seconds = remainingTime % 60;

    // Formatage pour avoir toujours deux chiffres (ex: 00:09)
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    // Affichage dans le HTML
    timerElement.textContent = `Expire dans ${minutes}:${seconds}`;

    // Si le temps est écoulé (arrive à 0)
    if (remainingTime <= 0) {
      // 1. On génère un nouveau code
      generate_new_code();
      
      // 2. On remet le chronomètre à 15 secondes pour recommencer un cycle
      remainingTime = 15; 
    } else {
      // Sinon on décrémente le temps
      remainingTime--;
    }
  }, 1000); // Toutes les 1 seconde
}

// Lancer le timer dès le chargement de la page et lier le bouton copier
window.onload = function() {
  generate_new_code()
  start_timer();
};