#!/usr/bin/env python3
"""
Script 03: Prétraitement des données
Nettoyage, encodage, normalisation et séparation train/test

Auteure: Sorelle
Encadrant: Dr. Jean-Pierre TCHAPET
"""

import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def charger_dataset():
    """Charge le dataset brut généré par script 01."""
    data_file = Path(__file__).parent.parent / 'raw' / 'dataset_dt1_cameroun.csv'

    if not data_file.exists():
        logger.error(f"❌ Fichier introuvable: {data_file}")
        logger.error("   Exécutez d'abord: python 01_generer_dataset.py")
        raise FileNotFoundError(data_file)

    df = pd.read_csv(data_file)
    logger.info(f"✓ Dataset chargé: {df.shape[0]} patients, {df.shape[1]} variables")
    return df


def verifier_qualite_donnees(df):
    """Vérifie la qualité des données."""
    logger.info("\n" + "="*70)
    logger.info("VÉRIFICATION QUALITÉ DONNÉES")
    logger.info("="*70)

    # Valeurs manquantes
    missing = df.isnull().sum()
    if missing.sum() > 0:
        logger.warning(f"\n⚠ Valeurs manquantes détectées:")
        for col, count in missing[missing > 0].items():
            logger.warning(f"  - {col}: {count} ({count/len(df)*100:.2f}%)")
    else:
        logger.info("\n✓ Aucune valeur manquante détectée")

    # Valeurs aberrantes (exemple: âge négatif)
    if (df['age'] < 0).any():
        logger.warning(f"⚠ Âges négatifs détectés: {(df['age'] < 0).sum()}")

    # Distribution classes
    class_counts = df['diagnostic_dt1'].value_counts()
    logger.info(f"\n✓ Distribution classes:")
    logger.info(f"  - Classe 0 (Sains): {class_counts[0]} ({class_counts[0]/len(df)*100:.1f}%)")
    logger.info(f"  - Classe 1 (DT1): {class_counts[1]} ({class_counts[1]/len(df)*100:.1f}%)")

    return df


def preparer_features(df):
    """Prépare les features pour l'apprentissage."""
    logger.info("\n" + "="*70)
    logger.info("PRÉPARATION FEATURES")
    logger.info("="*70)

    # Séparer target et features
    X = df.drop('diagnostic_dt1', axis=1)
    y = df['diagnostic_dt1']

    logger.info(f"\n✓ Séparation X/y:")
    logger.info(f"  - X (features): {X.shape}")
    logger.info(f"  - y (target): {y.shape}")

    # Vérifier types de features
    numerical_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

    logger.info(f"\n✓ Types de features:")
    logger.info(f"  - Numériques: {len(numerical_features)} features")
    logger.info(f"  - Catégorielles: {len(categorical_features)} features")

    if len(categorical_features) > 0:
        logger.info(f"\nFeatures catégorielles détectées: {categorical_features}")
        logger.info("Note: sex_masculin et antecedents_familiaux sont déjà encodés (0/1)")

    return X, y, numerical_features


def normaliser_features(X_train, X_test, numerical_features, output_dir):
    """Normalise les features numériques avec StandardScaler."""
    logger.info("\n" + "="*70)
    logger.info("NORMALISATION FEATURES")
    logger.info("="*70)

    # Initialiser scaler
    scaler = StandardScaler()

    # Fit sur train seulement
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    X_train_scaled[numerical_features] = scaler.fit_transform(X_train[numerical_features])
    X_test_scaled[numerical_features] = scaler.transform(X_test[numerical_features])

    logger.info(f"\n✓ Normalisation appliquée sur {len(numerical_features)} features")
    logger.info(f"  - Moyenne train: {X_train_scaled[numerical_features].mean().mean():.6f}")
    logger.info(f"  - Std train: {X_train_scaled[numerical_features].std().mean():.6f}")

    # Sauvegarder scaler
    scaler_file = output_dir / 'scaler.pkl'
    joblib.dump(scaler, scaler_file)
    logger.info(f"\n✓ Scaler sauvegardé: {scaler_file}")

    return X_train_scaled, X_test_scaled, scaler


def separer_train_test(X, y, test_size=0.2, random_state=42):
    """Sépare données en train/test stratifié."""
    logger.info("\n" + "="*70)
    logger.info("SÉPARATION TRAIN/TEST")
    logger.info("="*70)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y  # Important pour classes déséquilibrées
    )

    logger.info(f"\n✓ Séparation effectuée:")
    logger.info(f"  - Train: {X_train.shape[0]} échantillons ({(1-test_size)*100:.0f}%)")
    logger.info(f"  - Test: {X_test.shape[0]} échantillons ({test_size*100:.0f}%)")

    # Vérifier stratification
    logger.info(f"\n✓ Vérification stratification:")
    logger.info(f"  - Train DT1: {y_train.sum()} ({y_train.mean()*100:.1f}%)")
    logger.info(f"  - Test DT1: {y_test.sum()} ({y_test.mean()*100:.1f}%)")

    return X_train, X_test, y_train, y_test


def sauvegarder_donnees(X_train, X_test, y_train, y_test, output_dir):
    """Sauvegarde les datasets prétraités."""
    logger.info("\n" + "="*70)
    logger.info("SAUVEGARDE DATASETS")
    logger.info("="*70)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Sauvegarder en CSV
    pd.DataFrame(X_train).to_csv(output_dir / 'X_train.csv', index=False)
    pd.DataFrame(X_test).to_csv(output_dir / 'X_test.csv', index=False)
    pd.DataFrame(y_train, columns=['diagnostic_dt1']).to_csv(output_dir / 'y_train.csv', index=False)
    pd.DataFrame(y_test, columns=['diagnostic_dt1']).to_csv(output_dir / 'y_test.csv', index=False)

    logger.info(f"\n✓ 4 fichiers sauvegardés dans: {output_dir}")
    logger.info(f"  - X_train.csv: {X_train.shape}")
    logger.info(f"  - X_test.csv: {X_test.shape}")
    logger.info(f"  - y_train.csv: {y_train.shape}")
    logger.info(f"  - y_test.csv: {y_test.shape}")

    # Sauvegarder métadonnées
    metadata = {
        'n_train': len(X_train),
        'n_test': len(X_test),
        'n_features': X_train.shape[1],
        'features': X_train.columns.tolist(),
        'train_dt1_rate': float(y_train.mean()),
        'test_dt1_rate': float(y_test.mean()),
        'test_size': 0.2,
        'random_state': 42
    }

    import json
    with open(output_dir / 'preprocessing_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"\n✓ Métadonnées sauvegardées: preprocessing_metadata.json")


def main():
    """Pipeline complet de prétraitement."""
    logger.info("="*70)
    logger.info("SCRIPT 03: PRÉTRAITEMENT DONNÉES")
    logger.info("="*70)

    # Chemins
    output_dir = Path(__file__).parent.parent / 'processed'

    # 1. Chargement
    df = charger_dataset()

    # 2. Vérification qualité
    df = verifier_qualite_donnees(df)

    # 3. Préparation features
    X, y, numerical_features = preparer_features(df)

    # 4. Séparation train/test
    X_train, X_test, y_train, y_test = separer_train_test(X, y)

    # 5. Normalisation
    X_train_scaled, X_test_scaled, scaler = normaliser_features(
        X_train, X_test, numerical_features, output_dir
    )

    # 6. Sauvegarde
    sauvegarder_donnees(X_train_scaled, X_test_scaled, y_train, y_test, output_dir)

    logger.info("\n" + "="*70)
    logger.info("✅ SCRIPT 03 TERMINÉ AVEC SUCCÈS")
    logger.info("="*70)
    logger.info("Prochaine étape: python 04_train_models.py")


if __name__ == "__main__":
    main()
