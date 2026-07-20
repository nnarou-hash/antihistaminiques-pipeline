"""
predict_simple.py — Version simplifiee sans MLflow
Charge le modele .joblib local + les donnees Gold depuis Snowflake
"""
import os
import sys
import joblib
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db_connector import read_sql

MARTS = "ANTIHISTAMINIQUE_ANALYTICS.DBT_AMICOLIER_MARTS"


def build_prediction_dataset(classe_atc: str = "R06") -> pd.DataFrame:
    """
    Reconstruit les donnees depuis Snowflake (equivalent de gold_ml + gold_ml_advanced)
    """
    df = read_sql(f"SELECT * FROM {MARTS}.GOLD_ML_{classe_atc}")

    try:
        df_advanced = read_sql(f"SELECT * FROM {MARTS}.GOLD_ML_ADVANCED")
        advanced_columns = [
            "annee_mois_str", "ruptures_lag1", "gram_lag_mois", "cumul_thermique"
        ]
        advanced_columns = [c for c in advanced_columns if c in df_advanced.columns]
        df = df.merge(df_advanced[advanced_columns], on="annee_mois_str", how="left")
    except Exception:
        pass  # gold_ml_advanced pas disponible, on continue sans

    return df


def predict_latest_rupture(classe_atc: str = "R06") -> dict:
    """
    Charge le modele .joblib local et predit le risque pour la derniere periode.
    Meme structure de retour que la version MLflow de l'original.
    """
    model_path = f"models/{classe_atc}/rf_classifier.joblib"
    if not os.path.exists(model_path):
        model_path = "models/rf_classifier.joblib"

    model = joblib.load(model_path)
    df = build_prediction_dataset(classe_atc)

    if hasattr(model, "feature_names_in_"):
        feature_columns = list(model.feature_names_in_)
    else:
        raise AttributeError("Le modele ne contient pas feature_names_in_")

    missing_columns = [c for c in feature_columns if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Colonnes manquantes : {', '.join(missing_columns)}")

    usable_rows = df.dropna(subset=feature_columns).copy()
    if usable_rows.empty:
        raise ValueError("Aucune ligne complete disponible pour la prediction.")

    usable_rows = usable_rows.sort_values("annee_mois_str")
    latest_row = usable_rows.iloc[[-1]].copy()

    X_latest = latest_row[feature_columns].astype("float64")
    prediction = int(model.predict(X_latest)[0])
    probability = float(model.predict_proba(X_latest)[0, 1])

    return {
        "classe_atc": classe_atc,
        "periode": str(latest_row["annee_mois_str"].iloc[0]),
        "prediction": prediction,
        "niveau_risque": "eleve" if prediction == 1 else "faible",
        "probabilite_rupture": round(probability * 100, 2),
        "gram_moy": float(latest_row["gram_moy"].iloc[0]),
        "temp_moy": float(latest_row["temp_moy"].iloc[0]),
        "precip": float(latest_row["precip"].iloc[0]),
        "ruptures_lag1": (
            float(latest_row["ruptures_lag1"].iloc[0])
            if "ruptures_lag1" in latest_row.columns else 0.0
        ),
    }
