# 📚 NOTEBOOKS PÉDAGOGIQUES

Ce dossier contient les **6 notebooks Jupyter** du projet, conçus pour un apprentissage progressif du Machine Learning appliqué à la détection du DT1.

## 📖 Liste des notebooks

### Semaine 1: Introduction Python + ML
**Fichier:** `Semaine01_Introduction_Python_ML.ipynb`  
**Durée:** 12-14 heures  
**Contenu:**
- NumPy (vecteurs, matrices)
- Pandas (DataFrame, manipulation)
- Matplotlib (visualisation)
- Premier modèle: Decision Tree

### Semaine 2: Exploration des données
**Fichier:** `Semaine02_Exploration_Donnees.ipynb`  
**Durée:** 12-14 heures  
**Contenu:**
- Statistiques descriptives
- Tests statistiques (Shapiro-Wilk, Mann-Whitney)
- Matrice de corrélation
- Distributions et visualisations

### Semaine 3: Modélisation simple
**Fichier:** `Semaine03_Modelisation_Simple.ipynb`  
**Durée:** 12-14 heures  
**Contenu:**
- 4 algorithmes de base: Logistic Regression, Decision Tree, Random Forest, SVM
- Métriques d'évaluation
- Courbes ROC

### Semaines 4-5: Modèles avancés
**Fichier:** `Semaine04-05_Modeles_Avances.ipynb`  
**Durée:** 20-24 heures  
**Contenu:**
- XGBoost (avec scale_pos_weight)
- LightGBM (avec class_weight)
- SMOTE (gestion déséquilibre)
- Comparaisons

### Semaine 6: Optimisation
**Fichier:** `Semaine06_Optimisation_Validation.ipynb`  
**Durée:** 12-14 heures  
**Contenu:**
- Validation croisée (Stratified K-Fold)
- GridSearchCV (Random Forest)
- RandomizedSearchCV (XGBoost)
- Sauvegarde modèle final

### Semaine 7: Interprétabilité
**Fichier:** `Semaine07_Interpretation_Resultats.ipynb`  
**Durée:** 12-14 heures  
**Contenu:**
- SHAP values (TreeExplainer)
- Summary Plots, Dependence Plots, Force Plots
- Analyse des erreurs
- Génération figures pour mémoire

## 🚀 Utilisation

```bash
# Activer l'environnement
conda activate dt1_cameroun

# Lancer Jupyter
jupyter notebook

# Ouvrir le notebook souhaité
```

## 📝 Notes importantes

- **Exécuter dans l'ordre** (Semaine 1 → 7)
- Chaque notebook contient des exercices pratiques
- Les notebooks utilisent le dataset généré dans `2_DONNEES/`
- Toutes les cellules doivent s'exécuter sans erreur

---
*Projet: Détection précoce DT1 Cameroun - Master 2 Biophysique 2025/2026*
