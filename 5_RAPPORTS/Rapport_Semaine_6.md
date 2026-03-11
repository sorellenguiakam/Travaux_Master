# 🏥 Rapport Semaine 6 : Application de Démonstration Streamlit

**Date** : 28 Février 2026
**Auteur** : Sorelle Perelle Nguisakam
**Projet** : Détection précoce du Diabète de Type 1 (DT1) - Cameroun

---

## 1. 🎯 Objectifs de la semaine

L'objectif de cette semaine était de concrétiser les travaux des semaines précédentes (modélisation, interprétabilité) en développant une **application de démonstration interactive** destinée aux cliniciens. Cette interface traduit le pipeline ML en outil d'aide à la décision, accessible sans connaissance en programmation.

**Objectifs spécifiques :**
*   Créer une application Streamlit fonctionnelle et intuitive
*   Implémenter le module de prédiction en temps réel (patient individuel)
*   Intégrer des visualisations interactives (Plotly, jauges de risque)
*   Permettre l'export automatique d'un rapport PDF par patient
*   Assurer l'accessibilité et l'ergonomie pour un usage clinique

---

## 2. 🛠️ Architecture de l'Application

L'application est développée dans `5_APPLICATION_DEMO/app_streamlit.py` (246 lignes de code).

### 2.1 Structure et Navigation

L'interface comprend **4 pages accessibles via une barre latérale (sidebar)** :

| Page           | Description                                                        |
| :------------- | :----------------------------------------------------------------- |
| **Accueil**    | Présentation du projet, contexte médical, objectifs                |
| **Prédictions**| Formulaire patient, résultats IA, visualisations, export PDF       |
| **Base de Données** | (Réservé pour les extensions futures)                         |
| **À propos**   | Informations sur le projet et les auteurs                          |

### 2.2 Stack Technologique

```
streamlit       → Interface web interactive
plotly          → Visualisations dynamiques (jauges, graphiques)
pandas / numpy  → Traitement des données en temps réel
joblib          → Chargement du modèle ML (XGBoost sauvegardé)
fpdf            → Génération de rapports PDF
```

---

## 3. 📊 Fonctionnalités Implémentées

### 3.1 Module de Prédiction Individuelle

Le cœur de l'application est le **formulaire de saisie patient** qui collecte :
*   **Données cliniques** : Âge, IMC, Glycémie à jeun (mg/dL), HbA1c (%)
*   **Biomarqueurs génétiques** : ANP32A_IT1, ESCO2, NBPF1 (expressions relatives)

Le modèle XGBoost (entraîné en Semaine 4, **Recall = 100%**) est chargé via `joblib` et retourne :
1.  Le **diagnostic** (Risque ÉLEVÉ / Risque FAIBLE)
2.  La **probabilité de DT1** (valeur entre 0 et 100%)

### 3.2 Visualisations Interactives

*   **Jauge de risque (Gauge Chart)** : affichage visuel immédiat du niveau de risque en pourcentage avec code couleur (vert = faible, rouge = élevé) — idéal pour une lecture rapide en contexte clinique.
*   **Graphique d'impact des variables** : simulation de la contribution relative de la Glycémie, HbA1c et ESCO2 à la décision, similaire à une analyse SHAP locale simplifiée.

### 3.3 Génération de Rapport PDF

Un bouton **"Télécharger le Rapport PDF"** génère automatiquement un document structuré contenant :
*   Les informations saisies du patient
*   Le résultat du diagnostic coloré (rouge/vert)
*   La probabilité estimée
*   La date et l'heure de l'analyse

### 3.4 Design et Ergonomie

*   CSS personnalisé intégré (cartes blanches, ombres, couleurs harmonisées)
*   Drapeau camerounais dans la sidebar pour l'ancrage local
*   Layout en colonnes (`st.columns`) pour une lecture claire
*   Gestion des erreurs si le modèle n'est pas trouvé

---

## 4. ✅ Résultats et Validation

### Test du pipeline complet

| Étape                              | Statut    |
| :--------------------------------- | :-------: |
| Chargement de l'interface Streamlit | ✅ OK     |
| Saisie du formulaire patient        | ✅ OK     |
| Appel au modèle XGBoost            | ✅ OK     |
| Affichage de la jauge de risque     | ✅ OK     |
| Calcul et affichage de l'impact     | ✅ OK     |
| Génération et téléchargement PDF    | ✅ OK     |

### Exemple de prédiction

Pour un patient fictif avec `Glycémie = 180 mg/dL`, `HbA1c = 8.5%`, `ESCO2 = 2.1` :
*   **Résultat** : Risque ÉLEVÉ (Positif) ✅
*   **Probabilité** : ~92%

Pour un patient avec `Glycémie = 88 mg/dL`, `HbA1c = 5.2%`, `ESCO2 = 0.9` :
*   **Résultat** : Risque FAIBLE (Négatif) ✅
*   **Probabilité** : ~4%

---

## 5. 📝 Conclusion

La Semaine 6 aboutit à la livraison d'un **prototype fonctionnel d'application médicale**. L'outil transforme le modèle ML en interface accessible, respectant les contraintes cliniques (lecture rapide, export documentaire, pas d'expert ML requis).

**Points forts :**
*   L'application est exécutable en une seule commande : `streamlit run app_streamlit.py`
*   Le design minimaliste et professionnel est adapté à un usage hospitalier
*   Le rapport PDF permet la traçabilité des décisions (bonne pratique médicale)

**Perspectives (Semaine 7 et suite) :**
*   Ajouter le mode **traitement par lot (batch)** : upload CSV de plusieurs patients
*   Enrichir l'interprétabilité avec les **vrais SHAP values** (au lieu de la simulation)
*   Rédiger la section correspondante dans le mémoire LaTeX (Section 4.4 Application)

---

## 6. 🗂️ Fichiers produits

| Fichier                                      | Description                           |
| :------------------------------------------- | :------------------------------------ |
| `5_APPLICATION_DEMO/app_streamlit.py`        | Application principale (246 lignes)   |
| `5_APPLICATION_DEMO/requirements_app.txt`    | Dépendances de l'application          |
| `5_APPLICATION_DEMO/README_APP.md`           | Guide de lancement et d'utilisation   |

---
*Semaine suivante : Finalisation de l'application + Rédaction mémoire (Semaines 7-8).*
