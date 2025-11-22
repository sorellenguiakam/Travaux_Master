# 🏥 Projet DT1 Cameroun - Détection Précoce du Diabète de Type 1

## 📋 Description du Projet

Ce projet de Master 2 vise à développer un système de détection précoce du Diabète de Type 1 (DT1) adapté aux populations camerounaises et d'Afrique subsaharienne, en utilisant des techniques d'apprentissage automatique (Machine Learning) pour identifier des biomarqueurs génétiques pertinents.

**Étudiante :** Sorelle
**Encadrant :** Dr. TCHAPET NJAFA Jean-Pierre
**Conseiller scientifique :** Prof. NANA Engo (remarques et orientations sur le sujet)
**Durée :** 14 semaines
**Contexte :** Cameroun et Afrique subsaharienne
**Objectif final :** Soutenance publique de Master 2

---

## 🎯 Objectifs

1. **Scientifique** : Identifier des biomarqueurs génétiques (ANP32A-IT1, ESCO2, NBPF1) adaptés aux populations africaines
2. **Technique** : Développer un pipeline ML reproductible pour la détection précoce du DT1
3. **Pratique** : Créer une application de démonstration utilisable par des cliniciens
4. **Académique** : Produire un mémoire de Master 2 de qualité (maximum 60 pages)
5. **Professionnel** : Défendre publiquement le travail devant un jury

---

## 🚀 Démarrage Rapide (Quick Start)

### Prérequis

- **Système d'exploitation** : Windows, macOS, ou Linux
- **Python** : Version 3.10 ou supérieure
- **RAM** : Minimum 8 GB (recommandé 16-32 GB)
- **Espace disque** : Minimum 5 GB d'espace libre
- **Connexion internet** : Nécessaire pour l'installation initiale (téléchargement des packages)

### Installation (10 minutes)

#### Étape 1 : Installer Python et Anaconda

**Windows :**
1. Télécharger [Anaconda](https://www.anaconda.com/products/distribution) (version Python 3.10+)
2. Exécuter l'installateur et suivre les instructions
3. Cocher "Add Anaconda to PATH" lors de l'installation

**macOS/Linux :**
```bash
# Télécharger Anaconda pour votre système
wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
bash Anaconda3-2024.02-1-Linux-x86_64.sh
```

#### Étape 2 : Créer l'environnement virtuel

```bash
# Ouvrir un terminal (ou Anaconda Prompt sur Windows)
cd chemin/vers/projet_dt1_cameroun

# Créer l'environnement virtuel
conda create -n dt1_cameroun python=3.10 -y

# Activer l'environnement
conda activate dt1_cameroun
```

#### Étape 3 : Installer les dépendances

```bash
# Installer les bibliothèques de base
pip install -r requirements_base.txt

# Vérifier l'installation
python -c "import numpy, pandas, sklearn; print('✅ Installation réussie!')"
```

#### Étape 4 : Tester Jupyter Notebook

```bash
# Lancer Jupyter
jupyter notebook

# Dans le navigateur qui s'ouvre, naviguer vers :
# 3_NOTEBOOKS_PEDAGOGIQUES/Test_Installation.ipynb
# Exécuter toutes les cellules (menu "Cell" > "Run All")
```

### Vérification de l'installation

Si tout fonctionne, vous devriez voir :
- ✅ Tous les imports Python réussissent sans erreur
- ✅ Un graphique de test s'affiche
- ✅ Message "Votre environnement est prêt !"

---

## 📂 Structure du Projet

```
projet_dt1_cameroun/
│
├── 0_GUIDE_DEMARRAGE/          # Commencez ici !
│   ├── README_FIRST.md         # Guide de démarrage pas-à-pas
│   ├── installation_environnement.md
│   └── troubleshooting.md      # Solutions aux problèmes courants
│
├── 1_CONTEXTE_THEORIQUE/       # Fondamentaux à connaître
│   ├── fiches_concepts_ml.md   # Glossaire ML illustré
│   ├── biologie_dt1_afrique.md # Contexte médical
│   └── references_bibliographiques.bib
│
├── 2_DONNEES/                  # Datasets et preprocessing
│   ├── raw/                    # Données brutes (ne jamais modifier)
│   ├── processed/              # Données nettoyées
│   ├── synthetic/              # Données synthétiques pour tests
│   ├── dictionnaire_donnees.xlsx
│   └── scripts_preprocessing/  # Scripts de nettoyage
│
├── 3_NOTEBOOKS_PEDAGOGIQUES/   # Apprentissage progressif
│   ├── Semaine01_Introduction_Python_ML.ipynb
│   ├── Semaine02_Exploration_Donnees.ipynb
│   ├── Semaine03_Modelisation_Simple.ipynb
│   ├── Semaine04-05_Modeles_Avances.ipynb
│   ├── Semaine06_Optimisation_Validation.ipynb
│   └── Semaine07_Interpretation_Resultats.ipynb
│
├── 4_SCRIPTS_PRODUCTION/       # Code pour production
│   ├── pipeline_complet.py     # Script principal à exécuter
│   ├── config.yaml             # Paramètres centralisés
│   ├── models/                 # Modèles ML entraînés (.pkl)
│   └── utils/                  # Fonctions réutilisables
│
├── 5_APPLICATION_DEMO/         # Application de démonstration
│   ├── app_streamlit.py        # Application principale
│   ├── requirements_app.txt    # Dépendances spécifiques
│   ├── assets/                 # Logos, images
│   └── exemples_test/          # Cas d'usage pour tester
│
├── 6_MEMOIRE_LATEX/            # Mémoire académique
│   ├── main.tex                # Document principal
│   ├── sections/               # Chapitres du mémoire
│   ├── figures/                # Graphiques (générés automatiquement)
│   ├── tableaux/               # Tableaux (exports CSV→LaTeX)
│   └── bibliographie.bib       # Références bibliographiques
│
├── 7_PLANIFICATION/            # Gestion du projet
│   ├── demarche_methodologique_sorelle.md  # Calendrier détaillé
│   ├── checklist_livrables.md
│   └── criteres_evaluation.md
│
├── 8_RESSOURCES_COMPLEMENTAIRES/ # Pour aller plus loin
│   ├── tutoriels_video_recommandes.md
│   ├── articles_cles_annottes.pdf
│   └── contacts_experts_cameroun.md
│
├── README.md                   # Ce fichier
├── requirements_base.txt       # Dépendances Python de base
└── requirements_full.txt       # Toutes les dépendances
```

---

## 🗓️ Calendrier des 14 Semaines

Consultez le **calendrier détaillé jour par jour** dans :
```
7_PLANIFICATION/demarche_methodologique_sorelle.md
```

**Résumé rapide :**
- **Semaines 1-2** : Fondamentaux Python/ML + Exploration des données
- **Semaines 3-5** : Modélisation et optimisation
- **Semaines 6-7** : Application de démonstration
- **Semaines 8-9** : Visualisations et validation
- **Semaines 10-12** : Rédaction du mémoire (Résultats, Discussion)
- **Semaines 13-14** : Finalisation et préparation de la soutenance

---

## 💻 Utilisation

### Exécuter le Pipeline Complet

Pour exécuter l'ensemble du pipeline de détection du DT1 :

```bash
# Activer l'environnement
conda activate dt1_cameroun

# Exécuter le pipeline
cd 4_SCRIPTS_PRODUCTION
python pipeline_complet.py --config config.yaml
```

Le pipeline exécute automatiquement :
1. Chargement des données brutes
2. Preprocessing et nettoyage
3. Feature engineering
4. Entraînement des modèles
5. Évaluation et sélection du meilleur modèle
6. Sauvegarde des résultats et visualisations

### Lancer l'Application de Démonstration

Pour tester l'application Streamlit localement :

```bash
cd 5_APPLICATION_DEMO
streamlit run app_streamlit.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

**Fonctionnalités de l'application :**
- 📤 Upload de données patients (CSV)
- 🔍 Prédiction du risque de DT1 en temps réel
- 📊 Visualisation de l'importance des biomarqueurs
- 📄 Génération de rapports PDF pour usage clinique

---

## 📊 Données

### Datasets Disponibles

1. **Données synthétiques** (utilisées par défaut)
   - Fichier : `2_DONNEES/synthetic/dataset_dt1_cameroun_synthetic.csv`
   - Taille : ~1000 patients, 25 features
   - Générées à partir de distributions réalistes basées sur la littérature

2. **Données réelles** (si disponibles)
   - Fichier : `2_DONNEES/raw/dataset_dt1_cameroun_real.csv`
   - Source : [À compléter selon disponibilité]

### Variables Principales

| Variable       | Type        | Description                                      |
|----------------|-------------|--------------------------------------------------|
| ID_patient     | Texte       | Identifiant unique anonymisé                     |
| age            | Numérique   | Âge en années                                    |
| sexe           | Catégoriel  | M (Masculin) ou F (Féminin)                      |
| region         | Catégoriel  | Région du Cameroun (Yaoundé, Douala, etc.)       |
| ANP32A-IT1     | Numérique   | Niveau d'expression du biomarqueur (unités: U/mL)|
| ESCO2          | Numérique   | Niveau d'expression du biomarqueur (unités: U/mL)|
| NBPF1          | Numérique   | Niveau d'expression du biomarqueur (unités: U/mL)|
| diagnostic     | Binaire     | 0 (DT1-) ou 1 (DT1+)                             |

Consultez le fichier `2_DONNEES/dictionnaire_donnees.xlsx` pour la description complète de toutes les variables.

---

## 🔬 Méthodologie

### Algorithmes de Machine Learning Utilisés

1. **Régression Logistique** : Modèle linéaire de référence, très interprétable
2. **Random Forest** : Ensemble d'arbres de décision, robuste et performant
3. **XGBoost** : Gradient Boosting optimisé, état de l'art pour données tabulaires
4. **LightGBM** : Version légère de Gradient Boosting, optimisée pour efficacité
5. **Support Vector Machines (SVM)** : Efficace en haute dimension
6. **K-Nearest Neighbors (K-NN)** : Méthode simple basée sur la proximité

### Métriques d'Évaluation

**Priorité en contexte médical : Maximiser le Recall (Sensibilité)**

| Métrique   | Description                                           | Objectif      |
|------------|-------------------------------------------------------|---------------|
| Recall     | % de vrais DT1+ détectés (VP / (VP + FN))            | **Maximiser** |
| Precision  | % de diagnostics DT1+ corrects (VP / (VP + FP))      | Équilibrer    |
| F1-Score   | Moyenne harmonique Recall et Precision                | Équilibrer    |
| AUC-ROC    | Capacité globale de discrimination (0.5=hasard, 1=parfait) | Maximiser |
| Accuracy   | % de prédictions correctes (VP + VN) / Total         | Moins prioritaire |

**Justification clinique :** En détection précoce du DT1, manquer un patient malade (Faux Négatif) est plus grave que diagnostiquer à tort un patient sain (Faux Positif), car cela peut entraîner un retard de traitement et des complications mortelles.

---

## 📚 Ressources Pédagogiques

### Documentation Officielle

- **Scikit-learn** : [scikit-learn.org](https://scikit-learn.org/stable/documentation.html)
- **Pandas** : [pandas.pydata.org](https://pandas.pydata.org/docs/)
- **NumPy** : [numpy.org/doc](https://numpy.org/doc/)
- **Matplotlib** : [matplotlib.org](https://matplotlib.org/stable/contents.html)
- **Streamlit** : [docs.streamlit.io](https://docs.streamlit.io/)

### Cours en Ligne Recommandés

1. **Scikit-learn MOOC** (Inria) : [inria.github.io/scikit-learn-mooc](https://inria.github.io/scikit-learn-mooc/)
   - Gratuit, en français, orienté débutant
   - Durée : ~20 heures

2. **Machine Learning Crash Course** (Google) : [developers.google.com/machine-learning](https://developers.google.com/machine-learning/crash-course)
   - Gratuit, en anglais (sous-titres français)
   - Durée : ~15 heures

3. **OpenClassrooms - Initiez-vous au Machine Learning** : [openclassrooms.com](https://openclassrooms.com/fr/courses/8063076-initiez-vous-au-machine-learning)
   - En français, niveau débutant
   - Durée : ~10 heures

### Articles Scientifiques Clés

Consultez la bibliographie complète dans `1_CONTEXTE_THEORIQUE/references_bibliographiques.bib`.

**Incontournables :**
1. Katte JC et al. (2023). "The phenotype of type 1 diabetes in sub-Saharan Africa". *Frontiers in Public Health*.
2. Mbanya JC et al. (2010). "Diabetes in sub-Saharan Africa". *The Lancet*.
3. Atun R et al. (2017). "Diabetes in sub-Saharan Africa: from clinical care to health policy". *The Lancet Diabetes & Endocrinology*.

---

## 🛠️ Dépannage (Troubleshooting)

### Problèmes Courants

#### 1. Erreur d'importation de module

**Symptôme :**
```
ModuleNotFoundError: No module named 'sklearn'
```

**Solution :**
```bash
# Vérifier que l'environnement est activé
conda activate dt1_cameroun

# Réinstaller le package manquant
pip install scikit-learn
```

#### 2. Jupyter Notebook ne se lance pas

**Solution :**
```bash
# Installer/réinstaller Jupyter
conda install jupyter notebook -y

# Lancer avec le chemin complet
python -m jupyter notebook
```

#### 3. Erreur de mémoire (RAM insuffisante)

**Symptôme :**
```
MemoryError: Unable to allocate array
```

**Solutions :**
- Réduire la taille du dataset (échantillonner)
- Utiliser Google Colab (gratuit, 12 GB RAM)
- Réduire `n_estimators` dans les modèles (ex: 100 → 50)

#### 4. Modèle très lent à entraîner

**Solutions :**
- Utiliser LightGBM au lieu de XGBoost (6-8× plus rapide)
- Réduire la grille de recherche dans GridSearchCV
- Utiliser `n_jobs=-1` pour paralléliser sur tous les CPU

#### 5. Connexion internet intermittente

**Solutions :**
- Télécharger tous les packages en une fois (voir `requirements_full.txt`)
- Sauvegarder documentations en local (PDF)
- Utiliser notebooks avec outputs pré-sauvegardés

Pour plus de solutions, consultez : `0_GUIDE_DEMARRAGE/troubleshooting.md`

---

## 🤝 Contribution et Support

### Signaler un Bug

Si vous rencontrez un problème technique :
1. Vérifier `0_GUIDE_DEMARRAGE/troubleshooting.md`
2. Contacter l'encadrant : Prof. NANA Engo
3. Documenter le problème : message d'erreur complet, étapes pour reproduire

### Demander de l'Aide

**Ressources disponibles :**
- **Encadrant académique** : Prof. NANA Engo (réunions hebdomadaires)
- **Forums en ligne** : Stack Overflow, Reddit r/machinelearning
- **Documentation** : Voir section "Ressources Pédagogiques" ci-dessus

---

## 📜 Licence et Crédits

### Licence

Ce projet est destiné à un usage académique dans le cadre du Master 1 de Sorelle.

**Utilisation autorisée :**
- Recherche et enseignement
- Publication académique (avec citation appropriée)

**Utilisation NON autorisée sans validation supplémentaire :**
- Déploiement clinique en conditions réelles
- Usage commercial

### Crédits

**Développement :**
- Sorelle (Étudiante M1, Physique Atomique, Moléculaire et Biophysique)
- Prof. NANA Engo (Encadrant)
- Claude 4.5 (Assistant IA pour la structure du projet)

**Données :**
- Données synthétiques générées à partir de distributions réalistes basées sur :
  - Littérature scientifique sur le DT1 en Afrique subsaharienne
  - Études génétiques des populations camerounaises

**Bibliographie :**
- Mbanya JC, Sobngwi E, Kengne AP et collaborateurs
- Recherches du Centre de Biotechnologie de Nkolbisson (Yaoundé)
- Publications OMS et African Diabetes Association

---

## 📞 Contact

**Étudiante :** Sorelle
**Institution :** [À compléter : Université, département]
**Email :** [À compléter]

**Encadrant :** Dr. TCHAPET NJAFA Jean-Pierre
**Email :** [À compléter]

**Conseiller scientifique :** Prof. NANA Engo
**Rôle :** Remarques et orientations sur le sujet affiné

---

## 🎓 Citation

Si vous utilisez ce travail dans une publication, veuillez citer :

```bibtex
@mastersthesis{sorelle2026dt1cameroun,
  author = {Sorelle},
  title = {Détection précoce du Diabète de Type 1 en Afrique subsaharienne par apprentissage automatique : identification de biomarqueurs génétiques adaptés aux populations camerounaises},
  school = {[Nom de l'université]},
  year = {2026},
  type = {Mémoire de Master 2},
  address = {Cameroun},
  note = {Encadré par Dr. TCHAPET NJAFA Jean-Pierre}
}
```

---

## 🚀 Commencer Maintenant

Vous êtes prête à démarrer ? Suivez ces 3 étapes :

1. ✅ **Installation** : Suivre les instructions ci-dessus (10 minutes)
2. 📖 **Lecture** : Ouvrir `0_GUIDE_DEMARRAGE/README_FIRST.md`
3. 💻 **Premier notebook** : Lancer `3_NOTEBOOKS_PEDAGOGIQUES/Semaine01_Introduction_Python_ML.ipynb`

**Bon courage pour ces 14 semaines passionnantes ! 🎉**

---

*Dernière mise à jour : Novembre 2025*
