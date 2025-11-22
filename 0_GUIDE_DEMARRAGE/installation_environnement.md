# 🔧 Guide d'Installation de l'Environnement

Ce guide vous accompagne pas à pas dans l'installation de tous les outils nécessaires pour votre projet de Master 2.

---

## ⏱️ Temps estimé : 30-45 minutes

---

## 📋 Prérequis Système

### Configuration minimale
- **RAM** : 8 GB (recommandé 16-32 GB)
- **Processeur** : Intel i5 ou équivalent (i7 11e gen disponible ✅)
- **Espace disque** : 5 GB minimum (10 GB recommandé)
- **Système d'exploitation** : Windows 10/11, macOS 10.14+, ou Linux (Ubuntu 18.04+)
- **Connexion internet** : Nécessaire pour téléchargement initial (puis travail offline possible)

### Votre configuration
- ✅ 32 GB RAM
- ✅ Intel i7 11e génération
- ⚠️ Pas de GPU dédié (mais Google Colab disponible pour tâches intensives)

---

## 🐍 Étape 1 : Installer Python via Anaconda (15 minutes)

### Pourquoi Anaconda ?
- Gère les environnements virtuels facilement
- Pré-installe de nombreuses bibliothèques scientifiques
- Évite les conflits entre versions de packages

### Installation Windows

1. **Télécharger Anaconda**
   - Aller sur : https://www.anaconda.com/products/distribution
   - Choisir "Download" pour Windows
   - Version : Python 3.10 ou 3.11

2. **Exécuter l'installateur**
   - Double-cliquer sur le fichier `.exe` téléchargé
   - **Important** : Cocher "Add Anaconda to PATH" (malgré avertissement)
   - Cocher "Register Anaconda as default Python"
   - Suivre les instructions (installation complète)

3. **Vérifier l'installation**
   - Ouvrir "Anaconda Prompt" (chercher dans le menu Démarrer)
   - Taper :
     ```bash
     python --version
     ```
   - Attendu : `Python 3.10.x` ou `Python 3.11.x`

### Installation macOS

1. **Télécharger Anaconda**
   - Aller sur : https://www.anaconda.com/products/distribution
   - Choisir "Download" pour macOS

2. **Exécuter l'installateur**
   ```bash
   bash ~/Downloads/Anaconda3-*-MacOSX-x86_64.sh
   # Ou pour Apple Silicon (M1/M2):
   bash ~/Downloads/Anaconda3-*-MacOSX-arm64.sh
   ```
   - Accepter la licence (taper "yes")
   - Choisir emplacement d'installation (défaut recommandé)

3. **Vérifier**
   - Ouvrir Terminal
   - Taper : `python --version`

### Installation Linux (Ubuntu/Debian)

```bash
# Télécharger
wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh

# Installer
bash Anaconda3-2024.02-1-Linux-x86_64.sh

# Recharger le shell
source ~/.bashrc

# Vérifier
python --version
```

---

## 📦 Étape 2 : Créer l'Environnement Virtuel (5 minutes)

### Qu'est-ce qu'un environnement virtuel ?
Un espace isolé où vos packages Python ne interfèrent pas avec d'autres projets.

### Création

```bash
# Ouvrir Anaconda Prompt (Windows) ou Terminal (macOS/Linux)

# Créer environnement nommé "dt1_cameroun" avec Python 3.10
conda create -n dt1_cameroun python=3.10 -y

# Attendre la fin de l'installation (2-3 minutes)
```

### Activation

```bash
# Activer l'environnement
conda activate dt1_cameroun

# Votre prompt devrait maintenant afficher: (dt1_cameroun)
```

**Important** : Vous devrez activer cet environnement à chaque nouvelle session de travail !

---

## 📚 Étape 3 : Installer les Bibliothèques Python (10-15 minutes)

### Naviguer vers le projet

```bash
# Aller dans le dossier du projet
cd chemin/vers/projet_dt1_cameroun

# Exemple Windows:
# cd C:\Users\Sorelle\Documents\projet_dt1_cameroun

# Exemple macOS/Linux:
# cd ~/Documents/projet_dt1_cameroun
```

### Installation des dépendances de base

```bash
# Installer depuis requirements_base.txt
pip install -r requirements_base.txt

# Durée estimée: 5-10 minutes
# Vous verrez défiler les installations
```

**Packages installés** :
- `numpy`, `pandas` : Manipulation de données
- `scikit-learn` : Machine Learning
- `matplotlib`, `seaborn` : Visualisation
- `jupyter` : Notebooks interactifs

### Vérification de l'installation

```bash
# Tester les imports
python -c "import numpy; import pandas; import sklearn; print('✅ Tous les imports réussis!')"
```

Si vous voyez "✅ Tous les imports réussis!", c'est bon !

### Installation des packages supplémentaires (optionnel maintenant, requis plus tard)

```bash
# Pour plus tard dans le projet (Semaines 4-5)
pip install xgboost lightgbm shap lime
```

---

## 📓 Étape 4 : Installer et Tester Jupyter (5 minutes)

### Vérifier Jupyter

```bash
# Jupyter devrait déjà être installé via requirements_base.txt
jupyter --version
```

### Configurer Jupyter pour l'environnement

```bash
# Enregistrer l'environnement comme kernel Jupyter
python -m ipykernel install --user --name=dt1_cameroun --display-name="Python (DT1 Cameroun)"
```

### Lancer Jupyter

```bash
# Lancer Jupyter Notebook
jupyter notebook

# Votre navigateur devrait s'ouvrir automatiquement
# Sinon, copier-coller l'URL affichée (http://localhost:8888/...)
```

### Test

1. Dans le navigateur, naviguer vers `3_NOTEBOOKS_PEDAGOGIQUES/`
2. Créer un nouveau notebook : "New" → "Python (DT1 Cameroun)"
3. Dans une cellule, taper :
   ```python
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt

   # Test simple
   x = np.linspace(0, 10, 100)
   plt.plot(x, np.sin(x))
   plt.title("Test d'installation ✅")
   plt.show()

   print("Environnement prêt!")
   ```
4. Exécuter (Shift + Enter)
5. Vous devriez voir un graphique sinusoïdal

---

## 🎨 Étape 5 : Configurer un Éditeur de Texte (optionnel, 10 minutes)

Pour éditer les scripts `.py` en dehors de Jupyter.

### Option 1 : VS Code (recommandé)

1. **Télécharger** : https://code.visualstudio.com/
2. **Installer** : Suivre instructions
3. **Extensions essentielles** :
   - Python (Microsoft)
   - Jupyter (Microsoft)
   - Python Docstring Generator
   - GitLens (pour versioning)

4. **Configuration Python** :
   - Ouvrir VS Code
   - Ouvrir le dossier du projet
   - Ctrl+Shift+P → "Python: Select Interpreter"
   - Choisir "dt1_cameroun"

### Option 2 : PyCharm Community (alternative)

1. **Télécharger** : https://www.jetbrains.com/pycharm/download/
2. **Installer** version Community (gratuite)
3. **Configurer** :
   - Ouvrir le projet
   - File → Settings → Project → Python Interpreter
   - Ajouter l'environnement Conda "dt1_cameroun"

### Option 3 : Utiliser seulement Jupyter (simple)

Si vous débutez, Jupyter suffit pour tout le projet !

---

## 🔍 Étape 6 : Vérification Finale (5 minutes)

### Checklist d'installation

Exécutez ce script de vérification :

```bash
# Créer un fichier test
cat > test_installation.py << 'EOF'
"""
Script de vérification de l'installation
"""
print("=" * 50)
print("VÉRIFICATION DE L'ENVIRONNEMENT DT1 CAMEROUN")
print("=" * 50)

# Test imports
packages = [
    ('numpy', 'np'),
    ('pandas', 'pd'),
    ('sklearn', 'sklearn'),
    ('matplotlib', 'matplotlib'),
    ('seaborn', 'sns'),
    ('jupyter', 'jupyter'),
]

for package_name, import_name in packages:
    try:
        __import__(import_name if import_name != package_name else package_name)
        print(f"✅ {package_name.ljust(15)} : OK")
    except ImportError:
        print(f"❌ {package_name.ljust(15)} : MANQUANT")

print("=" * 50)

# Test versions
import numpy as np
import pandas as pd
import sklearn

print(f"\nVersions installées:")
print(f"  NumPy      : {np.__version__}")
print(f"  Pandas     : {pd.__version__}")
print(f"  Scikit-learn : {sklearn.__version__}")

print("\n" + "=" * 50)
print("✅ ENVIRONNEMENT PRÊT !")
print("=" * 50)
EOF

# Exécuter
python test_installation.py
```

Tous les packages doivent afficher "OK".

---

## 🆘 Problèmes Fréquents et Solutions

### Problème 1 : "conda: command not found"

**Cause** : Anaconda n'est pas dans le PATH

**Solution Windows** :
1. Chercher "Variables d'environnement" dans Windows
2. Éditer PATH
3. Ajouter : `C:\Users\VotreNom\Anaconda3\Scripts`

**Solution macOS/Linux** :
```bash
echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Problème 2 : "pip install" échoue avec erreur de permission

**Solution** :
```bash
# Utiliser --user
pip install --user -r requirements_base.txt
```

### Problème 3 : Jupyter ne trouve pas l'environnement

**Solution** :
```bash
# Réinstaller ipykernel
conda install ipykernel -y
python -m ipykernel install --user --name=dt1_cameroun
```

### Problème 4 : Installation très lente

**Solutions** :
```bash
# Utiliser les miroirs plus rapides
conda config --add channels conda-forge
conda config --set channel_priority strict

# Ou utiliser mamba (plus rapide)
conda install mamba -y
mamba install -c conda-forge <package>
```

### Problème 5 : Espace disque insuffisant

**Solutions** :
- Nettoyer cache Conda : `conda clean --all -y`
- Désinstaller packages non-utilisés
- Libérer espace sur le disque

---

## 📱 Configuration pour Travail Offline

### Télécharger tout en une fois (si connexion disponible)

```bash
# Installer toutes les dépendances
pip install -r requirements_full.txt

# Télécharger documentations en local
pip install --download docs/ numpy pandas scikit-learn
```

### Sauvegarder l'environnement

```bash
# Exporter l'environnement complet
conda env export > environment.yml

# Pour recréer plus tard (sur autre machine):
# conda env create -f environment.yml
```

---

## 🎯 Google Colab : Alternative Cloud (gratuit)

Si problèmes d'installation locale :

1. **Accéder** : https://colab.research.google.com/
2. **Se connecter** avec compte Google
3. **Avantages** :
   - Rien à installer
   - GPU gratuit (15 GB VRAM)
   - Packages pré-installés
4. **Inconvénients** :
   - Nécessite connexion internet
   - Sessions limitées (12h max)
   - Fichiers non persistants (sauvegarder sur Google Drive)

### Utiliser Colab pour ce projet

```python
# Dans un notebook Colab, installer packages manquants:
!pip install lightgbm shap lime streamlit

# Monter Google Drive pour sauvegarder
from google.colab import drive
drive.mount('/content/drive')
```

---

## ✅ Prochaines Étapes

Maintenant que votre environnement est installé :

1. ✅ Fermer Anaconda Prompt / Terminal
2. ✅ Rouvrir et taper `conda activate dt1_cameroun`
3. ✅ Naviguer vers le projet : `cd chemin/vers/projet_dt1_cameroun`
4. ✅ Lancer Jupyter : `jupyter notebook`
5. ✅ Ouvrir `3_NOTEBOOKS_PEDAGOGIQUES/Semaine01_Introduction_Python_ML.ipynb`
6. ✅ Commencer les exercices !

---

## 📞 Besoin d'Aide ?

- **Problèmes techniques** : Consulter `troubleshooting.md`
- **Erreurs spécifiques** : Google le message d'erreur complet
- **Blocage** : Contacter Dr. TCHAPET NJAFA Jean-Pierre

---

**Félicitations ! Votre environnement est prêt pour 14 semaines de Machine Learning ! 🎉**

*Document créé pour le projet Master 2 de Sorelle*
*Dernière mise à jour : Novembre 2025*
