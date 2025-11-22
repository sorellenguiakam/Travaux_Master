# 📝 MÉMOIRE LATEX

Structure LaTeX du mémoire de Master 2.

## 📁 Structure

```
6_MEMOIRE_LATEX/
├── main.tex              # Document principal
├── bibliographie.bib     # Références (64+ entrées)
├── sections/             # Chapitres du mémoire
│   ├── 00_page_garde.tex
│   ├── 01_introduction.tex  (PRÉ-REMPLIE)
│   ├── 02_etat_art.tex
│   ├── 03_methodologie.tex
│   ├── 04_resultats.tex
│   ├── 05_discussion.tex
│   └── 06_conclusion.tex
├── figures/              # Figures (à générer depuis notebooks)
└── tableaux/             # Tableaux LaTeX
```

## 🔧 Compilation

```bash
cd 6_MEMOIRE_LATEX

# Compilation complète
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# OU utiliser latexmk (recommandé)
latexmk -pdf main.tex
```

## 📊 Contenu pré-rempli

**01_introduction.tex** (11 KB):
- Contexte épidémiologique DT1 en Afrique
- Problématique dataset shift
- Justification biomarqueurs
- Objectifs du projet

**Reste à compléter:**
- État de l'art (40-50 références)
- Méthodologie détaillée
- Résultats + figures
- Discussion
- Conclusion + Abstract

## 📖 Bibliographie

**bibliographie.bib:** 64+ références
- DT1 Afrique (Katte, Kengne, Oram)
- Biomarqueurs (Endocrine J. 2023)
- Algorithmes ML (XGBoost, LightGBM, RF)
- Interprétabilité (SHAP, LIME)
- Méthodologie (SMOTE, validation)
- Livres (Hastie ESL, James ISLR)

**Citation:** `\cite{Katte2023}`

## 📏 Contraintes

- **Maximum:** 60 pages (hors annexes)
- **Langue:** Français
- **Format:** A4, 12pt
- **Marges:** 2.5cm

## 🎨 Génération des figures

Les figures doivent être générées depuis les notebooks:

```python
# Dans chaque notebook
plt.savefig('../6_MEMOIRE_LATEX/figures/nom_figure.pdf', 
            dpi=300, bbox_inches='tight')
```

**Formats acceptés:** PDF (vectoriel recommandé), PNG (300 dpi min)

---
*Compilation testée avec TeX Live 2025*
