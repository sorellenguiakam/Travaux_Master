#!/usr/bin/env python3
"""
Script 05: Interprétabilité et explications modèle
Analyse SHAP, importance features, explications prédictions

Auteure: Sorelle
Encadrant: Dr. Jean-Pierre TCHAPET
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
import joblib
import shap

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Style plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100


def charger_modele_et_donnees():
    """Charge le meilleur modèle et les données de test."""
    processed_dir = Path(__file__).parent.parent / 'processed'
    models_dir = Path(__file__).parent.parent / 'models'

    # Charger modèle
    model_file = models_dir / 'best_model.pkl'
    if not model_file.exists():
        logger.error(f"❌ Modèle introuvable: {model_file}")
        logger.error("   Exécutez d'abord: python 04_train_models.py")
        raise FileNotFoundError(model_file)

    model = joblib.load(model_file)
    logger.info(f"✓ Modèle chargé: {type(model).__name__}")

    # Charger données test
    X_test = pd.read_csv(processed_dir / 'X_test.csv')
    y_test = pd.read_csv(processed_dir / 'y_test.csv')['diagnostic_dt1']

    logger.info(f"✓ Données test chargées: {X_test.shape}")

    return model, X_test, y_test


def analyser_feature_importance(model, X_test, output_dir):
    """Analyse l'importance des features (pour modèles basés arbres)."""
    logger.info("\n" + "="*70)
    logger.info("IMPORTANCE DES FEATURES")
    logger.info("="*70)

    # Vérifier si le modèle a feature_importances_
    if not hasattr(model, 'feature_importances_'):
        logger.warning("⚠ Modèle ne supporte pas feature_importances_ (ex: SVM)")
        return None

    # Extraire importance
    importances = model.feature_importances_
    feature_names = X_test.columns

    # Créer DataFrame
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)

    logger.info("\n✓ Top 10 features importantes:")
    for idx, row in importance_df.head(10).iterrows():
        logger.info(f"  {row['feature']:20s}: {row['importance']:.4f}")

    # Visualisation
    fig, ax = plt.subplots(figsize=(10, 8))
    top_n = 15
    importance_df_top = importance_df.head(top_n)

    ax.barh(range(top_n), importance_df_top['importance'], color='steelblue')
    ax.set_yticks(range(top_n))
    ax.set_yticklabels(importance_df_top['feature'])
    ax.set_xlabel('Importance', fontsize=12)
    ax.set_title('Top 15 Features - Importance Modèle', fontsize=14, pad=15)
    ax.invert_yaxis()
    plt.tight_layout()

    output_file = output_dir / '01_feature_importance.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"\n✓ Visualisation sauvegardée: {output_file.name}")

    # Sauvegarder CSV
    importance_df.to_csv(output_dir / 'feature_importance.csv', index=False)
    logger.info(f"✓ CSV sauvegardé: feature_importance.csv")

    return importance_df


def calculer_shap_values(model, X_test, max_samples=100):
    """Calcule les valeurs SHAP pour l'interprétabilité."""
    logger.info("\n" + "="*70)
    logger.info("CALCUL VALEURS SHAP")
    logger.info("="*70)

    # Limiter nombre échantillons pour performance
    X_test_sample = X_test.sample(min(max_samples, len(X_test)), random_state=42)

    logger.info(f"\n✓ Échantillon: {len(X_test_sample)} patients")

    # Créer explainer SHAP approprié
    model_type = type(model).__name__

    try:
        if 'Tree' in model_type or 'Forest' in model_type or 'XGB' in model_type:
            # Tree-based models
            explainer = shap.TreeExplainer(model)
            logger.info(f"✓ TreeExplainer utilisé pour {model_type}")
        else:
            # Linear models ou autres
            explainer = shap.Explainer(model, X_test_sample)
            logger.info(f"✓ KernelExplainer utilisé pour {model_type}")

        # Calculer SHAP values
        logger.info("⏳ Calcul SHAP values en cours...")
        shap_values = explainer(X_test_sample)

        logger.info("✓ SHAP values calculées avec succès")
        return shap_values, X_test_sample

    except Exception as e:
        logger.error(f"❌ Erreur calcul SHAP: {str(e)}")
        return None, X_test_sample


def visualiser_shap(shap_values, X_test_sample, output_dir):
    """Crée visualisations SHAP."""
    logger.info("\n" + "="*70)
    logger.info("VISUALISATIONS SHAP")
    logger.info("="*70)

    if shap_values is None:
        logger.warning("⚠ Pas de valeurs SHAP disponibles, skip visualisations")
        return

    # 1. Summary plot (bar)
    fig, ax = plt.subplots(figsize=(10, 8))
    shap.summary_plot(shap_values, X_test_sample, plot_type="bar", show=False)
    plt.title('SHAP - Importance Globale Features', fontsize=14, pad=15)
    plt.tight_layout()
    output_file = output_dir / '02_shap_summary_bar.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"✓ {output_file.name}")

    # 2. Summary plot (beeswarm)
    fig, ax = plt.subplots(figsize=(10, 8))
    shap.summary_plot(shap_values, X_test_sample, show=False)
    plt.title('SHAP - Distribution Impact Features', fontsize=14, pad=15)
    plt.tight_layout()
    output_file = output_dir / '03_shap_summary_beeswarm.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"✓ {output_file.name}")

    # 3. Waterfall plot (première prédiction DT1)
    # Trouver un patient DT1 dans l'échantillon
    try:
        y_test_sample = pd.read_csv(
            Path(__file__).parent.parent / 'processed' / 'y_test.csv'
        )['diagnostic_dt1']
        dt1_indices = y_test_sample[y_test_sample == 1].index
        sample_indices = X_test_sample.index

        dt1_in_sample = [i for i, idx in enumerate(sample_indices) if idx in dt1_indices]

        if len(dt1_in_sample) > 0:
            idx = dt1_in_sample[0]
            fig, ax = plt.subplots(figsize=(10, 6))
            shap.waterfall_plot(shap_values[idx], show=False)
            plt.title('SHAP Waterfall - Exemple Patient DT1', fontsize=14)
            plt.tight_layout()
            output_file = output_dir / '04_shap_waterfall_dt1.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            logger.info(f"✓ {output_file.name}")
        else:
            logger.warning("⚠ Aucun patient DT1 dans échantillon, skip waterfall")

    except Exception as e:
        logger.warning(f"⚠ Erreur waterfall plot: {str(e)}")

    logger.info(f"\n✓ Visualisations SHAP terminées")


def analyser_biomarqueurs_cles(shap_values, X_test_sample, output_dir):
    """Analyse spécifique des 3 biomarqueurs génétiques clés."""
    logger.info("\n" + "="*70)
    logger.info("ANALYSE BIOMARQUEURS GÉNÉTIQUES CLÉS")
    logger.info("="*70)

    biomarqueurs = ['anp32a_it1', 'esco2', 'nbpf1']

    # Vérifier présence
    available = [b for b in biomarqueurs if b in X_test_sample.columns]
    logger.info(f"\n✓ Biomarqueurs trouvés: {available}")

    if shap_values is None or len(available) == 0:
        logger.warning("⚠ Données insuffisantes pour analyse biomarqueurs")
        return

    # Créer figure comparative
    fig, axes = plt.subplots(1, len(available), figsize=(5*len(available), 5))
    if len(available) == 1:
        axes = [axes]

    for i, bio in enumerate(available):
        ax = axes[i]
        bio_idx = X_test_sample.columns.get_loc(bio)

        # SHAP values pour ce biomarqueur
        shap_bio = shap_values.values[:, bio_idx]
        feature_values = X_test_sample[bio].values

        # Scatter plot
        scatter = ax.scatter(feature_values, shap_bio,
                           c=shap_bio, cmap='RdBu_r',
                           alpha=0.6, s=50)
        ax.set_xlabel(f'Valeur {bio.upper()}', fontsize=11)
        ax.set_ylabel('Impact SHAP', fontsize=11)
        ax.set_title(f'{bio.upper()}', fontsize=12, fontweight='bold')
        ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
        ax.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax, label='Impact SHAP')

    plt.suptitle('Impact des Biomarqueurs Génétiques sur Prédiction DT1',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    output_file = output_dir / '05_biomarqueurs_shap_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"\n✓ Analyse biomarqueurs: {output_file.name}")

    # Statistiques SHAP par biomarqueur
    logger.info("\n✓ Statistiques SHAP biomarqueurs:")
    for bio in available:
        bio_idx = X_test_sample.columns.get_loc(bio)
        shap_bio = shap_values.values[:, bio_idx]
        logger.info(f"  {bio.upper():15s}: mean_abs_shap={np.abs(shap_bio).mean():.4f}")


def main():
    """Pipeline complet d'interprétabilité."""
    logger.info("="*70)
    logger.info("SCRIPT 05: INTERPRÉTABILITÉ MODÈLE")
    logger.info("="*70)

    # Chemins
    output_dir = Path(__file__).parent.parent / 'interpretability'
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Chargement
    model, X_test, y_test = charger_modele_et_donnees()

    # 2. Feature importance (si disponible)
    analyser_feature_importance(model, X_test, output_dir)

    # 3. Calcul SHAP values
    shap_values, X_test_sample = calculer_shap_values(model, X_test, max_samples=100)

    # 4. Visualisations SHAP
    visualiser_shap(shap_values, X_test_sample, output_dir)

    # 5. Analyse biomarqueurs clés
    analyser_biomarqueurs_cles(shap_values, X_test_sample, output_dir)

    logger.info("\n" + "="*70)
    logger.info("✅ SCRIPT 05 TERMINÉ AVEC SUCCÈS")
    logger.info("="*70)
    logger.info("Prochaine étape: python 06_validation.py")


if __name__ == "__main__":
    main()
