from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from dotenv import load_dotenv

# Charge le .env a la racine du projet
load_dotenv("/Users/nellyta/Jedha/.env")

DBT_CLOUD_ACCOUNT_ID = os.getenv("DBT_CLOUD_ACCOUNT_ID")
DBT_CLOUD_JOB_ID      = os.getenv("DBT_CLOUD_JOB_ID")
DBT_CLOUD_API_TOKEN   = os.getenv("DBT_CLOUD_API_TOKEN")

# Chemin vers ton venv PROJET (celui avec pandas, sklearn, etc.)
# Attention : different du airflow_venv !
VENV_PROJET = "source /Users/nellyta/venv/bin/activate"
PROJECT_DIR = "/Users/nellyta/Jedha"

default_args = {
    "owner": "nelly",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="antihistaminiques_pipeline_hebdo",
    default_args=default_args,
    schedule_interval="0 6 * * 1",  # Tous les lundis a 6h
    start_date=datetime(2026, 6, 1),
    catchup=False,
    tags=["antihistaminiques", "jedha"],
) as dag:

    # ── Tache 0 : Declenche le job dbt Cloud (Snowflake) ──────────────
    trigger_dbt_run = BashOperator(
        task_id="trigger_dbt_cloud_run",
        bash_command=f"""
        curl -s -X POST \
          "https://cloud.getdbt.com/api/v2/accounts/{DBT_CLOUD_ACCOUNT_ID}/jobs/{DBT_CLOUD_JOB_ID}/run/" \
          -H "Authorization: Token {DBT_CLOUD_API_TOKEN}" \
          -H "Content-Type: application/json" \
          -d '{{"cause": "Declenche automatiquement par Airflow - pipeline hebdo"}}'
        """,
    )

    build_gold_r06 = BashOperator(
        task_id="build_gold_r06",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/transformations/build_gold.py --classe R06",
    )

    build_gold_r03 = BashOperator(
        task_id="build_gold_r03",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/transformations/build_gold.py --classe R03",
    )

    build_gold_j01 = BashOperator(
        task_id="build_gold_j01",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/transformations/build_gold.py --classe J01",
    )

    features_advanced = BashOperator(
        task_id="features_advanced",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/transformations/features_advanced.py",
    )

    train_r06 = BashOperator(
        task_id="train_model_r06",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/ml/train_model.py --classe R06",
    )

    train_r03 = BashOperator(
        task_id="train_model_r03",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/ml/train_model.py --classe R03",
    )

    train_j01 = BashOperator(
        task_id="train_model_j01",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/ml/train_model.py --classe J01",
    )

    # ── Ordre d'execution ──────────────────────────────────────────────
    # dbt run tourne en premier (rafraichit les marts Snowflake)
    # puis les taches Python existantes suivent
    trigger_dbt_run >> [build_gold_r06, build_gold_r03, build_gold_j01] >> features_advanced
    features_advanced >> [train_r06, train_r03, train_j01]
