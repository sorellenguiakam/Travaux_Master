# Scripts de Production - Pipeline ML Diabète Type 1

**Auteure:** Sorelle
**Encadrant:** Dr. Jean-Pierre TCHAPET

## Vue d'ensemble

Ce répertoire contient 6 scripts Python formant un pipeline complet de machine learning pour la détection précoce du Diabète de Type 1 (DT1) chez les populations camerounaises, basé sur des biomarqueurs génétiques.

## Architecture du pipeline

```
01_generer_dataset.py    →  Génération données synthétiques
           ↓
02_eda.py               →  Analyse exploratoire
           ↓
03_preprocessing.py     →  Prétraitement et normalisation
           ↓
04_train_models.py      →  Entraînement modèles ML
           ↓
05_interpretability.py  →  Analyse SHAP et interprétabilité
           ↓
06_validation.py        →  Validation clinique finale
```

## Scripts détaillés

### Script 01: Génération Dataset
**Fichier:** `01_generer_dataset.py`
**Temps d'exécution:** ~10 secondes
**Mémoire:** ~50 MB

**Fonction:**
- Génère 1000 patients synthétiques (850 sains, 150 DT1)
- Distributions réalistes basées sur littérature scientifique
- 16 features incluant 3 biomarqueurs génétiques clés

**Biomarqueurs génétiques:**
- **ANP32A-IT1:** Surexpression associée au DT1
- **ESCO2:** Sous-expression associée au DT1
- **NBPF1:** Marqueur complémentaire

**Sortie:** `../raw/dataset_dt1_cameroun.csv`

**Usage:**
```bash
cd 2_DONNEES/scripts_production
python 01_generer_dataset.py
```

---

### Script 02: Analyse Exploratoire (EDA)
**Fichier:** `02_eda.py`
**Temps d'exécution:** ~1 minute
**Mémoire:** ~100 MB

**Fonction:**
- Statistiques descriptives (moyennes, écarts-types, min/max)
- Répartition diagnostic DT1 vs Sains
- 3 visualisations clés

**Visualisations générées:**
1. `01_distributions_biomarqueurs.png` - Histogrammes superposés
2. `02_matrice_correlations.png` - Heatmap corrélations
3. `03_boxplots_comparaison.png` - Comparaison DT1 vs Sains

**Sortie:** `../processed/figures/`

**Usage:**
```bash
python 02_eda.py
```

---

### Script 03: Prétraitement
**Fichier:** `03_preprocessing.py`
**Temps d'exécution:** ~10 secondes
**Mémoire:** ~100 MB

**Fonction:**
- Vérification qualité données (valeurs manquantes, aberrantes)
- Séparation features (X) et target (y)
- Split train/test stratifié (80/20)
- Normalisation StandardScaler (fit sur train uniquement)

**Sorties:**
- `../processed/X_train.csv` (800 patients)
- `../processed/X_test.csv` (200 patients)
- `../processed/y_train.csv`
- `../processed/y_test.csv`
- `../processed/scaler.pkl` (pour production)
- `../processed/preprocessing_metadata.json`

**Usage:**
```bash
python 03_preprocessing.py
```

---

### Script 04: Entraînement Modèles
**Fichier:** `04_train_models.py`
**Temps d'exécution:** ~3-5 minutes
**Mémoire:** ~200 MB

**Fonction:**
- Entraîne 4 algorithmes de ML
- Optimisation hyperparamètres via GridSearchCV
- Cross-validation 5-fold
- Sélection meilleur modèle basé sur F1-score

**Algorithmes:**
1. **Logistic Regression** (baseline)
2. **Random Forest** (arbres)
3. **XGBoost** (gradient boosting)
4. **SVM** (support vectors)

**Sorties:**
- `../models/best_model.pkl` (meilleur modèle)
- `../models/training_results.json` (tous résultats)
- `../models/models_comparison.csv` (tableau comparatif)

**Usage:**
```bash
python 04_train_models.py
```

**Note:** Utilise `n_jobs=-1` pour parallélisation multi-core

---

### Script 05: Interprétabilité
**Fichier:** `05_interpretability.py`
**Temps d'exécution:** ~2-3 minutes
**Mémoire:** ~150 MB

**Fonction:**
- Analyse importance features (si modèle basé arbres)
- Calcul valeurs SHAP (SHapley Additive exPlanations)
- Analyse spécifique des 3 biomarqueurs génétiques
- 5 visualisations détaillées

**Visualisations générées:**
1. `01_feature_importance.png` - Top 15 features importantes
2. `02_shap_summary_bar.png` - Importance globale SHAP
3. `03_shap_summary_beeswarm.png` - Distribution impact features
4. `04_shap_waterfall_dt1.png` - Explication patient DT1 individuel
5. `05_biomarqueurs_shap_analysis.png` - Focus ANP32A/ESCO2/NBPF1

**Sorties:** `../interpretability/`

**Usage:**
```bash
python 05_interpretability.py
```

**Note:** Échantillon limité à 100 patients pour performance SHAP

---

### Script 06: Validation Clinique
**Fichier:** `06_validation.py`
**Temps d'exécution:** ~1-2 minutes
**Mémoire:** ~150 MB

**Fonction:**
- Métriques cliniques détaillées
- Intervalles confiance 95% (bootstrap 1000 itérations)
- Analyse robustesse sous-groupes (âge, sexe)
- Courbe ROC
- Rapport validation complet

**Métriques cliniques:**
- Accuracy, Sensibilité, Spécificité
- PPV (Positive Predictive Value)
- NPV (Negative Predictive Value)
- Likelihood Ratios (LR+, LR-)
- ROC-AUC

**Sorties:**
- `../validation/validation_report.json` (données structurées)
- `../validation/validation_summary.txt` (rapport lisible)
- `../validation/roc_curve.png`

**Usage:**
```bash
python 06_validation.py
```

---

## Installation dépendances

```bash
pip install numpy pandas matplotlib seaborn scikit-learn xgboost shap joblib scipy
```

**Versions recommandées:**
- Python: 3.8+
- scikit-learn: 1.3+
- xgboost: 2.0+
- shap: 0.42+

## Exécution complète du pipeline

```bash
cd 2_DONNEES/scripts_production

# Étape 1: Générer dataset
python 01_generer_dataset.py

# Étape 2: Analyse exploratoire
python 02_eda.py

# Étape 3: Prétraitement
python 03_preprocessing.py

# Étape 4: Entraînement modèles (le plus long)
python 04_train_models.py

# Étape 5: Interprétabilité
python 05_interpretability.py

# Étape 6: Validation clinique
python 06_validation.py
```

**Ou en une seule commande:**
```bash
for i in {01..06}; do
  python ${i}_*.py
done
```

## Structure des sorties

```
2_DONNEES/
├── raw/
│   ├── dataset_dt1_cameroun.csv          (1000 patients × 16 features)
│   └── metadata.json
│
├── processed/
│   ├── figures/                          (3 visualisations EDA)
│   ├── X_train.csv, X_test.csv
│   ├── y_train.csv, y_test.csv
│   ├── scaler.pkl
│   └── preprocessing_metadata.json
│
├── models/
│   ├── best_model.pkl                    (meilleur modèle entraîné)
│   ├── training_results.json
│   └── models_comparison.csv
│
├── interpretability/
│   ├── 01_feature_importance.png
│   ├── 02-05_shap_*.png
│   └── feature_importance.csv
│
└── validation/
    ├── validation_report.json
    ├── validation_summary.txt
    └── roc_curve.png
```

## Résultats attendus

### Performances typiques (données synthétiques)

| Métrique      | Valeur attendue |
|---------------|-----------------|
| Accuracy      | 0.85 - 0.95     |
| Sensibilité   | 0.80 - 0.95     |
| Spécificité   | 0.85 - 0.95     |
| F1-Score      | 0.75 - 0.90     |
| ROC-AUC       | 0.90 - 0.98     |

**Note:** Ces résultats sont sur données synthétiques. Validation sur cohortes réelles requise.

## Ressources matérielles

### Configuration requise

| Ressource        | Minimum  | Recommandé | Utilisé (pic) |
|------------------|----------|------------|---------------|
| RAM              | 2 GB     | 4 GB       | ~200 MB       |
| Processeur       | 2 cores  | 4+ cores   | Parallèle OK  |
| Espace disque    | 100 MB   | 500 MB     | ~250 MB       |
| Temps total      | -        | -          | 5-10 minutes  |

### Configuration testée

- **Processeur:** Intel Core i7 11e génération
- **RAM:** 32 GB (marge 160×)
- **Résultat:** ✅ 100% compatible

## Notes importantes

### 1. Données synthétiques vs réelles
Les scripts utilisent des **données synthétiques** générées selon distributions scientifiques. Pour utilisation clinique:
- Remplacer `01_generer_dataset.py` par import données réelles
- Conserver format CSV avec mêmes colonnes
- Adapter scripts 02-06 si nécessaire

### 2. Biomarqueurs génétiques
Les 3 biomarqueurs (ANP32A-IT1, ESCO2, NBPF1) sont basés sur:
- Étude TEDDY (USA/Europe)
- Limitation: populations caucasiennes majoritaires
- **Objectif thèse:** Valider pertinence populations africaines

### 3. Interprétabilité médicale
L'analyse SHAP (script 05) répond à la question:
> "Pourquoi le modèle prédit DT1 pour ce patient?"

Essentiel pour:
- Confiance cliniciens
- Acceptabilité éthique
- Compréhension mécanismes biologiques

### 4. Prochaines étapes
Après validation synthétique:
1. Collaboration centres médicaux Yaoundé
2. Recrutement cohorte prospective
3. Validation externe (autres régions Cameroun)
4. Étude coût-efficacité

## Troubleshooting

### Erreur: "Fichier introuvable"
```bash
# Vérifier ordre exécution
ls ../raw/dataset_dt1_cameroun.csv  # Doit exister après script 01
```

### Erreur: "ImportError: No module named 'xgboost'"
```bash
pip install xgboost
```

### Performance lente (Script 04)
```bash
# Réduire grille hyperparamètres dans 04_train_models.py
# Ou augmenter `n_jobs` dans GridSearchCV
```

### SHAP prend trop de temps (Script 05)
```python
# Ligne 81 dans 05_interpretability.py
shap_values, X_test_sample = calculer_shap_values(model, X_test, max_samples=50)
# Réduire max_samples de 100 à 50
```

## Références scientifiques

1. **ANP32A-IT1 et DT1:**
   TEDDY Study Group. *The Environmental Determinants of Diabetes in the Young (TEDDY) Study*. Diabetes Care, 2015.

2. **ESCO2 biomarqueur:**
   Evangelou M, et al. *Genetic analysis of over 1 million people identifies 535 new loci associated with blood pressure traits*. Nature Genetics, 2018.

3. **SHAP interprétabilité:**
   Lundberg SM, Lee SI. *A unified approach to interpreting model predictions*. NeurIPS 2017.

## Contact

**Étudiante:** Sorelle
**Encadrant:** Dr. TCHAPET NJAFA Jean-Pierre
**Email:** jean-pierre.tchapet@facsciences-uy1.cm
**Institution:** Université de Yaoundé I, Cameroun

---

**Dernière mise à jour:** Novembre 2025
