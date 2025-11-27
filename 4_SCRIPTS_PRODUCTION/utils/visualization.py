#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MODULE VISUALIZATION - FONCTIONS DE VISUALISATION
================================================================================

Ce module contient des fonctions pour générer des visualisations de qualité
publication pour le projet de détection précoce du DT1.

Auteur: Dr. TCHAPET NJAFA Jean-Pierre avec assistance Claude Code
Date: Novembre 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve
from pathlib import Path

# Configuration par défaut de matplotlib
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (10, 6)


def tracer_matrice_confusion(y_true, y_pred, classes=['Sain', 'DT1+'],
                              titre='Matrice de Confusion',
                              sauvegarder=None, dpi=300):
    """
    Trace une matrice de confusion avec style publication.

    Args:
        y_true: Vraies étiquettes
        y_pred: Prédictions
        classes: Noms des classes
        titre: Titre du graphique
        sauvegarder: Chemin de sauvegarde (optionnel)
        dpi: Résolution de l'image

    Returns:
        matplotlib.figure.Figure: Figure créée
    """
    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Tracer la heatmap
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        cbar=True,
        square=True,
        ax=ax,
        xticklabels=classes,
        yticklabels=classes,
        annot_kws={'size': 14, 'weight': 'bold'}
    )

    ax.set_xlabel('Classe Prédite', fontsize=12, weight='bold')
    ax.set_ylabel('Vraie Classe', fontsize=12, weight='bold')
    ax.set_title(titre, fontsize=14, weight='bold', pad=20)

    # Annotations contextuelles
    tn, fp, fn, tp = cm.ravel()
    ax.text(0.5, -0.15, f'FN={fn} ⚠️ CRITIQUE (patients DT1+ manqués)',
            ha='center', transform=ax.transAxes, fontsize=10, color='red')

    plt.tight_layout()

    if sauvegarder:
        plt.savefig(sauvegarder, dpi=dpi, bbox_inches='tight')
        print(f"✅ Matrice de confusion sauvegardée: {sauvegarder}")

    return fig


def tracer_courbe_roc(y_true, y_proba, titre='Courbe ROC',
                      sauvegarder=None, dpi=300):
    """
    Trace une courbe ROC avec AUC.

    Args:
        y_true: Vraies étiquettes
        y_proba: Probabilités de prédiction
        titre: Titre du graphique
        sauvegarder: Chemin de sauvegarde (optionnel)
        dpi: Résolution

    Returns:
        matplotlib.figure.Figure: Figure créée
    """
    fpr, tpr, seuils = roc_curve(y_true, y_proba)
    auc_score = auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Tracer la courbe ROC
    ax.plot(fpr, tpr, color='blue', lw=2,
            label=f'Courbe ROC (AUC = {auc_score:.3f})')

    # Ligne de référence
    ax.plot([0, 1], [0, 1], 'k--', lw=1, label='Chance (AUC = 0.5)')

    # Configuration
    ax.set_xlabel('Taux de Faux Positifs (1 - Spécificité)', fontsize=12)
    ax.set_ylabel('Taux de Vrais Positifs (Sensibilité)', fontsize=12)
    ax.set_title(titre, fontsize=14, weight='bold')
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(True, alpha=0.3)

    # Limites
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])

    plt.tight_layout()

    if sauvegarder:
        plt.savefig(sauvegarder, dpi=dpi, bbox_inches='tight')
        print(f"✅ Courbe ROC sauvegardée: {sauvegarder}")

    return fig


def tracer_precision_recall(y_true, y_proba, titre='Courbe Précision-Recall',
                             sauvegarder=None, dpi=300):
    """
    Trace une courbe Précision-Recall.

    Args:
        y_true: Vraies étiquettes
        y_proba: Probabilités de prédiction
        titre: Titre du graphique
        sauvegarder: Chemin de sauvegarde
        dpi: Résolution

    Returns:
        matplotlib.figure.Figure: Figure créée
    """
    from sklearn.metrics import average_precision_score

    precision, recall, seuils = precision_recall_curve(y_true, y_proba)
    avg_precision = average_precision_score(y_true, y_proba)

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.plot(recall, precision, color='blue', lw=2,
            label=f'Précision-Recall (AP = {avg_precision:.3f})')

    # Baseline (proportion de positifs)
    baseline = y_true.mean() if isinstance(y_true, np.ndarray) else y_true.value_counts(normalize=True)[1]
    ax.axhline(y=baseline, color='r', linestyle='--',
               label=f'Baseline (proportion DT1+ = {baseline:.3f})')

    ax.set_xlabel('Recall (Sensibilité)', fontsize=12)
    ax.set_ylabel('Précision (VPP)', fontsize=12)
    ax.set_title(titre, fontsize=14, weight='bold')
    ax.legend(loc='best', fontsize=11)
    ax.grid(True, alpha=0.3)

    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])

    plt.tight_layout()

    if sauvegarder:
        plt.savefig(sauvegarder, dpi=dpi, bbox_inches='tight')
        print(f"✅ Courbe Précision-Recall sauvegardée: {sauvegarder}")

    return fig


def tracer_importance_features(importances, feature_names, n_top=15,
                                titre='Importance des Features',
                                sauvegarder=None, dpi=300):
    """
    Trace l'importance des features.

    Args:
        importances: Scores d'importance
        feature_names: Noms des features
        n_top: Nombre de features à afficher
        titre: Titre du graphique
        sauvegarder: Chemin de sauvegarde
        dpi: Résolution

    Returns:
        matplotlib.figure.Figure: Figure créée
    """
    # Trier par importance
    indices = np.argsort(importances)[::-1][:n_top]
    importances_top = importances[indices]
    names_top = [feature_names[i] for i in indices]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Tracer
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(names_top)))
    bars = ax.barh(range(len(names_top)), importances_top, color=colors)

    ax.set_yticks(range(len(names_top)))
    ax.set_yticklabels(names_top, fontsize=10)
    ax.invert_yaxis()

    ax.set_xlabel('Importance', fontsize=12)
    ax.set_title(titre, fontsize=14, weight='bold')
    ax.grid(axis='x', alpha=0.3)

    # Annotations
    for i, (bar, val) in enumerate(zip(bars, importances_top)):
        ax.text(val + 0.01, bar.get_y() + bar.get_height()/2,
                f'{val:.4f}', va='center', fontsize=9)

    plt.tight_layout()

    if sauvegarder:
        plt.savefig(sauvegarder, dpi=dpi, bbox_inches='tight')
        print(f"✅ Importance des features sauvegardée: {sauvegarder}")

    return fig


def tracer_distribution_biomarqueurs(df, biomarqueurs, cible='diagnostic',
                                      titre='Distribution des Biomarqueurs',
                                      sauvegarder=None, dpi=300):
    """
    Trace la distribution des biomarqueurs par classe.

    Args:
        df: DataFrame avec données
        biomarqueurs: Liste des biomarqueurs
        cible: Nom de la variable cible
        titre: Titre général
        sauvegarder: Chemin de sauvegarde
        dpi: Résolution

    Returns:
        matplotlib.figure.Figure: Figure créée
    """
    n_bio = len(biomarqueurs)
    n_cols = 3
    n_rows = (n_bio + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
    axes = axes.flatten() if n_bio > 1 else [axes]

    for idx, bio in enumerate(biomarqueurs):
        if bio not in df.columns:
            print(f"⚠️ Biomarqueur '{bio}' absent du DataFrame")
            continue

        ax = axes[idx]

        # Boxplot par classe
        df.boxplot(column=bio, by=cible, ax=ax)

        ax.set_title(f'{bio}', fontsize=12, weight='bold')
        ax.set_xlabel('Diagnostic', fontsize=10)
        ax.set_ylabel(f'Valeur {bio}', fontsize=10)
        ax.get_figure().suptitle('')  # Supprimer titre automatique

    # Masquer axes non utilisés
    for idx in range(len(biomarqueurs), len(axes)):
        axes[idx].axis('off')

    fig.suptitle(titre, fontsize=16, weight='bold', y=1.02)
    plt.tight_layout()

    if sauvegarder:
        plt.savefig(sauvegarder, dpi=dpi, bbox_inches='tight')
        print(f"✅ Distribution biomarqueurs sauvegardée: {sauvegarder}")

    return fig


def tracer_matrice_correlation(df, colonnes=None, titre='Matrice de Corrélation',
                                sauvegarder=None, dpi=300):
    """
    Trace une matrice de corrélation.

    Args:
        df: DataFrame
        colonnes: Colonnes à inclure (None = toutes numériques)
        titre: Titre du graphique
        sauvegarder: Chemin de sauvegarde
        dpi: Résolution

    Returns:
        matplotlib.figure.Figure: Figure créée
    """
    if colonnes is None:
        # Sélectionner toutes les colonnes numériques
        colonnes = df.select_dtypes(include=[np.number]).columns.tolist()

    corr_matrix = df[colonnes].corr()

    fig, ax = plt.subplots(figsize=(12, 10))

    # Heatmap
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={'shrink': 0.8},
        ax=ax
    )

    ax.set_title(titre, fontsize=14, weight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()

    if sauvegarder:
        plt.savefig(sauvegarder, dpi=dpi, bbox_inches='tight')
        print(f"✅ Matrice de corrélation sauvegardée: {sauvegarder}")

    return fig


def tracer_comparaison_modeles(resultats_modeles, metrique='recall',
                                titre='Comparaison des Modèles',
                                sauvegarder=None, dpi=300):
    """
    Compare les performances de plusieurs modèles.

    Args:
        resultats_modeles: Dict {nom_modele: metriques_dict}
        metrique: Métrique à comparer
        titre: Titre du graphique
        sauvegarder: Chemin de sauvegarde
        dpi: Résolution

    Returns:
        matplotlib.figure.Figure: Figure créée
    """
    # Extraire les métriques
    noms_modeles = list(resultats_modeles.keys())
    metriques_principales = ['accuracy', 'precision', 'recall', 'f1_score']

    data = {metric: [] for metric in metriques_principales}

    for nom in noms_modeles:
        for metric in metriques_principales:
            val = resultats_modeles[nom].get(metric, 0)
            data[metric].append(val)

    # Créer le graphique
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(len(noms_modeles))
    width = 0.2

    for idx, metric in enumerate(metriques_principales):
        offset = (idx - len(metriques_principales)/2) * width + width/2
        bars = ax.bar(x + offset, data[metric], width, label=metric.capitalize())

        # Annotations
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}',
                    ha='center', va='bottom', fontsize=8)

    ax.set_xlabel('Modèles', fontsize=12, weight='bold')
    ax.set_ylabel('Score', fontsize=12, weight='bold')
    ax.set_title(titre, fontsize=14, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(noms_modeles, rotation=45, ha='right')
    ax.legend(loc='best')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim([0, 1.1])

    plt.tight_layout()

    if sauvegarder:
        plt.savefig(sauvegarder, dpi=dpi, bbox_inches='tight')
        print(f"✅ Comparaison modèles sauvegardée: {sauvegarder}")

    return fig


def tracer_courbes_apprentissage(historique_train, historique_val,
                                  metrique='loss', titre='Courbes d\'Apprentissage',
                                  sauvegarder=None, dpi=300):
    """
    Trace les courbes d'apprentissage (pour réseaux de neurones).

    Args:
        historique_train: Historique train
        historique_val: Historique validation
        metrique: Métrique à tracer
        titre: Titre du graphique
        sauvegarder: Chemin de sauvegarde
        dpi: Résolution

    Returns:
        matplotlib.figure.Figure: Figure créée
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    epochs = range(1, len(historique_train) + 1)

    ax.plot(epochs, historique_train, 'b-o', label=f'Train {metrique}', linewidth=2)
    ax.plot(epochs, historique_val, 'r-s', label=f'Validation {metrique}', linewidth=2)

    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel(metrique.capitalize(), fontsize=12)
    ax.set_title(titre, fontsize=14, weight='bold')
    ax.legend(loc='best', fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if sauvegarder:
        plt.savefig(sauvegarder, dpi=dpi, bbox_inches='tight')
        print(f"✅ Courbes d'apprentissage sauvegardées: {sauvegarder}")

    return fig


def generer_rapport_visuel_complet(y_true, y_pred, y_proba, importances=None,
                                    feature_names=None, dossier_sortie='./figures',
                                    prefixe='model'):
    """
    Génère un ensemble complet de visualisations pour un modèle.

    Args:
        y_true: Vraies étiquettes
        y_pred: Prédictions
        y_proba: Probabilités
        importances: Scores d'importance (optionnel)
        feature_names: Noms des features (optionnel)
        dossier_sortie: Dossier de sauvegarde
        prefixe: Préfixe des noms de fichiers

    Returns:
        list: Liste des chemins des fichiers générés
    """
    Path(dossier_sortie).mkdir(parents=True, exist_ok=True)

    fichiers_generes = []

    print("=" * 80)
    print("🎨 GÉNÉRATION DU RAPPORT VISUEL COMPLET")
    print("=" * 80)

    # 1. Matrice de confusion
    chemin = Path(dossier_sortie) / f'{prefixe}_confusion_matrix.png'
    tracer_matrice_confusion(y_true, y_pred, sauvegarder=chemin)
    fichiers_generes.append(chemin)

    # 2. Courbe ROC
    chemin = Path(dossier_sortie) / f'{prefixe}_roc_curve.png'
    tracer_courbe_roc(y_true, y_proba, sauvegarder=chemin)
    fichiers_generes.append(chemin)

    # 3. Courbe Précision-Recall
    chemin = Path(dossier_sortie) / f'{prefixe}_precision_recall.png'
    tracer_precision_recall(y_true, y_proba, sauvegarder=chemin)
    fichiers_generes.append(chemin)

    # 4. Importance des features (si disponible)
    if importances is not None and feature_names is not None:
        chemin = Path(dossier_sortie) / f'{prefixe}_feature_importance.png'
        tracer_importance_features(importances, feature_names, sauvegarder=chemin)
        fichiers_generes.append(chemin)

    print("\n" + "=" * 80)
    print(f"✅ {len(fichiers_generes)} visualisations générées dans {dossier_sortie}")
    print("=" * 80)

    return fichiers_generes


if __name__ == '__main__':
    """Tests unitaires basiques des fonctions."""

    print("=" * 80)
    print("TESTS DU MODULE VISUALIZATION")
    print("=" * 80)

    # Créer des données de test
    np.random.seed(42)
    n = 200

    y_true = np.random.randint(0, 2, n)
    y_proba = np.random.uniform(0, 1, n)
    y_pred = (y_proba >= 0.5).astype(int)

    # Créer dossier temporaire
    dossier_test = Path('./test_visualizations')
    dossier_test.mkdir(exist_ok=True)

    print("\n1️⃣ Test: Matrice de confusion")
    tracer_matrice_confusion(y_true, y_pred,
                             sauvegarder=dossier_test / 'test_confusion.png')

    print("\n2️⃣ Test: Courbe ROC")
    tracer_courbe_roc(y_true, y_proba,
                      sauvegarder=dossier_test / 'test_roc.png')

    print("\n3️⃣ Test: Importance features")
    importances = np.random.uniform(0, 1, 10)
    feature_names = [f'Feature_{i}' for i in range(10)]
    tracer_importance_features(importances, feature_names,
                                sauvegarder=dossier_test / 'test_importance.png')

    print("\n4️⃣ Test: Rapport visuel complet")
    generer_rapport_visuel_complet(
        y_true, y_pred, y_proba,
        importances=importances,
        feature_names=feature_names,
        dossier_sortie=dossier_test,
        prefixe='test_model'
    )

    print(f"\n✅ Tous les tests terminés. Vérifiez le dossier: {dossier_test}")
