import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

st.set_page_config(
    page_title="Antihistaminiques — Dashboard",
    page_icon="💊",
    layout="wide"
)

DB_URL = st.secrets.get('DB_URL') or os.getenv('DB_URL')
engine = create_engine(DB_URL)

# =====================
# HEADER
# =====================
st.title("💊 Surveillance Ruptures Antihistaminiques")
st.markdown("**Projet Jedha 2026** — Pipeline Data Engineering + ML — Prédire les ruptures de stock à partir du pollen et de la météo")
st.divider()

# =====================
# FILTRE ATC
# =====================
classe = st.selectbox(
    "Classe ATC",
    ['R06 — Antihistaminiques', 'R03 — Antiasthmatiques', 'J01 — Antibiotiques'],
    index=0
)
code_atc = classe.split(' ')[0]

@st.cache_data
def load_gold(code):
    path = f'data/gold/gold_ml_{code}.csv'
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.read_csv('data/gold/gold_ml.csv')

@st.cache_data
def load_pred(code):
    path = f'data/gold/gold_predictions_{code}.csv'
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.read_csv('data/gold/gold_predictions.csv')

df = load_gold(code_atc)
pred = load_pred(code_atc)

mois_noms = {1:'Jan',2:'Fev',3:'Mar',4:'Avr',5:'Mai',6:'Jun',
             7:'Jul',8:'Aou',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

st.divider()

st.info(
    "**Sources du pipeline :** OpenMedic / CNAM (remboursements), ANSM (signalements de tensions et ruptures), "
    "BDPM (référentiel des médicaments), RNSA et CAMS / Copernicus (pollens), Open-Meteo (météo), "
    "Sentinelles / INSERM (repères épidémiologiques). Les données sont rapprochées dans les couches Silver puis Gold."
)
st.caption(
    "Les volumes remboursés et les signalements ne mesurent pas les stocks physiques disponibles. "
    "Les probabilités du modèle sont des estimations statistiques, pas une confirmation de rupture."
)

tab_vue, tab_historique, tab_predictions, tab_sources = st.tabs(
    ["Vue d’ensemble", "Historique des tensions", "Prédictions & modèle", "Sources & limites"]
)

with tab_vue:
    st.subheader(f"Indicateurs observés — {classe}")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        taux = df['target_rupture'].mean() * 100
        st.metric("Taux de rupture", f"{taux:.1f}%", help="% de mois avec au moins une rupture ou tension")
    with col2:
        mois_risque = df.groupby('mois')['target_rupture'].mean().idxmax()
        st.metric("Mois le plus à risque", mois_noms[mois_risque], help="Mois avec le plus fort taux historique")
    with col3:
        st.metric("Mois en tension", f"{int(df['target_rupture'].sum())} / {len(df)}", help="Mois avec rupture ou tension dans le jeu de données")
    with col4:
        corr = df['ambroisie_moy'].corr(df['target_rupture']) if 'ambroisie_moy' in df.columns else 0
        st.metric("Signal ambroisie", f"r={corr:.3f}", help="Corrélation descriptive ambroisie / tensions")
    with col5:
        annee_max = df.groupby('annee')['nb_ruptures'].sum().idxmax()
        st.metric("Année la plus touchée", str(annee_max), help="Année avec le plus grand nombre de signalements")
    st.divider()
    st.subheader("Indicateurs du modèle")
    col6, col7, col8, col9 = st.columns(4)
    with col6:
        st.metric("ROC-AUC Random Forest", "0.771", help="Score présenté dans la documentation du projet")
    with col7:
        st.metric("ROC-AUC baseline logistique", "0.457", help="Modèle de référence")
    with col8:
        nb_risque = int((pred['pred_rupture'] == 1).sum()) if pred is not None else 0
        st.metric("Mois classés à risque", f"{nb_risque} / {len(pred)}" if pred is not None else "—")
    with col9:
        proba_max = pred['proba_rupture'].max() * 100 if pred is not None else 0
        mois_max = pred.loc[pred['proba_rupture'].idxmax(), 'annee_mois_str'] if pred is not None else ''
        st.metric("Probabilité maximale estimée", f"{proba_max:.1f}%" if pred is not None else "—", help=f"Mois correspondant : {mois_max}")

with tab_historique:
    st.subheader(f"Évolution historique des tensions — {classe}")
    fig = px.bar(
        df, x='annee_mois_str', y='nb_ruptures',
        color='target_rupture',
        color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
        labels={'annee_mois_str': 'Mois', 'nb_ruptures': 'Nombre de signalements', 'target_rupture': 'Tension'},
        title=f'Événements observés par mois · {code_atc} · 2021–2026'
    )
    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=430, legend=dict(orientation='h', x=0.5, y=1.1, xanchor='center'))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Le graphique décrit les événements présents dans le jeu de données ; il ne mesure pas la prévalence nationale des pénuries.")

with tab_predictions:
    st.subheader(f"Probabilité de tension estimée — {classe}")
    if pred is not None and not pred.empty:
        pred['proba_pct'] = (pred['proba_rupture'] * 100).round(1)
        pred['risque'] = pred['pred_rupture'].map({0: 'Pas de risque classé', 1: 'Rupture prédite'})
        fig2 = px.bar(
            pred, x='annee_mois_str', y='proba_pct',
            color='risque',
            color_discrete_map={'Pas de risque classé': '#2ecc71', 'Rupture prédite': '#e74c3c'},
            labels={'annee_mois_str': 'Mois', 'proba_pct': 'Probabilité estimée (%)', 'risque': 'Classe prédite'},
            title=f'Probabilité estimée par mois · {code_atc}'
        )
        fig2.add_hline(y=50, line_dash='dash', line_color='black', annotation_text='Seuil illustratif 50 %')
        fig2.update_xaxes(tickangle=45)
        fig2.update_layout(height=430, legend=dict(orientation='h', x=0.5, y=1.1, xanchor='center'))
        st.plotly_chart(fig2, use_container_width=True)
        st.dataframe(pred[['annee_mois_str', 'proba_pct', 'pred_rupture']], use_container_width=True, hide_index=True)
    else:
        st.warning("Aucun fichier de prédictions n'est disponible pour cette classe ATC.")

with tab_sources:
    st.subheader("Sources et périmètre")
    st.markdown(
        """
- **OpenMedic / CNAM** : volumes de boîtes remboursées en ville.
- **ANSM** : signalements de ruptures, risques de rupture et informations de disponibilité.
- **BDPM** : référentiel public des spécialités et substances actives.
- **RNSA / ATMO / CAMS-Copernicus** : observations et estimations polliniques, avec des périodes et méthodes différentes selon la source.
- **Open-Meteo** : variables météorologiques agrégées.
- **Sentinelles / INSERM** : indicateurs épidémiologiques contextuels.
        """
    )
    st.subheader("Comment lire les résultats")
    st.markdown(
        """
- Les sources n'ont pas toutes le même grain, la même couverture géographique ni la même période.
- Les remboursements ne sont pas équivalents aux ventes totales ni à la disponibilité en pharmacie.
- Les signalements ANSM ne donnent pas accès aux stocks physiques des laboratoires, grossistes ou officines.
- Une corrélation entre pollen, météo et tensions ne démontre pas de causalité.
- Les prédictions dépendent des données disponibles, du périmètre ATC et du modèle entraîné ; elles doivent être interprétées comme une aide exploratoire, pas comme une alerte opérationnelle.
        """
    )

st.caption("Projet Antihistaminiques — pipeline de données, analyses et démonstration ML.")
