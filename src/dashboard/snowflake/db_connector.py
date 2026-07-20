# src/dashboard/snowflake/db_connector.py
import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

# Charge le .env local si present (developpement local uniquement)
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def _get_secret(key):
    """Lit d'abord dans st.secrets (Streamlit Cloud), sinon dans .env (local)."""
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

def get_engine():
    engine = create_engine(URL(
        account   = _get_secret("SNOWFLAKE_ACCOUNT"),
        user      = _get_secret("SNOWFLAKE_USER"),
        password  = _get_secret("SNOWFLAKE_PASSWORD"),
        warehouse = _get_secret("SNOWFLAKE_WAREHOUSE"),
        role      = _get_secret("SNOWFLAKE_ROLE"),
    ))
    return engine

def read_sql(query: str) -> pd.DataFrame:
    engine = get_engine()
    df = pd.read_sql(query, engine)
    df.columns = [c.lower() for c in df.columns]
    # Conversion automatique des colonnes numeriques
    # (Snowflake peut renvoyer certains types NUMBER sous forme de texte via le connecteur)
    for col in df.columns:
        if df[col].dtype == object:
            converted = pd.to_numeric(df[col], errors='coerce')
            # On ne remplace que si la conversion n'a pas tout transforme en NaN
            # (evite de casser les vraies colonnes texte comme annee_mois_str)
            if converted.notna().sum() == df[col].notna().sum():
                df[col] = converted
    return df
