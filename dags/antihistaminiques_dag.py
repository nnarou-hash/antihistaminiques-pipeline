from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Chemin vers ton venv PROJET (celui avec pandas, sklearn, etc.)
# Attention : différent du airflow_venv !
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
    schedule_interval="0 6 * * 1",  # Tous les lundis aA6h
    start_date=datetime(2026, 6, 1),
    catchup=False,
    tags=["antihistaminiques", "jedha"],
) as dag:

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

    predict_r06 = BashOperator(
        task_id="predict_r06",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/ml/predict.py --classe R06",
    )

    predict_r03 = BashOperator(
        task_id="predict_r03",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/ml/predict.py --classe R03",
    )

    predict_j01 = BashOperator(
        task_id="predict_j01",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/ml/predict.py --classe J01",
    )

    load_olap = BashOperator(
        task_id="load_olap",
        bash_command=f"cd {PROJECT_DIR} && {VENV_PROJET} && python src/transformations/load_olap.py",
    )

    # Orchestration : build_gold -> features_advanced -> train -> predict -> load_olap
    [build_gold_r06, build_gold_r03, build_gold_j01] >> features_advanced
    features_advanced >> train_r06 >> predict_r06
    features_advanced >> train_r03 >> predict_r03
    features_advanced >> train_j01 >> predict_j01
    [predict_r06, predict_r03, predict_j01] >> load_olap
