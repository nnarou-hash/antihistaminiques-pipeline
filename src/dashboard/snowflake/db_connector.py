# src/dashboard/snowflake/db_connector.py
import os
import pandas as pd
from dotenv import load_dotenv
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

# Charge le .env qui se trouve dans le meme dossier que ce fichier
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def get_engine():
    engine = create_engine(URL(
        account   = os.getenv("SNOWFLAKE_ACCOUNT"),
        user      = os.getenv("SNOWFLAKE_USER"),
        password  = os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse = os.getenv("SNOWFLAKE_WAREHOUSE"),
        role      = os.getenv("SNOWFLAKE_ROLE"),
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
