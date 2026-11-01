CREATE TABLE Vote.Electeur (
    idElecteur VARCHAR(50) PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50)
);

CREATE TABLE Vote.Scrutin (
    idScrutin VARCHAR(50) PRIMARY KEY,
    type VARCHAR(50),
    dateOuverture DATE,
    dateCloture DATE,
    statut VARCHAR(50)
);

CREATE TABLE Vote.Choix (
    idChoix VARCHAR(50) PRIMARY KEY,
    libelle VARCHAR(50),
    idScrutin VARCHAR(50) NOT NULL,
    FOREIGN KEY (idScrutin)
        REFERENCES Vote.Scrutin(idScrutin),
    UNIQUE (idChoix, idScrutin)
);

CREATE TABLE Vote.Bulletin (
    idBulletin VARCHAR(50) PRIMARY KEY,
    vote VARCHAR(50) NOT NULL,
    idChoix VARCHAR(50) NOT NULL,
    idScrutin VARCHAR(50) NOT NULL,

    FOREIGN KEY (idChoix, idScrutin)
        REFERENCES Vote.Choix(idChoix, idScrutin)
);

CREATE TABLE Vote.Ville (
    codePostal VARCHAR(50) PRIMARY KEY,
    nomVille VARCHAR(50)
);

CREATE TABLE Vote.Participation (
    idElecteur VARCHAR(50),
    idScrutin VARCHAR(50),
    aVote BOOLEAN NOT NULL DEFAULT FALSE,

    PRIMARY KEY (idElecteur, idScrutin),

    FOREIGN KEY (idElecteur)
        REFERENCES Vote.Electeur(idElecteur),

    FOREIGN KEY (idScrutin)
        REFERENCES Vote.Scrutin(idScrutin)
);

CREATE TABLE Vote.Lieu (
    idLieu VARCHAR(50) PRIMARY KEY,
    nom VARCHAR(50),
    codePostal VARCHAR(50) NOT NULL,

    FOREIGN KEY (codePostal)
        REFERENCES Vote.Ville(codePostal)
);

CREATE TABLE Vote.autorise (
    idScrutin VARCHAR(50),
    idLieu VARCHAR(50),

    PRIMARY KEY (idScrutin, idLieu),

    FOREIGN KEY (idScrutin)
        REFERENCES Vote.Scrutin(idScrutin),

    FOREIGN KEY (idLieu)
        REFERENCES Vote.Lieu(idLieu)
);
