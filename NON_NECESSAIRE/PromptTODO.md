# CONTEXTE DU PROJET

Tu es un expert en Biophysique, Intelligence Artificielle médicale et pédagogie, chargé de concevoir un projet de mémoire de Master 1 complet et clé-en-main pour une étudiante camerounaise (Sorelle) en Physique Atomique, Moléculaire et Biophysique.

## CONTRAINTES CRITIQUES

**Durée:** 14 semaines (incluant la rédaction du mémoire)
**Ressources computationnelles:** 
- Machine locale: 32GB RAM, Intel i7 11e gen, pas de GPU dédié
- Accès à Google Colab (GPU gratuit limité)
- Connexion internet INTERMITTENTE (privilégier téléchargements ponctuels, travail offline)

**Niveau de l'étudiante:**
- Python: débutant (nécessite codes très commentés)
- Machine Learning: aucune expérience (tutoriels intégrés obligatoires)
- LaTeX: maîtrise confirmée

**Ancrage géographique IMPÉRATIF:**
- Contexte: Cameroun et Afrique subsaharienne
- Problématique: Santé publique avec données/réalités locales
- Éviter tout "parachutage" de solutions occidentales non adaptées

## THÉMATIQUE VALIDÉE

**Sujet affiné suite aux remarques du Prof. NANA Engo:**

"Détection précoce du Diabète de Type 1 en Afrique subsaharienne par apprentissage automatique : identification de biomarqueurs génétiques adaptés aux populations camerounaises"

**Justification scientifique (issues de Rapport.md):**
1. Le DT1 est sous-diagnostiqué en Afrique (forme idiopathique sans auto-anticorps)
2. Les modèles occidentaux (entraînés sur populations caucasiennes) sont inefficaces (dataset shift)
3. Biomarqueurs validés (ANP32A-IT1, ESCO2, NBPF1) mais nécessitent adaptation locale
4. Besoin réel: outils de détection précoce adaptés génétiquement aux Africains
5. Mortalité infantile élevée due au retard diagnostique

## LIVRABLES ATTENDUS

### 1. MÉMOIRE LaTeX (structure pré-remplie)
- Template complet avec bibliographie africaine déjà intégrée
- Sections pré-rédigées (Introduction, État de l'art) basées sur sources accessibles
- Espaces clairement identifiés pour résultats de l'étudiante
- Citations correctement formatées (BibTeX fourni)

### 2. PIPELINE DE CODE FONCTIONNEL
- Scripts Python reproductibles, exécutables séquentiellement
- Notebooks Colab avec outputs sauvegardés (pour référence offline)
- Gestion intelligente des ressources (batch processing, modèles légers)
- Tests unitaires simples pour validation des étapes

### 3. APPLICATION DE DÉMONSTRATION
- Dashboard interactif (Streamlit ou Gradio, déployable localement)
- Interface permettant:
  - Upload de données de biomarqueurs
  - Prédiction du risque de DT1
  - Visualisation des résultats (importance des features, courbes ROC)
  - Génération de rapport PDF pour usage clinique

### 4. DATASETS NETTOYÉS ET ANNOTÉS
- Données synthétiques réalistes si données réelles camerounaises indisponibles
- Métadonnées détaillées (dictionnaire de données)
- Scripts de nettoyage et preprocessing documentés
- Validation de la qualité des données

## STRUCTURE D'ARBORESCENCE REQUISE

```
projet_dt1_cameroun/
│
├── 0_GUIDE_DEMARRAGE/
│   ├── README_FIRST.md (guide de démarrage pas-à-pas)
│   ├── installation_environnement.md
│   └── troubleshooting.md
│
├── 1_CONTEXTE_THEORIQUE/
│   ├── fiches_concepts_ml.md (glossaire illustré)
│   ├── biologie_dt1_afrique.md
│   └── references_bibliographiques.bib
│
├── 2_DONNEES/
│   ├── raw/ (données brutes + sources)
│   ├── processed/ (données nettoyées)
│   ├── synthetic/ (données synthétiques pour tests)
│   ├── dictionnaire_donnees.xlsx
│   └── scripts_preprocessing/
│       ├── 01_nettoyage.py
│       ├── 02_feature_engineering.py
│       └── 03_split_train_test.py
│
├── 3_NOTEBOOKS_PEDAGOGIQUES/
│   ├── Semaine01_Introduction_Python_ML.ipynb
│   ├── Semaine02_Exploration_Donnees.ipynb
│   ├── Semaine03_Modelisation_Simple.ipynb
│   ├── Semaine04-05_Modeles_Avances.ipynb
│   ├── Semaine06_Optimisation_Validation.ipynb
│   └── Semaine07_Interpretation_Resultats.ipynb
│
├── 4_SCRIPTS_PRODUCTION/
│   ├── pipeline_complet.py (script principal)
│   ├── config.yaml (paramètres centralisés)
│   ├── models/ (modèles entraînés sauvegardés)
│   └── utils/ (fonctions réutilisables)
│
├── 5_APPLICATION_DEMO/
│   ├── app_streamlit.py
│   ├── requirements_app.txt
│   ├── assets/ (logos, images)
│   └── exemples_test/ (cas d'usage)
│
├── 6_MEMOIRE_LATEX/
│   ├── main.tex (document principal pré-structuré)
│   ├── sections/
│   │   ├── 01_introduction.tex (pré-remplie)
│   │   ├── 02_etat_art.tex (pré-remplie)
│   │   ├── 03_methodologie.tex (template)
│   │   ├── 04_resultats.tex (template avec exemples)
│   │   ├── 05_discussion.tex (template)
│   │   └── 06_conclusion.tex (template)
│   ├── figures/ (graphiques générés automatiquement)
│   ├── tableaux/ (exports CSV→LaTeX)
│   └── bibliographie.bib (500+ références africaines)
│
├── 7_PLANIFICATION/
│   ├── calendrier_14_semaines.md (détaillé jour par jour)
│   ├── checklist_livrables.md
│   └── criteres_evaluation.md
│
└── 8_RESSOURCES_COMPLEMENTAIRES/
    ├── tutoriels_video_recommandes.md
    ├── articles_cles_annottes.pdf
    └── contacts_experts_cameroun.md
```

## INSTRUCTIONS POUR TOI (Claude)

### PHASE 1: RECHERCHE APPROFONDIE (Utilise web_search intensivement)

**Recherche 1-5:** Données camerounaises
- Cherche: "Cameroon diabetes type 1 genetic data", "African biomarkers diabetes", "sub-Saharan diabetes datasets public"
- Identifie: bases de données publiques (NCBI, ENA), publications avec données supplémentaires
- Objectif: Trouver AU MOINS 3 sources de données réelles ou protocoles pour générer données synthétiques réalistes

**Recherche 6-10:** Modèles légers et efficaces
- Cherche: "lightweight machine learning diabetes", "edge ML medical diagnosis", "CPU-friendly deep learning"
- Identifie: architectures optimisées (Random Forest, XGBoost, LightGBM, MobileNet si images)
- Objectif: Garantir temps d'entraînement <2h sur config étudiante

**Recherche 11-15:** Littérature africaine
- Cherche: "diabetes Africa scholarly articles", "Cameroon endocrinology research", auteurs: "Sobngwi", "Mbanya", "Kengne"
- Identifie: 50+ publications pertinentes (PubMed, Google Scholar)
- Objectif: Construire bibliographie authentiquement africaine

**Recherche 16-20:** Outils pédagogiques ML
- Cherche: "machine learning tutorials beginners healthcare", "scikit-learn medical examples"
- Identifie: ressources francophones si disponibles
- Objectif: Intégrer tutoriels progressifs dans notebooks

### PHASE 2: CONSTRUCTION DU CALENDRIER (Très détaillé)

Crée un fichier `demarche_methodologique_sorelle.md` structuré ainsi:

```markdown
# SEMAINE X: [Titre thématique]

## Objectifs pédagogiques
- [ ] Objectif 1 (mesurable)
- [ ] Objectif 2
- [ ] Objectif 3

## Livrables de la semaine
1. **Livrable technique** (ex: script de nettoyage fonctionnel)
2. **Livrable documentaire** (ex: section mémoire rédigée)

## Programme détaillé

### Jour 1 (Lundi): [Focus du jour]
**Matin (3h):**
- Tâche 1: [Description précise] → Fichier: `chemin/vers/fichier.py`
- Tâche 2: [...]

**Après-midi (3h):**
- Tâche 3: [...]
- ⚠️ Point de vigilance: [Piège courant à éviter]

**Ressources:**
- 📖 Lecture: [Article/chapitre spécifique]
- 🎥 Vidéo (optionnelle): [Lien YouTube si pertinent]
- 💻 Code de référence: `chemin/notebook.ipynb`

### Jour 2-5: [Idem, structure répétée]

## Auto-évaluation fin de semaine
- [ ] J'ai compris [concept clé 1]
- [ ] Je sais exécuter [compétence technique]
- [ ] J'ai documenté mes résultats dans [section mémoire]

## Si retard/difficulté
- Plan B: [Alternative simplifiée]
- Ressources d'aide: [Où chercher aide]
```

**Distribution temporelle suggérée (à affiner):**
- Semaines 1-2: Fondamentaux ML + exploration données
- Semaines 3-5: Modélisation et expérimentations
- Semaines 6-7: Optimisation et interprétation
- Semaines 8-9: Application démo + visualisations
- Semaines 10-12: Rédaction mémoire (sections résultats/discussion)
- Semaines 13-14: Finalisation, relecture, préparation soutenance

### PHASE 3: GÉNÉRATION DES CODES

**Principes directeurs:**
1. **Commentaires abondants** (ratio 1 ligne code = 1 ligne commentaire)
2. **Gestion des erreurs systématique** (try/except avec messages clairs)
3. **Compatibilité offline** (téléchargements séparés, caching)
4. **Logs détaillés** (progression visible, temps d'exécution)
5. **Modularité** (fonctions réutilisables, pas de monolithes)

**Exemple de structure attendue pour CHAQUE script:**

```python
"""
TITRE: [Nom descriptif du script]
OBJECTIF: [Ce que fait le script]
INPUTS: [Fichiers/paramètres requis]
OUTPUTS: [Fichiers générés]
DURÉE ESTIMÉE: [Temps d'exécution sur config étudiante]
AUTEUR: Claude 4.5 (adapté contexte camerounais)
DATE: [Date génération]
"""

# === IMPORTS ===
import pandas as pd  # Manipulation données tabulaires
import numpy as np   # Calculs numériques
# ... (imports groupés par thématique)

# === CONFIGURATION ===
CONFIG = {
    'chemin_donnees': '../2_DONNEES/raw/dataset.csv',
    'seuil_qualite': 0.95,  # 95% valeurs non-manquantes
    # ... (tous paramètres centralisés)
}

# === FONCTIONS UTILITAIRES ===
def charger_donnees_robuste(chemin, encodage='utf-8'):
    """
    Charge CSV avec gestion erreurs multiples encodages.
    
    Args:
        chemin (str): Chemin vers fichier CSV
        encodage (str): Encodage à tester en premier
    
    Returns:
        pd.DataFrame: Données chargées
        
    Raises:
        FileNotFoundError: Si fichier introuvable
    
    Exemple:
        >>> df = charger_donnees_robuste('data.csv')
        >>> print(df.shape)
        (1000, 25)
    """
    try:
        return pd.read_csv(chemin, encoding=encodage)
    except UnicodeDecodeError:
        # Tentative encodage alternatif (fréquent avec données africaines)
        return pd.read_csv(chemin, encoding='latin-1')
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ Fichier non trouvé: {chemin}")

# === SCRIPT PRINCIPAL ===
def main():
    """Point d'entrée principal avec orchestration des étapes."""
    
    print("="*60)
    print("🚀 DÉMARRAGE: Nettoyage des données DT1 Cameroun")
    print("="*60)
    
    # ÉTAPE 1: Chargement
    print("\n📂 Étape 1/5: Chargement des données...")
    df = charger_donnees_robuste(CONFIG['chemin_donnees'])
    print(f"   ✅ {df.shape[0]} lignes, {df.shape[1]} colonnes chargées")
    
    # ÉTAPE 2: Nettoyage
    # ... (code avec prints informatifs à chaque étape)
    
    # ÉTAPE 5: Sauvegarde
    print("\n💾 Étape 5/5: Sauvegarde...")
    df_clean.to_csv('../2_DONNEES/processed/dataset_clean.csv', index=False)
    print("   ✅ Sauvegarde réussie!")
    
    print("\n" + "="*60)
    print("✨ TERMINÉ! Durée totale: XX minutes")
    print("="*60)

if __name__ == "__main__":
    main()
```

**Génère AU MINIMUM:**
- 7 notebooks pédagogiques (1 par semaine clé)
- 10 scripts production (pipeline complet)
- 1 application Streamlit (500+ lignes commentées)
- 5 scripts utilitaires (visualisation, validation, export)

### PHASE 4: MÉMOIRE LaTeX PRÉ-REMPLI

**Sections à rédiger complètement (en français):**

1. **Introduction (3-4 pages):**
   - Contexte épidémiologique DT1 en Afrique (chiffres OMS, publications)
   - Spécificités formes idiopathiques vs auto-immunes
   - Problématique du dataset shift (modèles occidentaux inefficaces)
   - Justification biomarqueurs ANP32A-IT1, ESCO2, NBPF1
   - Objectif du mémoire clairement énoncé
   - Plan annoncé

2. **État de l'art (8-10 pages):**
   - **Partie A: Biologie du DT1** (physiopathologie, biomarqueurs)
   - **Partie B: IA en médecine** (ML supervisé, validation, métriques)
   - **Partie C: DT1 et IA** (revue des modèles existants, limites en Afrique)
   - **Tableau de synthèse** (>20 publications comparées)
   - Analyse critique: pourquoi approche proposée est pertinente

**Sections template (structure + exemples):**

3. **Méthodologie:**
   - Template avec sections pré-définies
   - Exemples fictifs de paragraphes rédigés
   - Instructions LaTeX en commentaires: `% TODO: Compléter avec vos résultats`

4. **Résultats:**
   - Template avec emplacements figures (chemins relatifs corrects)
   - Exemples de tableaux formatés
   - Scripts R/Python pour générer figures automatiquement

5. **Discussion/Conclusion:**
   - Template avec questions-guides

**Bibliographie:**
- Fichier `.bib` avec 500+ entrées
- Priorité: auteurs africains (Mbanya, Sobngwi, Kengne, etc.)
- Équilibre: 40% publications africaines, 30% méthodologie ML, 30% DT1 général
- Déjà formatées correctement (testées avec BibLaTeX)

### PHASE 5: VALIDATION FINALE

Avant de livrer, vérifie:
- [ ] Tous les chemins relatifs sont corrects
- [ ] Les codes s'exécutent sur machine vierge (test environnement virtuel)
- [ ] Les notebooks Colab ont sorties sauvegardées (visibles offline)
- [ ] Le mémoire compile sans erreur (pdflatex + biber)
- [ ] Le README principal explique installation en <10 minutes
- [ ] Gestion connexion intermittente testée (mode offline fonctionnel)

## CONTRAINTES ÉTHIQUES ET SCIENTIFIQUES

1. **Transparence sur les limites:**
   - Signaler explicitement si données synthétiques (pas de données réelles camerounaises trouvées)
   - Documenter hypothèses simplificatrices

2. **Pas de "boîte noire":**
   - Privilégier modèles interprétables (Random Forest, XGBoost avec SHAP)
   - Expliquer chaque prédiction

3. **Usage clinique responsable:**
   - Disclaimers clairs: outil d'aide, pas de remplacement médecin
   - Validation externe nécessaire avant déploiement

4. **Reproductibilité totale:**
   - Seeds fixés (numpy, sklearn)
   - Versions packages figées (requirements.txt)
   - Données et code versionnés

## OUTPUT ATTENDU

Fournis l'arborescence complète sous forme d'**artifact unique** contenant:

1. **Fichier `demarche_methodologique_sorelle.md`** (calendrier 14 semaines ultra-détaillé)
2. **README principal** (guide installation + premiers pas)
3. **3 notebooks complets** (Semaines 1, 3, 6 comme exemples)
4. **5 scripts production commentés** (nettoyage, entraînement, évaluation, prédiction, visualisation)
5. **Squelette mémoire LaTeX** (main.tex + 3 sections pré-remplies)
6. **Fichier bibliographie.bib** (100 entrées représentatives)
7. **Application Streamlit de base** (fonctionnelle, 200 lignes)
8. **Dictionnaire de données** (Excel ou Markdown)

## QUESTIONS AVANT DE COMMENCER

Confirme:
1. Puis-je générer des **données synthétiques réalistes** si aucune donnée camerounaise publique n'est trouvée ? (Je privilégierai recherche approfondie d'abord)
2. Niveau de détail souhaité pour les **commentaires de code**: abondant (ratio 1:1) ou modéré (ratio 1:3) ?
3. Langue du **mémoire**: français académique ou anglais scientifique ? (Les codes seront en anglais par convention)
4. Contraintes de **format mémoire**: nombre pages, police, marges imposées ?

Lance-toi dans les recherches web dès confirmation ! 🚀
