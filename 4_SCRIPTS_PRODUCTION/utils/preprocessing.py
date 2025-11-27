#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MODULE PREPROCESSING - FONCTIONS DE PRÉTRAITEMENT RÉUTILISABLES
================================================================================

Ce module contient des fonctions utilitaires pour le prétraitement des données
du projet de détection précoce du DT1.

Auteur: Dr. TCHAPET NJAFA Jean-Pierre avec assistance Claude Code
Date: Novembre 2025
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import logging


def verifier_valeurs_manquantes(df, afficher=True):
    """
    Vérifie la présence de valeurs manquantes dans un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame à analyser
        afficher (bool): Afficher le résumé des valeurs manquantes

    Returns:
        pd.Series: Nombre de valeurs manquantes par colonne
    """
    valeurs_manquantes = df.isnull().sum()

    if afficher:
        total = valeurs_manquantes.sum()
        if total > 0:
            print(f"⚠️ {total} valeurs manquantes détectées:")
            print(valeurs_manquantes[valeurs_manquantes > 0])
        else:
            print("✅ Aucune valeur manquante")

    return valeurs_manquantes


def imputer_valeurs_manquantes(df, strategie='median', colonnes=None):
    """
    Impute les valeurs manquantes avec une stratégie donnée.

    Args:
        df (pd.DataFrame): DataFrame avec valeurs manquantes
        strategie (str): Stratégie d'imputation ('mean', 'median', 'most_frequent')
        colonnes (list): Liste de colonnes à imputer (None = toutes)

    Returns:
        pd.DataFrame: DataFrame avec valeurs imputées
    """
    df_copy = df.copy()

    # Sélectionner les colonnes
    if colonnes is None:
        colonnes = df_copy.columns[df_copy.isnull().any()].tolist()

    if not colonnes:
        return df_copy

    # Imputer
    imputer = SimpleImputer(strategy=strategie)
    df_copy[colonnes] = imputer.fit_transform(df_copy[colonnes])

    print(f"✅ Imputation ({strategie}) appliquée sur {len(colonnes)} colonnes")

    return df_copy


def detecter_outliers_iqr(df, colonne, facteur=1.5):
    """
    Détecte les outliers avec la méthode IQR (Interquartile Range).

    Args:
        df (pd.DataFrame): DataFrame contenant les données
        colonne (str): Nom de la colonne à analyser
        facteur (float): Facteur multiplicateur pour IQR (défaut: 1.5)

    Returns:
        tuple: (outliers_indices, seuil_bas, seuil_haut)
    """
    Q1 = df[colonne].quantile(0.25)
    Q3 = df[colonne].quantile(0.75)
    IQR = Q3 - Q1

    seuil_bas = Q1 - facteur * IQR
    seuil_haut = Q3 + facteur * IQR

    outliers = df[(df[colonne] < seuil_bas) | (df[colonne] > seuil_haut)].index

    print(f"📊 Colonne '{colonne}': {len(outliers)} outliers détectés")
    print(f"   Seuils: [{seuil_bas:.2f}, {seuil_haut:.2f}]")

    return outliers, seuil_bas, seuil_haut


def encoder_variables_categorielles(df, colonnes, methode='label'):
    """
    Encode les variables catégorielles.

    Args:
        df (pd.DataFrame): DataFrame contenant les variables
        colonnes (list): Liste des colonnes catégorielles
        methode (str): 'label' pour LabelEncoder, 'onehot' pour OneHot

    Returns:
        pd.DataFrame: DataFrame avec variables encodées
    """
    df_copy = df.copy()
    encoders = {}

    if methode == 'label':
        for col in colonnes:
            if col in df_copy.columns:
                le = LabelEncoder()
                df_copy[col] = le.fit_transform(df_copy[col].astype(str))
                encoders[col] = le
                print(f"✅ '{col}' encodée (label): {len(le.classes_)} classes")

    elif methode == 'onehot':
        df_copy = pd.get_dummies(df_copy, columns=colonnes, drop_first=True)
        print(f"✅ One-Hot encoding appliqué sur {len(colonnes)} colonnes")

    return df_copy, encoders


def normaliser_features_numeriques(df, colonnes=None, methode='standard'):
    """
    Normalise les features numériques.

    Args:
        df (pd.DataFrame): DataFrame avec features numériques
        colonnes (list): Liste de colonnes à normaliser (None = toutes numériques)
        methode (str): 'standard' (StandardScaler) ou 'minmax' (MinMaxScaler)

    Returns:
        tuple: (df_normalized, scaler)
    """
    df_copy = df.copy()

    # Sélectionner colonnes numériques si non spécifié
    if colonnes is None:
        colonnes = df_copy.select_dtypes(include=[np.number]).columns.tolist()

    if methode == 'standard':
        scaler = StandardScaler()
    elif methode == 'minmax':
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
    else:
        raise ValueError(f"Méthode inconnue: {methode}")

    # Normaliser
    df_copy[colonnes] = scaler.fit_transform(df_copy[colonnes])

    print(f"✅ Normalisation ({methode}) appliquée sur {len(colonnes)} colonnes")

    return df_copy, scaler


def creer_features_biomedicales(df):
    """
    Crée des features dérivées spécifiques au contexte biomédical.

    Args:
        df (pd.DataFrame): DataFrame avec features de base

    Returns:
        pd.DataFrame: DataFrame avec features augmentées
    """
    df_copy = df.copy()

    # Ratio redox (si biomarqueurs présents)
    if 'NADH' in df_copy.columns and 'FAD' in df_copy.columns:
        df_copy['ratio_NADH_FAD'] = df_copy['NADH'] / (df_copy['FAD'] + 1e-10)
        print("✅ Feature créée: ratio_NADH_FAD")

    # Score de biomarqueurs composite (si disponibles)
    biomarqueurs = ['ANP32A_IT1', 'ESCO2', 'NBPF1']
    if all(b in df_copy.columns for b in biomarqueurs):
        # Normaliser d'abord chaque biomarqueur (0-1)
        for bio in biomarqueurs:
            min_val = df_copy[bio].min()
            max_val = df_copy[bio].max()
            df_copy[f'{bio}_norm'] = (df_copy[bio] - min_val) / (max_val - min_val + 1e-10)

        # Score composite (moyenne pondérée)
        df_copy['score_biomarqueurs'] = (
            0.4 * df_copy['ANP32A_IT1_norm'] +
            0.35 * df_copy['ESCO2_norm'] +
            0.25 * df_copy['NBPF1_norm']
        )
        print("✅ Feature créée: score_biomarqueurs")

    # Catégories IMC selon OMS
    if 'IMC' in df_copy.columns:
        df_copy['categorie_IMC'] = pd.cut(
            df_copy['IMC'],
            bins=[0, 18.5, 25, 30, 100],
            labels=['Maigreur', 'Normal', 'Surpoids', 'Obesite']
        )
        print("✅ Feature créée: categorie_IMC")

    # Catégories glycémie (seuils DT1)
    if 'glycemie_jeun' in df_copy.columns:
        df_copy['categorie_glycemie'] = pd.cut(
            df_copy['glycemie_jeun'],
            bins=[0, 5.6, 6.9, 100],
            labels=['Normal', 'Prediabete', 'Diabete']
        )
        print("✅ Feature créée: categorie_glycemie")

    # Interaction âge × glycémie (facteur de risque)
    if 'age' in df_copy.columns and 'glycemie_jeun' in df_copy.columns:
        df_copy['risque_age_glycemie'] = df_copy['age'] * df_copy['glycemie_jeun'] / 100
        print("✅ Feature créée: risque_age_glycemie")

    return df_copy


def verifier_equilibre_classes(y, afficher=True):
    """
    Vérifie l'équilibre des classes de la variable cible.

    Args:
        y (pd.Series ou np.array): Variable cible
        afficher (bool): Afficher le résumé

    Returns:
        dict: Statistiques d'équilibre
    """
    distribution = pd.Series(y).value_counts()
    ratio = distribution.min() / distribution.max()

    stats = {
        'distribution': distribution,
        'ratio': ratio,
        'desequilibre': ratio < 0.5
    }

    if afficher:
        print("📊 Distribution des classes:")
        print(distribution)
        print(f"\n📐 Ratio d'équilibre: {ratio:.3f}")

        if stats['desequilibre']:
            print("⚠️ Déséquilibre détecté! Considérer SMOTE ou class_weight.")
        else:
            print("✅ Classes relativement équilibrées")

    return stats


def appliquer_smote(X, y, sampling_strategy=0.5, random_state=42):
    """
    Applique SMOTE pour équilibrer les classes.

    Args:
        X (pd.DataFrame ou np.array): Features
        y (pd.Series ou np.array): Variable cible
        sampling_strategy (float): Ratio de sureschantillonnage
        random_state (int): Seed aléatoire

    Returns:
        tuple: (X_resampled, y_resampled)
    """
    from imblearn.over_sampling import SMOTE

    print("🔧 Application de SMOTE...")
    print(f"Distribution avant: {pd.Series(y).value_counts().to_dict()}")

    smote = SMOTE(sampling_strategy=sampling_strategy, random_state=random_state)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    print(f"Distribution après: {pd.Series(y_resampled).value_counts().to_dict()}")
    print(f"✅ SMOTE appliqué: {len(X)} → {len(X_resampled)} échantillons")

    return X_resampled, y_resampled


def verifier_correlations_elevees(df, seuil=0.95, afficher=True):
    """
    Détecte les features fortement corrélées (potentiellement redondantes).

    Args:
        df (pd.DataFrame): DataFrame avec features numériques
        seuil (float): Seuil de corrélation (défaut: 0.95)
        afficher (bool): Afficher les paires corrélées

    Returns:
        list: Liste de tuples (feature1, feature2, correlation)
    """
    # Calculer la matrice de corrélation
    corr_matrix = df.corr().abs()

    # Extraire le triangle supérieur
    upper_tri = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )

    # Trouver les paires fortement corrélées
    paires_correlees = []
    for col in upper_tri.columns:
        for row in upper_tri.index:
            val = upper_tri.loc[row, col]
            if val > seuil:
                paires_correlees.append((row, col, val))

    if afficher:
        if paires_correlees:
            print(f"⚠️ {len(paires_correlees)} paires de features corrélées (>{seuil}):")
            for f1, f2, corr in paires_correlees:
                print(f"  - {f1} ↔ {f2}: {corr:.3f}")
            print("💡 Considérer de supprimer une des deux features")
        else:
            print(f"✅ Aucune corrélation excessive (seuil: {seuil})")

    return paires_correlees


# ============================================================================
# FONCTIONS SPÉCIFIQUES AU CONTEXTE CAMEROUNAIS
# ============================================================================

def categoriser_region_cameroun(df, colonne_region='region'):
    """
    Catégorise les régions du Cameroun en zones géographiques.

    Args:
        df (pd.DataFrame): DataFrame avec colonne région
        colonne_region (str): Nom de la colonne région

    Returns:
        pd.DataFrame: DataFrame avec colonne 'zone_geographique'
    """
    df_copy = df.copy()

    mapping_zones = {
        'Centre': 'Centre',
        'Littoral': 'Côte',
        'Ouest': 'Hauts-Plateaux',
        'Nord-Ouest': 'Hauts-Plateaux',
        'Sud-Ouest': 'Côte',
        'Adamaoua': 'Grand-Nord',
        'Nord': 'Grand-Nord',
        'Extrême-Nord': 'Grand-Nord',
        'Est': 'Forêt',
        'Sud': 'Forêt'
    }

    if colonne_region in df_copy.columns:
        df_copy['zone_geographique'] = df_copy[colonne_region].map(mapping_zones)
        print("✅ Feature créée: zone_geographique")

    return df_copy


def ajuster_seuils_cliniques_contexte_africain(df):
    """
    Applique des seuils cliniques adaptés au contexte africain/camerounais.

    Note: Les seuils standards peuvent nécessiter des ajustements selon
    les spécificités génétiques et environnementales de la population.

    Args:
        df (pd.DataFrame): DataFrame avec variables cliniques

    Returns:
        pd.DataFrame: DataFrame avec features ajustées
    """
    df_copy = df.copy()

    # Glycémie à jeun (valeurs en mmol/L)
    if 'glycemie_jeun' in df_copy.columns:
        df_copy['hyperglycemie'] = (df_copy['glycemie_jeun'] >= 7.0).astype(int)
        print("✅ Feature créée: hyperglycemie (seuil africain: 7.0 mmol/L)")

    # HbA1c (si disponible)
    if 'HbA1c' in df_copy.columns:
        df_copy['HbA1c_elevee'] = (df_copy['HbA1c'] >= 6.5).astype(int)
        print("✅ Feature créée: HbA1c_elevee (seuil: 6.5%)")

    return df_copy


if __name__ == '__main__':
    """Tests unitaires basiques des fonctions."""

    print("=" * 80)
    print("TESTS DU MODULE PREPROCESSING")
    print("=" * 80)

    # Créer un dataset de test
    np.random.seed(42)
    df_test = pd.DataFrame({
        'age': np.random.randint(20, 60, 100),
        'IMC': np.random.uniform(18, 35, 100),
        'glycemie_jeun': np.random.uniform(4.5, 10, 100),
        'ANP32A_IT1': np.random.uniform(2, 5, 100),
        'ESCO2': np.random.uniform(2, 5, 100),
        'NBPF1': np.random.uniform(2, 5, 100),
        'diagnostic': np.random.randint(0, 2, 100)
    })

    # Introduire quelques valeurs manquantes
    df_test.loc[0:5, 'IMC'] = np.nan

    print("\n1️⃣ Test: Vérification valeurs manquantes")
    verifier_valeurs_manquantes(df_test)

    print("\n2️⃣ Test: Imputation")
    df_imputed = imputer_valeurs_manquantes(df_test, strategie='median')

    print("\n3️⃣ Test: Création features biomédicales")
    df_augmented = creer_features_biomedicales(df_test)
    print(f"   Nouvelles colonnes: {[c for c in df_augmented.columns if c not in df_test.columns]}")

    print("\n4️⃣ Test: Vérification équilibre classes")
    verifier_equilibre_classes(df_test['diagnostic'])

    print("\n5️⃣ Test: Détection outliers (glycémie)")
    outliers, _, _ = detecter_outliers_iqr(df_test, 'glycemie_jeun')

    print("\n✅ Tous les tests terminés")
