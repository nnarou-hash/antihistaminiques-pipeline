"""
prompts.py — Prompt LangChain pour la synthese IA
Reutilise la structure de prompt de ton collegue
"""
from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
Tu es un assistant specialise dans l'analyse des risques de rupture
de medicaments antihistaminiques.

Tu recois le resultat d'un modele de machine learning (Random Forest Classifier).

Regles :
- redige une synthese courte, claire et professionnelle en francais ;
- indique la classe ATC, la periode et la probabilite ;
- distingue explicitement une prediction d'une certitude ;
- n'invente aucune relation causale ;
- ne donne aucun conseil medical individuel ;
- precise que la decision finale reste humaine.
"""

prediction_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            """
Resultat du pipeline ML :

Classe ATC : {classe_atc}
Periode : {periode}
Prediction binaire : {prediction}
Niveau de risque : {niveau_risque}
Probabilite de rupture : {probabilite_rupture} %
Graminees moyennes : {gram_moy}
Temperature moyenne : {temp_moy}
Precipitations : {precip}
Ruptures a la periode precedente : {ruptures_lag1}

Redige une synthese de quatre a six phrases.
""",
        ),
    ]
)
