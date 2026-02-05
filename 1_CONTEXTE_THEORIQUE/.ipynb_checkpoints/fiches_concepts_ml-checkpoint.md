# 📚 FICHES DE CONCEPTS - MACHINE LEARNING

Glossaire illustré des concepts essentiels pour votre projet de Master 2.

---

## 🤖 QU'EST-CE QUE LE MACHINE LEARNING ?

**Définition** : Branche de l'Intelligence Artificielle où les machines "apprennent" à partir de données sans être explicitement programmées.

**Analogie** : Comme un enfant apprend à reconnaître un chat en voyant beaucoup d'exemples de chats, un algorithme ML apprend à reconnaître des patterns en voyant beaucoup d'exemples.

**Types de ML** :
1. **Supervisé** : Apprendre avec des exemples étiquetés (notre cas : patients DT1+ ou DT1-)
2. **Non-supervisé** : Trouver des structures cachées sans étiquettes
3. **Par renforcement** : Apprendre par essai-erreur avec récompenses

---

## 📊 CONCEPTS FONDAMENTAUX

### 1. Features (Variables, Caractéristiques)

**Définition** : Les inputs du modèle, les mesures/attributs utilisés pour prédire.

**Dans notre projet** :
- ANP32A-IT1, ESCO2, NBPF1 (biomarqueurs génétiques)
- Âge, sexe, région (démographie)
- Autres variables cliniques

**Notation mathématique** :
- Une feature = `x`
- Plusieurs features = vecteur `X = [x₁, x₂, ..., xₙ]`
- Pour m patients : matrice `X` de taille `(m, n)`

**Exemple** :
```
Patient 1: [age=25, sexe=F, ESCO2=3.2, ANP32A=1.5, ...]
Patient 2: [age=30, sexe=M, ESCO2=2.1, ANP32A=2.3, ...]
```

---

### 2. Labels (Étiquettes, Classes)

**Définition** : L'output qu'on veut prédire, la "bonne réponse".

**Dans notre projet** :
- `0` = DT1- (patient sain)
- `1` = DT1+ (patient diabétique)

**Notation** :
- Un label = `y`
- Plusieurs labels = vecteur `y = [y₁, y₂, ..., yₘ]`

---

### 3. Dataset (Jeu de Données)

**Définition** : Collection de données utilisée pour entraîner et tester le modèle.

**Structure** :
```
┌──────────┬─────┬──────┬───────┬─────────┬───────────┐
│ ID       │ Âge │ Sexe │ ESCO2 │ ANP32A  │ Diagnostic│
├──────────┼─────┼──────┼───────┼─────────┼───────────┤
│ PAT001   │ 25  │ F    │ 3.2   │ 1.5     │ 0         │
│ PAT002   │ 30  │ M    │ 5.8   │ 4.2     │ 1         │
│ ...      │ ... │ ...  │ ...   │ ...     │ ...       │
└──────────┴─────┴──────┴───────┴─────────┴───────────┘
      ↑                Features                  ↑
      ID                                      Label
```

**Dimensions** :
- Lignes = exemples/patients (m)
- Colonnes = features (n)
- Notre projet : ~1000 patients, ~25 features

---

## 🔄 WORKFLOW MACHINE LEARNING

### Les 5 Étapes Essentielles

```
1. COLLECTER   →   2. PRÉPARER   →   3. ENTRAÎNER   →   4. ÉVALUER   →   5. PRÉDIRE
   Données          Nettoyer          Modèle           Performance        Nouveaux cas
```

**Détails** :

**1. Collecter les données**
- Rassembler dataset (ici: biomarqueurs patients camerounais)
- Vérifier qualité, quantité suffisante

**2. Préparer les données** (80% du temps !)
- Nettoyer (valeurs manquantes, outliers)
- Standardiser (même échelle)
- Encoder (texte → nombres)
- Séparer train/test

**3. Entraîner le modèle**
- Choisir algorithme (Random Forest, XGBoost, etc.)
- Le modèle "apprend" les patterns dans les données train
- Ajuster hyperparamètres

**4. Évaluer la performance**
- Tester sur données test (non vues pendant l'entraînement)
- Calculer métriques (Accuracy, Recall, etc.)
- Diagnostiquer problèmes (overfitting, etc.)

**5. Prédire sur nouveaux cas**
- Utiliser le modèle entraîné sur de nouveaux patients
- Déployer en production (notre application Streamlit)

---

## 🎯 TRAIN / VALIDATION / TEST SPLIT

**Pourquoi séparer ?** Pour évaluer honnêtement la performance sur données non vues.

### Proportions typiques
```
Total Dataset (100%)
│
├─ 60% TRAIN      : Entraîner le modèle
├─ 20% VALIDATION : Ajuster hyperparamètres, comparer modèles
└─ 20% TEST       : Évaluation finale (UNE SEULE FOIS !)
```

**Règle d'or** : Ne JAMAIS regarder le test set avant la fin !

**Code Python** :
```python
from sklearn.model_selection import train_test_split

# Split train/temp (80%/20%)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Split temp en validation/test (50%/50% de 20% = 10%/10% du total)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)
```

**Attention** : `stratify=y` garantit même proportion DT1+/DT1- dans chaque ensemble.

---

## 📈 CLASSIFICATION VS. RÉGRESSION

| Aspect          | Classification                     | Régression                      |
|-----------------|------------------------------------|---------------------------------|
| **Output**      | Catégorie discrète (0/1, chat/chien) | Valeur continue (prix, température) |
| **Notre projet**| DT1+ ou DT1- (classification)      | -                               |
| **Exemple**     | Spam ou Non-spam                   | Prédire le prix d'une maison    |
| **Métriques**   | Accuracy, Recall, Precision        | MSE, RMSE, R²                   |

---

## 🌳 ALGORITHMES DE CLASSIFICATION

### 1. Régression Logistique

**Principe** : Modèle linéaire avec fonction sigmoïde pour prédire probabilités.

**Avantages** :
- ✅ Très interprétable (coefficients = importance features)
- ✅ Rapide à entraîner
- ✅ Bon baseline

**Inconvénients** :
- ❌ Suppose relations linéaires
- ❌ Performances limitées sur problèmes complexes

**Quand l'utiliser** : Comme premier modèle de référence.

---

### 2. Arbres de Décision

**Principe** : Arbre de questions binaires (if-then rules).

**Exemple** :
```
                      ESCO2 > 3.0 ?
                    /              \
                 Oui                Non
                  ↓                  ↓
           ANP32A > 2.0 ?        NBPF1 > 1.5 ?
           /          \          /          \
        DT1+         DT1-      DT1+         DT1-
```

**Avantages** :
- ✅ Très visuel et intuitif
- ✅ Pas besoin de standardisation
- ✅ Capture relations non-linéaires

**Inconvénients** :
- ❌ Overfit facilement (profondeur trop grande)
- ❌ Instable (petits changements données = arbre différent)

---

### 3. Random Forest

**Principe** : "Forêt" de nombreux arbres de décision votant ensemble.

**Analogie** : Demander l'avis de 100 experts au lieu d'un seul.

**Avantages** :
- ✅ Excellentes performances "out-of-the-box"
- ✅ Réduit overfitting vs. un seul arbre
- ✅ Importance des features intégrée
- ✅ Robuste aux outliers

**Inconvénients** :
- ❌ Plus lent à entraîner
- ❌ Moins interprétable qu'un seul arbre

**Hyperparamètres clés** :
- `n_estimators` : Nombre d'arbres (50-200)
- `max_depth` : Profondeur max de chaque arbre
- `min_samples_split` : Minimum d'exemples pour split

---

### 4. Gradient Boosting (XGBoost, LightGBM)

**Principe** : Construire arbres séquentiellement, chaque arbre corrige erreurs du précédent.

**Analogie** : Équipe qui améliore son travail itérativement.

**Avantages** :
- ✅ État de l'art sur données tabulaires
- ✅ Performances exceptionnelles
- ✅ Régularisation intégrée

**Inconvénients** :
- ❌ Plus complexe à configurer
- ❌ Risque d'overfitting si mal tuné
- ❌ Plus lent (sauf LightGBM)

**Quand l'utiliser** : Pour performances maximales après Random Forest.

---

### 5. Support Vector Machines (SVM)

**Principe** : Trouver l'hyperplan qui sépare au mieux les classes.

**Avantages** :
- ✅ Efficace en haute dimension
- ✅ Marche bien avec peu de données

**Inconvénients** :
- ❌ Lent sur gros datasets
- ❌ Sensible au choix du kernel
- ❌ Difficile à interpréter

---

### 6. K-Nearest Neighbors (K-NN)

**Principe** : "Dis-moi qui sont tes voisins, je te dirai qui tu es."

**Avantages** :
- ✅ Très simple conceptuellement
- ✅ Pas de phase d'entraînement

**Inconvénients** :
- ❌ Lent en prédiction (chercher voisins)
- ❌ Sensible à l'échelle des features
- ❌ Mauvais en haute dimension

---

## 📊 MÉTRIQUES D'ÉVALUATION

### Matrice de Confusion

```
                    Prédiction
                 DT1-        DT1+
Réalité  DT1-   | TN  |     | FP  |  ← Faux Positif (erreur tolérable)
         DT1+   | FN  |     | TP  |  ← Vrai Positif (bon!)
                  ↑              ↑
         Faux Négatif    Vrai Positif
         (GRAVE!)        (objectif)

TN = True Negative  (Vrai Négatif)
TP = True Positive  (Vrai Positif)
FN = False Negative (Faux Négatif) ← À minimiser en médecine!
FP = False Positive (Faux Positif)
```

### Métriques Principales

**1. Accuracy (Exactitude)**
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```
- **Interprétation** : % de prédictions correctes
- **Limite** : Trompeuse si classes déséquilibrées
- **Exemple** : 95% accuracy mais rate 50% des DT1+ !

---

**2. Recall / Sensitivity (Sensibilité, Rappel)**
```
Recall = TP / (TP + FN)
```
- **Interprétation** : % de vrais DT1+ correctement détectés
- **Prioritaire en médecine** : On ne veut PAS manquer de malades
- **Objectif** : Maximiser le Recall !

**Exemple clinique** :
- 100 patients DT1+ réels
- Modèle détecte 85 → Recall = 85%
- 15 manqués (FN) = 15 patients non traités = grave!

---

**3. Precision (Précision)**
```
Precision = TP / (TP + FP)
```
- **Interprétation** : % de diagnostics DT1+ qui sont corrects
- **Trade-off** : Recall ↑ → Precision ↓

**Exemple** :
- Modèle prédit 100 DT1+
- 85 sont vrais, 15 sont faux → Precision = 85%
- 15 patients sains diagnostiqués à tort (FP) = examens inutiles mais moins grave que FN

---

**4. F1-Score**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```
- **Interprétation** : Moyenne harmonique Precision et Recall
- **Usage** : Équilibrer les deux métriques

---

**5. AUC-ROC (Area Under Curve)**
```
Graphique : Taux de Vrais Positifs vs. Taux de Faux Positifs
AUC : Aire sous la courbe
```
- **Valeurs** : 0.5 = hasard, 1.0 = parfait
- **Interprétation** : Capacité globale à discriminer
- **Avantage** : Indépendant du seuil de décision

**Interprétation AUC** :
- 0.90-1.00 : Excellent
- 0.80-0.90 : Très bon
- 0.70-0.80 : Bon
- 0.60-0.70 : Moyen
- 0.50-0.60 : Mauvais

---

## ⚖️ OVERFITTING VS. UNDERFITTING

### Overfitting (Sur-apprentissage)

**Symptôme** : Performance train >> Performance test

**Exemple** :
```
Train Accuracy: 99%
Test Accuracy:  65%
→ Le modèle a "mémorisé" au lieu d'apprendre
```

**Causes** :
- Modèle trop complexe (trop de paramètres)
- Pas assez de données
- Trop d'entraînement

**Solutions** :
- Régularisation (L1, L2)
- Réduire complexité modèle (max_depth, n_estimators)
- Augmenter données (SMOTE, augmentation)
- Early stopping
- Cross-validation

---

### Underfitting (Sous-apprentissage)

**Symptôme** : Performance train ET test faibles

**Exemple** :
```
Train Accuracy: 60%
Test Accuracy:  58%
→ Le modèle est trop simple
```

**Causes** :
- Modèle trop simple
- Pas assez de features
- Mauvais preprocessing

**Solutions** :
- Augmenter complexité modèle
- Ajouter features (feature engineering)
- Essayer algorithme plus puissant (Random Forest → XGBoost)

---

### Le Juste Équilibre

```
Performance
    ↑
    │         ┌─── Overfitting
    │       ╱
    │     ╱
    │   ╱  ← Sweet Spot
    │ ╱
    │─────────────────────→ Complexité
  Underfitting
```

---

## 🎛️ HYPERPARAMÈTRES

**Définition** : Paramètres fixés AVANT l'entraînement (vs. paramètres appris).

**Analogie** : Les réglages d'une recette (température four, temps cuisson) vs. le plat final.

### Exemples pour Random Forest

| Hyperparamètre      | Description                        | Valeurs typiques |
|---------------------|-----------------------------------|------------------|
| `n_estimators`      | Nombre d'arbres                   | 50-200           |
| `max_depth`         | Profondeur max arbres             | 5-15             |
| `min_samples_split` | Min exemples pour split           | 2-10             |
| `max_features`      | Features considérées par split    | 'sqrt', 'log2'   |

### Comment les trouver ?

**1. Grid Search** : Tester TOUTES les combinaisons (exhaustif, lent)
**2. Random Search** : Échantillonner aléatoirement (plus rapide)
**3. Bayesian Optimization** : Modéliser l'espace intelligemment (avancé)

---

## 🔄 VALIDATION CROISÉE (CROSS-VALIDATION)

**Problème** : Un seul split train/test peut être chanceux ou malchanceux.

**Solution** : K-Fold Cross-Validation

```
Dataset divisé en 5 folds (exemples K=5):

Itération 1: [Test][Train][Train][Train][Train]
Itération 2: [Train][Test][Train][Train][Train]
Itération 3: [Train][Train][Test][Train][Train]
Itération 4: [Train][Train][Train][Test][Train]
Itération 5: [Train][Train][Train][Train][Test]

→ Score final = Moyenne des 5 scores
→ Plus robuste qu'un seul split
```

**Code** :
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X_train, y_train, cv=5, scoring='recall')
print(f"Recall moyen: {scores.mean():.3f} ± {scores.std():.3f}")
```

---

## 🎨 FEATURE ENGINEERING

**Définition** : Créer de nouvelles features à partir des existantes.

**Exemples** :
```python
# 1. Ratios
df['ratio_esco2_anp32a'] = df['ESCO2'] / df['ANP32A-IT1']

# 2. Binning (catégoriser)
df['age_groupe'] = pd.cut(df['age'], bins=[0, 18, 30, 100],
                           labels=['enfant', 'jeune', 'adulte'])

# 3. Interactions
df['bio_score'] = df['ESCO2'] * df['ANP32A-IT1'] * df['NBPF1']

# 4. Agrégations
df['bio_mean'] = df[['ESCO2', 'ANP32A-IT1', 'NBPF1']].mean(axis=1)
```

**Principe** : Aider le modèle en lui donnant features plus informatives.

---

## 📏 STANDARDISATION ET NORMALISATION

**Pourquoi ?** Mettre toutes features sur même échelle.

**Problème sans** :
```
Âge:     [20, 25, 30]       (petites valeurs)
ESCO2:   [1000, 5000, 8000] (grandes valeurs)
→ ESCO2 domine le modèle !
```

### StandardScaler (Standardisation)
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()  # mean=0, std=1
X_scaled = scaler.fit_transform(X_train)

# Résultat: Moyenne=0, Écart-type=1
```

### MinMaxScaler (Normalisation)
```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()  # [0, 1]
X_scaled = scaler.fit_transform(X_train)

# Résultat: Toutes valeurs entre 0 et 1
```

**Important** :
- `fit` sur train seulement
- `transform` sur train, validation, test

---

## 🧬 SPÉCIFICITÉS DE NOTRE PROJET

### 1. Classes Déséquilibrées

**Problème** : Si 80% DT1- et 20% DT1+, modèle peut prédire toujours DT1- et avoir 80% accuracy !

**Solutions** :
- `class_weight='balanced'` dans modèles
- SMOTE (générer exemples synthétiques DT1+)
- Sous-échantillonnage classe majoritaire
- Ajuster seuil de décision (0.5 → 0.3)

---

### 2. Dataset Shift

**Problème** : Modèles entraînés sur Caucasiens ne marchent pas sur Africains.

**Cause** : Distributions génétiques différentes.

**Notre solution** : Entraîner sur données camerounaises/africaines.

---

### 3. Interprétabilité Clinique

**Exigence** : Médecins veulent comprendre POURQUOI le modèle prédit DT1+.

**Outils** :
- SHAP (SHapley Additive exPlanations)
- LIME (Local Interpretable Model-agnostic Explanations)
- Feature importance
- Partial Dependence Plots

---

## 📚 POUR ALLER PLUS LOIN

### Concepts avancés (Semaines 4-7)

- **Ensemble Methods** : Bagging, Boosting, Stacking
- **Regularization** : L1 (Lasso), L2 (Ridge), Elastic Net
- **Feature Selection** : SelectKBest, RFE, PCA
- **Imbalanced Learning** : SMOTE, ADASYN, Tomek Links
- **Model Calibration** : Calibrer probabilités
- **Explainable AI** : SHAP, LIME, Anchors

---

## 🎯 CHECKLIST CONCEPTS MAÎTRISÉS

À la fin du projet, vous devriez pouvoir :

- [ ] Expliquer ML supervisé vs. non-supervisé
- [ ] Décrire le workflow complet (collecte → prédiction)
- [ ] Justifier le split train/val/test
- [ ] Comparer classification et régression
- [ ] Expliquer 6 algorithmes de classification
- [ ] Interpréter matrice de confusion
- [ ] Choisir métrique appropriée (Recall vs. Precision)
- [ ] Diagnostiquer overfitting vs. underfitting
- [ ] Tuner hyperparamètres avec Grid/Random Search
- [ ] Utiliser Cross-Validation correctement
- [ ] Créer nouvelles features (feature engineering)
- [ ] Standardiser/normaliser données
- [ ] Gérer classes déséquilibrées
- [ ] Interpréter prédictions avec SHAP

---

**Félicitations ! Vous avez maintenant les bases théoriques pour votre projet Master 2. 🎓**

*Fiches de concepts ML - Projet Sorelle*
*Dernière mise à jour : Novembre 2025*
