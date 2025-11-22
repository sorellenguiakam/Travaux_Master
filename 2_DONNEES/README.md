# 📊 DONNÉES

Ce dossier contient les données synthétiques du projet et les scripts de prétraitement.

## 📁 Structure

```
2_DONNEES/
├── raw/                          # Données brutes
│   └── dataset_dt1_cameroun_synthetic.csv
├── processed/                    # Données nettoyées
│   └── dataset_clean.csv
├── scripts_preprocessing/        # Scripts de nettoyage
│   └── 01_nettoyage.py
├── generate_synthetic_data.py    # Génération du dataset
└── README.md
```

## 🔬 Dataset synthétique

**Fichier:** `raw/dataset_dt1_cameroun_synthetic.csv`  
**Taille:** 1000 patients  
**Variables:** 12 colonnes

### Variables incluses:

**Démographiques:**
- `patient_id`: Identifiant unique
- `age`: Âge (5-80 ans)
- `sexe`: M/F

**Cliniques:**
- `IMC`: Indice de Masse Corporelle
- `glycemie_jeun`: Glycémie à jeun (mmol/L)
- `HbA1c`: Hémoglobine glyquée (%)
- `antecedents_familiaux`: 0/1

**Biomarqueurs génétiques (principaux):**
- `ANP32A_IT1`: Expression du gène ANP32A-IT1
- `ESCO2`: Expression du gène ESCO2
- `NBPF1`: Expression du gène NBPF1

**Cible:**
- `diagnostic`: 0 (Sain) ou 1 (DT1+)

### Distribution:
- **DT1+:** 250 patients (25%)
- **Sains:** 750 patients (75%)

## 🔧 Génération des données

```bash
# Générer le dataset synthétique
python generate_synthetic_data.py

# Nettoyer les données
cd scripts_preprocessing
python 01_nettoyage.py
```

## ✨ Dataset nettoyé

**Fichier:** `processed/dataset_clean.csv`

**Prétraitement appliqué:**
- Imputation des valeurs manquantes (médiane)
- Détection des outliers (IQR method - conservés)
- Encodage variables catégorielles
- Ajout features encodées

**Prêt pour modélisation ML!**

---
*Données synthétiques - Ne pas utiliser en clinique*
