// Fonction pour gérer le retour en arrière
function go_back() {
    window.history.back();
}

// Fonction de validation des chaînes de caractères (string)
function validate_string_input(inputValue) {
    return typeof inputValue === 'string' && inputValue.trim().length > 0;
}

// Fonction pour nettoyer les messages d'erreurs et bordures rouges
function clear_errors(fieldsList) {
    fieldsList.forEach(fieldId => {
        const element = document.getElementById(fieldId);
        if (element) {
            element.classList.remove('error-input');
        }
    });
}

// Fonction principale de gestion de la soumission (clic sur Enregistrer)
function handle_submit(event) {
    event.preventDefault(); // Bloque l'envoi réel (pas de persistance demandée)

    // Récupération des éléments du DOM (camelCase)
    const ballotTitle = document.getElementById('ballotTitle').value;
    const ballotDescription = document.getElementById('ballotDescription').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const locationSelect = document.getElementById('locationSelect').value;

    const errorBanner = document.getElementById('errorBanner');
    const successBanner = document.getElementById('successBanner');

    // Liste des IDs pour réinitialiser le style d'erreur
    const fieldsList = ['ballotTitle', 'ballotDescription', 'startDate', 'endDate', 'locationSelect'];
    clear_errors(fieldsList);

    let missingFields = [];
    let isFormValid = true;

    // 1. Vérification Titre (Obligatoire + String)
    if (!validate_string_input(ballotTitle)) {
        document.getElementById('ballotTitle').classList.add('error-input');
        missingFields.push('Titre du scrutin');
        isFormValid = false;
    }

    // 2. Vérification Description (Obligatoire + String)
    if (!validate_string_input(ballotDescription)) {
        document.getElementById('ballotDescription').classList.add('error-input');
        missingFields.push('Description');
        isFormValid = false;
    }

    // 3. Vérification Date de début
    if (!startDate) {
        document.getElementById('startDate').classList.add('error-input');
        missingFields.push('Date de début');
        isFormValid = false;
    }

    // 4. Vérification Date de fin
    if (!endDate) {
        document.getElementById('endDate').classList.add('error-input');
        missingFields.push('Date de fin');
        isFormValid = false;
    }

    // 5. Vérification du Lieu (select : au moins un élément choisi)
    if (!locationSelect || locationSelect === "") {
        document.getElementById('locationSelect').classList.add('error-input');
        missingFields.push('Lieu de vote');
        isFormValid = false;
    }

    // Affichage des retours visuels selon la validité
    if (!isFormValid) {
        successBanner.classList.add('hidden');
        errorBanner.innerHTML = `<strong>Champs manquants ou invalides :</strong> ${missingFields.join(', ')}. Veuillez les remplir correctement en rouge.`;
        errorBanner.classList.remove('hidden');
    } else {
        errorBanner.classList.add('hidden');
        successBanner.classList.remove('hidden');
        console.log("Formulaire valide (simulation front-end réussie) !");
    }
}