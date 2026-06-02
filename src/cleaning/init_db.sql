CREATE TABLE IF NOT EXISTS medicaments (
    cis                    BIGINT PRIMARY KEY,
    nom_medicament         TEXT NOT NULL,
    laboratoire            TEXT,
    code_atc               VARCHAR(20),
    molecule               TEXT,
    nb_patients_ville      FLOAT,
    substance_active       TEXT,
    pct_age_0_19_ans       FLOAT,
    pct_age_20_59_ans      FLOAT,
    pct_age_60_ans_et_plus FLOAT,
    pct_sexe_female        FLOAT,
    pct_sexe_male          FLOAT,
    est_antihistaminique   BOOLEAN
);

CREATE TABLE IF NOT EXISTS ruptures (
    id                   SERIAL PRIMARY KEY,
    cis                  BIGINT,
    nom_medicament       TEXT,
    cause                TEXT,
    classification       TEXT,
    date_evenement       DATE,
    code_atc             VARCHAR(20),
    molecule             TEXT,
    laboratoire          TEXT,
    nb_patients_ville    FLOAT,
    est_antihistaminique BOOLEAN,
    annee                INTEGER,
    mois                 INTEGER,
    trimestre            INTEGER,
    saison_allergies     BOOLEAN,
    cause_categorie      TEXT
);
