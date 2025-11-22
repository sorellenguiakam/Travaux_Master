"""
APPLICATION STREAMLIT - Détection Précoce DT1 Cameroun
Interface interactive pour prédiction en temps réel
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

# === CONFIGURATION PAGE ===
st.set_page_config(
    page_title="DT1 Detector Cameroun",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === STYLES CSS ===
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# === HEADER ===
st.markdown('<h1 class="main-header">🏥 Détection Précoce du Diabète Type 1</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Système adapté aux populations camerounaises</p>', unsafe_allow_html=True)

# === SIDEBAR ===
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisir une page:", ["🏠 Accueil", "🔍 Prédiction", "📊 À propos"])

# === PAGE ACCUEIL ===
if page == "🏠 Accueil":
    st.header("Bienvenue dans l'outil de détection DT1")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Objectif")
        st.write("""
        Cette application utilise l'apprentissage automatique pour détecter
        précocement le Diabète de Type 1 chez les patients camerounais,
        en analysant des biomarqueurs génétiques spécifiques.
        """)

        st.subheader("🧬 Biomarqueurs analysés")
        st.markdown("""
        - **ANP32A-IT1** : Régulation immunitaire
        - **ESCO2** : Cycle cellulaire
        - **NBPF1** : Expression pancréatique
        """)

    with col2:
        st.subheader("📌 Contexte")
        st.write("""
        Le DT1 en Afrique subsaharienne présente des spécificités :
        - Formes idiopathiques (sans auto-anticorps)
        - Diagnostic souvent tardif
        - Mortalité infantile élevée

        Ce système vise à améliorer le diagnostic précoce.
        """)

        st.subheader("⚠️ Important")
        st.warning("""
        Cet outil est une **aide à la décision**, pas un diagnostic médical.
        Toute prédiction positive doit être confirmée cliniquement.
        """)

    st.markdown("---")
    st.info("👈 Utilisez le menu de gauche pour naviguer vers **Prédiction**")

# === PAGE PRÉDICTION ===
elif page == "🔍 Prédiction":
    st.header("Analyse et Prédiction DT1")

    # Mode de saisie
    mode = st.radio("Mode de saisie:", ["📝 Saisie manuelle (1 patient)", "📄 Upload CSV (plusieurs patients)"])

    if mode == "📝 Saisie manuelle (1 patient)":
        st.subheader("Entrez les informations du patient")

        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.number_input("Âge (années)", min_value=5, max_value=70, value=25)
            sexe = st.selectbox("Sexe", ["M", "F"])
            region = st.selectbox("Région", ["Yaoundé", "Douala", "Bafoussam", "Garoua", "Bamenda", "Maroua", "Ngaoundéré"])

        with col2:
            imc = st.number_input("IMC (kg/m²)", min_value=15.0, max_value=40.0, value=22.0, step=0.1)
            glycemie = st.number_input("Glycémie à jeun (mmol/L)", min_value=3.0, max_value=20.0, value=5.5, step=0.1)
            hba1c = st.number_input("HbA1c (%)", min_value=4.0, max_value=14.0, value=5.5, step=0.1)

        with col3:
            anp32a = st.number_input("ANP32A-IT1 (U/mL)", min_value=0.5, max_value=10.0, value=2.0, step=0.1)
            esco2 = st.number_input("ESCO2 (U/mL)", min_value=1.0, max_value=15.0, value=3.0, step=0.1)
            nbpf1 = st.number_input("NBPF1 (U/mL)", min_value=0.8, max_value=8.0, value=2.0, step=0.1)

        antecedents = st.checkbox("Antécédents familiaux de diabète")

        if st.button("🔮 Analyser", type="primary"):
            # Créer DataFrame
            data = {
                'age': [age],
                'sexe': [1 if sexe == 'F' else 0],
                'IMC': [imc],
                'glycemie_jeun': [glycemie],
                'HbA1c': [hba1c],
                'antecedents_familiaux': [1 if antecedents else 0],
                'ANP32A_IT1': [anp32a],
                'ESCO2': [esco2],
                'NBPF1': [nbpf1],
            }

            df_patient = pd.DataFrame(data)

            # Simulation prédiction (en attendant modèle entraîné)
            # Logique simple basée sur biomarqueurs
            risk_score = (esco2 * 0.4 + anp32a * 0.35 + nbpf1 * 0.25) / 10
            proba_dt1 = min(max(risk_score, 0.1), 0.95)  # Entre 10% et 95%

            st.markdown("---")
            st.subheader("📊 Résultats de l'analyse")

            col_res1, col_res2 = st.columns(2)

            with col_res1:
                if proba_dt1 > 0.5:
                    st.error(f"⚠️ **Risque élevé de DT1** ({proba_dt1*100:.1f}%)")
                    st.write("Recommandation : Examens complémentaires urgents")
                else:
                    st.success(f"✅ **Risque faible de DT1** ({proba_dt1*100:.1f}%)")
                    st.write("Recommandation : Surveillance standard")

                # Gauge chart
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = proba_dt1 * 100,
                    title = {'text': "Probabilité DT1"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkred" if proba_dt1 > 0.5 else "green"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgreen"},
                            {'range': [30, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "lightcoral"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 50
                        }
                    }
                ))
                fig_gauge.update_layout(height=300)
                st.plotly_chart(fig_gauge, use_container_width=True)

            with col_res2:
                st.write("**Importance des biomarqueurs:**")

                importance = pd.DataFrame({
                    'Biomarqueur': ['ESCO2', 'ANP32A-IT1', 'NBPF1'],
                    'Importance': [40, 35, 25]
                })

                fig_imp = px.bar(importance, x='Importance', y='Biomarqueur',
                                 orientation='h', color='Importance',
                                 color_continuous_scale='Reds')
                fig_imp.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig_imp, use_container_width=True)

    else:  # Mode CSV
        st.subheader("Upload fichier CSV")

        st.write("Format attendu : colonnes `age`, `sexe`, `ANP32A_IT1`, `ESCO2`, `NBPF1`, etc.")

        uploaded_file = st.file_uploader("Choisir un fichier CSV", type=['csv'])

        if uploaded_file is not None:
            df_upload = pd.read_csv(uploaded_file)
            st.success(f"✅ Fichier chargé : {len(df_upload)} patients")

            st.dataframe(df_upload.head())

            if st.button("🔮 Analyser tous les patients"):
                st.info("Analyse en cours... (simulation)")

                # Simulation
                df_upload['Probabilite_DT1'] = np.random.uniform(0.1, 0.9, len(df_upload))
                df_upload['Diagnostic_predit'] = df_upload['Probabilite_DT1'].apply(
                    lambda x: 'DT1+' if x > 0.5 else 'DT1-'
                )

                st.subheader("📈 Résultats")
                st.dataframe(df_upload[['ID_patient', 'Probabilite_DT1', 'Diagnostic_predit']])

                # Distribution
                fig_dist = px.histogram(df_upload, x='Probabilite_DT1', nbins=20,
                                        title="Distribution des probabilités DT1")
                st.plotly_chart(fig_dist, use_container_width=True)

                # Téléchargement
                csv = df_upload.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Télécharger résultats (CSV)",
                    data=csv,
                    file_name='resultats_dt1.csv',
                    mime='text/csv',
                )

# === PAGE À PROPOS ===
else:
    st.header("À propos du projet")

    st.subheader("🎓 Contexte académique")
    st.write("""
    Ce projet a été développé dans le cadre d'un **mémoire de Master 2** en
    Physique Atomique, Moléculaire et Biophysique.

    - **Étudiante** : Sorelle
    - **Encadrant** : Dr. TCHAPET NJAFA Jean-Pierre
    - **Conseiller** : Prof. NANA Engo
    - **Année** : 2025-2026
    """)

    st.subheader("🔬 Méthodologie")
    st.write("""
    - **Dataset** : 1000 patients synthétiques (distributions réalistes)
    - **Algorithmes testés** : Random Forest, XGBoost, LightGBM, SVM
    - **Métriques** : Recall (sensibilité) prioritaire, AUC-ROC
    - **Interprétabilité** : SHAP, LIME
    """)

    st.subheader("📚 Références scientifiques")
    st.markdown("""
    - Katte et al. (2023) - Phénotype DT1 en Afrique subsaharienne
    - Mbanya et al. (2010) - Diabète en Afrique subsaharienne (*The Lancet*)
    - Zhang et al. (2022) - Biomarqueurs DT1 par bioinformatique
    """)

    st.subheader("📞 Contact")
    st.info("Pour plus d'informations, contacter Dr. TCHAPET NJAFA Jean-Pierre")

    st.markdown("---")
    st.caption("© 2025 - Projet DT1 Cameroun - Master 2 Biophysique")

# === FOOTER ===
st.sidebar.markdown("---")
st.sidebar.caption("🇨🇲 Fait au Cameroun, pour le Cameroun")
st.sidebar.caption("Version 1.0 - Novembre 2025")
