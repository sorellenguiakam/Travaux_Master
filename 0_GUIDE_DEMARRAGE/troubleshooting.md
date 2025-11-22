# 🔧 Guide de Dépannage (Troubleshooting)

Solutions aux problèmes courants rencontrés pendant le projet de Master 2.

---

## 🐍 PROBLÈMES PYTHON ET ANACONDA

### ❌ Erreur : "ModuleNotFoundError: No module named 'XXX'"

**Cause** : Package Python non installé ou environnement non activé

**Solutions** :
```bash
# 1. Vérifier que l'environnement est activé
conda activate dt1_cameroun

# 2. Installer le package manquant
pip install nom_du_package

# 3. Si ça persiste, réinstaller requirements
pip install --force-reinstall -r requirements_base.txt
```

---

### ❌ Erreur : "conda: command not found"

**Cause** : Anaconda pas dans le PATH système

**Solution Windows** :
1. Ouvrir "Variables d'environnement système"
2. Éditer la variable PATH
3. Ajouter : `C:\Users\VotreNom\Anaconda3` et `C:\Users\VotreNom\Anaconda3\Scripts`
4. Redémarrer le terminal

**Solution Linux/macOS** :
```bash
# Ajouter au fichier de configuration shell
echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

### ❌ Erreur : "Python version mismatch"

**Cause** : Mauvaise version de Python activée

**Solution** :
```bash
# Vérifier version actuelle
python --version

# Recréer l'environnement avec bonne version
conda deactivate
conda remove -n dt1_cameroun --all
conda create -n dt1_cameroun python=3.10 -y
conda activate dt1_cameroun
pip install -r requirements_base.txt
```

---

## 📓 PROBLÈMES JUPYTER NOTEBOOK

### ❌ Jupyter ne démarre pas

**Solutions** :
```bash
# 1. Réinstaller Jupyter
pip install --upgrade jupyter notebook

# 2. Lancer avec chemin complet
python -m jupyter notebook

# 3. Vérifier les ports occupés
jupyter notebook --port=8889  # Essayer autre port
```

---

### ❌ Kernel "dt1_cameroun" introuvable dans Jupyter

**Cause** : Kernel not registered

**Solution** :
```bash
# Installer ipykernel
pip install ipykernel

# Enregistrer l'environnement comme kernel
python -m ipykernel install --user --name=dt1_cameroun --display-name="Python (DT1 Cameroun)"

# Relancer Jupyter
jupyter notebook
```

---

### ❌ Notebook "Out of Memory" / MemoryError

**Cause** : Dataset trop gros pour la RAM

**Solutions** :
```python
# 1. Charger seulement un échantillon
import pandas as pd
df = pd.read_csv('data.csv', nrows=1000)  # Seulement 1000 lignes

# 2. Utiliser chunks
for chunk in pd.read_csv('data.csv', chunksize=500):
    # Traiter chunk par chunk
    pass

# 3. Optimiser types de données
df = pd.read_csv('data.csv', dtype={'col1': 'int32', 'col2': 'float32'})

# 4. Utiliser Colab (12 GB RAM gratuit)
```

---

### ❌ Cellules Jupyter ne s'exécutent pas

**Solutions** :
1. **Vérifier kernel** : En haut à droite, doit indiquer "Python (DT1 Cameroun)"
2. **Redémarrer kernel** : Menu "Kernel" → "Restart"
3. **Clear outputs** : Menu "Cell" → "All Output" → "Clear"
4. **Relancer Jupyter** : Fermer et rouvrir

---

## 🤖 PROBLÈMES MACHINE LEARNING

### ❌ Modèle trop lent à entraîner

**Causes et solutions** :

**1. Dataset trop gros**
```python
# Échantillonner les données
from sklearn.model_selection import train_test_split
X_sample, _, y_sample, _ = train_test_split(X, y, train_size=0.1, random_state=42)
```

**2. Trop d'estimateurs**
```python
# Réduire n_estimators
model = RandomForestClassifier(n_estimators=50)  # Au lieu de 200
```

**3. Pas de parallélisation**
```python
# Utiliser tous les CPU
model = RandomForestClassifier(n_jobs=-1)
```

**4. Utiliser LightGBM au lieu de XGBoost**
```python
import lightgbm as lgb
model = lgb.LGBMClassifier()  # 6-8x plus rapide que XGBoost
```

---

### ❌ GridSearchCV prend des heures

**Solutions** :
```python
# 1. Réduire la grille de recherche
param_grid = {
    'n_estimators': [50, 100],  # Au lieu de [50, 100, 200, 300]
    'max_depth': [5, 10]        # Au lieu de [3, 5, 7, 10, 15]
}

# 2. Utiliser RandomizedSearchCV
from sklearn.model_selection import RandomizedSearchCV
search = RandomizedSearchCV(model, param_distributions, n_iter=20)

# 3. Réduire CV folds
search = GridSearchCV(model, param_grid, cv=3)  # Au lieu de cv=5

# 4. Utiliser moins de données
X_subset = X_train[:1000]
y_subset = y_train[:1000]
```

---

### ❌ Modèle overfit (train 99%, test 60%)

**Causes et solutions** :

**1. Trop de features**
```python
from sklearn.feature_selection import SelectKBest, f_classif
selector = SelectKBest(f_classif, k=10)  # Garder top 10 features
X_train_selected = selector.fit_transform(X_train, y_train)
```

**2. Modèle trop complexe**
```python
# Random Forest: Réduire profondeur
model = RandomForestClassifier(max_depth=5, min_samples_split=10)

# XGBoost: Ajouter régularisation
model = xgb.XGBClassifier(max_depth=3, reg_alpha=0.1, reg_lambda=1.0)
```

**3. Pas assez de données**
```python
# Augmenter données avec SMOTE
from imblearn.over_sampling import SMOTE
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
```

---

### ❌ Accuracy élevée mais Recall très bas

**Cause** : Classes déséquilibrées

**Solutions** :
```python
# 1. Utiliser class_weight
model = RandomForestClassifier(class_weight='balanced')

# 2. Ajuster seuil de décision
y_proba = model.predict_proba(X_test)[:, 1]
y_pred = (y_proba >= 0.3).astype(int)  # Seuil à 0.3 au lieu de 0.5

# 3. SMOTE
from imblearn.over_sampling import SMOTE
smote = SMOTE()
X_res, y_res = smote.fit_resample(X_train, y_train)
```

---

## 📊 PROBLÈMES VISUALISATION

### ❌ Graphiques ne s'affichent pas dans Jupyter

**Solutions** :
```python
# Ajouter au début du notebook
%matplotlib inline
import matplotlib.pyplot as plt

# Ou utiliser
plt.show()  # À la fin de chaque plot
```

---

### ❌ Erreur : "ValueError: x and y must have same first dimension"

**Cause** : Dimensions incompatibles pour plot

**Solution** :
```python
# Vérifier dimensions
print(f"x shape: {x.shape}")
print(f"y shape: {y.shape}")

# S'assurer qu'elles correspondent
x = x.reshape(-1)  # Aplatir si nécessaire
y = y.reshape(-1)
```

---

### ❌ Figures trop petites / illisibles

**Solution** :
```python
# Augmenter taille
plt.figure(figsize=(12, 6))
plt.plot(x, y)

# Augmenter taille police
plt.rcParams.update({'font.size': 14})
```

---

## 📦 PROBLÈMES PACKAGES SPÉCIFIQUES

### ❌ XGBoost/LightGBM installation échoue

**Windows** :
```bash
# Installer via conda (plus fiable)
conda install -c conda-forge xgboost lightgbm
```

**Linux** :
```bash
# Installer dépendances build
sudo apt-get install cmake build-essential
pip install xgboost lightgbm
```

**Solution universelle : Utiliser Colab**
```python
# XGBoost et LightGBM pré-installés sur Colab
```

---

### ❌ SHAP prend trop de temps

**Solutions** :
```python
import shap

# 1. Utiliser échantillon
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test[:100])  # Seulement 100 samples

# 2. Désactiver interactions
explainer = shap.TreeExplainer(model, feature_perturbation='tree_path_dependent')
```

---

## 💾 PROBLÈMES DONNÉES

### ❌ "FileNotFoundError: No such file or directory"

**Causes et solutions** :

**1. Mauvais chemin**
```python
# Vérifier chemin actuel
import os
print(os.getcwd())

# Utiliser chemin absolu
df = pd.read_csv('/chemin/complet/vers/data.csv')

# Ou chemin relatif correct
df = pd.read_csv('../2_DONNEES/raw/data.csv')
```

**2. Fichier pas téléchargé**
```python
# Vérifier existence
import os
if not os.path.exists('data.csv'):
    print("Fichier manquant!")
```

---

### ❌ "UnicodeDecodeError" lors du chargement CSV

**Cause** : Mauvais encodage

**Solutions** :
```python
# Essayer différents encodages
encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
for encoding in encodings:
    try:
        df = pd.read_csv('data.csv', encoding=encoding)
        print(f"✅ Encodage {encoding} fonctionne!")
        break
    except UnicodeDecodeError:
        continue
```

---

### ❌ Valeurs manquantes (NaN) causent erreurs

**Solutions** :
```python
# 1. Supprimer lignes avec NaN
df_clean = df.dropna()

# 2. Remplir avec médiane
df['column'].fillna(df['column'].median(), inplace=True)

# 3. Imputation avancée
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
df[cols] = imputer.fit_transform(df[cols])
```

---

## 🌐 PROBLÈMES STREAMLIT

### ❌ "streamlit: command not found"

**Solution** :
```bash
# Installer Streamlit
pip install streamlit

# Tester
streamlit hello
```

---

### ❌ Application Streamlit plante

**Solutions** :
```python
# 1. Ajouter gestion erreurs
import streamlit as st

try:
    # Votre code
    pass
except Exception as e:
    st.error(f"Erreur : {e}")

# 2. Vérifier versions
pip install --upgrade streamlit

# 3. Relancer
streamlit run app.py --server.port 8502
```

---

## 📝 PROBLÈMES LATEX

### ❌ LaTeX ne compile pas

**Erreurs courantes** :

**1. Caractères spéciaux non échappés**
```latex
% ❌ Mauvais
50% de patients

% ✅ Bon
50\% de patients
```

**2. Packages manquants**
```latex
% Ajouter dans le préambule
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
```

**3. Bibliographie**
```bash
# Compiler dans l'ordre :
pdflatex main.tex
biber main  # ou bibtex main
pdflatex main.tex
pdflatex main.tex  # 2 fois pour les références
```

---

## 🔌 PROBLÈMES CONNEXION INTERNET

### Travailler offline

**Avant de perdre connexion** :
```bash
# 1. Télécharger toutes dépendances
pip download -r requirements_full.txt -d packages/

# 2. Installer offline
pip install --no-index --find-links=packages/ -r requirements_full.txt

# 3. Sauvegarder documentations
# Télécharger PDFs des docs officielles
```

**Utiliser Colab avec Google Drive** :
- Télécharger notebooks sur Drive quand connexion disponible
- Travailler offline dans Colab montant Drive
- Synchroniser quand connexion revient

---

## 🆘 COMMENT DÉBUGGER

### Méthodologie générale

1. **Lire le message d'erreur complet**
   - Dernière ligne = type d'erreur
   - Lignes précédentes = où l'erreur s'est produite

2. **Googler l'erreur**
   ```
   Copier-coller message d'erreur + "python" dans Google
   ```

3. **Vérifier versions**
   ```python
   import package_name
   print(package_name.__version__)
   ```

4. **Tester avec exemple minimal**
   ```python
   # Isoler le problème
   # Commenter tout le code sauf la ligne problématique
   ```

5. **Demander aide**
   - Stack Overflow
   - Dr. TCHAPET NJAFA Jean-Pierre
   - Forum du cours

---

## 📞 RESSOURCES D'AIDE

- **Stack Overflow** : https://stackoverflow.com/ (chercher erreur)
- **Documentation Scikit-learn** : https://scikit-learn.org/
- **Documentation Pandas** : https://pandas.pydata.org/
- **Forum Machine Learning** : https://www.reddit.com/r/machinelearning/
- **GitHub Issues** : Chercher si d'autres ont eu le même problème

---

## ✅ SI TOUT EST CASSÉ : RÉINITIALISATION COMPLÈTE

Dernier recours si rien ne fonctionne :

```bash
# 1. Supprimer environnement
conda deactivate
conda env remove -n dt1_cameroun

# 2. Nettoyer cache
conda clean --all -y
pip cache purge

# 3. Recréer de zéro
conda create -n dt1_cameroun python=3.10 -y
conda activate dt1_cameroun

# 4. Réinstaller
pip install -r requirements_base.txt

# 5. Tester
python test_installation.py
```

---

**Rappel** : 90% des problèmes ont déjà été rencontrés par quelqu'un d'autre. Google est votre ami ! 🔍

*Guide de dépannage - Projet Master 2 Sorelle*
*Dernière mise à jour : Novembre 2025*
