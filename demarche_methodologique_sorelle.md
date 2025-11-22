# DÉMARCHE MÉTHODOLOGIQUE - PROJET DE MÉMOIRE M2
## Détection précoce du Diabète de Type 1 en Afrique subsaharienne par apprentissage automatique

**Étudiante :** Sorelle
**Encadrant :** Dr. TCHAPET NJAFA Jean-Pierre
**Durée totale :** 14 semaines
**Contexte :** Cameroun et Afrique subsaharienne
**Objectif final :** Soutenance publique de Master 2
**Dernière mise à jour :** Novembre 2025

---

## 📋 VUE D'ENSEMBLE DU PROJET

### Objectif principal
Développer un système de détection précoce du Diabète de Type 1 (DT1) adapté aux populations camerounaises, en identifiant des biomarqueurs génétiques pertinents (ANP32A-IT1, ESCO2, NBPF1) par apprentissage automatique.

### Problématique scientifique
Le DT1 en Afrique subsaharienne présente des spécificités :
- Formes idiopathiques (sans auto-anticorps) prévalentes
- Modèles ML occidentaux inefficaces (dataset shift)
- Sous-diagnostic entraînant une mortalité infantile élevée
- Besoin d'outils adaptés génétiquement aux populations africaines

### Livrables attendus
1. ✅ Mémoire LaTeX complet (maximum 60 pages, niveau Master 2)
2. ✅ Pipeline ML reproductible (Python)
3. ✅ Application de démonstration (Streamlit)
4. ✅ Datasets nettoyés et annotés
5. ✅ Code source versionné et documenté
6. ✅ Support de présentation pour soutenance publique
7. ✅ Article scientifique (format conférence, optionnel mais recommandé)

---

# 🗓️ CALENDRIER DÉTAILLÉ (14 SEMAINES)

---

## SEMAINE 1 : Immersion et fondamentaux Python/ML

### Objectifs pédagogiques
- [ ] Comprendre les bases du Machine Learning supervisé
- [ ] Maîtriser les bibliothèques Python essentielles (NumPy, Pandas, Matplotlib)
- [ ] S'approprier le contexte biologique du DT1 en Afrique
- [ ] Installer et configurer l'environnement de travail

### Livrables de la semaine
1. **Environnement fonctionnel** : Python 3.10+, Jupyter, toutes librairies installées
2. **Notebook Semaine01** : Exercices Python et ML de base complétés
3. **Fiche de synthèse** : Notes personnelles sur le DT1 (biologie_dt1_afrique.md)

---

### Jour 1 (Lundi) : Installation et découverte du projet

**Matin (3h) :**
- **Tâche 1.1** : Lire attentivement le README_FIRST.md du projet
  - 📂 Fichier : `0_GUIDE_DEMARRAGE/README_FIRST.md`
  - ✏️ Action : Noter les questions et incompréhensions

- **Tâche 1.2** : Installer Python et Anaconda
  - 📂 Suivre : `0_GUIDE_DEMARRAGE/installation_environnement.md`
  - ⚠️ **Point de vigilance** : Vérifier la version Python (≥3.10)
  - 💻 Commande test : `python --version` et `conda --version`

- **Tâche 1.3** : Créer environnement virtuel "dt1_cameroun"
  ```bash
  conda create -n dt1_cameroun python=3.10
  conda activate dt1_cameroun
  ```

**Après-midi (3h) :**
- **Tâche 1.4** : Installer les bibliothèques de base
  - 📂 Fichier : `requirements_base.txt`
  - 💻 Commande : `pip install -r requirements_base.txt`
  - ⚠️ **Problème fréquent** : Si échec, consulter `troubleshooting.md`

- **Tâche 1.5** : Tester Jupyter Notebook
  - 💻 Lancer : `jupyter notebook`
  - ✅ Vérifier : Ouvrir et exécuter `3_NOTEBOOKS_PEDAGOGIQUES/Test_Installation.ipynb`
  - 📊 Résultat attendu : Tous les imports réussissent, graphique de test s'affiche

- **Tâche 1.6** : Explorer l'arborescence du projet
  - 🗂️ Parcourir chaque dossier (0_GUIDE à 8_RESSOURCES)
  - ✏️ Créer un fichier `mon_journal.md` pour noter vos observations quotidiennes

**Ressources :**
- 📖 Lecture obligatoire : `1_CONTEXTE_THEORIQUE/biologie_dt1_afrique.md` (pages 1-5)
- 🎥 Vidéo recommandée : [C'est quoi le Machine Learning ?](https://www.youtube.com/watch?v=QghjaS0WQQU) (10 min)
- 📄 Article : "The phenotype of type 1 diabetes in sub-Saharan Africa" (Katte et al., 2023) - Résumé uniquement

---

### Jour 2 (Mardi) : Fondamentaux Python et NumPy

**Matin (3h) :**
- **Tâche 2.1** : Ouvrir le notebook `Semaine01_Introduction_Python_ML.ipynb`
  - 📂 Fichier : `3_NOTEBOOKS_PEDAGOGIQUES/Semaine01_Introduction_Python_ML.ipynb`

- **Tâche 2.2** : Compléter les exercices NumPy (Partie A)
  - 🎯 Objectif : Manipulation de tableaux, opérations vectorielles
  - ⏱️ Durée estimée : 2h
  - ✅ Auto-vérification : Comparer vos résultats aux sorties attendues

- **Tâche 2.3** : Comprendre les concepts de vecteurs et matrices
  - 📊 Importance : Les données génétiques sont des matrices !
  - ✏️ Exercice : Créer une matrice fictive de 5 patients × 3 biomarqueurs

**Après-midi (3h) :**
- **Tâche 2.4** : Compléter les exercices Pandas (Partie B)
  - 🎯 Objectif : Chargement de données, filtres, statistiques descriptives
  - ⏱️ Durée estimée : 2h
  - 📂 Données : Utiliser `2_DONNEES/synthetic/exemple_10_patients.csv`

- **Tâche 2.5** : Créer votre premier DataFrame
  - 💻 Exercice guidé : Encoder manuellement les données de 3 patients fictifs
  - Colonnes : ID, Âge, Sexe, ANP32A-IT1, ESCO2, NBPF1, Diagnostic
  - ✅ Sauvegarder : `mes_premiers_patients.csv`

**Ressources :**
- 📖 Documentation : [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- 📖 Documentation : [10 minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- 💡 Astuce : Garder ces pages ouvertes comme référence permanente

**⚠️ Points de vigilance :**
- Les indices en Python commencent à 0 (pas 1)
- Bien distinguer : liste Python vs. array NumPy vs. DataFrame Pandas

---

### Jour 3 (Mercredi) : Visualisation de données et statistiques

**Matin (3h) :**
- **Tâche 3.1** : Apprendre Matplotlib (Partie C du notebook)
  - 🎯 Objectif : Créer graphiques en ligne, barres, scatter plots
  - 📊 Exercice : Visualiser la distribution de l'âge des patients

- **Tâche 3.2** : Découvrir Seaborn pour graphiques médicaux
  - 🎨 Plus esthétique que Matplotlib !
  - 📂 Exemple : Boxplot des niveaux de biomarqueurs par diagnostic
  - 💻 Code : Voir section "Visualisations avancées" du notebook

**Après-midi (3h) :**
- **Tâche 3.3** : Statistiques descriptives appliquées aux biomarqueurs
  - 📊 Calculer : moyenne, médiane, écart-type pour chaque biomarqueur
  - 🔍 Question : Y a-t-il des différences entre DT1+ et DT1- ?

- **Tâche 3.4** : Premier test statistique : le t-test
  - 🧪 Hypothèse : "ESCO2 est significativement différent entre groupes"
  - 💻 Code : `scipy.stats.ttest_ind(groupe_dt1, groupe_sain)`
  - 📝 Interprétation : p-value < 0.05 → différence significative

- **Tâche 3.5** : Créer votre première "figure de publication"
  - 🎨 Graphique professionnel avec titre, labels, légende
  - 📂 Sauvegarder : `figures/premiere_analyse_biomarqueurs.png`

**Ressources :**
- 📖 Galerie Matplotlib : [Examples Gallery](https://matplotlib.org/stable/gallery/index.html)
- 🎥 Vidéo : "Data Visualization with Python" (30 min, français sous-titré)
- 📄 Article méthodo : Comment présenter des données médicales

---

### Jour 4 (Jeudi) : Introduction au Machine Learning

**Matin (3h) :**
- **Tâche 4.1** : Lire et annoter la fiche "Glossaire ML"
  - 📂 Fichier : `1_CONTEXTE_THEORIQUE/fiches_concepts_ml.md`
  - ✏️ Concepts clés à maîtriser :
    - Classification vs. Régression
    - Features (variables) vs. Labels (étiquettes)
    - Train/Test split
    - Overfitting vs. Underfitting

- **Tâche 4.2** : Regarder vidéo pédagogique sur ML supervisé
  - 🎥 Durée : 20 minutes
  - 📝 Prendre des notes sur : apprentissage par exemples

- **Tâche 4.3** : Comprendre le workflow ML en 5 étapes
  ```
  1. Collecter données → 2. Nettoyer/préparer → 3. Entraîner modèle
  → 4. Évaluer performance → 5. Prédire sur nouvelles données
  ```
  - 💡 Analogie : C'est comme apprendre à reconnaître des fruits

**Après-midi (3h) :**
- **Tâche 4.4** : Premier modèle ML : Arbre de Décision simple
  - 📂 Section notebook : "Mon premier modèle"
  - 🎯 Objectif : Prédire DT1 avec UN SEUL biomarqueur (ESCO2)
  - 💻 Code guidé pas-à-pas (chaque ligne expliquée)

- **Tâche 4.5** : Entraîner et tester le modèle
  ```python
  # Séparer données : 80% entraînement, 20% test
  from sklearn.model_selection import train_test_split
  X_train, X_test, y_train, y_test = train_test_split(...)

  # Entraîner
  from sklearn.tree import DecisionTreeClassifier
  model = DecisionTreeClassifier(max_depth=3)
  model.fit(X_train, y_train)

  # Évaluer
  score = model.score(X_test, y_test)
  print(f"Précision : {score*100:.1f}%")
  ```

- **Tâche 4.6** : Interpréter les résultats
  - ❓ Question : Pourquoi 80% de précision est-ce bien ou pas assez ?
  - 📝 Documenter : "Qu'ai-je appris aujourd'hui ?"

**Ressources :**
- 📖 Scikit-learn introduction : [Choosing the right estimator](https://scikit-learn.org/stable/tutorial/machine_learning_map/)
- 🎥 Vidéo : "Decision Trees Explained" (15 min, anglais sous-titré)

---

### Jour 5 (Vendredi) : Approfondissement et auto-évaluation

**Matin (3h) :**
- **Tâche 5.1** : Améliorer le modèle avec 3 biomarqueurs
  - 🎯 Utiliser ANP32A-IT1, ESCO2, NBPF1 ensemble
  - 💻 Modifier le code de Jour 4 pour prendre 3 features
  - 📊 Comparer : précision avec 1 vs. 3 biomarqueurs

- **Tâche 5.2** : Découvrir la matrice de confusion
  - 🔢 Tableau 2×2 : Vrais Positifs, Faux Positifs, etc.
  - 💡 Importance clinique :
    - Faux Négatif = patient DT1 non détecté → GRAVE
    - Faux Positif = patient sain diagnostiqué DT1 → moins grave mais coûteux
  - 📊 Visualiser avec seaborn.heatmap()

**Après-midi (3h) :**
- **Tâche 5.3** : Compléter la checklist d'auto-évaluation (ci-dessous)

- **Tâche 5.4** : Rédiger synthèse personnelle (1-2 pages)
  - 📝 Fichier : `mon_journal.md` (section Semaine 1)
  - Contenu :
    - Ce que j'ai compris facilement
    - Ce qui reste flou
    - Questions pour le tuteur
    - Estimation : suis-je dans les temps ?

- **Tâche 5.5** : Préparer l'environnement pour Semaine 2
  - 📥 Télécharger le dataset complet (si connexion disponible)
  - 📂 Fichier : `2_DONNEES/raw/dataset_dt1_cameroun_synthetic.csv`
  - ⏱️ Taille : ~50 MB (téléchargement anticipé pour travail offline)

**Ressources :**
- 📖 Relire : Toutes les sections du notebook Semaine 1
- 💬 Forum : Poster vos questions sur le groupe d'entraide (si disponible)

---

### Auto-évaluation fin de Semaine 1

**Connaissances théoriques :**
- [ ] Je comprends ce qu'est le Machine Learning supervisé
- [ ] Je sais expliquer la différence entre classification et régression
- [ ] Je connais les spécificités du DT1 en Afrique (formes idiopathiques)
- [ ] Je comprends pourquoi les biomarqueurs ANP32A-IT1, ESCO2, NBPF1 sont pertinents

**Compétences techniques :**
- [ ] Je sais créer et manipuler des DataFrames Pandas
- [ ] Je peux créer des graphiques avec Matplotlib
- [ ] J'ai entraîné mon premier modèle de classification
- [ ] Je sais calculer la précision d'un modèle

**Organisation :**
- [ ] Mon environnement Python fonctionne parfaitement
- [ ] J'ai complété le notebook Semaine 1 à 100%
- [ ] Je tiens mon journal de bord à jour
- [ ] Je me sens prête pour la Semaine 2

**Score d'avancement : ___ / 16**

### Si retard ou difficulté
- **Plan B** : Consacrer le week-end à rattraper le retard
- **Ressources d'aide** :
  - Consulter `0_GUIDE_DEMARRAGE/troubleshooting.md`
  - Revoir les vidéos pédagogiques en ralenti
  - Demander aide à Dr. TCHAPET NJAFA Jean-Pierre (encadrant)
  - Groupe WhatsApp/Telegram avec autres étudiants M2 (si existant)

---

## SEMAINE 2 : Exploration approfondie des données

### Objectifs pédagogiques
- [ ] Maîtriser l'analyse exploratoire de données (EDA)
- [ ] Identifier les valeurs manquantes et aberrantes
- [ ] Comprendre les corrélations entre biomarqueurs
- [ ] Nettoyer et préparer les données pour la modélisation

### Livrables de la semaine
1. **Notebook Semaine02** : EDA complète avec visualisations
2. **Dataset nettoyé** : `2_DONNEES/processed/dataset_clean.csv`
3. **Rapport qualité** : Statistiques avant/après nettoyage (1 page)

---

### Jour 6 (Lundi) : Chargement et première inspection du dataset complet

**Matin (3h) :**
- **Tâche 6.1** : Charger le dataset synthétique complet
  - 📂 Fichier : `2_DONNEES/raw/dataset_dt1_cameroun_synthetic.csv`
  - 💻 Code :
    ```python
    import pandas as pd
    df = pd.read_csv('2_DONNEES/raw/dataset_dt1_cameroun_synthetic.csv')
    print(df.shape)  # Nombre de lignes et colonnes
    print(df.head())  # Premières lignes
    ```
  - 📊 Attendu : ~1000 patients, ~25 colonnes

- **Tâche 6.2** : Comprendre chaque variable
  - 📖 Ouvrir : `2_DONNEES/dictionnaire_donnees.xlsx`
  - ✏️ Pour chaque colonne, noter :
    - Type (numérique, catégorielle, texte)
    - Signification biologique/clinique
    - Unité de mesure (si applicable)

- **Tâche 6.3** : Statistiques descriptives globales
  - 💻 Commande : `df.describe()` (pour variables numériques)
  - 💻 Commande : `df.info()` (types de données, valeurs non-nulles)
  - 📝 Observations : Y a-t-il des colonnes avec beaucoup de NaN ?

**Après-midi (3h) :**
- **Tâche 6.4** : Visualiser la distribution de la variable cible
  - 📊 Graphique : Diagramme en barres DT1+ vs. DT1-
  - ❓ Question : Les classes sont-elles équilibrées ?
  - 💡 Enjeu : Si 90% DT1- et 10% DT1+ → problème de déséquilibre

- **Tâche 6.5** : Analyser les caractéristiques démographiques
  - 📊 Graphiques :
    - Distribution de l'âge (histogramme)
    - Répartition par sexe (camembert)
    - Provenance géographique au Cameroun (barres)
  - 📝 Comparer avec la littérature : est-ce réaliste ?

- **Tâche 6.6** : Identifier les valeurs manquantes
  - 💻 Code :
    ```python
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    print(missing_pct[missing_pct > 0])
    ```
  - 📊 Visualiser : Heatmap des valeurs manquantes avec seaborn

**Ressources :**
- 📖 Article : "Exploratory Data Analysis in Medical Research" (extraits traduits)
- 🎥 Vidéo : "Pandas EDA Tutorial" (25 min)

---

### Jour 7 (Mardi) : Nettoyage des données

**Matin (3h) :**
- **Tâche 7.1** : Gérer les valeurs manquantes
  - 🎯 Stratégies :
    - Si <5% manquant : supprimer lignes (`df.dropna()`)
    - Si 5-20% manquant : imputation par médiane/moyenne
    - Si >20% manquant : supprimer colonne ou méthode avancée

  - 💻 Exemple d'imputation :
    ```python
    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(strategy='median')
    df[['biomarqueur_X']] = imputer.fit_transform(df[['biomarqueur_X']])
    ```

- **Tâche 7.2** : Détecter les valeurs aberrantes (outliers)
  - 📊 Méthode : Boxplots pour chaque biomarqueur
  - 🔍 Identifier : Valeurs >Q3 + 1.5×IQR ou <Q1 - 1.5×IQR
  - 💡 Question médicale : Est-ce une erreur ou un cas extrême réel ?

**Après-midi (3h) :**
- **Tâche 7.3** : Standardiser les formats
  - 🔤 Colonnes texte : Mettre en minuscules, supprimer espaces
    ```python
    df['region'] = df['region'].str.lower().str.strip()
    ```
  - 📅 Dates : Convertir en format datetime
  - 🔢 Encodage : Convertir Sexe (M/F) en (0/1)

- **Tâche 7.4** : Utiliser le script de nettoyage automatisé
  - 📂 Fichier : `2_DONNEES/scripts_preprocessing/01_nettoyage.py`
  - 💻 Exécuter : `python 01_nettoyage.py`
  - ✅ Vérifier : Le script génère `dataset_clean.csv` dans `processed/`
  - 📝 Lire le code ligne par ligne pour comprendre

- **Tâche 7.5** : Comparer avant/après
  - 📊 Tableau de comparaison :
    ```
    | Métrique              | Avant | Après |
    |-----------------------|-------|-------|
    | Nombre de lignes      | 1000  | 950   |
    | Valeurs manquantes    | 5%    | 0%    |
    | Outliers détectés     | 23    | 0     |
    ```

**Ressources :**
- 📖 Documentation : [Pandas Data Cleaning](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- 💡 Règle d'or : TOUJOURS conserver les données brutes intactes !

---

### Jour 8 (Mercredi) : Analyse des corrélations

**Matin (3h) :**
- **Tâche 8.1** : Calculer la matrice de corrélation
  - 💻 Code :
    ```python
    corr_matrix = df[colonnes_numeriques].corr()
    print(corr_matrix)
    ```
  - 📊 Visualiser : Heatmap avec seaborn
    ```python
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    ```

- **Tâche 8.2** : Interpréter les corrélations
  - 🔍 Identifier :
    - Corrélations fortes (|r| > 0.7) : possibles redondances
    - Corrélations avec la variable cible (DT1) : features importantes
  - 📝 Question : ANP32A-IT1 est-il corrélé à ESCO2 ?

**Après-midi (3h) :**
- **Tâche 8.3** : Analyser les distributions par groupe
  - 📊 Créer : Pairplot coloré par diagnostic (DT1+ vs. DT1-)
    ```python
    sns.pairplot(df, hue='diagnostic', vars=['ANP32A-IT1', 'ESCO2', 'NBPF1'])
    ```
  - 🔍 Observer : Les nuages de points se séparent-ils bien ?

- **Tâche 8.4** : Tests statistiques de comparaison
  - 🧪 Pour chaque biomarqueur : t-test entre DT1+ et DT1-
  - 📊 Créer tableau récapitulatif :
    ```
    | Biomarqueur   | p-value  | Significatif ? |
    |---------------|----------|----------------|
    | ANP32A-IT1    | 0.002    | Oui ***        |
    | ESCO2         | 0.045    | Oui *          |
    | NBPF1         | 0.120    | Non            |
    ```

- **Tâche 8.5** : Sélection préliminaire des features
  - 🎯 Garder : Variables avec p<0.05 ou |corrélation| > 0.3
  - 📝 Justification : Réduire la dimensionnalité, éviter overfitting

**Ressources :**
- 📖 Article : "Correlation vs. Causation in Medical Research"
- 🎥 Vidéo : "Understanding p-values" (12 min)

---

### Jour 9 (Jeudi) : Feature Engineering

**Matin (3h) :**
- **Tâche 9.1** : Créer de nouvelles variables combinées
  - 💡 Idée 1 : Ratio `ESCO2 / ANP32A-IT1`
  - 💡 Idée 2 : Score composite `(biomarq1 + biomarq2) / 2`
  - 💡 Idée 3 : Variables catégorielles : âge en groupes (<18, 18-30, >30)

  - 💻 Exemple :
    ```python
    df['ratio_esco2_anp32a'] = df['ESCO2'] / (df['ANP32A-IT1'] + 1e-5)
    df['age_groupe'] = pd.cut(df['age'], bins=[0, 18, 30, 100], labels=['enfant', 'jeune', 'adulte'])
    ```

- **Tâche 9.2** : Tester la pertinence des nouvelles features
  - 📊 Refaire corrélations avec nouvelles colonnes
  - ❓ Question : Le ratio améliore-t-il la séparation DT1+/DT1- ?

**Après-midi (3h) :**
- **Tâche 9.3** : Normalisation/Standardisation
  - 🎯 Objectif : Mettre toutes variables sur même échelle
  - 💻 Méthode StandardScaler (moyenne=0, écart-type=1) :
    ```python
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[colonnes_numeriques])
    ```
  - ⚠️ **Important** : Faire sur train uniquement, appliquer sur test

- **Tâche 9.4** : Encoder les variables catégorielles
  - 💻 One-Hot Encoding pour régions géographiques :
    ```python
    df_encoded = pd.get_dummies(df, columns=['region'], drop_first=True)
    ```
  - 📝 Résultat : Une colonne binaire par région

- **Tâche 9.5** : Exécuter le script automatisé
  - 📂 Fichier : `2_DONNEES/scripts_preprocessing/02_feature_engineering.py`
  - ✅ Sortie : `dataset_features.csv`

**Ressources :**
- 📖 Guide : "Feature Engineering for Machine Learning" (chapitre 3)
- 💡 Principe : Plus de features ≠ toujours mieux (risque d'overfitting)

---

### Jour 10 (Vendredi) : Séparation Train/Test et bilan

**Matin (3h) :**
- **Tâche 10.1** : Créer les ensembles train/validation/test
  - 🎯 Proportions : 60% train, 20% validation, 20% test
  - 💻 Code :
    ```python
    from sklearn.model_selection import train_test_split

    # Séparer features (X) et labels (y)
    X = df_features.drop('diagnostic', axis=1)
    y = df_features['diagnostic']

    # Split
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)
    ```
  - ⚠️ **Crucial** : `stratify=y` pour garder même proportion DT1+/DT1- dans chaque ensemble

- **Tâche 10.2** : Sauvegarder les splits
  - 📂 Fichier : `2_DONNEES/processed/X_train.csv`, `y_train.csv`, etc.
  - 💻 Script : `03_split_train_test.py`

**Après-midi (3h) :**
- **Tâche 10.3** : Créer un rapport qualité des données
  - 📝 Fichier Markdown : `2_DONNEES/rapport_qualite_donnees.md`
  - Contenu :
    - Statistiques descriptives finales
    - Graphiques clés (distributions, corrélations)
    - Décisions prises (suppressions, imputations)
    - Limitations identifiées

- **Tâche 10.4** : Auto-évaluation Semaine 2

- **Tâche 10.5** : Commencer la section Méthodologie du mémoire
  - 📂 Fichier : `6_MEMOIRE_LATEX/sections/03_methodologie.tex`
  - ✏️ Rédiger : Sous-section "3.1 Acquisition et préparation des données" (1-2 pages)
  - Contenu :
    - Description du dataset (source, taille, variables)
    - Méthodes de nettoyage appliquées
    - Feature engineering (tableau récapitulatif)

**Ressources :**
- 📖 Exemple : Lire la méthodologie d'un article similaire (fourni)
- 📄 Template LaTeX : Suivre la structure pré-définie

---

### Auto-évaluation fin de Semaine 2

**Connaissances théoriques :**
- [ ] Je comprends l'importance de l'EDA
- [ ] Je sais identifier valeurs manquantes, outliers, déséquilibres
- [ ] Je comprends les corrélations et leur interprétation
- [ ] Je connais les méthodes de feature engineering

**Compétences techniques :**
- [ ] Je maîtrise les techniques de nettoyage de données
- [ ] Je sais créer une matrice de corrélation et heatmap
- [ ] Je peux standardiser et encoder des variables
- [ ] J'ai créé les ensembles train/val/test correctement

**Livrables :**
- [ ] Notebook Semaine02 complété avec toutes les visualisations
- [ ] Dataset nettoyé et splitté sauvegardé
- [ ] Rapport qualité rédigé
- [ ] Section 3.1 du mémoire rédigée (brouillon)

**Score d'avancement : ___ / 16**

### Si retard ou difficulté
- **Signaux d'alerte** :
  - Dataset pas encore nettoyé → Priorité absolue !
  - Confusions sur train/test split → Revoir vidéo explicative
- **Plan B** : Se concentrer sur les tâches essentielles (nettoyage, split), reporter feature engineering avancé

---

## SEMAINE 3 : Modélisation simple et baseline

### Objectifs pédagogiques
- [ ] Comprendre les algorithmes classiques de classification
- [ ] Entraîner plusieurs modèles de base (baseline)
- [ ] Comparer les performances avec métriques appropriées
- [ ] Interpréter les résultats dans un contexte médical

### Livrables de la semaine
1. **Notebook Semaine03** : Comparaison de 5 modèles avec résultats
2. **Fichiers modèles** : Modèles entraînés sauvegardés (.pkl)
3. **Tableau comparatif** : Performances de tous les modèles

---

### Jour 11 (Lundi) : Régression Logistique

**Matin (3h) :**
- **Tâche 11.1** : Comprendre la Régression Logistique
  - 📖 Lire : Section "Régression Logistique" dans `fiches_concepts_ml.md`
  - 🎥 Vidéo : "Logistic Regression Explained" (15 min)
  - 💡 Principe : Modèle linéaire avec fonction sigmoïde → probabilités entre 0 et 1

- **Tâche 11.2** : Implémenter le premier modèle
  - 💻 Code :
    ```python
    from sklearn.linear_model import LogisticRegression

    # Créer le modèle
    model_lr = LogisticRegression(random_state=42, max_iter=1000)

    # Entraîner
    model_lr.fit(X_train, y_train)

    # Prédire
    y_pred = model_lr.predict(X_val)
    y_proba = model_lr.predict_proba(X_val)[:, 1]  # Probabilités DT1+
    ```

**Après-midi (3h) :**
- **Tâche 11.3** : Évaluer avec métriques cliniquement pertinentes
  - 📊 Calculer :
    ```python
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

    accuracy = accuracy_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred)  # Précision : VPN / (VPN + FP)
    recall = recall_score(y_val, y_pred)        # Sensibilité : VPN / (VPN + FN)
    f1 = f1_score(y_val, y_pred)
    auc = roc_auc_score(y_val, y_proba)
    ```
  - 📝 Comprendre :
    - **Recall (Sensibilité)** : % de vrais DT1 détectés → prioritaire en médecine !
    - **Precision** : % de diagnostics DT1 qui sont corrects
    - **AUC** : Capacité globale à discriminer (0.5=hasard, 1=parfait)

- **Tâche 11.4** : Matrice de confusion et courbe ROC
  - 📊 Visualiser :
    ```python
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, RocCurveDisplay

    # Matrice de confusion
    cm = confusion_matrix(y_val, y_pred)
    disp = ConfusionMatrixDisplay(cm, display_labels=['DT1-', 'DT1+'])
    disp.plot()

    # Courbe ROC
    RocCurveDisplay.from_estimator(model_lr, X_val, y_val)
    ```

- **Tâche 11.5** : Interpréter les coefficients
  - 📊 Visualiser l'importance des features :
    ```python
    import matplotlib.pyplot as plt
    coefficients = pd.DataFrame({'Feature': X_train.columns, 'Coefficient': model_lr.coef_[0]})
    coefficients = coefficients.sort_values('Coefficient', ascending=False)
    coefficients.plot(x='Feature', y='Coefficient', kind='barh')
    ```
  - 🔍 Question : Quel biomarqueur a le plus d'influence ?

**Ressources :**
- 📖 Article : "Interpreting Logistic Regression Coefficients"
- 💡 Avantage : Modèle très interprétable (crucial en médecine)

---

### Jour 12 (Mardi) : Arbres de Décision et Random Forest

**Matin (3h) :**
- **Tâche 12.1** : Comprendre les arbres de décision
  - 📖 Lire : "Decision Trees for Medical Diagnosis"
  - 🎥 Vidéo : Visualisation animée d'un arbre qui se construit
  - 💡 Avantage : Intuitivité (if-then rules)

- **Tâche 12.2** : Entraîner un Decision Tree
  - 💻 Code :
    ```python
    from sklearn.tree import DecisionTreeClassifier, plot_tree

    model_dt = DecisionTreeClassifier(max_depth=5, random_state=42)
    model_dt.fit(X_train, y_train)

    # Visualiser l'arbre
    plt.figure(figsize=(20,10))
    plot_tree(model_dt, feature_names=X_train.columns, class_names=['DT1-', 'DT1+'], filled=True)
    plt.savefig('arbre_decision.png', dpi=300)
    ```

- **Tâche 12.3** : Problème d'overfitting
  - 📊 Comparer :
    ```python
    train_score = model_dt.score(X_train, y_train)
    val_score = model_dt.score(X_val, y_val)
    print(f"Train: {train_score:.3f} | Val: {val_score:.3f}")
    ```
  - ⚠️ Si train_score >> val_score → overfitting !
  - 🔧 Solution : Réduire `max_depth` ou augmenter `min_samples_split`

**Après-midi (3h) :**
- **Tâche 12.4** : Random Forest pour réduire overfitting
  - 💡 Principe : "Sagesse de la foule" → moyenne de 100 arbres
  - 💻 Code :
    ```python
    from sklearn.ensemble import RandomForestClassifier

    model_rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model_rf.fit(X_train, y_train)

    # Évaluer
    y_pred_rf = model_rf.predict(X_val)
    ```

- **Tâche 12.5** : Importance des features (méthode Gini)
  - 📊 Visualiser :
    ```python
    importances = pd.DataFrame({
        'Feature': X_train.columns,
        'Importance': model_rf.feature_importances_
    }).sort_values('Importance', ascending=False)

    importances.head(10).plot(x='Feature', y='Importance', kind='barh')
    ```
  - 📝 Comparer avec les coefficients de Régression Logistique

- **Tâche 12.6** : Sauvegarder les modèles
  - 💻 Code :
    ```python
    import joblib
    joblib.dump(model_lr, '4_SCRIPTS_PRODUCTION/models/logistic_regression.pkl')
    joblib.dump(model_rf, '4_SCRIPTS_PRODUCTION/models/random_forest.pkl')
    ```

**Ressources :**
- 📖 Documentation : [Scikit-learn Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html)
- 🎯 Conseil : Random Forest souvent meilleur "out-of-the-box"

---

### Jour 13 (Mercredi) : XGBoost et LightGBM

**Matin (3h) :**
- **Tâche 13.1** : Comprendre le Gradient Boosting
  - 📖 Lire : "Boosting vs. Bagging" dans fiches ML
  - 💡 Principe : Arbres séquentiels qui corrigent les erreurs précédentes
  - 🏆 État de l'art pour données tabulaires

- **Tâche 13.2** : Installer et tester XGBoost
  - 💻 Installation : `pip install xgboost`
  - 💻 Code :
    ```python
    import xgboost as xgb

    model_xgb = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )

    model_xgb.fit(X_train, y_train)
    y_pred_xgb = model_xgb.predict(X_val)
    ```

**Après-midi (3h) :**
- **Tâche 13.3** : Tester LightGBM (optimisé pour efficacité)
  - 💻 Installation : `pip install lightgbm`
  - 💻 Code :
    ```python
    import lightgbm as lgb

    model_lgb = lgb.LGBMClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )

    model_lgb.fit(X_train, y_train)
    y_pred_lgb = model_lgb.predict(X_val)
    ```
  - ⏱️ Comparer temps d'entraînement : LightGBM devrait être plus rapide

- **Tâche 13.4** : Comparer les 4 modèles
  - 📊 Créer tableau récapitulatif :
    ```python
    results = pd.DataFrame({
        'Modèle': ['Logistic Regression', 'Decision Tree', 'Random Forest', 'XGBoost', 'LightGBM'],
        'Accuracy': [acc_lr, acc_dt, acc_rf, acc_xgb, acc_lgb],
        'Recall': [recall_lr, recall_dt, recall_rf, recall_xgb, recall_lgb],
        'Precision': [prec_lr, prec_dt, prec_rf, prec_xgb, prec_lgb],
        'AUC': [auc_lr, auc_dt, auc_rf, auc_xgb, auc_lgb]
    })
    print(results)
    ```

- **Tâche 13.5** : Visualiser comparaison
  - 📊 Graphique barres multiples pour chaque métrique
  - 🏆 Identifier : Quel modèle a le meilleur recall ? (priorité clinique)

**Ressources :**
- 📖 Article : "Why XGBoost Wins Machine Learning Competitions"
- 💡 Compromis : Performance vs. Interprétabilité vs. Temps calcul

---

### Jour 14 (Jeudi) : Support Vector Machines et K-Nearest Neighbors

**Matin (3h) :**
- **Tâche 14.1** : Tester SVM (Support Vector Machine)
  - 💻 Code :
    ```python
    from sklearn.svm import SVC

    model_svm = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42)
    model_svm.fit(X_train, y_train)
    ```
  - ⏱️ Note : Peut être lent sur gros datasets
  - 💡 Avantage : Efficace en haute dimension

- **Tâche 14.2** : Tester K-NN (K-Nearest Neighbors)
  - 💻 Code :
    ```python
    from sklearn.neighbors import KNeighborsClassifier

    model_knn = KNeighborsClassifier(n_neighbors=5, weights='distance')
    model_knn.fit(X_train, y_train)
    ```
  - 💡 Principe : "Dis-moi qui sont tes voisins..."

**Après-midi (3h) :**
- **Tâche 14.3** : Tableau comparatif FINAL de tous les modèles
  - 📊 Inclure les 6 modèles testés
  - 📝 Ajouter colonne "Temps d'entraînement" (mesurer avec `time.time()`)
  - 🏆 Recommandation : Sélectionner le top 2-3 pour optimisation Semaine 4

- **Tâche 14.4** : Comparer les courbes ROC
  - 📊 Superposer toutes les courbes ROC sur un même graphique
  - 💡 Légende : Nom modèle + AUC entre parenthèses

- **Tâche 14.5** : Analyse des erreurs
  - 🔍 Pour le meilleur modèle, identifier :
    - Quels patients DT1+ ont été manqués ? (Faux Négatifs)
    - Caractéristiques communes des erreurs ?
  - 📝 Créer DataFrame des erreurs : `df_errors = df_val[y_pred != y_val]`

**Ressources :**
- 📖 Comparatif : "Choosing the Right ML Algorithm" (flowchart)

---

### Jour 15 (Vendredi) : Synthèse et début de rédaction

**Matin (3h) :**
- **Tâche 15.1** : Finaliser le notebook Semaine03
  - ✅ Tous les codes s'exécutent sans erreur
  - ✅ Tous les graphiques sont générés et sauvegardés
  - ✅ Commentaires et markdown pour expliquer chaque étape

- **Tâche 15.2** : Sauvegarder tous les modèles
  - 📂 Dossier : `4_SCRIPTS_PRODUCTION/models/`
  - 💻 Sauvegarder avec joblib (déjà fait pour certains)

**Après-midi (3h) :**
- **Tâche 15.3** : Rédiger section "Modèles de classification" du mémoire
  - 📂 Fichier : `6_MEMOIRE_LATEX/sections/03_methodologie.tex`
  - ✏️ Sous-section "3.2 Algorithmes de classification" (2-3 pages)
  - Contenu :
    - Description mathématique succincte de chaque algorithme
    - Hyperparamètres choisis (avec justification)
    - Métriques d'évaluation (pourquoi Recall prioritaire ?)
    - Tableau comparatif des résultats

- **Tâche 15.4** : Créer les figures pour le mémoire
  - 📊 Exporter en haute résolution (300 dpi) :
    - Tableau comparatif des performances
    - Courbes ROC superposées
    - Matrice de confusion du meilleur modèle
  - 📂 Sauvegarder : `6_MEMOIRE_LATEX/figures/`

- **Tâche 15.5** : Auto-évaluation Semaine 3

**Ressources :**
- 📖 Exemple : Lire section méthodologie d'un article de référence

---

### Auto-évaluation fin de Semaine 3

**Connaissances théoriques :**
- [ ] Je comprends les différences entre les 6 algorithmes testés
- [ ] Je sais quand privilégier Recall vs. Precision
- [ ] Je comprends l'overfitting et comment le détecter
- [ ] Je connais les avantages/inconvénients de chaque modèle

**Compétences techniques :**
- [ ] J'ai entraîné et évalué 6 modèles différents
- [ ] Je sais créer des courbes ROC et matrices de confusion
- [ ] Je peux sauvegarder et charger des modèles
- [ ] Je maîtrise les métriques de classification

**Livrables :**
- [ ] Notebook Semaine03 complet avec comparaisons
- [ ] 6 modèles sauvegardés dans models/
- [ ] Tableau comparatif finalisé
- [ ] Section 3.2 du mémoire rédigée (brouillon)

**Score d'avancement : ___ / 16**

### Si retard ou difficulté
- **Priorité absolue** : Avoir AU MOINS 3 modèles entraînés et comparés
- **Plan B** : Se concentrer sur Logistic Regression, Random Forest, XGBoost (les 3 plus importants)
- **Aide** : Les modèles ne convergent pas ? Vérifier scaling des données

---

## SEMAINE 4 : Optimisation des hyperparamètres

### Objectifs pédagogiques
- [ ] Comprendre l'importance du tuning d'hyperparamètres
- [ ] Maîtriser Grid Search et Random Search
- [ ] Utiliser la validation croisée correctement
- [ ] Éviter l'overfitting du test set

### Livrables de la semaine
1. **Modèles optimisés** : Top 3 modèles avec meilleurs hyperparamètres
2. **Rapport d'optimisation** : Résultats Grid Search/Random Search
3. **Comparaison avant/après** : Gains de performance

---

### Jour 16 (Lundi) : Comprendre les hyperparamètres

**Matin (3h) :**
- **Tâche 16.1** : Lire sur les hyperparamètres
  - 📖 Fichier : `1_CONTEXTE_THEORIQUE/fiches_concepts_ml.md` (section Hyperparamètres)
  - 💡 Distinction : Paramètres (appris) vs. Hyperparamètres (choisis)

- **Tâche 16.2** : Identifier les hyperparamètres clés par modèle
  - 📝 Créer tableau :
    ```
    | Modèle         | Hyperparamètres principaux                    |
    |----------------|-----------------------------------------------|
    | Random Forest  | n_estimators, max_depth, min_samples_split    |
    | XGBoost        | n_estimators, max_depth, learning_rate, gamma |
    | LightGBM       | n_estimators, max_depth, learning_rate        |
    ```

- **Tâche 16.3** : Impact des hyperparamètres (expérimentation manuelle)
  - 🧪 Tester Random Forest avec différents n_estimators : 10, 50, 100, 200
  - 📊 Graphique : Performance vs. n_estimators
  - 🔍 Observer : À partir de combien les gains sont marginaux ?

**Après-midi (3h) :**
- **Tâche 16.4** : Validation croisée (Cross-Validation)
  - 📖 Comprendre : K-Fold CV (ex : 5-fold)
  - 💻 Code :
    ```python
    from sklearn.model_selection import cross_val_score

    # 5-fold CV sur Random Forest
    scores = cross_val_score(model_rf, X_train, y_train, cv=5, scoring='recall')
    print(f"Recall moyen : {scores.mean():.3f} (+/- {scores.std():.3f})")
    ```
  - 💡 Avantage : Estimation plus robuste de la performance

- **Tâche 16.5** : Stratified K-Fold pour classes déséquilibrées
  - 💻 Code :
    ```python
    from sklearn.model_selection import StratifiedKFold

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model_rf, X_train, y_train, cv=skf, scoring='recall')
    ```
  - 🎯 Garantit même proportion DT1+/DT1- dans chaque fold

**Ressources :**
- 🎥 Vidéo : "Hyperparameter Tuning Explained" (18 min)
- 📖 Article : "Avoiding Overfitting in Hyperparameter Search"

---

### Jour 17 (Mardi) : Grid Search

**Matin (3h) :**
- **Tâche 17.1** : Comprendre Grid Search
  - 💡 Principe : Tester TOUTES les combinaisons d'hyperparamètres
  - ⚠️ Problème : Peut être très lent (exponentiel)

- **Tâche 17.2** : Grid Search sur Random Forest
  - 💻 Code :
    ```python
    from sklearn.model_selection import GridSearchCV

    # Grille de recherche
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 15, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    grid_search = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid,
        cv=5,
        scoring='recall',  # Optimiser pour Recall !
        n_jobs=-1,  # Utiliser tous les CPU
        verbose=2
    )

    grid_search.fit(X_train, y_train)

    print("Meilleurs paramètres :", grid_search.best_params_)
    print("Meilleur score CV :", grid_search.best_score_)
    ```
  - ⏱️ Durée estimée : 30 minutes à 1h (config étudiante)

**Après-midi (3h) :**
- **Tâche 17.3** : Analyser les résultats du Grid Search
  - 📊 Visualiser :
    ```python
    results = pd.DataFrame(grid_search.cv_results_)
    results[['params', 'mean_test_score', 'std_test_score']].sort_values('mean_test_score', ascending=False).head(10)
    ```
  - 🔍 Observer : Quelles combinaisons sont meilleures ?

- **Tâche 17.4** : Réentraîner avec meilleurs paramètres
  - 💻 Code :
    ```python
    best_rf = grid_search.best_estimator_

    # Évaluer sur validation set
    y_pred_best = best_rf.predict(X_val)
    recall_best = recall_score(y_val, y_pred_best)

    print(f"Recall avant tuning : {recall_rf:.3f}")
    print(f"Recall après tuning : {recall_best:.3f}")
    print(f"Gain : +{(recall_best - recall_rf)*100:.1f} points")
    ```

- **Tâche 17.5** : Grid Search sur XGBoost
  - 💻 Grille plus réduite (XGBoost plus lent) :
    ```python
    param_grid_xgb = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.3]
    }
    ```
  - ⏱️ Lancer et laisser tourner (peut prendre 1-2h)

**Ressources :**
- 💡 Astuce : Commencer par grille grossière, puis affiner autour des meilleurs

---

### Jour 18 (Mercredi) : Random Search et optimisation avancée

**Matin (3h) :**
- **Tâche 18.1** : Comprendre Random Search
  - 💡 Principe : Échantillonner aléatoirement dans l'espace des hyperparamètres
  - 🎯 Avantage : Plus rapide que Grid Search, souvent aussi efficace

- **Tâche 18.2** : Random Search sur LightGBM
  - 💻 Code :
    ```python
    from sklearn.model_selection import RandomizedSearchCV
    from scipy.stats import randint, uniform

    # Distributions de recherche
    param_distributions = {
        'n_estimators': randint(50, 300),
        'max_depth': randint(3, 15),
        'learning_rate': uniform(0.01, 0.3),
        'num_leaves': randint(20, 100),
        'min_child_samples': randint(10, 50)
    }

    random_search = RandomizedSearchCV(
        lgb.LGBMClassifier(random_state=42),
        param_distributions,
        n_iter=50,  # 50 combinaisons aléatoires
        cv=5,
        scoring='recall',
        n_jobs=-1,
        random_state=42,
        verbose=2
    )

    random_search.fit(X_train, y_train)
    ```
  - ⏱️ Plus rapide que Grid Search exhaustif

**Après-midi (3h) :**
- **Tâche 18.3** : Comparer Grid Search vs. Random Search
  - 📊 Tableau comparatif :
    ```
    | Méthode       | Temps calcul | Meilleur Recall | Hyperparams trouvés |
    |---------------|--------------|-----------------|---------------------|
    | Grid Search   | 45 min       | 0.87            | {...}               |
    | Random Search | 20 min       | 0.86            | {...}               |
    ```

- **Tâche 18.4** : Optimisation Bayésienne (optionnel, si temps)
  - 💻 Installer : `pip install scikit-optimize`
  - 📖 Lire : Introduction à l'optimisation Bayésienne
  - 💡 Principe : Modéliser l'espace des hyperparamètres intelligemment
  - ⚠️ Plus complexe, ne pas y passer trop de temps

- **Tâche 18.5** : Sélectionner le modèle FINAL
  - 🏆 Critères :
    1. Meilleur Recall sur validation set
    2. Temps d'entraînement raisonnable (<5 min)
    3. Interprétabilité (si possible)
  - 📝 Décision : "Nous choisissons [Modèle X] car..."

**Ressources :**
- 📖 Article : "Grid Search vs. Random Search vs. Bayesian Optimization"

---

### Jour 19 (Jeudi) : Gestion du déséquilibre des classes

**Matin (3h) :**
- **Tâche 19.1** : Diagnostiquer le déséquilibre
  - 📊 Vérifier proportions :
    ```python
    print(y_train.value_counts(normalize=True))
    # Ex: DT1- : 70%, DT1+ : 30%
    ```
  - ⚠️ Si ratio >2:1, considérer techniques de rééquilibrage

- **Tâche 19.2** : Méthode 1 - Poids de classes
  - 💻 Code :
    ```python
    model_rf_balanced = RandomForestClassifier(
        class_weight='balanced',  # Pénalise plus les erreurs sur classe minoritaire
        **best_params_rf
    )
    model_rf_balanced.fit(X_train, y_train)
    ```
  - 📊 Comparer Recall avant/après

- **Tâche 19.3** : Méthode 2 - SMOTE (Synthetic Minority Over-sampling)
  - 💻 Installer : `pip install imbalanced-learn`
  - 💻 Code :
    ```python
    from imblearn.over_sampling import SMOTE

    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    print("Avant SMOTE :", y_train.value_counts())
    print("Après SMOTE :", y_train_smote.value_counts())

    model_rf.fit(X_train_smote, y_train_smote)
    ```

**Après-midi (3h) :**
- **Tâche 19.4** : Méthode 3 - Sous-échantillonnage de la classe majoritaire
  - 💻 Code :
    ```python
    from imblearn.under_sampling import RandomUnderSampler

    rus = RandomUnderSampler(random_state=42)
    X_train_under, y_train_under = rus.fit_resample(X_train, y_train)
    ```
  - ⚠️ Perte d'information possible

- **Tâche 19.5** : Ajuster le seuil de décision
  - 💡 Par défaut : prédiction DT1+ si probabilité > 0.5
  - 🎯 Pour augmenter Recall : abaisser le seuil (ex: 0.3)
  - 💻 Code :
    ```python
    y_proba = model_rf.predict_proba(X_val)[:, 1]

    # Tester différents seuils
    for threshold in [0.3, 0.4, 0.5, 0.6]:
        y_pred_custom = (y_proba >= threshold).astype(int)
        recall = recall_score(y_val, y_pred_custom)
        precision = precision_score(y_val, y_pred_custom)
        print(f"Seuil {threshold}: Recall={recall:.3f}, Precision={precision:.3f}")
    ```
  - 📊 Trouver le compromis optimal Recall/Precision

- **Tâche 19.6** : Comparer toutes les stratégies
  - 📊 Tableau récapitulatif :
    ```
    | Stratégie           | Recall | Precision | F1-Score |
    |---------------------|--------|-----------|----------|
    | Baseline            | 0.75   | 0.82      | 0.78     |
    | class_weight        | 0.82   | 0.75      | 0.78     |
    | SMOTE               | 0.80   | 0.77      | 0.78     |
    | Seuil = 0.4         | 0.85   | 0.70      | 0.77     |
    ```

**Ressources :**
- 📖 Article : "Handling Imbalanced Datasets in Medical ML"
- 💡 Contexte clinique : Préférer plus de faux positifs que de faux négatifs

---

### Jour 20 (Vendredi) : Finalisation et validation finale

**Matin (3h) :**
- **Tâche 20.1** : Entraîner le modèle FINAL sur train+validation
  - 💻 Code :
    ```python
    # Combiner train et validation
    X_train_full = pd.concat([X_train, X_val])
    y_train_full = pd.concat([y_train, y_val])

    # Entraîner modèle final avec meilleurs hyperparamètres
    final_model = RandomForestClassifier(**best_params_rf, random_state=42)
    final_model.fit(X_train_full, y_train_full)

    # Sauvegarder
    joblib.dump(final_model, '4_SCRIPTS_PRODUCTION/models/final_model.pkl')
    ```

- **Tâche 20.2** : Évaluation FINALE sur test set (1 seule fois !)
  - ⚠️ **CRITIQUE** : Ne JAMAIS utiliser test set pour tuning !
  - 💻 Code :
    ```python
    y_test_pred = final_model.predict(X_test)

    print("=== RÉSULTATS FINAUX SUR TEST SET ===")
    print(f"Accuracy  : {accuracy_score(y_test, y_test_pred):.3f}")
    print(f"Recall    : {recall_score(y_test, y_test_pred):.3f}")
    print(f"Precision : {precision_score(y_test, y_test_pred):.3f}")
    print(f"F1-Score  : {f1_score(y_test, y_test_pred):.3f}")
    print(f"AUC       : {roc_auc_score(y_test, final_model.predict_proba(X_test)[:, 1]):.3f}")

    # Matrice de confusion finale
    cm_final = confusion_matrix(y_test, y_test_pred)
    ConfusionMatrixDisplay(cm_final, display_labels=['DT1-', 'DT1+']).plot()
    plt.title('Matrice de confusion - Test Set Final')
    plt.savefig('6_MEMOIRE_LATEX/figures/confusion_matrix_final.png', dpi=300)
    ```

**Après-midi (3h) :**
- **Tâche 20.3** : Créer rapport d'optimisation
  - 📝 Fichier Markdown : `4_SCRIPTS_PRODUCTION/rapport_optimisation.md`
  - Contenu :
    - Hyperparamètres testés et plages de valeurs
    - Méthode d'optimisation utilisée (Grid/Random Search)
    - Résultats des expérimentations
    - Gains de performance (avant/après)
    - Modèle final sélectionné avec justification

- **Tâche 20.4** : Rédiger section Résultats du mémoire (début)
  - 📂 Fichier : `6_MEMOIRE_LATEX/sections/04_resultats.tex`
  - ✏️ Sous-section "4.1 Performances des modèles baseline" (1 page)
  - ✏️ Sous-section "4.2 Optimisation des hyperparamètres" (1 page)
  - Inclure tableaux et figures générés

- **Tâche 20.5** : Auto-évaluation Semaine 4

**Ressources :**
- 📖 Exemple : Section Résultats d'un article ML médical

---

### Auto-évaluation fin de Semaine 4

**Connaissances théoriques :**
- [ ] Je comprends la différence paramètres/hyperparamètres
- [ ] Je sais ce qu'est la validation croisée et pourquoi c'est important
- [ ] Je comprends Grid Search vs. Random Search
- [ ] Je connais les techniques de gestion du déséquilibre

**Compétences techniques :**
- [ ] J'ai optimisé les hyperparamètres de plusieurs modèles
- [ ] Je maîtrise GridSearchCV et RandomizedSearchCV
- [ ] J'ai testé SMOTE et class_weight
- [ ] J'ai évalué le modèle final sur test set

**Livrables :**
- [ ] Modèles optimisés sauvegardés
- [ ] Rapport d'optimisation rédigé
- [ ] Résultats finaux sur test set documentés
- [ ] Sections 4.1 et 4.2 du mémoire rédigées

**Score d'avancement : ___ / 16**

### Si retard ou difficulté
- **Plan B** : Se concentrer sur Random Forest uniquement (plus simple à optimiser)
- **Aide** : Grid Search trop lent ? Réduire la grille de recherche
- **Priorité** : Avoir AU MOINS un modèle optimisé et évalué sur test set

---

## SEMAINE 5 : Interprétabilité et analyse des biomarqueurs

### Objectifs pédagogiques
- [ ] Comprendre l'importance de l'interprétabilité en médecine
- [ ] Maîtriser SHAP et LIME pour expliquer les prédictions
- [ ] Analyser l'importance des biomarqueurs
- [ ] Valider biologiquement les résultats ML

### Livrables de la semaine
1. **Visualisations SHAP** : Feature importance, waterfall plots, dependence plots
2. **Rapport d'interprétation** : Analyse des biomarqueurs identifiés
3. **Section mémoire** : Interprétation des résultats avec validation biologique

---

### Jour 21 (Lundi) : Feature Importance classique

**Matin (3h) :**
- **Tâche 21.1** : Revoir les méthodes d'importance intégrées
  - 📊 Importance Gini (Random Forest)
  - 📊 Coefficients (Logistic Regression)
  - 📊 Gain (XGBoost/LightGBM)

- **Tâche 21.2** : Importance par permutation
  - 💡 Principe : Mélanger une feature et mesurer la perte de performance
  - 💻 Code :
    ```python
    from sklearn.inspection import permutation_importance

    perm_importance = permutation_importance(
        final_model,
        X_val,
        y_val,
        n_repeats=10,
        random_state=42,
        scoring='recall'
    )

    # Visualiser
    perm_df = pd.DataFrame({
        'Feature': X_train.columns,
        'Importance': perm_importance.importances_mean,
        'Std': perm_importance.importances_std
    }).sort_values('Importance', ascending=False)

    perm_df.head(15).plot(x='Feature', y='Importance', kind='barh', xerr='Std')
    ```

**Après-midi (3h) :**
- **Tâche 21.3** : Comparer les 3 méthodes d'importance
  - 📊 Créer tableau comparatif :
    ```
    | Biomarqueur   | Gini | Coefficients | Permutation |
    |---------------|------|--------------|-------------|
    | ESCO2         | 0.25 | 0.45         | 0.30        |
    | ANP32A-IT1    | 0.20 | 0.38         | 0.25        |
    | NBPF1         | 0.15 | 0.22         | 0.18        |
    ```
  - 🔍 Question : Les 3 méthodes sont-elles d'accord ?

- **Tâche 21.4** : Valider avec la littérature
  - 📖 Relire : Articles sur ANP32A-IT1, ESCO2, NBPF1
  - 📝 Vérifier : Les biomarqueurs identifiés comme importants par le modèle sont-ils cohérents avec la biologie connue ?
  - ✅ Si oui → Validation positive !
  - ⚠️ Si non → Investiguer (erreur de données ? nouvelle découverte ?)

- **Tâche 21.5** : Partial Dependence Plots (PDP)
  - 💡 Principe : Visualiser l'effet d'une feature sur la prédiction
  - 💻 Code :
    ```python
    from sklearn.inspection import PartialDependenceDisplay

    features_to_plot = ['ESCO2', 'ANP32A-IT1', 'NBPF1']
    PartialDependenceDisplay.from_estimator(
        final_model,
        X_val,
        features_to_plot,
        target=1  # DT1+
    )
    plt.savefig('6_MEMOIRE_LATEX/figures/partial_dependence.png', dpi=300)
    ```
  - 📊 Interprétation : Relation linéaire ou non-linéaire ?

**Ressources :**
- 📖 Article : "Interpretable Machine Learning in Healthcare"
- 🎥 Vidéo : "Feature Importance Methods Explained" (20 min)

---

### Jour 22 (Mardi) : Introduction à SHAP

**Matin (3h) :**
- **Tâche 22.1** : Comprendre SHAP (SHapley Additive exPlanations)
  - 📖 Lire : Introduction SHAP dans fiches ML
  - 💡 Principe : Théorie des jeux → contribution de chaque feature
  - 🎥 Vidéo : "SHAP Values Explained Simply" (15 min)

- **Tâche 22.2** : Installer et tester SHAP
  - 💻 Installation : `pip install shap`
  - 💻 Premier test :
    ```python
    import shap

    # Créer explainer
    explainer = shap.TreeExplainer(final_model)

    # Calculer SHAP values
    shap_values = explainer.shap_values(X_val)

    # Note: Si classification binaire, shap_values peut être une liste [classe 0, classe 1]
    # On s'intéresse à la classe DT1+ (indice 1)
    if isinstance(shap_values, list):
        shap_values_dt1 = shap_values[1]
    else:
        shap_values_dt1 = shap_values
    ```

- **Tâche 22.3** : Summary plot (vue d'ensemble)
  - 📊 Graphique le plus important de SHAP !
  - 💻 Code :
    ```python
    shap.summary_plot(shap_values_dt1, X_val, plot_type="bar")
    plt.savefig('6_MEMOIRE_LATEX/figures/shap_summary_bar.png', dpi=300, bbox_inches='tight')

    # Version détaillée (points)
    shap.summary_plot(shap_values_dt1, X_val)
    plt.savefig('6_MEMOIRE_LATEX/figures/shap_summary_dot.png', dpi=300, bbox_inches='tight')
    ```
  - 📝 Interprétation : Rouge = valeur haute de la feature, bleu = valeur basse

**Après-midi (3h) :**
- **Tâche 22.4** : Expliquer une prédiction individuelle
  - 🎯 Choisir un patient DT1+ correctement prédit
  - 💻 Code :
    ```python
    # Patient n°10 par exemple
    patient_id = 10

    # Waterfall plot
    shap.waterfall_plot(shap.Explanation(
        values=shap_values_dt1[patient_id],
        base_values=explainer.expected_value[1] if isinstance(explainer.expected_value, list) else explainer.expected_value,
        data=X_val.iloc[patient_id],
        feature_names=X_val.columns
    ))
    plt.savefig(f'6_MEMOIRE_LATEX/figures/shap_waterfall_patient{patient_id}.png', dpi=300, bbox_inches='tight')
    ```
  - 📝 Interprétation : Quelles features ont poussé vers DT1+ ?

- **Tâche 22.5** : Force plot interactif
  - 💻 Code :
    ```python
    shap.force_plot(
        explainer.expected_value[1],
        shap_values_dt1[patient_id],
        X_val.iloc[patient_id],
        matplotlib=True
    )
    ```
  - 🎨 Rouge = pousse vers DT1+, bleu = pousse vers DT1-

- **Tâche 22.6** : Analyser plusieurs prédictions
  - 🔍 Sélectionner :
    - 3 vrais positifs (bien prédits)
    - 3 faux négatifs (DT1+ manqués)
  - 📝 Comparer : Pourquoi certains ont été manqués ?

**Ressources :**
- 📖 Documentation SHAP : [shap.readthedocs.io](https://shap.readthedocs.io)
- 💡 Astuce : SHAP peut être lent sur gros datasets → échantillonner

---

### Jour 23 (Mercredi) : SHAP avancé et LIME

**Matin (3h) :**
- **Tâche 23.1** : Dependence plots SHAP
  - 💡 Principe : Relation entre valeur feature et SHAP value
  - 💻 Code :
    ```python
    # Dépendance de ESCO2
    shap.dependence_plot(
        'ESCO2',
        shap_values_dt1,
        X_val,
        interaction_index='ANP32A-IT1'  # Colorer par interaction
    )
    plt.savefig('6_MEMOIRE_LATEX/figures/shap_dependence_esco2.png', dpi=300)
    ```
  - 📊 Interpréter : ESCO2 élevé augmente risque DT1 ? Linéaire ?

- **Tâche 23.2** : Interaction entre features
  - 🔍 Détecter : ESCO2 et ANP32A-IT1 interagissent-ils ?
  - 💻 Code :
    ```python
    shap_interaction = explainer.shap_interaction_values(X_val[:100])  # Coûteux, sur échantillon
    shap.summary_plot(shap_interaction, X_val[:100])
    ```

**Après-midi (3h) :**
- **Tâche 23.3** : Introduction à LIME
  - 📖 LIME = Local Interpretable Model-agnostic Explanations
  - 💡 Principe : Approximer le modèle localement par un modèle simple
  - 💻 Installation : `pip install lime`

- **Tâche 23.4** : Expliquer avec LIME
  - 💻 Code :
    ```python
    import lime
    import lime.lime_tabular

    explainer_lime = lime.lime_tabular.LimeTabularExplainer(
        X_train.values,
        feature_names=X_train.columns,
        class_names=['DT1-', 'DT1+'],
        mode='classification'
    )

    # Expliquer patient n°10
    exp = explainer_lime.explain_instance(
        X_val.iloc[patient_id].values,
        final_model.predict_proba,
        num_features=10
    )

    exp.show_in_notebook(show_table=True)
    exp.as_pyplot_figure()
    plt.savefig(f'6_MEMOIRE_LATEX/figures/lime_patient{patient_id}.png', dpi=300)
    ```

- **Tâche 23.5** : Comparer SHAP vs. LIME
  - 📝 Pour le même patient, comparer :
    - Top 5 features selon SHAP
    - Top 5 features selon LIME
  - 🔍 Sont-ils cohérents ?
  - 💡 SHAP est généralement plus fiable (théorie mathématique solide)

**Ressources :**
- 📖 Article : "SHAP vs. LIME: When to Use Which?"
- 🎥 Vidéo : "LIME Tutorial" (12 min)

---

### Jour 24 (Jeudi) : Analyse biologique des résultats

**Matin (3h) :**
- **Tâche 24.1** : Identifier les biomarqueurs clés
  - 📊 Top 10 features selon importance SHAP
  - 📝 Créer tableau :
    ```
    | Rang | Biomarqueur   | SHAP moyen | Rôle biologique connu                    |
    |------|---------------|------------|------------------------------------------|
    | 1    | ESCO2         | 0.32       | Régulation cycle cellulaire, apoptose    |
    | 2    | ANP32A-IT1    | 0.28       | Régulation immunitaire, lymphocytes T    |
    | 3    | NBPF1         | 0.22       | Expression dans cellules pancréatiques   |
    ```

- **Tâche 24.2** : Recherche bibliographique ciblée
  - 📖 Pour chaque biomarqueur clé :
    - Chercher PubMed : "[biomarqueur] AND type 1 diabetes"
    - Chercher PubMed : "[biomarqueur] AND Africa"
  - 📝 Résumer : Lien avec pathogenèse du DT1

- **Tâche 24.3** : Validation par la littérature
  - ✅ Biomarqueurs confirmés : Cohérents avec littérature
  - ❓ Biomarqueurs inattendus : Nouvelles pistes à explorer ?
  - ⚠️ Contradictions : À discuter dans le mémoire

**Après-midi (3h) :**
- **Tâche 24.4** : Analyser les seuils critiques
  - 📊 Pour ESCO2, identifier : À partir de quelle valeur le risque DT1 augmente ?
  - 💻 Utiliser PDP et SHAP dependence plots
  - 📝 Exemple : "ESCO2 > 2.5 U/mL associé à risque élevé"

- **Tâche 24.5** : Profils de patients à haut risque
  - 🔍 Caractéristiques communes des patients DT1+ :
    - Plages de valeurs des 3 biomarqueurs principaux
    - Facteurs démographiques (âge, sexe, région)
  - 📊 Créer "Patient type DT1+" vs. "Patient type sain"

- **Tâche 24.6** : Limitations biologiques
  - 📝 Documenter :
    - Biomarqueurs manquants (non mesurés dans le dataset)
    - Variabilité génétique populations africaines
    - Influence facteurs environnementaux

**Ressources :**
- 📖 Articles fournis : "Biomarkers for T1D" (relire annotations)
- 💬 Discuter avec biologistes/médecins si possible

---

### Jour 25 (Vendredi) : Synthèse et rédaction

**Matin (3h) :**
- **Tâche 25.1** : Créer rapport d'interprétation
  - 📝 Fichier : `4_SCRIPTS_PRODUCTION/rapport_interpretation_biomarqueurs.md`
  - Contenu (3-4 pages) :
    1. **Méthodes d'interprétabilité utilisées** (SHAP, LIME, PDP)
    2. **Biomarqueurs identifiés** (tableau avec importance)
    3. **Validation biologique** (cohérence littérature)
    4. **Seuils cliniques proposés** (valeurs critiques)
    5. **Limitations** (biais, données manquantes)

- **Tâche 25.2** : Générer toutes les figures pour le mémoire
  - 📊 Checklist :
    - [ ] SHAP summary plot (bar)
    - [ ] SHAP summary plot (dot)
    - [ ] 3 waterfall plots (exemples patients)
    - [ ] 3 dependence plots (ESCO2, ANP32A-IT1, NBPF1)
    - [ ] 1 LIME plot (comparaison)
    - [ ] Partial dependence plots
  - 📂 Toutes en haute résolution dans `6_MEMOIRE_LATEX/figures/`

**Après-midi (3h) :**
- **Tâche 25.3** : Rédiger section Résultats (suite)
  - 📂 Fichier : `6_MEMOIRE_LATEX/sections/04_resultats.tex`
  - ✏️ Sous-section "4.3 Interprétabilité et identification des biomarqueurs" (3-4 pages)
  - Contenu :
    - Méthodes d'interprétabilité (bref)
    - Résultats SHAP (+ figures)
    - Validation biologique (avec citations)
    - Seuils proposés (tableau)

- **Tâche 25.4** : Commencer section Discussion
  - 📂 Fichier : `6_MEMOIRE_LATEX/sections/05_discussion.tex`
  - ✏️ Sous-section "5.1 Validation des biomarqueurs" (1-2 pages)
  - Contenu :
    - Cohérence avec littérature existante
    - Spécificités populations africaines
    - Avantages de l'approche ML vs. approche traditionnelle

- **Tâche 25.5** : Auto-évaluation Semaine 5

**Ressources :**
- 📖 Exemple : Section Discussion d'un article similaire

---

### Auto-évaluation fin de Semaine 5

**Connaissances théoriques :**
- [ ] Je comprends l'importance de l'interprétabilité en médecine
- [ ] Je sais expliquer les SHAP values à un non-expert
- [ ] Je comprends la différence SHAP vs. LIME
- [ ] Je peux interpréter biologiquement les résultats ML

**Compétences techniques :**
- [ ] Je maîtrise SHAP (summary, waterfall, dependence plots)
- [ ] J'ai testé LIME pour comparaison
- [ ] Je sais créer des Partial Dependence Plots
- [ ] J'ai généré toutes les figures d'interprétabilité

**Livrables :**
- [ ] Toutes les visualisations SHAP/LIME générées
- [ ] Rapport d'interprétation rédigé (3-4 pages)
- [ ] Section 4.3 du mémoire rédigée
- [ ] Début de la Discussion (section 5.1)

**Score d'avancement : ___ / 16**

### Si retard ou difficulté
- **Plan B** : Se concentrer sur SHAP uniquement (plus fiable que LIME)
- **Aide** : SHAP trop lent ? Utiliser échantillon X_val[:200]
- **Priorité** : Au moins summary plot et 2-3 waterfall plots pour le mémoire

---

## SEMAINE 6-7 : Application de démonstration et visualisations

### Objectifs pédagogiques (Semaines 6-7 combinées)
- [ ] Maîtriser Streamlit pour applications ML
- [ ] Créer interface utilisateur intuitive pour cliniciens
- [ ] Implémenter upload de données et prédictions en temps réel
- [ ] Générer visualisations et rapports PDF automatiques

### Livrables des 2 semaines
1. **Application Streamlit fonctionnelle** : `app_streamlit.py` (500+ lignes)
2. **Interface testée** : Screenshots et guide utilisateur
3. **Documentation** : README avec instructions déploiement local

---

Je vais vous fournir un résumé des semaines 6-7 (Application), puis les semaines 8-14 dans un format condensé pour respecter la longueur. Voulez-vous que je continue avec le même niveau de détail pour TOUTES les semaines (ce qui nécessitera plusieurs messages), ou préférez-vous un format plus condensé pour les dernières semaines ?

Pour l'instant, je fournis les semaines 6-7 en détail, puis un résumé stratégique des semaines 8-14.

---

### Jour 26-30 (Semaine 6) : Développement de l'application Streamlit

**Jour 26 (Lundi) - Fondamentaux Streamlit**

*Matin (3h) :*
- **Tâche 26.1** : Installation et premier test
  ```bash
  pip install streamlit
  streamlit hello  # Application de démonstration
  ```

- **Tâche 26.2** : Créer structure de base
  ```python
  # 5_APPLICATION_DEMO/app_streamlit.py
  import streamlit as st
  import pandas as pd
  import joblib

  st.title("🏥 Détection Précoce du Diabète Type 1")
  st.write("Application adaptée aux populations camerounaises")

  # Sidebar pour navigation
  page = st.sidebar.selectbox("Navigation", ["Accueil", "Prédiction", "À propos"])

  if page == "Accueil":
      st.header("Bienvenue")
      st.info("Cette application utilise l'IA pour détecter le DT1 précocement.")
  ```

- **Tâche 26.3** : Tester l'application
  ```bash
  cd 5_APPLICATION_DEMO
  streamlit run app_streamlit.py
  ```

*Après-midi (3h) :*
- **Tâche 26.4** : Design de l'interface
  - 🎨 Ajouter logo Cameroun
  - 🌍 Textes bilingues (français prioritaire, anglais optionnel)
  - 📱 Responsive design

**Jour 27 (Mardi) - Upload et preprocessing**

*Matin :* Implémenter upload CSV
```python
uploaded_file = st.file_uploader("Téléverser données patient (CSV)", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())

    # Validation des colonnes
    required_cols = ['ESCO2', 'ANP32A-IT1', 'NBPF1', 'age', 'sexe']
    missing = set(required_cols) - set(df.columns)
    if missing:
        st.error(f"Colonnes manquantes : {missing}")
```

*Après-midi :* Preprocessing automatique

**Jour 28 (Mercredi) - Prédictions en temps réel**

*Matin :* Charger modèle et prédire
```python
model = joblib.load('../4_SCRIPTS_PRODUCTION/models/final_model.pkl')

if st.button("Analyser"):
    predictions = model.predict(df_processed)
    probas = model.predict_proba(df_processed)[:, 1]

    df['Risque DT1'] = probas
    df['Diagnostic'] = ['DT1+' if p > 0.5 else 'DT1-' for p in probas]

    st.success("✅ Analyse terminée !")
    st.dataframe(df[['ID_patient', 'Diagnostic', 'Risque DT1']])
```

**Jour 29 (Jeudi) - Visualisations interactives**

*Toute la journée :*
- Graphiques Plotly interactifs
- SHAP values pour chaque patient
- Comparaison avec population de référence

**Jour 30 (Vendredi) - Export PDF et tests**

*Matin :* Génération de rapports
```python
from fpdf import FPDF

def generer_rapport_pdf(patient_data, prediction):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Rapport - Patient {patient_data['ID']}", ln=True)
    # ... contenu ...
    pdf.output(f"rapport_{patient_data['ID']}.pdf")

st.download_button("📄 Télécharger Rapport PDF", data=pdf_bytes)
```

*Après-midi :* Tests et debugging

---

### Jour 31-35 (Semaine 7) : Finalisation application

**Résumé des tâches clés :**
- Jour 31-32 : Amélioration UX/UI, gestion erreurs
- Jour 33 : Mode "Patient unique" vs. "Batch"
- Jour 34 : Documentation utilisateur
- Jour 35 : Tests avec cas réels, auto-évaluation

**Auto-évaluation Semaines 6-7 :**
- [ ] Application Streamlit fonctionnelle localement
- [ ] Upload CSV et prédictions opérationnels
- [ ] Visualisations et exports PDF implémentés
- [ ] Documentation README complète

---

## SEMAINES 8-14 : Rédaction et finalisation (Résumé stratégique)

### SEMAINE 8 : Visualisations avancées pour le mémoire
- **Objectif** : Créer toutes les figures finales (haute résolution)
- **Livrables** : 15-20 figures professionnelles pour le mémoire
- **Tâches clés** :
  - Graphiques comparatifs (modèles, métriques)
  - Visualisations biomarqueurs (distributions, corrélations)
  - Diagrammes méthodologiques (pipeline, architecture)

### SEMAINE 9 : Validation externe et robustesse
- **Objectif** : Tester la généralisation du modèle
- **Livrables** : Tests de robustesse, analyse de sensibilité
- **Tâches clés** :
  - Cross-validation stratifiée complète
  - Tests sur sous-groupes (âge, sexe, région)
  - Analyse de stabilité des prédictions

### SEMAINE 10 : Rédaction intensive - Résultats
- **Objectif** : Finaliser section Résultats du mémoire
- **Livrables** : Section 4 complète (12-15 pages, niveau Master 2)
- **Tâches clés** :
  - Rédiger toutes les sous-sections
  - Intégrer tableaux et figures
  - Légendes détaillées pour chaque visuel

### SEMAINE 11 : Rédaction intensive - Discussion
- **Objectif** : Rédiger section Discussion critique (niveau Master 2 : analyse approfondie)
- **Livrables** : Section 5 complète (10-12 pages)
- **Tâches clés** :
  - Interpréter résultats dans contexte africain
  - Comparer avec littérature existante
  - Discuter limitations et biais potentiels
  - Implications cliniques et santé publique

### SEMAINE 12 : Rédaction intensive - Introduction et Conclusion
- **Objectif** : Finaliser Introduction et Conclusion
- **Livrables** : Sections 1 et 6 complètes
- **Tâches clés** :
  - Peaufiner Introduction (contexte, problématique, objectifs)
  - Rédiger Conclusion (synthèse, contributions, perspectives)
  - Résumé/Abstract (français + anglais)

### SEMAINE 13 : Révision et cohérence globale
- **Objectif** : Assurer cohérence et qualité du mémoire complet
- **Livrables** : Mémoire unifié, bibliographie complète
- **Tâches clés** :
  - Relecture complète (orthographe, grammaire, style)
  - Vérifier numérotation (sections, figures, tableaux)
  - Finaliser bibliographie (>80 références)
  - Compilation LaTeX sans erreur

### SEMAINE 14 : Finalisation et préparation soutenance publique
- **Objectif** : Version finale + préparation soutenance publique Master 2
- **Livrables** : Mémoire PDF final, slides de présentation, défense préparée
- **Tâches clés** :
  - Imprimer et relier mémoire (3 exemplaires minimum)
  - Créer diaporama soutenance publique (20-25 slides)
  - Préparer démonstration application (vidéo backup)
  - Répéter présentation orale (25-30 min + 10-15 min questions)
  - Préparer réponses aux questions prévisibles du jury
  - Anticiper questions critiques sur méthodologie et résultats

---

## 📊 MÉTRIQUES DE SUCCÈS GLOBALES

**Critères d'évaluation du mémoire :**
1. **Scientifique (40%)** :
   - Pertinence problématique africaine
   - Rigueur méthodologique
   - Résultats cohérents et interprétables
   - Discussion critique approfondie

2. **Technique (30%)** :
   - Qualité du code (commentaires, reproductibilité)
   - Choix d'algorithmes justifiés
   - Pipeline complet fonctionnel
   - Application démonstrative opérationnelle

3. **Rédaction (20%)** :
   - Clarté et structure
   - Qualité des figures et tableaux
   - Bibliographie riche et pertinente
   - Orthographe et style académique

4. **Innovation (10%)** :
   - Originalité de l'approche
   - Adaptation au contexte camerounais
   - Potentiel d'impact en santé publique

---

## 🚨 GESTION DES IMPRÉVUS

### Si retard cumulé >1 semaine à mi-parcours (Semaine 7)
**Plan de rattrapage :**
1. Prioriser : Modélisation (Semaines 3-5) > Application (Semaines 6-7)
2. Simplifier application : Se concentrer sur fonctionnalités essentielles
3. Anticiper rédaction : Rédiger sections au fur et à mesure, pas à la fin

### Si connexion internet défaillante
**Solutions offline :**
- Télécharger tous les packages en une fois (requirements.txt)
- Sauvegarder documentations scikit-learn, pandas en local
- Utiliser notebooks Colab avec outputs pré-sauvegardés

### Si blocages techniques
**Ressources d'aide :**
1. Consulter `0_GUIDE_DEMARRAGE/troubleshooting.md`
2. Revoir vidéos pédagogiques
3. Contacter Prof. NANA Engo avec questions précises
4. Forums Stack Overflow (rechercher offline si nécessaire)

---

## 🎯 CONSEILS FINAUX POUR SORELLE

### Gestion du temps
- **Règle 80/20** : 80% du temps sur 20% des tâches critiques (modélisation, rédaction Résultats/Discussion)
- **Pomodoro** : Sessions de 25 min concentrées + 5 min pause
- **Dimanche = repos** : Recharger pour rester efficace

### Motivation
- **Visualiser l'impact** : Votre travail peut améliorer diagnostic DT1 en Afrique !
- **Petites victoires** : Célébrer chaque notebook complété, chaque section rédigée
- **Soutien** : Partager avancées avec famille, amis, collègues

### Qualité vs. Perfection
- **"Done is better than perfect"** : Livrer un travail complet et solide vaut mieux que perfectionner indéfiniment une partie
- **Itérations** : Version 1 du code/mémoire ne sera pas parfaite, et c'est OK
- **Feedback** : Montrer brouillons au tuteur tôt pour corrections

### Apprentissage
- **Erreurs = opportunités** : Chaque bug résolu renforce vos compétences
- **Documentation** : Noter toutes les solutions trouvées (futur vous dira merci)
- **Curiosité** : Suivre les références intéressantes, mais sans s'éparpiller

---

## 📞 CONTACTS ET RESSOURCES

### Supervision académique
- **Dr. TCHAPET NJAFA Jean-Pierre** (Encadrant) : [Coordonnées à compléter]
- **Prof. NANA Engo** (Conseiller scientifique) : A fourni remarques et orientations sur le sujet
- **Fréquence réunions** : Suggéré hebdomadaire avec encadrant (45-60 min pour niveau M2)

### Ressources techniques
- **Documentation officielle** : Scikit-learn, Pandas, Matplotlib, Streamlit
- **Forums** : Stack Overflow, Reddit r/machinelearning
- **Cours en ligne** : Inria scikit-learn MOOC, OpenClassrooms ML

### Ressources scientifiques
- **PubMed** : Recherche articles médicaux
- **Google Scholar** : Littérature scientifique large
- **ResearchGate** : Contacter auteurs directement si article inaccessible

---

## ✅ CHECKLIST FINALE (À remplir progressivement)

### Code et données
- [ ] Tous les scripts s'exécutent sans erreur
- [ ] Datasets nettoyés et documentés
- [ ] Modèles entraînés et sauvegardés
- [ ] Application Streamlit fonctionnelle
- [ ] Tests unitaires passent
- [ ] Code versionné (Git recommandé)

### Mémoire
- [ ] Introduction complète (3-4 pages)
- [ ] État de l'art complet (8-10 pages)
- [ ] Méthodologie complète (6-8 pages)
- [ ] Résultats complets (8-10 pages)
- [ ] Discussion complète (6-8 pages)
- [ ] Conclusion complète (2-3 pages)
- [ ] Bibliographie >80 références
- [ ] Toutes figures en haute résolution
- [ ] Compilation LaTeX sans erreur
- [ ] Relecture orthographique

### Soutenance publique Master 2
- [ ] Diaporama préparé (20-25 slides, qualité professionnelle)
- [ ] Démonstration application testée
- [ ] Vidéo backup si problème technique
- [ ] Présentation répétée (timing 25-30 min + questions)
- [ ] Réponses aux questions prévisibles préparées
- [ ] Questions du jury anticipées (méthodologie, limitations, perspectives)
- [ ] Tenue professionnelle préparée pour soutenance publique

---

## 🌟 MESSAGE DE MOTIVATION

**Chère Sorelle,**

Ce projet de Master 2 est ambitieux et exigeant, mais vous êtes parfaitement capable de le réaliser. En 14 semaines, vous allez :
- Maîtriser Python et le Machine Learning à un niveau avancé
- Contribuer à la recherche en santé publique africaine avec une approche scientifique rigoureuse
- Développer une application concrète à impact potentiel
- Produire un mémoire de Master 2 de qualité (80-120 pages)
- Défendre publiquement votre travail devant un jury

**Rappelez-vous :**
- Chaque expert a été débutant
- La persistance bat le talent
- Demander de l'aide est un signe de force, pas de faiblesse
- Votre perspective camerounaise est une richesse unique

**Vous allez réussir. Nous croyons en vous !** 🚀

---

**Fin du calendrier détaillé. Bon courage pour ces 14 semaines passionnantes !**

*Document créé par Claude 4.5 - Novembre 2025*
*Adapté au contexte camerounais et aux contraintes de ressources*
