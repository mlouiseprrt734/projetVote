const x = document.getElementById("user-location");

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(success, error);
  } else {
    x.innerHTML = "L'accès à la localisation n'est pas supporté par ce navigateur.";
  }
}

function success(position) {
  x.innerHTML = "Verifying location...";

  // Send coordinates to the server controller
  fetch("/verify-location", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      latitude: position.coords.latitude,
      longitude: position.coords.longitude
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.allowed) {
      x.innerHTML = "Go.";
    } else {
      x.innerHTML = "Accès refusé, vous devez vous trouver sur le lieu de vote pour pouvoir voter.";
    }
  })
  .catch(err => {
    console.error("Error sending coordinates:", err);
    x.innerHTML = "An error occurred while verifying your location.";
  });
}

function error(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED:
      x.innerHTML = "Vous avez refusé l'accès à votre localisation, merci de l'accepter pour continuer."
      break;
    case error.POSITION_UNAVAILABLE:
      x.innerHTML = "Les informations de localisation sont indisponibles."
      break;
    case error.TIMEOUT:
      x.innerHTML = "La demande d'accès à votre localisation a expiré."
      break;
    case error.UNKNOWN_ERROR:
      x.innerHTML = "Une erreur inconnue s'est produite."
      break;
  }
}