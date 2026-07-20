"""
pages/6_synthese_ia.py — Synthese IA (LangChain + Mistral)
Prend la prediction ML et genere une explication en langage naturel
"""
import streamlit as st
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

st.set_page_config(page_title="Synthese IA", page_icon="🤖", layout="wide")
st.title("Synthese IA — Explication en langage naturel")
st.caption("Random Forest (prediction) + LangChain + Mistral (explication)")
st.divider()

# ── Verification cle Mistral ──────────────────────────────────────
def _get_secret(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

MISTRAL_API_KEY = _get_secret("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    st.error("MISTRAL_API_KEY manquante. Ajoute-la dans les secrets Streamlit Cloud.")
    st.stop()

os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY

# ── Import des modules (apres avoir garanti la cle) ──────────────
from predict_simple import predict_latest_rupture
from prompts import prediction_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI

# ── Sidebar ────────────────────────────────────────────────────────
st.sidebar.title("Parametres")
classe_select = st.sidebar.selectbox(
    "Classe ATC",
    ["R06 — Antihistaminiques"],
    index=0
)
code_atc = classe_select.split(" ")[0]

# ── Generation ─────────────────────────────────────────────────────
@st.cache_resource
def get_llm():
    return ChatMistralAI(model="mistral-small-latest", temperature=0.2)

@st.cache_data(ttl=3600)
def get_prediction(code):
    return predict_latest_rupture(code)

if st.button("Generer la synthese", type="primary"):
    with st.spinner("Calcul de la prediction et generation de la synthese..."):
        try:
            prediction_data = get_prediction(code_atc)

            col1, col2, col3 = st.columns(3)
            col1.metric("Periode", prediction_data["periode"])
            col2.metric("Probabilite de rupture", f"{prediction_data['probabilite_rupture']}%")
            col3.metric("Niveau de risque", prediction_data["niveau_risque"].capitalize())

            st.divider()

            llm = get_llm()
            chain = prediction_prompt | llm | StrOutputParser()
            summary = chain.invoke(prediction_data)

            st.subheader("Synthese generee")
            st.info(summary)

        except Exception as e:
            st.error(f"Erreur lors de la generation : {e}")
else:
    st.info("Clique sur le bouton pour generer une synthese basee sur la derniere periode disponible.")

st.divider()
st.caption("Projet Antihistaminiques — Jedha 2026 — AAKN")
