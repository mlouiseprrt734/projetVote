CREATE SCHEMA IF NOT EXISTS "Vote";
SET search_path TO "Vote";

CREATE TABLE Electeur (
    idElecteur INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50)
);

CREATE TABLE Scrutin (
    idScrutin INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type VARCHAR(50),
    dateOuverture DATE,
    dateCloture DATE,
    statut VARCHAR(50)
);

CREATE TABLE Choix (
    idChoix INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    libelle VARCHAR(50),
    idScrutin INTEGER NOT NULL,
    CONSTRAINT fk_choix_scrutin
        FOREIGN KEY (idScrutin) REFERENCES Scrutin(idScrutin),
    -- Permet à Bulletin de vérifier que le choix appartient au scrutin indiqué.
    CONSTRAINT uq_choix_id_scrutin UNIQUE (idChoix, idScrutin)
);

CREATE TABLE Bulletin (
    idBulletin INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    vote VARCHAR(50),
    idChoix INTEGER NOT NULL,
    idScrutin INTEGER NOT NULL,
    CONSTRAINT fk_bulletin_choix_scrutin
        FOREIGN KEY (idChoix, idScrutin)
        REFERENCES Choix(idChoix, idScrutin)
);

CREATE TABLE Ville (
    codePostal VARCHAR(50) PRIMARY KEY,
    nomVille VARCHAR(50)
);

CREATE TABLE Participation (
    idElecteur INTEGER NOT NULL,
    idScrutin INTEGER NOT NULL,
    aVote BOOLEAN,
    PRIMARY KEY (idElecteur, idScrutin),
    CONSTRAINT fk_participation_electeur
        FOREIGN KEY (idElecteur) REFERENCES Electeur(idElecteur),
    CONSTRAINT fk_participation_scrutin
        FOREIGN KEY (idScrutin) REFERENCES Scrutin(idScrutin)
);

CREATE TABLE Lieu (
    idLieu INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom VARCHAR(50),
    codePostal VARCHAR(50) NOT NULL,
    CONSTRAINT fk_lieu_ville
        FOREIGN KEY (codePostal) REFERENCES Ville(codePostal)
);

CREATE TABLE Autorise (
    idScrutin INTEGER NOT NULL,
    idLieu INTEGER NOT NULL,
    PRIMARY KEY (idScrutin, idLieu),
    CONSTRAINT fk_autorise_scrutin
        FOREIGN KEY (idScrutin) REFERENCES Scrutin(idScrutin),
    CONSTRAINT fk_autorise_lieu
        FOREIGN KEY (idLieu) REFERENCES Lieu(idLieu)
);
