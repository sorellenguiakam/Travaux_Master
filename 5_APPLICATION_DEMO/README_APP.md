# Application de Démonstration - Dépistage DT1

Ce dossier contient l'application Streamlit démontrant le modèle de Machine Learning pour la détection précoce du Diabète de Type 1.

## Installation

1. Assurez-vous d'avoir Python 3.8+ installé.
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Pré-requis

Le modèle doit être entraîné avant de lancer l'application. Si ce n'est pas fait :
1. Exécutez le script d'entraînement :
   ```bash
   python ../4_SCRIPTS_PRODUCTION/train_model_week6.py
   ```
   Cela générera `../4_MODELES/models/final_model.pkl`.

## Lancement

Pour démarrer l'application :
```bash
streamlit run app_streamlit.py
```

## Fonctionnalités

*   **Accueil** : Contexte du projet.
*   **Prédictions** : Formulaire interactif pour entrer les données d'un patient (Âge, IMC, Glycémie, Génétique...).
*   **Visualisation** : Jauge de risque et probabilité.
*   **Rapport** : Génération automatique d'un rapport PDF téléchargeable.
