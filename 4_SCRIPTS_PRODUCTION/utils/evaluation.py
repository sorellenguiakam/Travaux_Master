#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MODULE EVALUATION - FONCTIONS D'ÉVALUATION DES MODÈLES ML
================================================================================

Ce module contient des fonctions pour évaluer les performances des modèles
dans le contexte médical de détection précoce du DT1.

PRIORITÉ: Maximiser le Recall (sensibilité) pour minimiser les faux négatifs.

Auteur: Dr. TCHAPET NJAFA Jean-Pierre avec assistance Claude Code
Date: Novembre 2025
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, auc, precision_recall_curve, average_precision_score
)
import matplotlib.pyplot as plt
import seaborn as sns


def calculer_metriques_completes(y_true, y_pred, y_proba=None):
    """
    Calcule toutes les métriques d'évaluation pertinentes.

    Args:
        y_true: Vraies étiquettes
        y_pred: Prédictions
        y_proba: Probabilités de prédiction (optionnel)

    Returns:
        dict: Dictionnaire avec toutes les métriques
    """
    metriques = {}

    # Métriques de base
    metriques['accuracy'] = accuracy_score(y_true, y_pred)
    metriques['precision'] = precision_score(y_true, y_pred, zero_division=0)
    metriques['recall'] = recall_score(y_true, y_pred, zero_division=0)  # ⭐ Prioritaire
    metriques['f1_score'] = f1_score(y_true, y_pred, zero_division=0)

    # Spécificité (important en contexte médical)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    metriques['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0
    metriques['sensitivity'] = metriques['recall']  # Alias

    # Taux de faux positifs et négatifs
    metriques['false_positive_rate'] = fp / (fp + tn) if (fp + tn) > 0 else 0
    metriques['false_negative_rate'] = fn / (fn + tp) if (fn + tp) > 0 else 0

    # Valeurs prédictives
    metriques['ppv'] = tp / (tp + fp) if (tp + fp) > 0 else 0  # Positive Predictive Value
    metriques['npv'] = tn / (tn + fn) if (tn + fn) > 0 else 0  # Negative Predictive Value

    # ROC-AUC (si probabilités disponibles)
    if y_proba is not None and len(np.unique(y_true)) > 1:
        metriques['roc_auc'] = roc_auc_score(y_true, y_proba)
        metriques['average_precision'] = average_precision_score(y_true, y_proba)

    # Matrice de confusion
    metriques['confusion_matrix'] = confusion_matrix(y_true, y_pred)
    metriques['tn'] = tn
    metriques['fp'] = fp
    metriques['fn'] = fn
    metriques['tp'] = tp

    return metriques


def afficher_metriques(metriques, nom_modele="Modèle"):
    """
    Affiche les métriques de manière formatée et lisible.

    Args:
        metriques (dict): Métriques calculées
        nom_modele (str): Nom du modèle évalué
    """
    print("=" * 80)
    print(f"📊 RÉSULTATS D'ÉVALUATION - {nom_modele}")
    print("=" * 80)

    print("\n🎯 MÉTRIQUES PRINCIPALES:")
    print(f"  Accuracy:   {metriques['accuracy']:.4f}")
    print(f"  Precision:  {metriques['precision']:.4f}")
    print(f"  Recall:     {metriques['recall']:.4f} ⭐ (prioritaire en contexte médical)")
    print(f"  F1-Score:   {metriques['f1_score']:.4f}")

    if 'roc_auc' in metriques:
        print(f"  ROC-AUC:    {metriques['roc_auc']:.4f}")

    print("\n🔬 MÉTRIQUES CLINIQUES:")
    print(f"  Sensibilité (Recall):  {metriques['sensitivity']:.4f}")
    print(f"  Spécificité:           {metriques['specificity']:.4f}")
    print(f"  PPV (Precision):       {metriques['ppv']:.4f}")
    print(f"  NPV:                   {metriques['npv']:.4f}")

    print("\n⚠️ TAUX D'ERREURS:")
    print(f"  Faux Positifs (FPR):   {metriques['false_positive_rate']:.4f}")
    print(f"  Faux Négatifs (FNR):   {metriques['false_negative_rate']:.4f} ⚠️ Critique!")

    print("\n📋 MATRICE DE CONFUSION:")
    print(f"  VN (True Negative):    {metriques['tn']}")
    print(f"  FP (False Positive):   {metriques['fp']}")
    print(f"  FN (False Negative):   {metriques['fn']} ⚠️ À minimiser!")
    print(f"  VP (True Positive):    {metriques['tp']}")

    print("=" * 80)


def comparer_modeles(resultats_modeles, critere='recall'):
    """
    Compare plusieurs modèles selon un critère donné.

    Args:
        resultats_modeles (dict): Dictionnaire {nom_modele: metriques}
        critere (str): Métrique de comparaison (défaut: 'recall')

    Returns:
        pd.DataFrame: Tableau comparatif trié
    """
    # Construire le DataFrame de comparaison
    comparaison = []

    for nom, metriques in resultats_modeles.items():
        comparaison.append({
            'Modèle': nom,
            'Accuracy': metriques['accuracy'],
            'Precision': metriques['precision'],
            'Recall ⭐': metriques['recall'],
            'F1-Score': metriques['f1_score'],
            'ROC-AUC': metriques.get('roc_auc', np.nan),
            'FNR ⚠️': metriques['false_negative_rate']
        })

    df_comparaison = pd.DataFrame(comparaison)

    # Trier par critère
    critere_map = {
        'recall': 'Recall ⭐',
        'accuracy': 'Accuracy',
        'precision': 'Precision',
        'f1_score': 'F1-Score',
        'roc_auc': 'ROC-AUC'
    }

    colonne_tri = critere_map.get(critere, 'Recall ⭐')
    df_comparaison = df_comparaison.sort_values(by=colonne_tri, ascending=False)

    print("\n📊 COMPARAISON DES MODÈLES:")
    print("=" * 100)
    print(df_comparaison.to_string(index=False, float_format=lambda x: f'{x:.4f}'))
    print("=" * 100)
    print(f"🏆 Meilleur modèle (selon {critere}): {df_comparaison.iloc[0]['Modèle']}")
    print("=" * 100)

    return df_comparaison


def calculer_seuil_optimal(y_true, y_proba, critere='youden'):
    """
    Calcule le seuil de décision optimal pour maximiser un critère donné.

    Args:
        y_true: Vraies étiquettes
        y_proba: Probabilités de prédiction
        critere (str): Critère d'optimisation
            - 'youden': Indice de Youden (Sensibilité + Spécificité - 1)
            - 'f1': F1-Score
            - 'recall_90': Seuil pour atteindre Recall ≥ 0.90

    Returns:
        tuple: (seuil_optimal, metriques_au_seuil)
    """
    fpr, tpr, seuils = roc_curve(y_true, y_proba)

    if critere == 'youden':
        # Indice de Youden = Sensibilité + Spécificité - 1
        specificite = 1 - fpr
        youden_index = tpr + specificite - 1
        idx_optimal = np.argmax(youden_index)
        seuil_optimal = seuils[idx_optimal]

        print(f"🎯 Seuil optimal (Youden): {seuil_optimal:.4f}")
        print(f"   Sensibilité: {tpr[idx_optimal]:.4f}")
        print(f"   Spécificité: {specificite[idx_optimal]:.4f}")

    elif critere == 'f1':
        # Maximiser le F1-Score
        precision_vals, recall_vals, seuils_pr = precision_recall_curve(y_true, y_proba)
        f1_scores = 2 * (precision_vals * recall_vals) / (precision_vals + recall_vals + 1e-10)
        idx_optimal = np.argmax(f1_scores)
        seuil_optimal = seuils_pr[idx_optimal] if idx_optimal < len(seuils_pr) else 0.5

        print(f"🎯 Seuil optimal (F1): {seuil_optimal:.4f}")
        print(f"   F1-Score: {f1_scores[idx_optimal]:.4f}")

    elif critere == 'recall_90':
        # Trouver le seuil pour atteindre Recall ≥ 0.90
        idx_recall_90 = np.where(tpr >= 0.90)[0]
        if len(idx_recall_90) > 0:
            idx_optimal = idx_recall_90[0]
            seuil_optimal = seuils[idx_optimal]
            print(f"🎯 Seuil pour Recall ≥ 0.90: {seuil_optimal:.4f}")
            print(f"   Recall atteint: {tpr[idx_optimal]:.4f}")
            print(f"   Spécificité: {1 - fpr[idx_optimal]:.4f}")
        else:
            seuil_optimal = 0.5
            print("⚠️ Impossible d'atteindre Recall ≥ 0.90")

    else:
        raise ValueError(f"Critère inconnu: {critere}")

    # Calculer les prédictions avec le nouveau seuil
    y_pred_optimal = (y_proba >= seuil_optimal).astype(int)
    metriques_optimales = calculer_metriques_completes(y_true, y_pred_optimal, y_proba)

    return seuil_optimal, metriques_optimales


def analyser_erreurs(X, y_true, y_pred, feature_names=None):
    """
    Analyse les erreurs de prédiction (faux positifs et faux négatifs).

    Args:
        X: Features
        y_true: Vraies étiquettes
        y_pred: Prédictions
        feature_names: Noms des features (optionnel)

    Returns:
        tuple: (faux_positifs_df, faux_negatifs_df)
    """
    # Convertir X en DataFrame si nécessaire
    if not isinstance(X, pd.DataFrame):
        if feature_names is not None:
            X = pd.DataFrame(X, columns=feature_names)
        else:
            X = pd.DataFrame(X)

    X = X.copy()
    X['y_true'] = y_true
    X['y_pred'] = y_pred

    # Identifier les erreurs
    faux_positifs = X[(X['y_true'] == 0) & (X['y_pred'] == 1)]
    faux_negatifs = X[(X['y_true'] == 1) & (X['y_pred'] == 0)]

    print("\n🔍 ANALYSE DES ERREURS:")
    print("=" * 80)
    print(f"❌ Faux Positifs: {len(faux_positifs)} cas")
    print(f"⚠️ Faux Négatifs: {len(faux_negatifs)} cas (CRITIQUE!)")

    if len(faux_negatifs) > 0:
        print("\n📊 Statistiques des Faux Négatifs (patients DT1+ manqués):")
        print(faux_negatifs.drop(['y_true', 'y_pred'], axis=1).describe())

    if len(faux_positifs) > 0:
        print("\n📊 Statistiques des Faux Positifs:")
        print(faux_positifs.drop(['y_true', 'y_pred'], axis=1).describe())

    print("=" * 80)

    return faux_positifs, faux_negatifs


def evaluer_avec_validation_croisee(modele, X, y, cv=5, scoring='recall'):
    """
    Évalue un modèle avec validation croisée.

    Args:
        modele: Modèle scikit-learn
        X: Features
        y: Variable cible
        cv (int): Nombre de folds
        scoring (str): Métrique à calculer

    Returns:
        dict: Résultats de la validation croisée
    """
    from sklearn.model_selection import cross_val_score, cross_validate

    print(f"\n🔄 Validation croisée ({cv} folds)...")

    # Métriques multiples
    scoring_dict = {
        'accuracy': 'accuracy',
        'precision': 'precision',
        'recall': 'recall',
        'f1': 'f1',
        'roc_auc': 'roc_auc'
    }

    resultats = cross_validate(
        modele, X, y,
        cv=cv,
        scoring=scoring_dict,
        return_train_score=True,
        n_jobs=-1
    )

    print("\n📊 Résultats de la validation croisée:")
    print("=" * 80)
    for metric_name in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']:
        test_scores = resultats[f'test_{metric_name}']
        train_scores = resultats[f'train_{metric_name}']

        print(f"{metric_name.upper()}:")
        print(f"  Train: {train_scores.mean():.4f} (±{train_scores.std():.4f})")
        print(f"  Test:  {test_scores.mean():.4f} (±{test_scores.std():.4f})")

        # Détecter le surapprentissage
        diff = train_scores.mean() - test_scores.mean()
        if diff > 0.10:
            print(f"  ⚠️ Surapprentissage possible (écart: {diff:.4f})")

    print("=" * 80)

    return resultats


def verifier_seuils_cliniques(metriques, seuils_minimaux=None):
    """
    Vérifie si le modèle satisfait les seuils minimaux pour usage clinique.

    Args:
        metriques (dict): Métriques du modèle
        seuils_minimaux (dict): Seuils requis (défaut: contexte médical)

    Returns:
        tuple: (validation_ok, messages)
    """
    if seuils_minimaux is None:
        # Seuils par défaut pour contexte médical (DT1)
        seuils_minimaux = {
            'recall': 0.85,  # Minimum 85% de sensibilité
            'accuracy': 0.75,
            'roc_auc': 0.80,
            'false_negative_rate': 0.15  # Maximum 15% de FN
        }

    print("\n🏥 VÉRIFICATION DES SEUILS CLINIQUES:")
    print("=" * 80)

    validation_ok = True
    messages = []

    for metric, seuil in seuils_minimaux.items():
        valeur = metriques.get(metric, None)

        if valeur is None:
            continue

        # Pour FNR, on veut une valeur inférieure
        if metric == 'false_negative_rate':
            ok = valeur <= seuil
            comparateur = "≤"
        else:
            ok = valeur >= seuil
            comparateur = "≥"

        statut = "✅" if ok else "❌"
        print(f"{statut} {metric}: {valeur:.4f} {comparateur} {seuil:.4f}")

        if not ok:
            validation_ok = False
            messages.append(f"{metric} ne satisfait pas le seuil minimal")

    if validation_ok:
        print("\n✅ Le modèle satisfait tous les critères cliniques!")
    else:
        print("\n❌ Le modèle ne satisfait PAS tous les critères cliniques.")
        print("⚠️ NE PAS déployer en contexte médical sans amélioration.")

    print("=" * 80)

    return validation_ok, messages


def generer_rapport_classification(y_true, y_pred, target_names=None):
    """
    Génère un rapport de classification détaillé.

    Args:
        y_true: Vraies étiquettes
        y_pred: Prédictions
        target_names: Noms des classes (optionnel)

    Returns:
        str: Rapport formaté
    """
    if target_names is None:
        target_names = ['Sain (0)', 'DT1+ (1)']

    rapport = classification_report(y_true, y_pred, target_names=target_names, digits=4)

    print("\n📋 RAPPORT DE CLASSIFICATION DÉTAILLÉ:")
    print("=" * 80)
    print(rapport)
    print("=" * 80)

    return rapport


if __name__ == '__main__':
    """Tests unitaires basiques des fonctions."""

    print("=" * 80)
    print("TESTS DU MODULE EVALUATION")
    print("=" * 80)

    # Créer des données de test
    np.random.seed(42)
    n = 100

    y_true = np.random.randint(0, 2, n)
    y_proba = np.random.uniform(0, 1, n)
    y_pred = (y_proba >= 0.5).astype(int)

    print("\n1️⃣ Test: Calcul métriques complètes")
    metriques = calculer_metriques_completes(y_true, y_pred, y_proba)
    afficher_metriques(metriques, "Modèle Test")

    print("\n2️⃣ Test: Génération rapport classification")
    generer_rapport_classification(y_true, y_pred)

    print("\n3️⃣ Test: Seuil optimal (Youden)")
    seuil_opt, metriques_opt = calculer_seuil_optimal(y_true, y_proba, critere='youden')

    print("\n4️⃣ Test: Vérification seuils cliniques")
    validation_ok, messages = verifier_seuils_cliniques(metriques)

    print("\n✅ Tous les tests terminés")
