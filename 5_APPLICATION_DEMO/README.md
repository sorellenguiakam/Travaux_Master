# 🖥️ APPLICATION DÉMONSTRATION - STREAMLIT

Application web interactive pour la détection précoce du Diabète Type 1 au Cameroun.

## 🚀 Lancement

```bash
# Installer les dépendances
pip install -r requirements_app.txt

# Lancer l'application
streamlit run app_streamlit.py

# L'application s'ouvre dans votre navigateur
# URL: http://localhost:8501
```

## 📱 Fonctionnalités

### Page 1: Accueil
- Présentation du projet
- Contexte DT1 au Cameroun
- Description des biomarqueurs

### Page 2: Prédiction
**Mode manuel:**
- Saisie manuelle des 7 features
- Prédiction instantanée (DT1+ ou Sain)
- Affichage probabilité

**Mode batch (CSV):**
- Upload fichier CSV
- Prédictions multiples
- Téléchargement résultats

### Page 3: À propos
- Informations projet
- Méthodologie
- Contacts

## 📊 Format des données CSV

Pour le mode batch, le fichier doit contenir les colonnes:

```csv
age,IMC,glycemie_jeun,HbA1c,ANP32A_IT1,ESCO2,NBPF1
25,22.5,6.2,5.8,1.5,2.3,1.2
30,28.0,7.5,6.5,3.8,4.2,2.8
```

## 🧠 Modèle utilisé

**Algorithme:** XGBoost optimisé  
**Métriques:**
- Recall: >85%
- Precision: >70%
- AUC-ROC: >0.90

**Modèle sauvegardé:** `../4_MODELES/models/final_model.pkl`

## ⚠️ Avertissement

**Application de démonstration uniquement.**  
Ne pas utiliser pour diagnostic clinique réel.  
Données synthétiques - validation sur données réelles nécessaire.

---
*Projet Master 2 - Sorelle - 2025/2026*
