import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import base64
import os

# Configuration de la page
st.set_page_config(
    page_title="Dépistage Précoce DT1 - Cameroun",
    page_icon="🇨🇲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chemins (relatifs à la racine du projet ou ajustables)
MODEL_PATH = '../4_MODELES/models/final_model.pkl'
FEATURES_PATH = '../4_MODELES/models/features.pkl'

# --- FONCTIONS UTILITAIRES ---

def load_css():
    st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            width: 100%;
        }
        .metric-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Charge le modèle et la liste des features"""
    try:
        model = joblib.load(MODEL_PATH)
        # Tenter de charger les features sauvegardées, sinon utiliser la liste par défaut
        try:
            features = joblib.load(FEATURES_PATH)
        except:
            features = ['age', 'IMC', 'glycemie_jeun', 'HbA1c', 'ANP32A_IT1', 'ESCO2', 'NBPF1']
        return model, features
    except FileNotFoundError:
        return None, None

def predict_patient(model, features, data):
    """Effectue une prédiction pour un patient"""
    # S'assurer que les données sont dans le bon ordre des features
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = data
    
    # Vérifier et ordonner les colonnes
    df = df[features]
    
    # Prédiction (0=Sain, 1=DT1)
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    return prediction, probability

def generate_pdf(results):
    """Génère un rapport PDF simple"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Rapport de Dépistage - Diabète Type 1", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Date: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Informations Patient:", 0, 1)
    pdf.set_font("Arial", '', 12)
    for key, value in results['data'].items():
        pdf.cell(0, 8, f"{key}: {value}", 0, 1)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    status = "Risque ÉLEVÉ (Positif)" if results['prediction'] == 1 else "Risque FAIBLE (Négatif)"
    color = (255, 0, 0) if results['prediction'] == 1 else (0, 128, 0)
    pdf.set_text_color(*color)
    pdf.cell(0, 10, f"Résultat: {status}", 0, 1)
    pdf.set_text_color(0, 0, 0)
    
    pdf.cell(0, 10, f"Probabilité estimée: {results['probability']*100:.1f}%", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE PRINCIPALE ---

def main():
    load_css()
    
    # Sidebar
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Flag_of_Cameroon.svg/1200px-Flag_of_Cameroon.svg.png", width=100)
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Aller vers", ["Accueil", "Prédictions", "Base de Données", "À propos"])
    
    st.sidebar.markdown("---")
    st.sidebar.info("Projet Master 2 - Sorelle Perelle Nguisakam \nUniversité de Yaoundé I")

    model, model_features = load_model()

    if page == "Accueil":
        st.title("Dépistage Précoce du Diabète de Type 1 🏥")
        st.subheader("Contexte Africain & Camerounais")
        
        st.markdown("""
        Cette application démontre l'utilisation de l'Intelligence Artificielle pour le diagnostic précoce du DT1.
        
        **Objectifs :**
        *   Identifier les patients à risque avant l'apparition des symptômes graves.
        *   Utiliser des biomarqueurs génétiques spécifiques (ESCO2, ANP32A-IT1) et cliniques.
        *   Fournir un outil d'aide à la décision pour les cliniciens.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", caption="Recherche Médicale")
        with col2:
            st.info("""
            **Le saviez-vous ?**
            En Afrique subsaharienne, le diagnostic du DT1 est souvent tardif, entraînant des complications sévères.
            Ce modèle IA vise à changer la donne en intégrant la génétique locale.
            """)

    elif page == "Prédictions":
        if model is None:
            st.error("⚠️ Modèle non trouvé ! Veuillez exécuter le script d'entraînement `4_SCRIPTS_PRODUCTION/train_model_week6.py` d'abord.")
            return

        st.title("Module de Prédiction 🧬")
        st.markdown("Remplissez les informations cliniques et génétiques du patient.")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Données Patient")
            form = st.form("patient_form")
            age = form.number_input("Âge (années)", min_value=0, max_value=120, value=25)
            imc = form.number_input("IMC (kg/m²)", min_value=10.0, max_value=50.0, value=22.0)
            glycemie = form.number_input("Glycémie à jeun (mg/dL)", min_value=50, max_value=400, value=90)
            hba1c = form.number_input("HbA1c (%)", min_value=4.0, max_value=15.0, value=5.5)
            
            st.markdown("**Biomarqueurs Génétiques (Expression Relative)**")
            anp32 = form.number_input("ANP32A_IT1", value=1.0)
            esco2 = form.number_input("ESCO2", value=1.0)
            nbpf1 = form.number_input("NBPF1", value=1.0)
            
            submit = form.form_submit_button("Lancer l'analyse IA 🚀")

        with col2:
            if submit:
                # Préparer les données
                input_data = {
                    'age': age,
                    'IMC': imc,
                    'glycemie_jeun': glycemie,
                    'HbA1c': hba1c,
                    'ANP32A_IT1': anp32,
                    'ESCO2': esco2,
                    'NBPF1': nbpf1
                }
                
                # Prédiction
                pred, proba = predict_patient(model, model_features, input_data)
                
                # Affichage Résultats
                st.subheader("Résultats de l'Analyse")
                
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    if pred == 1:
                        st.error(f"### Risque ÉLEVÉ (Positif)")
                        st.markdown(f"**Probabilité de DT1 :** {proba*100:.1f}%")
                    else:
                        st.success(f"### Risque FAIBLE (Négatif)")
                        st.markdown(f"**Probabilité de DT1 :** {proba*100:.1f}%")
                
                with res_col2:
                    # Jauge de risque (Gauge Chart)
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = proba * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Niveau de Risque (%)"},
                        gauge = {
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "darkred" if pred==1 else "green"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgreen"},
                                {'range': [50, 100], 'color': "salmon"}],
                            'threshold': {
                                'line': {'color': "black", 'width': 4},
                                'thickness': 0.75,
                                'value': 50}}))
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                st.subheader("Interprétabilité (Pourquoi cette décision ?)")
                st.info("Ici s'afficherait le graphique SHAP Force Plot pour expliquer la contribution de chaque variable (Simulation pour la démo).")
                
                # Simulation simple de l'impact
                contributions = {
                    'Glycémie': (glycemie - 100) / 100,
                    'HbA1c': (hba1c - 5.7) / 2,
                    'ESCO2': (esco2 - 1.0) * 0.5
                }
                feature_imp = pd.DataFrame.from_dict(contributions, orient='index', columns=['Impact Relatif'])
                st.bar_chart(feature_imp)

                # Export PDF
                st.markdown("### Rapports")
                results_data = {'data': input_data, 'prediction': int(pred), 'probability': proba}
                pdf_bytes = generate_pdf(results_data)
                b64 = base64.b64encode(pdf_bytes).decode('latin-1')
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="rapport_patient.pdf" class="stButton">📥 Télécharger le Rapport PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
    
    elif page == "À propos":
        st.title("À propos")
        st.write("Application développée dans le cadre du Mémoire de Master 2 Biophysique.")
        st.write("Contact: Sorelle Perelle Nguisakam")

if __name__ == "__main__":
    main()
