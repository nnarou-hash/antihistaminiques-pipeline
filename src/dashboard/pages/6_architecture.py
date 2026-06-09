import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Architecture Pipeline", page_icon="🏗️", layout="wide")
st.title("🏗️ Architecture du Pipeline")
st.caption("Vue complète de l'architecture data engineering et ML du projet Antihistaminiques")
st.divider()

# =====================
# SECTION 1 — Schéma Medallion
# =====================
st.subheader("🥇 Architecture Medallion — Bronze → Silver → Gold → ML")
st.caption("Chaque couche enrichit et transforme les données brutes en insights actionnables.")

# Schéma SVG interactif via Plotly
fig = go.Figure()

# Couleurs par couche
colors = {
    'bronze': '#cd7f32',
    'silver': '#c0c0c0',
    'gold':   '#ffd700',
    'ml':     '#9b59b6',
    'api':    '#e74c3c',
    'dash':   '#2ecc71',
    'sent':   '#3498db',
}

# ── Couche BRONZE ──
bronze_sources = [
    ('CADA ANSM\nRuptures', 0.05),
    ('OpenMedic\n2021-2025', 0.22),
    ('Réseau\nSentinelles', 0.39),
    ('Météo\nFrance', 0.56),
    ('Pollen\nRNSA', 0.73),
    ('ANSM\n2026', 0.90),
]
for label, x in bronze_sources:
    fig.add_shape(type='rect', x0=x-0.07, x1=x+0.07, y0=0.82, y1=0.98,
                  fillcolor=colors['bronze'], opacity=0.85, line_color='white', line_width=1)
    fig.add_annotation(x=x, y=0.90, text=f"<b>{label}</b>", showarrow=False,
                       font=dict(size=9, color='white'), align='center')

fig.add_annotation(x=-0.03, y=0.90, text="<b>BRONZE</b>", showarrow=False,
                   font=dict(size=11, color=colors['bronze']), textangle=-90)

# Flèches Bronze → Silver
for _, x in bronze_sources:
    fig.add_annotation(x=x, y=0.81, ax=x, ay=0.74,
                       arrowhead=2, arrowsize=1, arrowwidth=1.5,
                       arrowcolor='#888', showarrow=True, text='')

# ── Couche SILVER ──
silver_files = [
    ('J0_silver\n_ruptures', 0.08),
    ('J0_silver\n_openmedic', 0.25),
    ('J0_silver\n_sentinelles', 0.42),
    ('J0_silver\n_meteo', 0.59),
    ('J0_silver\n_pollen', 0.76),
    ('J0_silver\n_ansm_2026', 0.93),
]
for label, x in silver_files:
    fig.add_shape(type='rect', x0=x-0.07, x1=x+0.07, y0=0.62, y1=0.78,
                  fillcolor=colors['silver'], opacity=0.85, line_color='white', line_width=1)
    fig.add_annotation(x=x, y=0.70, text=f"<b>{label}</b>", showarrow=False,
                       font=dict(size=9, color='#333'), align='center')

fig.add_annotation(x=-0.03, y=0.70, text="<b>SILVER</b>", showarrow=False,
                   font=dict(size=11, color='#888'), textangle=-90)

# Flèches Silver → Gold
fig.add_annotation(x=0.50, y=0.61, ax=0.50, ay=0.54,
                   arrowhead=2, arrowsize=1.5, arrowwidth=2,
                   arrowcolor='#555', showarrow=True, text='')
fig.add_annotation(x=0.50, y=0.575, text="build_gold.py\n--classe R06/R03/J01",
                   showarrow=False, font=dict(size=9, color='#555'))

# ── Couche GOLD ──
gold_files = [
    ('gold_ml_R06\n(60 mois, 35 col)', 0.18),
    ('gold_ml_R03\n(60 mois, 39 col)', 0.50),
    ('gold_ml_J01\n(60 mois, 39 col)', 0.82),
]
for label, x in gold_files:
    fig.add_shape(type='rect', x0=x-0.14, x1=x+0.14, y0=0.38, y1=0.54,
                  fillcolor=colors['gold'], opacity=0.85, line_color='white', line_width=1)
    fig.add_annotation(x=x, y=0.46, text=f"<b>{label}</b>", showarrow=False,
                       font=dict(size=10, color='#333'), align='center')

fig.add_annotation(x=-0.03, y=0.46, text="<b>GOLD</b>", showarrow=False,
                   font=dict(size=11, color='#b8860b'), textangle=-90)

# Flèches Gold → ML
for _, x in gold_files:
    fig.add_annotation(x=x, y=0.37, ax=x, ay=0.30,
                       arrowhead=2, arrowsize=1, arrowwidth=1.5,
                       arrowcolor='#888', showarrow=True, text='')

# ── Couche ML ──
ml_models = [
    ('RF Classifier\nR06\nROC-AUC CV: 0.738', 0.18),
    ('RF Classifier\nR03\nROC-AUC CV: 0.933', 0.50),
    ('RF Classifier\nJ01\nROC-AUC CV: 0.981', 0.82),
]
for label, x in ml_models:
    fig.add_shape(type='rect', x0=x-0.14, x1=x+0.14, y0=0.14, y1=0.30,
                  fillcolor=colors['ml'], opacity=0.85, line_color='white', line_width=1)
    fig.add_annotation(x=x, y=0.22, text=f"<b>{label}</b>", showarrow=False,
                       font=dict(size=9, color='white'), align='center')

fig.add_annotation(x=-0.03, y=0.22, text="<b>ML</b>", showarrow=False,
                   font=dict(size=11, color=colors['ml']), textangle=-90)

# Flèches ML → Outputs
for _, x in ml_models:
    fig.add_annotation(x=x, y=0.13, ax=x, ay=0.07,
                       arrowhead=2, arrowsize=1, arrowwidth=1.5,
                       arrowcolor='#888', showarrow=True, text='')

# ── Outputs ──
outputs = [
    ('FastAPI\n/predict', 0.10, colors['api']),
    ('gold_predictions\n_R06/R03/J01', 0.35, colors['gold']),
    ('OLAP Neon\n5 tables', 0.60, '#2980b9'),
    ('Dashboard\nStreamlit', 0.85, colors['dash']),
]
for label, x, color in outputs:
    fig.add_shape(type='rect', x0=x-0.11, x1=x+0.11, y0=0.00, y1=0.12,
                  fillcolor=color, opacity=0.85, line_color='white', line_width=1)
    fig.add_annotation(x=x, y=0.06, text=f"<b>{label}</b>", showarrow=False,
                       font=dict(size=9, color='white'), align='center')

fig.update_layout(
    height=550,
    margin=dict(l=40, r=20, t=20, b=20),
    xaxis=dict(visible=False, range=[-0.08, 1.02]),
    yaxis=dict(visible=False, range=[-0.05, 1.05]),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================
# SECTION 2 — Tableau des fichiers par couche
# =====================
st.subheader("📂 Inventaire des fichiers par couche")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🟤 Bronze — Sources brutes**")
    bronze_data = {
        'Fichier': [
            'ruptures_CADA.csv',
            'OPEN_MEDIC_2021-2025.csv',
            'pollen_*.csv',
            'meteo_*.csv',
            'export_disponibilites_ansm_2026.xlsx',
            'API Sentinelles'
        ],
        'Source': [
            'CADA ANSM',
            'Assurance Maladie',
            'RNSA',
            'Météo France',
            'ANSM',
            'INSERM'
        ]
    }
    st.dataframe(pd.DataFrame(bronze_data), use_container_width=True, hide_index=True)

with col2:
    st.markdown("**⚪ Silver — Données nettoyées**")
    silver_data = {
        'Fichier': [
            'J0_silver_ruptures.csv',
            'J0_silver_openmedic_2021_2025.csv',
            'J0_silver_ruptures_ansm_2026.csv',
            'J0_silver_sentinelles.csv',
            'J0_silver_medicaments.csv',
        ],
        'Lignes': ['~12 000', '~500 000', '268', '66', '~16 000']
    }
    st.dataframe(pd.DataFrame(silver_data), use_container_width=True, hide_index=True)

with col3:
    st.markdown("**🟡 Gold — Données ML-ready**")
    gold_data = {
        'Fichier': [
            'gold_ml_R06.csv',
            'gold_ml_R03.csv',
            'gold_ml_J01.csv',
            'gold_ml_advanced.csv',
            'gold_predictions_R06.csv',
            'gold_predictions_R03.csv',
            'gold_predictions_J01.csv',
        ],
        'Features': ['35', '39', '39', '42', '6', '6', '6']
    }
    st.dataframe(pd.DataFrame(gold_data), use_container_width=True, hide_index=True)

st.divider()

# =====================
# SECTION 3 — Métriques pipeline
# =====================
st.subheader("📊 Métriques du pipeline")

col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)

with col_m1:
    st.metric("Sources de données", "6", help="CADA, OpenMedic, ANSM 2026, Sentinelles, Pollen, Météo")
with col_m2:
    st.metric("Mois analysés", "60", help="Janvier 2021 → Décembre 2025")
with col_m3:
    st.metric("Features max", "23", help="R03 et J01 avec Sentinelles")
with col_m4:
    st.metric("Modèles entraînés", "9", help="3 classes × 3 modèles (LR, RF Regressor, RF Classifier)")
with col_m5:
    st.metric("Tables OLAP", "5", help="dim_date, dim_medicament, dim_region, dim_pollen, fact_ruptures")
with col_m6:
    st.metric("ROC-AUC CV max", "0.981", help="RF Classifier J01 avec Sentinelles")

st.divider()

# =====================
# SECTION 4 — Scripts du pipeline
# =====================
st.subheader("⚙️ Scripts du pipeline")
st.caption("Ordre d'exécution pour reconstruire le pipeline from scratch.")

scripts = [
    {"Étape": "1a", "Script": "clean_medicaments_ruptures.py", "Rôle": "Nettoyage ruptures CADA", "Couche": "Bronze → Silver"},
    {"Étape": "1b", "Script": "clean_openmedic.py", "Rôle": "Nettoyage OpenMedic + BDPM", "Couche": "Bronze → Silver"},
    {"Étape": "1c", "Script": "clean_pollen_meteo.py", "Rôle": "Nettoyage pollen + météo", "Couche": "Bronze → Silver"},
    {"Étape": "1d", "Script": "ingest_ruptures_ansm_2026.py", "Rôle": "Ingestion ANSM disponibilités 2026", "Couche": "Bronze → Silver"},
    {"Étape": "1e", "Script": "ingest_sentinelles.py", "Rôle": "Ingestion Réseau Sentinelles (grippal, IRA, diarrhée, varicelle)", "Couche": "Bronze → Silver"},
    {"Étape": "2a", "Script": "features_pollen.py", "Rôle": "Feature engineering pollen + météo", "Couche": "Silver → Gold"},
    {"Étape": "2b", "Script": "build_gold.py --classe R06/R03/J01", "Rôle": "Construction Gold par classe ATC", "Couche": "Silver → Gold"},
    {"Étape": "2c", "Script": "features_advanced.py", "Rôle": "Features avancées (lag, cumul thermique)", "Couche": "Gold → Gold"},
    {"Étape": "2d", "Script": "load_olap.py", "Rôle": "Chargement OLAP Neon PostgreSQL", "Couche": "Gold → OLAP"},
    {"Étape": "3",  "Script": "train_model.py --classe R06/R03/J01", "Rôle": "Entraînement RF Classifier + Regressor + SMOTE", "Couche": "Gold → Modèles"},
    {"Étape": "4",  "Script": "predict.py --classe R06/R03/J01", "Rôle": "Génération prédictions 60 mois", "Couche": "Modèles → Prédictions"},
]

df_scripts = pd.DataFrame(scripts)
st.dataframe(df_scripts, use_container_width=True, hide_index=True)

st.divider()

# =====================
# SECTION 5 — Stack technique
# =====================
st.subheader("🛠️ Stack technique")

col_t1, col_t2, col_t3, col_t4 = st.columns(4)

with col_t1:
    st.markdown("**Data Engineering**")
    st.markdown("- Python 3.9\n- Pandas\n- SQLAlchemy\n- Neon PostgreSQL")

with col_t2:
    st.markdown("**Machine Learning**")
    st.markdown("- Scikit-learn\n- Random Forest\n- SMOTE (imbalanced-learn)\n- SHAP")

with col_t3:
    st.markdown("**API & Dashboard**")
    st.markdown("- FastAPI\n- Streamlit\n- Plotly\n- Uvicorn")

with col_t4:
    st.markdown("**Sources de données**")
    st.markdown("- CADA ANSM\n- OpenMedic (AM)\n- Réseau Sentinelles\n- RNSA / Météo France")

st.caption("Projet Antihistaminiques — Jedha 2026 — LMN")
