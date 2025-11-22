#!/usr/bin/env python3
"""
Script 04: Entraînement et comparaison de modèles ML
Random Forest, XGBoost, SVM avec optimisation hyperparamètres

Auteure: Sorelle
Encadrant: Dr. Jean-Pierre TCHAPET
"""

import numpy as np
import pandas as pd
from pathlib import Path
import logging
import json
import joblib
import time

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

from sklearn.model_selection import GridSearchCV, cross_validate
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def charger_donnees_preprocessees():
    """Charge les données prétraitées du script 03."""
    processed_dir = Path(__file__).parent.parent / 'processed'

    required_files = ['X_train.csv', 'X_test.csv', 'y_train.csv', 'y_test.csv']
    for fname in required_files:
        if not (processed_dir / fname).exists():
            logger.error(f"❌ Fichier manquant: {processed_dir / fname}")
            logger.error("   Exécutez d'abord: python 03_preprocessing.py")
            raise FileNotFoundError(fname)

    X_train = pd.read_csv(processed_dir / 'X_train.csv')
    X_test = pd.read_csv(processed_dir / 'X_test.csv')
    y_train = pd.read_csv(processed_dir / 'y_train.csv')['diagnostic_dt1']
    y_test = pd.read_csv(processed_dir / 'y_test.csv')['diagnostic_dt1']

    logger.info(f"✓ Données chargées:")
    logger.info(f"  - X_train: {X_train.shape}")
    logger.info(f"  - X_test: {X_test.shape}")
    logger.info(f"  - Train DT1 rate: {y_train.mean()*100:.1f}%")
    logger.info(f"  - Test DT1 rate: {y_test.mean()*100:.1f}%")

    return X_train, X_test, y_train, y_test


def definir_modeles():
    """Définit les modèles et leurs grilles d'hyperparamètres."""
    logger.info("\n" + "="*70)
    logger.info("DÉFINITION MODÈLES")
    logger.info("="*70)

    models = {
        'Logistic Regression': {
            'model': LogisticRegression(max_iter=1000, random_state=42),
            'params': {
                'C': [0.1, 1.0, 10.0],
                'penalty': ['l2'],
                'class_weight': ['balanced']
            }
        },

        'Random Forest': {
            'model': RandomForestClassifier(random_state=42),
            'params': {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5],
                'class_weight': ['balanced']
            }
        },

        'XGBoost': {
            'model': XGBClassifier(random_state=42, eval_metric='logloss'),
            'params': {
                'n_estimators': [100, 200],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1],
                'scale_pos_weight': [1, 5]  # Pour classes déséquilibrées
            }
        },

        'SVM': {
            'model': SVC(probability=True, random_state=42),
            'params': {
                'C': [0.1, 1.0, 10.0],
                'kernel': ['rbf', 'linear'],
                'class_weight': ['balanced']
            }
        }
    }

    logger.info(f"\n✓ {len(models)} modèles configurés:")
    for name in models.keys():
        logger.info(f"  - {name}")

    return models


def entrainer_modele(name, model_config, X_train, y_train):
    """Entraîne un modèle avec GridSearchCV."""
    logger.info(f"\n{'='*70}")
    logger.info(f"ENTRAÎNEMENT: {name}")
    logger.info(f"{'='*70}")

    start_time = time.time()

    # GridSearch avec cross-validation
    grid_search = GridSearchCV(
        estimator=model_config['model'],
        param_grid=model_config['params'],
        cv=5,
        scoring='f1',
        n_jobs=-1,  # Utiliser tous les cores
        verbose=1
    )

    grid_search.fit(X_train, y_train)

    train_time = time.time() - start_time

    logger.info(f"\n✓ Entraînement terminé en {train_time:.2f}s")
    logger.info(f"  - Meilleur score CV: {grid_search.best_score_:.4f}")
    logger.info(f"  - Meilleurs paramètres: {grid_search.best_params_}")

    return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_, train_time


def evaluer_modele(name, model, X_test, y_test):
    """Évalue un modèle sur le set de test."""
    logger.info(f"\n{'-'*70}")
    logger.info(f"ÉVALUATION: {name}")
    logger.info(f"{'-'*70}")

    # Prédictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

    # Métriques
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_proba) if y_proba is not None else None
    }

    # Matrice confusion
    cm = confusion_matrix(y_test, y_pred)

    logger.info(f"\n✓ Métriques de performance:")
    logger.info(f"  - Accuracy: {metrics['accuracy']:.4f}")
    logger.info(f"  - Precision: {metrics['precision']:.4f}")
    logger.info(f"  - Recall: {metrics['recall']:.4f}")
    logger.info(f"  - F1-Score: {metrics['f1']:.4f}")
    if metrics['roc_auc']:
        logger.info(f"  - ROC-AUC: {metrics['roc_auc']:.4f}")

    logger.info(f"\n✓ Matrice de confusion:")
    logger.info(f"  TN={cm[0,0]}  FP={cm[0,1]}")
    logger.info(f"  FN={cm[1,0]}  TP={cm[1,1]}")

    return metrics, cm


def sauvegarder_resultats(results, output_dir):
    """Sauvegarde les résultats d'entraînement."""
    logger.info("\n" + "="*70)
    logger.info("SAUVEGARDE RÉSULTATS")
    logger.info("="*70)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Trouver meilleur modèle
    best_model_name = max(results.keys(), key=lambda k: results[k]['test_metrics']['f1'])
    best_model = results[best_model_name]['model']

    logger.info(f"\n✓ Meilleur modèle: {best_model_name}")
    logger.info(f"  - F1-Score: {results[best_model_name]['test_metrics']['f1']:.4f}")

    # Sauvegarder meilleur modèle
    model_file = output_dir / 'best_model.pkl'
    joblib.dump(best_model, model_file)
    logger.info(f"\n✓ Modèle sauvegardé: {model_file}")

    # Sauvegarder tous les résultats
    results_summary = {}
    for name, res in results.items():
        results_summary[name] = {
            'best_params': res['best_params'],
            'cv_score': float(res['cv_score']),
            'train_time': float(res['train_time']),
            'test_metrics': {k: float(v) if v is not None else None
                           for k, v in res['test_metrics'].items()},
            'confusion_matrix': res['confusion_matrix'].tolist()
        }

    results_file = output_dir / 'training_results.json'
    with open(results_file, 'w') as f:
        json.dump({
            'best_model': best_model_name,
            'models': results_summary
        }, f, indent=2)

    logger.info(f"✓ Résultats sauvegardés: {results_file}")

    # Tableau comparatif
    logger.info("\n" + "="*70)
    logger.info("TABLEAU COMPARATIF MODÈLES")
    logger.info("="*70)

    comparison_df = pd.DataFrame({
        name: {
            'CV F1': f"{res['cv_score']:.4f}",
            'Test F1': f"{res['test_metrics']['f1']:.4f}",
            'Test Accuracy': f"{res['test_metrics']['accuracy']:.4f}",
            'Test ROC-AUC': f"{res['test_metrics']['roc_auc']:.4f}" if res['test_metrics']['roc_auc'] else 'N/A',
            'Train Time (s)': f"{res['train_time']:.2f}"
        }
        for name, res in results.items()
    }).T

    logger.info("\n" + str(comparison_df))

    comparison_df.to_csv(output_dir / 'models_comparison.csv')
    logger.info(f"\n✓ Comparaison sauvegardée: models_comparison.csv")


def main():
    """Pipeline complet d'entraînement."""
    logger.info("="*70)
    logger.info("SCRIPT 04: ENTRAÎNEMENT MODÈLES ML")
    logger.info("="*70)

    # Chemins
    output_dir = Path(__file__).parent.parent / 'models'

    # 1. Chargement données
    X_train, X_test, y_train, y_test = charger_donnees_preprocessees()

    # 2. Définition modèles
    models = definir_modeles()

    # 3. Entraînement et évaluation
    results = {}

    for name, model_config in models.items():
        # Entraîner
        model, best_params, cv_score, train_time = entrainer_modele(
            name, model_config, X_train, y_train
        )

        # Évaluer
        test_metrics, cm = evaluer_modele(name, model, X_test, y_test)

        # Stocker résultats
        results[name] = {
            'model': model,
            'best_params': best_params,
            'cv_score': cv_score,
            'train_time': train_time,
            'test_metrics': test_metrics,
            'confusion_matrix': cm
        }

    # 4. Sauvegarde
    sauvegarder_resultats(results, output_dir)

    logger.info("\n" + "="*70)
    logger.info("✅ SCRIPT 04 TERMINÉ AVEC SUCCÈS")
    logger.info("="*70)
    logger.info("Prochaine étape: python 05_interpretability.py")


if __name__ == "__main__":
    main()
