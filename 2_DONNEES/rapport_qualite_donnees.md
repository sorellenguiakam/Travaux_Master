# Rapport Qualité des Données - Semaine 2

## 1. Vue d'ensemble
- **Source** : `dataset_dt1_cameroun_synthetic.csv`
- **Dimensions initiales** : 1000 patients, 12 variables
- **Variable cible** : `diagnostic` (0=Sain, 1=DT1)
- **Taux de prévalence initial** : 25.0%

## 2. Nettoyage des Données
- **Valeurs manquantes** :
  - Variables numériques : Imputation par la médiane.
  - Variables catégorielles : Imputation par la valeur la plus fréquente (si nécessaire).
- **Outliers** :
  - Traitement par capping (Winsorization) aux seuils [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
  - Variables concernées : ANP32A_IT1, ESCO2, NBPF1, glycemie_jeun, HbA1c, IMC, age.
- **Standardisation** :
  - Sexe : Harmonisation majuscules/espaces.
  - Région : Titre case.

## 3. Feature Engineering
- **Nouvelles variables créées** :
  - `ratio_esco2_anp32a` : Ratio entre biomarqueurs ESCO2 et ANP32A-IT1.
  - `age_groupe` : Catégorisation (enfant <18, jeune 18-30, adulte >30).
- **Encodage** :
  - One-Hot Encoding pour `sexe`, `region`, `age_groupe`.
- **Normalisation** :
  - StandardScaler appliqué sur toutes les variables numériques pour mise à l'échelle (moyenne=0, écart-type=1).

## 4. Préparation pour le Machine Learning
- **Dimensions finales** : 1000 samples, 20 features (après One-Hot).
- **Séparation des jeux de données (Stratifiée)** :
  - **Train** : 600 samples (60%)
  - **Validation** : 200 samples (20%)
  - **Test** : 200 samples (20%)
- **Distribution cible conservée** : ~25% de cas DT1 dans chaque sous-ensemble.

## 5. Conclusion
Les données sont propres, structurées et prêtes pour la phase de modélisation (Semaine 3). Les fichiers sont sauvegardés dans `2_DONNEES/processed/`.
