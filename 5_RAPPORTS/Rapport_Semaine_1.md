# Rapport Semaine 1: Introduction Python & ML

**Statut:** Terminé
**Fichier associé:** [Rapport_Semaine_1.pdf](Rapport_Semaine_1.pdf) (à générer)

## Résumé
Cette première semaine a été consacrée à la mise en place de l'environnement de développement et à l'initiation pratique au Machine Learning avec Python. L'objectif principal était de maîtriser les outils fondamentaux (NumPy, Pandas, Matplotlib) et de construire un premier modèle prédictif simple pour la détection du diabète de type 1.

## Travail Réalisé

### 1. Installation et Configuration
*   **Environnement:** Installation d'Anaconda et création de l'environnement virtuel dédié `dt1_cameroun` (Python 3.9).
*   **Dépendances:** Installation des bibliothèques nécessaires via `requirements.txt` (NumPy, Pandas, Scikit-learn, Matplotlib, Seaborn).
*   **Outils:** Prise en main de Jupyter Notebook pour le développement interactif et de Zotero pour la gestion bibliographique.

### 2. Développement Technique
Le travail technique s'est concentré sur le notebook `3_NOTEBOOKS_PEDAGOGIQUES/Semaine01_Introduction_Python_ML.ipynb`.

*   **Manipulation de Données:** Chargement et exploration d'un jeu de données synthétique préliminaire.
*   **Visualisation:** Création de graphiques pour comprendre la distribution des variables (Histogrammes, Scatter plots).
*   **Modélisation:** Entraînement d'un modèle d'**Arbre de Décision (Decision Tree)** pour classifier les patients (Sain vs DT1).

## Résultats Techniques

### Performance du Modèle
Le modèle d'Arbre de Décision a obtenu des résultats excellents sur le jeu de données test :

*   **Accuracy (Exactitude):** 99.50%
*   **Précision:** 98% (pour la classe DT1)
*   **Rappel (Recall):** 100% (pour la classe DT1) - *Crucial pour ne pas manquer de cas positifs.*

### Matrice de Confusion
| | Prédit Sain | Prédit DT1 |
|---|---|---|
| **Réel Sain** | 141 (Vrais Négatifs) | 1 (Faux Positif) |
| **Réel DT1** | 0 (Faux Négatifs) | 58 (Vrais Positifs) |

> [!NOTE]
> Le modèle n'a commis aucune erreur de type "Faux Négatif", ce qui est le résultat souhaité pour un outil de dépistage médical.

### Importance des Variables
L'analyse de l'importance des variables (Feature Importance) a révélé que la **Glycémie à jeun** est le prédicteur dominant pour ce modèle simple.

## Prochaines Étapes
*   Passer à la **Semaine 2 : Exploration des Données (EDA)**.
*   Générer le jeu de données synthétique plus complexe (`dataset_dt1_cameroun_synthetic.csv`) incluant les nouveaux biomarqueurs (ANP32A-IT1, ESCO2, NBPF1).
*   Approfondir l'analyse statistique des données.
