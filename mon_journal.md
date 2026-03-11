# Mon Journal de Bord — Projet DT1 Cameroun

**Auteure :** Sorelle Perelle Nguisakam
**Mémoire M2 :** Détection précoce du Diabète de Type 1 en Afrique subsaharienne

---

## Semaine 2 : Exploration approfondie des données

**Dates :** 3 – 7 Février 2026

---

### Ce que j'ai compris ✅

**Sur les données et leur préparation :**

1.  **L'importance cruciale du nettoyage.** Avant de toucher au moindre algorithme, il faut s'assurer que les données sont fiables. J'ai compris pourquoi des variables comme les triglycérides (36,2 % de manquants) sont directement supprimées : un modèle entraîné sur des colonnes creuses apprend du bruit, pas de la réalité. La règle des 30 % me semble maintenant une frontière naturelle.

2.  **La différence entre outlier et valeur extrême cliniquement réelle.** C'est là que la réflexion médicale entre en jeu. Une glycémie de 450 mg/dL dans notre dataset peut être une erreur de saisie OU un cas de décompensation réel. La Winsorization est un bon compromis : on atténue l'impact de l'extrême sans effacer l'observation, ce qui est honnête scientifiquement.

3.  **Pourquoi stratifier le split Train/Val/Test.** Si 25 % des patients sont DT1+, sans stratification, le hasard peut faire que l'ensemble de test contient 15 % de positifs. Le modèle serait évalué sur un échantillon non représentatif. J'ai compris que `stratify=y` dans scikit-learn est non négociable pour les données médicales déséquilibrées.

4.  **Le rôle du feature engineering.** Créer le ratio `ESCO2/ANP32A-IT1` n'est pas de la "triche" — c'est encoder une hypothèse biologique (l'interaction entre deux biomarqueurs) dans le modèle de manière explicite. Si ce ratio est discriminant, c'est que les deux gènes interagissent réellement dans la pathophysiologie du DT1.

5.  **L'algorithme missForest vs imputation simple.** La différence de RMSE sur l'IMC (3,23 → 0,57) m'a convaincu qu'une forêt aléatoire peut "deviner" une valeur manquante en s'appuyant sur toutes les autres variables du patient. C'est beaucoup plus intelligent que de mettre la médiane de la colonne.

**Sur les outils Python :**
- `df.isnull().sum()` et les heatmaps de valeurs manquantes avec seaborn
- Le One-Hot Encoding et pourquoi `drop_first=True` évite la multicolinéarité parfaite
- La standardisation avec `StandardScaler` et le fait capital : **on fit le scaler uniquement sur le train**, puis on l'applique (transform) sur val et test

---

### Ce qui reste flou ❓

1.  **Le choix de la stratégie d'imputation pour les biomarqueurs génomiques.**
    L'algorithme missForest est présenté pour l'IMC. Mais pour les expressions d'ARNm (ESCO2, ANP32A-IT1), est-ce que l'imputation par forêt aléatoire reste valide ? Ces valeurs ont une distribution biologique très différente de l'IMC. Je ne suis pas sûre qu'une valeur «imputée» pour un niveau d'expression génique ait un sens biologique.

2.  **La correction des effets de lot via ComBat.**
    Je comprends l'idée (des données mesurées à Yaoundé et à Johannesburg sur des machines différentes ne sont pas directement comparables), mais je n'ai pas encore bien compris comment ComBat distingue un "effet de lot" d'une vraie différence biologique entre populations. Est-ce qu'on risque d'effacer un signal réel ?

3.  **Le seuil de 30 % pour supprimer une variable.**
    La règle des 30 % est-elle universelle ou propre à ce projet ? J'ai vu des publications qui gardent des variables à 40 % de manquants après imputation. Comment choisir le bon seuil en pratique ?

4.  **L'impact de la taille du dataset sur la généralisation.**
    On travaille sur 894 patients (ou 1000 synthétiques en simulation). En médecine de précision, est-ce suffisant pour que le modèle généralise à d'autres patients en Afrique centrale ? Quel est le nombre minimal de patients pour un modèle ML robuste en contexte africain ?

---

### Questions pour Dr. TCHAPET NJAFA Jean-Pierre 📋

1.  **Sur la provenance des données :** L'étude YODA mentionne des recrutements au Cameroun, Ouganda et Afrique du Sud. Pour notre mémoire, utilisons-nous uniquement le sous-ensemble camerounais, ou la cohorte multicentrique complète ? Est-ce que cette décision doit apparaître explicitement dans la section Méthodologie ?

2.  **Sur la sélection des hub genes :** ANP32A-IT1, ESCO2 et NBPF1 ont-ils été sélectionnés *avant* la modélisation (connaissance biologique a priori) ou *après* (résultat de l'analyse de co-expression) ? Cela change le statut épistémique du résultat et son interprétabilité.

3.  **Sur les données synthétiques :** Dans quelle mesure peut-on présenter des résultats obtenus sur le dataset synthétique comme «validés» ? Faut-il ajouter une section «limites» spécifique sur ce point dans le mémoire ?

4.  **Sur le journal de bord :** Dois-je rédiger ce journal en français ou une version bilingue est-elle attendue pour la soutenance ?

---

### Estimation d'avancement ⏱️

| Tâche Semaine 2                              | Statut       |
| :------------------------------------------- | :----------: |
| Dataset nettoyé (`dataset_clean.csv`)         | ✅ Terminé  |
| Feature engineering (`dataset_features.csv`) | ✅ Terminé  |
| Split Train/Val/Test                         | ✅ Terminé  |
| Notebook EDA complet                         | ✅ Terminé  |
| Rapport qualité des données (.md)            | ✅ Terminé  |
| Section 3.1 mémoire LaTeX                    | ✅ Terminé  |
| Figure première analyse biomarqueurs         | ✅ Terminé  |
| Ce journal de bord                           | ✅ Terminé  |

**Sentiment global :** La Semaine 2 m'a appris que le ML médical est d'abord un travail de detective sur les données. Je me sens à l'aise avec les outils Python, mais les décisions méthodologiques (quel seuil choisir, quelle imputation, comment justifier la suppression d'une variable) demandent un dialogue avec l'encadrant que je ne peux pas résoudre seule.

---

*Prochaine section : Semaine 3 — Modélisation simple et comparaison des algorithmes de baseline.*
