# 🔧 SCRIPTS DE PRODUCTION - DT1 CAMEROUN

Ce dossier contient les scripts finaux optimisés pour la détection précoce du Diabète de Type 1 au Cameroun.

## 📁 Structure Complète

```
4_SCRIPTS_PRODUCTION/
├── config.yaml              # Configuration centralisée du pipeline
├── pipeline_complet.py      # Script principal d'exécution
├── models/                  # Modèles ML sauvegardés (après entraînement)
│   ├── final_model.pkl      # Meilleur modèle
│   ├── features.pkl         # Liste des features
│   ├── scaler.pkl           # StandardScaler
│   └── rapport_modele_final.txt  # Rapport de performances
├── utils/                   # Modules utilitaires
│   ├── __init__.py
│   ├── preprocessing.py     # ✅ Prétraitement des données
│   ├── evaluation.py        # ✅ Évaluation des modèles
│   ├── visualization.py     # ✅ Génération de visualisations
│   └── prediction.py        # ✅ Prédictions sur nouvelles données
└── README.md
```

## 🚀 Démarrage Rapide

### 1. Prérequis

Installez les dépendances Python :

```bash
pip install -r requirements_base.txt
```

**Packages principaux :** numpy, pandas, scikit-learn, xgboost, lightgbm, matplotlib, seaborn, shap, imbalanced-learn, pyyaml

### 2. Exécution du Pipeline Complet

Le pipeline complet entraîne plusieurs modèles ML, génère les visualisations et sauvegarde le meilleur modèle.

```bash
# Depuis le dossier 4_SCRIPTS_PRODUCTION/
python pipeline_complet.py --config config.yaml
```

**Ce que fait le pipeline :**
1. Charge les données depuis `../2_DONNEES/raw/dataset_dt1_cameroun_synthetic.csv`
2. Prétraite les données (gestion valeurs manquantes, normalisation, SMOTE)
3. Entraîne 6 modèles ML (LogisticRegression, RandomForest, XGBoost, LightGBM, SVM, KNN)
4. Évalue avec focus sur le **Recall** (métrique prioritaire en contexte médical)
5. Génère les visualisations (matrices confusion, courbes ROC, importance features)
6. Sauvegarde le meilleur modèle dans `models/`

**Durée estimée :** 5-15 minutes selon la taille des données.

## 📋 Description des Scripts

### pipeline_complet.py

**Script principal** orchestrant l'ensemble du workflow ML.

**Classes principales :**
- `PreprocesseurDonnees` : Gestion du prétraitement (imputation, normalisation, SMOTE)
- `GestionnaireModeles` : Entraînement et évaluation de multiples modèles
- `GenerateurVisualisations` : Création de toutes les visualisations

**Exemple d'utilisation :**
```bash
# Exécution standard
python pipeline_complet.py

# Avec configuration personnalisée
python pipeline_complet.py --config ma_config.yaml
```

**Logs :** Sauvegardés dans `./logs/pipeline_YYYYMMDD_HHMMSS.log`

### config.yaml

**Fichier de configuration centralisé** contenant tous les paramètres :
- Chemins des données (raw, processed, figures)
- Paramètres de prétraitement (test_size, random_state, SMOTE)
- Configuration de 6 modèles ML avec hyperparamètres
- Métriques d'évaluation (recall prioritaire)
- Contexte camerounais (régions, ethnies, seuils cliniques)

**Modifiez ce fichier** plutôt que de changer le code !

## 🔧 Modules Utilitaires (utils/)

### preprocessing.py

**Fonctions de prétraitement réutilisables :**
- `verifier_valeurs_manquantes()` - Détection de valeurs manquantes
- `imputer_valeurs_manquantes()` - Imputation (mean, median, most_frequent)
- `detecter_outliers_iqr()` - Détection d'outliers avec méthode IQR
- `encoder_variables_categorielles()` - Encodage (label, onehot)
- `normaliser_features_numeriques()` - Normalisation (StandardScaler, MinMaxScaler)
- `creer_features_biomedicales()` - Features dérivées (ratios, scores composites)
- `appliquer_smote()` - Équilibrage des classes
- `categoriser_region_cameroun()` - Regroupement des régions du Cameroun

**Exemple d'utilisation :**
```python
from utils.preprocessing import imputer_valeurs_manquantes, normaliser_features_numeriques

df_clean = imputer_valeurs_manquantes(df, strategie='median')
df_norm, scaler = normaliser_features_numeriques(df_clean)
```

### evaluation.py

**Fonctions d'évaluation des modèles :**
- `calculer_metriques_completes()` - Toutes les métriques (accuracy, precision, recall, F1, ROC-AUC, spécificité, VPP, VPN)
- `afficher_metriques()` - Affichage formaté des résultats
- `comparer_modeles()` - Tableau comparatif de plusieurs modèles
- `calculer_seuil_optimal()` - Optimisation du seuil de décision (Youden, F1, recall_90)
- `analyser_erreurs()` - Analyse des faux positifs et faux négatifs
- `evaluer_avec_validation_croisee()` - Cross-validation k-fold
- `verifier_seuils_cliniques()` - Validation des critères minimaux pour usage médical

**Exemple d'utilisation :**
```python
from utils.evaluation import calculer_metriques_completes, afficher_metriques

metriques = calculer_metriques_completes(y_test, y_pred, y_proba)
afficher_metriques(metriques, nom_modele="XGBoost")
```

### visualization.py

**Fonctions de visualisation de qualité publication :**
- `tracer_matrice_confusion()` - Matrice de confusion avec annotations
- `tracer_courbe_roc()` - Courbe ROC avec AUC
- `tracer_precision_recall()` - Courbe Précision-Recall
- `tracer_importance_features()` - Importance des features
- `tracer_distribution_biomarqueurs()` - Distributions par classe
- `tracer_matrice_correlation()` - Heatmap de corrélation
- `tracer_comparaison_modeles()` - Graphique comparatif multi-modèles
- `generer_rapport_visuel_complet()` - Génère toutes les visualisations en une fois

**Exemple d'utilisation :**
```python
from utils.visualization import tracer_matrice_confusion, tracer_courbe_roc

tracer_matrice_confusion(y_test, y_pred, sauvegarder='confusion.png')
tracer_courbe_roc(y_test, y_proba, sauvegarder='roc.png')
```

### prediction.py

**Pipeline de prédiction sur nouvelles données :**

**Classe `PredicteurDT1` :**
- Charge automatiquement le modèle, scaler et features depuis `models/`
- Méthode `predire()` : Prédiction sur un patient (dict ou DataFrame)
- Méthode `predire_batch()` : Prédictions sur fichier CSV
- Méthode `generer_rapport_patient()` : Rapport détaillé pour un patient

**Exemple d'utilisation :**
```python
from utils.prediction import PredicteurDT1

# Initialiser le prédicteur
predicteur = PredicteurDT1(dossier_modele='./models')

# Prédire pour un patient
patient = {
    'age': 28,
    'sexe': 1,
    'IMC': 24.5,
    'glycemie_jeun': 7.8,
    'ANP32A_IT1': 4.2,
    'ESCO2': 3.8,
    'NBPF1': 3.5,
    'antecedents_familiaux': 1,
    'ethnie': 2
}

resultat = predicteur.predire(patient)
print(resultat)
# {'prediction': 'DT1+', 'probabilite_DT1': 0.87, 'confiance': 'Élevée', ...}

# Générer rapport complet
predicteur.generer_rapport_patient(patient, sauvegarder='rapport_patient.txt')

# Prédictions batch
df_predictions = predicteur.predire_batch('nouveaux_patients.csv')
```

## 📊 Modèles ML Disponibles

Le pipeline entraîne et compare **6 modèles** :

1. **Logistic Regression** (baseline) - Rapide, interprétable
2. **Random Forest** - Robuste, gère non-linéarités
3. **XGBoost** - Haute performance, feature importance
4. **LightGBM** - Très rapide, équivalent XGBoost
5. **SVM** (désactivé par défaut) - Lent sur gros datasets
6. **K-Nearest Neighbors** - Simple, non-paramétrique

**Configuration :** Modifiez `config.yaml` section `modeles:` pour activer/désactiver ou ajuster les hyperparamètres.

## 🎯 Contexte Médical

### Priorité: Maximiser le Recall (Sensibilité)

Dans le contexte de la détection précoce du DT1, **manquer un patient malade (Faux Négatif) est plus grave qu'un faux positif**, car cela peut entraîner un retard de traitement et des complications mortelles (acidocétose diabétique).

**Objectifs minimaux :**
- Recall (Sensibilité) ≥ 0.85
- ROC-AUC ≥ 0.80
- Taux de Faux Négatifs ≤ 0.15

### Spécificités Cameroun

Le fichier `config.yaml` intègre le contexte camerounais :
- **10 régions** (Centre, Littoral, Ouest, etc.)
- **Ethnies principales** (Bamileke, Ewondo, Bassa, Douala, Fulani)
- **Seuils cliniques adaptés** (glycémie à jeun, HbA1c, IMC)

## 📈 Résultats Attendus

Après exécution du pipeline, vous obtiendrez :

### Modèles Sauvegardés (`models/`)
- `final_model.pkl` - Meilleur modèle (selon Recall)
- `scaler.pkl` - StandardScaler pour normalisation
- `features.pkl` - Liste ordonnée des features
- `rapport_modele_final.txt` - Rapport détaillé de performances

### Visualisations (`../6_MEMOIRE_LATEX/figures/`)
- `matrices_confusion.png` - Matrices de confusion de tous les modèles
- `courbes_roc.png` - Courbes ROC comparatives
- `importance_features.png` - Importance des features du meilleur modèle

### Logs (`logs/`)
- `pipeline_YYYYMMDD_HHMMSS.log` - Log complet de l'exécution

## ⚠️ Avertissements Importants

1. **Données Synthétiques** : Le modèle actuel est entraîné sur des données synthétiques générées à partir de distributions réalistes. Validation sur données réelles camerounaises **OBLIGATOIRE** avant tout déploiement clinique.

2. **Aide au Diagnostic** : Cet outil est une **aide à la décision médicale**, pas un remplacement de l'expertise d'un endocrinologue qualifié.

3. **Éthique** : Toute utilisation clinique doit respecter les normes éthiques et légales du Cameroun en matière de dispositifs médicaux.

4. **Validation Externe** : Le modèle doit être validé sur une cohorte camerounaise indépendante avant utilisation en pratique clinique.

## 🔧 Dépannage

### Erreur: "ModuleNotFoundError"
```bash
# Vérifier que l'environnement Python est activé
# Réinstaller les dépendances
pip install -r requirements_base.txt
```

### Erreur: "FileNotFoundError: dataset_dt1_cameroun_synthetic.csv"
```bash
# Vérifier que les données sont dans le bon dossier
ls ../2_DONNEES/raw/

# Si absent, générer les données synthétiques (voir ../2_DONNEES/scripts_generation/)
```

### Erreur: "CUDA/GPU not available" (pour XGBoost/LightGBM)
C'est normal si vous n'avez pas de GPU. Les modèles fonctionnent aussi sur CPU (plus lent mais fonctionne).

### Performances faibles (Recall < 0.80)
1. Vérifier la qualité des données (valeurs manquantes, outliers)
2. Ajuster les hyperparamètres dans `config.yaml`
3. Essayer d'augmenter le ratio SMOTE (section `preprocessing.smote_ratio`)
4. Utiliser l'optimisation d'hyperparamètres (section `optimization`)

## 📚 Références

**Biomarqueurs DT1 :**
- ANP32A-IT1, ESCO2, NBPF1 : Marqueurs génétiques prometteurs pour la prédiction du DT1 dans les populations africaines

**Machine Learning médical :**
- Priorité au Recall dans les tâches de dépistage médical
- Utilisation de SMOTE pour gérer le déséquilibre des classes
- Validation croisée et métriques adaptées au contexte clinique

## 📞 Support

**Pour toute question sur ce projet :**
- **Superviseur :** Dr. TCHAPET NJAFA Jean-Pierre
- **Institution :** Université de Yaoundé I, Cameroun
- **Département :** Physique (Physique Atomique, Moléculaire et Biophysique)

---

**Version :** 1.0 (Novembre 2025)
**Auteur :** Dr. TCHAPET NJAFA Jean-Pierre avec assistance Claude Code
**Projet :** Master 2 - Détection Précoce DT1 au Cameroun (14 semaines)
