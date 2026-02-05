# 🔧 SCRIPTS DE PRODUCTION

Ce dossier est destiné aux scripts et modèles finaux optimisés pour la production.

## 📁 Structure

```
4_SCRIPTS_PRODUCTION/
├── models/          # Modèles ML sauvegardés
├── utils/           # Scripts utilitaires
└── README.md
```

## 📦 Contenu attendu

### models/
**Fichiers générés après optimisation (Semaine 6):**
- `final_model.pkl` - Modèle XGBoost/RF optimisé final
- `features.pkl` - Liste des features utilisées
- `scaler.pkl` - StandardScaler si nécessaire
- `rapport_modele_final.txt` - Rapport de performances

**Sauvegarde depuis notebook Semaine 6:**
```python
import joblib

# Sauvegarder le modèle
joblib.dump(modele_final, '../4_SCRIPTS_PRODUCTION/models/final_model.pkl')
joblib.dump(features, '../4_SCRIPTS_PRODUCTION/models/features.pkl')
```

### utils/
**Scripts utilitaires optionnels:**
- `preprocessing.py` - Fonctions de prétraitement réutilisables
- `evaluation.py` - Fonctions de calcul des métriques
- `visualization.py` - Fonctions de visualisation
- `prediction.py` - Pipeline de prédiction

**Note:** Ces scripts ne sont **pas obligatoires** pour le projet Master 2. Ils peuvent être créés si besoin pour réutiliser du code.

## 🚀 Utilisation

### Charger le modèle final:
```python
import joblib
import pandas as pd

# Charger le modèle et features
modele = joblib.load('4_SCRIPTS_PRODUCTION/models/final_model.pkl')
features = joblib.load('4_SCRIPTS_PRODUCTION/models/features.pkl')

# Prédire sur nouvelles données
X_new = pd.DataFrame({
    'age': [30],
    'IMC': [25.5],
    'glycemie_jeun': [7.2],
    'HbA1c': [6.5],
    'ANP32A_IT1': [3.8],
    'ESCO2': [4.2],
    'NBPF1': [2.8]
})

prediction = modele.predict(X_new)
probabilite = modele.predict_proba(X_new)[:, 1]

print(f"Prédiction: {'DT1+' if prediction[0] == 1 else 'Sain'}")
print(f"Probabilité DT1+: {probabilite[0]*100:.1f}%")
```

## ⚠️ État actuel

**Ce dossier sera rempli après:**
- Semaine 6: Optimisation et sauvegarde du modèle final
- Semaine 7: Génération de toutes les figures finales

**Pour l'instant:** Les dossiers `models/` et `utils/` sont vides (normal).

---
*Scripts de production - Sera complété durant le projet*
