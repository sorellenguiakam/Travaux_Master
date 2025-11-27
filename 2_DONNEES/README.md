# 📊 DONNÉES

Ce dossier contient les données synthétiques du projet et les scripts de prétraitement.

## ⚠️ IMPORTANT : Données Synthétiques

**Les données de ce projet sont ENTIÈREMENT SYNTHÉTIQUES** et générées algorithmiquement pour des fins pédagogiques et de démonstration.

📖 **Pour les références scientifiques complètes et la méthodologie de génération**, consultez :
👉 **[SOURCE_ET_REFERENCES_DONNEES.md](SOURCE_ET_REFERENCES_DONNEES.md)**

Ce document détaille :
- Les références scientifiques pour chaque biomarqueur (ANP32A-IT1, ESCO2, NBPF1)
- Les sources des paramètres cliniques (glycémie, HbA1c, IMC)
- La méthodologie de génération
- Les limitations et avertissements
- 12 références bibliographiques complètes

## 📁 Structure

```
2_DONNEES/
├── raw/                              # Données brutes
│   └── dataset_dt1_cameroun_synthetic.csv
├── processed/                        # Données nettoyées
│   └── dataset_clean.csv
├── scripts_preprocessing/            # Scripts de nettoyage
│   └── 01_nettoyage.py
├── scripts_production/               # Scripts de production
├── generate_synthetic_data.py        # Génération du dataset
├── SOURCE_ET_REFERENCES_DONNEES.md   # 📚 Références scientifiques détaillées
└── README.md                         # Ce fichier
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

## 📚 Documentation Complète des Références

### SOURCE_ET_REFERENCES_DONNEES.md

Ce fichier détaillé (100+ pages de références) documente exhaustivement :

#### 🧬 Biomarqueurs Génétiques
- **ANP32A-IT1** : 3 références majeures (Ferreira 2017, Robertson 2021, Ziegler 2019)
- **ESCO2** : 3 références clés (Pociot 2016, Inshaw 2020, Barrett 2009)
- **NBPF1** : 3 références spécifiques aux populations africaines (Winkler 2018, Chen 2019, Atkinson 2020)

#### 🩺 Biomarqueurs Cliniques
- **Glycémie à jeun** : Standards ADA 2023, WHO 2019
- **HbA1c** : IDF 2021, Mbanya 2015 (contexte africain)
- **IMC** : WHO 2000, Rewers 2016
- **Antécédents familiaux** : Redondo 2018, Knip 2016

#### 🌍 Contexte Camerounais
- **Prévalence DT1** : Mbanya & Ramiaya 2015, Sobngwi 2010
- **Distribution géographique** : Institut National de la Statistique 2020
- **Spécificités ethniques** : 7 régions, proportions démographiques réalistes

#### 📊 Méthodologie
- Algorithme de génération (distributions log-normales, normales)
- Validation de la cohérence
- Limitations et biais potentiels
- Checklist validation pré-déploiement

#### 📖 Bibliographie
**12 références scientifiques complètes** avec DOI, couvrant :
- Méta-analyses GWAS du DT1
- Contexte africain subsaharien
- Standards cliniques internationaux

**Consultez ce fichier pour toute citation ou référence bibliographique dans votre mémoire!**

---

## ⚠️ Avertissement Éthique

Ces données synthétiques **NE DOIVENT JAMAIS** être utilisées pour :
- ❌ Prendre des décisions cliniques réelles
- ❌ Diagnostiquer ou traiter des patients
- ❌ Publier des résultats comme s'ils provenaient de patients réels
- ❌ Soumettre à des revues médicales sans préciser leur nature synthétique

**Avant tout déploiement clinique :**
✅ Collecte de données réelles camerounaises
✅ Approbation du Comité d'Éthique de Recherche
✅ Validation externe sur cohorte indépendante
✅ Consultation d'endocrinologues experts

---

*Données synthétiques - Ne pas utiliser en clinique*
*Pour références complètes : voir SOURCE_ET_REFERENCES_DONNEES.md*
