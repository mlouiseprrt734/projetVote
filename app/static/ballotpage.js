let lists = {};

// Afficher une étape du vote
function show_step(number) {
    for (let panel of document.querySelectorAll("[data-vote-stage]")) {
        panel.hidden = panel.dataset.voteStage != number;
    }

    for (let step of document.querySelectorAll("[data-progress-step]")) {
        step.classList.remove("is-current", "is-complete");

        if (step.dataset.progressStep == number) {
            step.classList.add("is-current");
        } else if (step.dataset.progressStep < number) {
            step.classList.add("is-complete");
        }
    }
}

// Ouvrir le scrutin choisi et afficher ses listes
function choose_scrutin(card) {
    const choices = lists[card.dataset.scrutin];
    const radios = document.querySelectorAll('input[name="voteChoice"]');

    for (let i = 0; i < radios.length; i++) {
        let radio = radios[i];
        let choice = choices[i];
        let label = radio.parentElement;

        radio.checked = false;
        radio.value = choice.nom;
        label.querySelector("strong").textContent = choice.nom;
        label.querySelector("small").textContent = choice.description;
    }

    document.getElementById("ballot-scrutin-title").textContent = card.dataset.title;
    document.getElementById("selected-scrutin-date").textContent = card.dataset.date;
    document.getElementById("selected-scrutin-location").textContent = card.dataset.location;
    document.getElementById("to-review").disabled = true;

    document.getElementById("scrutin-selection").hidden = true;
    document.getElementById("vote-screen").hidden = false;

    show_step(1);
}

// Vérifier le choix avant de confirmer
function review_choice() {
    const radio = document.querySelector('input[name="voteChoice"]:checked');
    if (radio == null) return;

    const label = radio.parentElement;

    document.getElementById("ballot-review-name").textContent =
        label.querySelector("strong").textContent;

    document.getElementById("ballot-review-description").textContent =
        label.querySelector("small").textContent;

    show_step(2);
}

// Retour à la liste des scrutins
function show_scrutins() {
    document.getElementById("vote-screen").hidden = true;
    document.getElementById("scrutin-selection").hidden = false;
}

// Au chargement de la page
window.onload = async function() {
    const response = await fetch("/static/scrutins.json");

    if (!response.ok) {
        alert("Impossible de charger les listes.");
        return;
    }

    lists = await response.json();

    // Choisir un scrutin
    for (let card of document.querySelectorAll(".scrutin-card")) {
        card.onclick = function() {
            choose_scrutin(card);
        };
    }

    // Sélectionner une liste
    for (let radio of document.querySelectorAll('input[name="voteChoice"]')) {
        radio.onchange = function() {
            document.getElementById("to-review").disabled = false;
        };
    }

    // Boutons du parcours
    document.getElementById("to-review").onclick = review_choice;
    document.getElementById("back-to-choice").onclick = function() { show_step(1); };
    document.getElementById("confirm-choice").onclick = function() { show_step(3); };

    document.getElementById("back-to-scrutins").onclick = show_scrutins;
    document.getElementById("back-to-lists").onclick = show_scrutins;
    document.getElementById("restart-vote").onclick = show_scrutins;
};
