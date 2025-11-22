#!/usr/bin/env python3
"""
Script 06: Validation clinique et analyse robustesse
Métriques cliniques, analyse sous-groupes, intervalles confiance

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
import json
from scipy import stats

from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score,
    recall_score, f1_score, roc_auc_score, roc_curve
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Style plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100


def charger_modele_et_donnees():
    """Charge le meilleur modèle et toutes les données."""
    processed_dir = Path(__file__).parent.parent / 'processed'
    models_dir = Path(__file__).parent.parent / 'models'
    raw_dir = Path(__file__).parent.parent / 'raw'

    # Charger modèle
    model = joblib.load(models_dir / 'best_model.pkl')
    logger.info(f"✓ Modèle chargé: {type(model).__name__}")

    # Charger données test preprocessées
    X_test = pd.read_csv(processed_dir / 'X_test.csv')
    y_test = pd.read_csv(processed_dir / 'y_test.csv')['diagnostic_dt1']

    # Charger dataset complet pour métadonnées
    df_full = pd.read_csv(raw_dir / 'dataset_dt1_cameroun.csv')

    logger.info(f"✓ Données chargées: {X_test.shape}")

    return model, X_test, y_test, df_full


def calculer_metriques_cliniques(y_true, y_pred, y_proba=None):
    """Calcule métriques cliniques détaillées."""
    logger.info("\n" + "="*70)
    logger.info("MÉTRIQUES CLINIQUES")
    logger.info("="*70)

    # Matrice confusion
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    # Métriques de base
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)  # PPV
    recall = recall_score(y_true, y_pred)  # Sensibilité
    f1 = f1_score(y_true, y_pred)

    # Métriques cliniques spécifiques
    specificity = tn / (tn + fp)  # Spécificité
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0  # Negative Predictive Value

    # Likelihood ratios
    lr_positive = recall / (1 - specificity) if specificity < 1 else np.inf
    lr_negative = (1 - recall) / specificity if specificity > 0 else np.inf

    # ROC-AUC
    auc = roc_auc_score(y_true, y_proba) if y_proba is not None else None

    metrics = {
        'accuracy': accuracy,
        'sensitivity': recall,
        'specificity': specificity,
        'ppv': precision,
        'npv': npv,
        'f1_score': f1,
        'lr_positive': lr_positive,
        'lr_negative': lr_negative,
        'roc_auc': auc,
        'confusion_matrix': {'TP': int(tp), 'TN': int(tn), 'FP': int(fp), 'FN': int(fn)}
    }

    # Affichage
    logger.info("\n✓ Métriques de Performance:")
    logger.info(f"  - Accuracy: {accuracy:.4f}")
    logger.info(f"  - Sensibilité (Recall): {recall:.4f}")
    logger.info(f"  - Spécificité: {specificity:.4f}")
    logger.info(f"  - PPV (Precision): {precision:.4f}")
    logger.info(f"  - NPV: {npv:.4f}")
    logger.info(f"  - F1-Score: {f1:.4f}")
    if auc:
        logger.info(f"  - ROC-AUC: {auc:.4f}")

    logger.info(f"\n✓ Likelihood Ratios:")
    logger.info(f"  - LR+: {lr_positive:.2f}")
    logger.info(f"  - LR-: {lr_negative:.2f}")

    logger.info(f"\n✓ Matrice de Confusion:")
    logger.info(f"               Prédiction")
    logger.info(f"             Sain    DT1")
    logger.info(f"  Réel Sain   {tn:4d}   {fp:4d}")
    logger.info(f"       DT1    {fn:4d}   {tp:4d}")

    return metrics


def bootstrap_confidence_intervals(model, X_test, y_test, n_iterations=1000, confidence=0.95):
    """Calcule intervalles de confiance par bootstrap."""
    logger.info("\n" + "="*70)
    logger.info("INTERVALLES DE CONFIANCE (Bootstrap)")
    logger.info("="*70)

    np.random.seed(42)
    metrics_boot = []

    logger.info(f"\n⏳ Bootstrap en cours ({n_iterations} itérations)...")

    for i in range(n_iterations):
        # Échantillon bootstrap
        indices = np.random.choice(len(X_test), size=len(X_test), replace=True)
        X_boot = X_test.iloc[indices]
        y_boot = y_test.iloc[indices]

        # Prédictions
        y_pred_boot = model.predict(X_boot)

        # Métriques
        metrics_boot.append({
            'accuracy': accuracy_score(y_boot, y_pred_boot),
            'sensitivity': recall_score(y_boot, y_pred_boot, zero_division=0),
            'specificity': confusion_matrix(y_boot, y_pred_boot).ravel()[0] /
                          (confusion_matrix(y_boot, y_pred_boot).ravel()[0] +
                           confusion_matrix(y_boot, y_pred_boot).ravel()[1])
                          if len(confusion_matrix(y_boot, y_pred_boot).ravel()) == 4 else 0,
            'f1': f1_score(y_boot, y_pred_boot, zero_division=0)
        })

    # Calculer percentiles
    df_boot = pd.DataFrame(metrics_boot)
    alpha = 1 - confidence
    lower = alpha / 2 * 100
    upper = (1 - alpha / 2) * 100

    ci_results = {}
    logger.info(f"\n✓ Intervalles de confiance {confidence*100:.0f}%:")

    for metric in df_boot.columns:
        ci_low = np.percentile(df_boot[metric], lower)
        ci_high = np.percentile(df_boot[metric], upper)
        mean_val = df_boot[metric].mean()

        ci_results[metric] = {
            'mean': float(mean_val),
            'ci_lower': float(ci_low),
            'ci_upper': float(ci_high)
        }

        logger.info(f"  - {metric:12s}: {mean_val:.4f} [{ci_low:.4f}, {ci_high:.4f}]")

    return ci_results


def analyser_sous_groupes(model, X_test, y_test, df_full):
    """Analyse performance sur sous-groupes démographiques."""
    logger.info("\n" + "="*70)
    logger.info("ANALYSE SOUS-GROUPES")
    logger.info("="*70)

    # Récupérer indices test
    test_indices = X_test.index
    df_test_full = df_full.loc[test_indices].reset_index(drop=True)

    # Prédictions
    y_pred = model.predict(X_test)

    results = {}

    # 1. Par sexe
    if 'sex_masculin' in X_test.columns:
        logger.info("\n✓ Performance par sexe:")
        for sex_val, sex_label in [(0, 'Féminin'), (1, 'Masculin')]:
            mask = (X_test['sex_masculin'] == sex_val).values
            if mask.sum() > 0:
                acc = accuracy_score(y_test[mask], y_pred[mask])
                sens = recall_score(y_test[mask], y_pred[mask], zero_division=0)
                spec = (confusion_matrix(y_test[mask], y_pred[mask]).ravel()[0] /
                       (confusion_matrix(y_test[mask], y_pred[mask]).ravel()[0] +
                        confusion_matrix(y_test[mask], y_pred[mask]).ravel()[1])
                       if len(confusion_matrix(y_test[mask], y_pred[mask]).ravel()) == 4 else 0)

                results[f'sex_{sex_label}'] = {
                    'n': int(mask.sum()),
                    'accuracy': float(acc),
                    'sensitivity': float(sens),
                    'specificity': float(spec)
                }

                logger.info(f"  {sex_label:10s} (n={mask.sum():3d}): "
                          f"Acc={acc:.3f}, Sens={sens:.3f}, Spec={spec:.3f}")

    # 2. Par groupe d'âge
    if 'age' in df_test_full.columns:
        logger.info("\n✓ Performance par groupe d'âge:")
        age_groups = [
            (0, 20, 'Enfants/Ados'),
            (20, 40, 'Jeunes adultes'),
            (40, 100, 'Adultes')
        ]

        for age_min, age_max, label in age_groups:
            mask = ((df_test_full['age'] >= age_min) &
                   (df_test_full['age'] < age_max)).values
            if mask.sum() > 0:
                acc = accuracy_score(y_test[mask], y_pred[mask])
                sens = recall_score(y_test[mask], y_pred[mask], zero_division=0)
                spec = (confusion_matrix(y_test[mask], y_pred[mask]).ravel()[0] /
                       (confusion_matrix(y_test[mask], y_pred[mask]).ravel()[0] +
                        confusion_matrix(y_test[mask], y_pred[mask]).ravel()[1])
                       if len(confusion_matrix(y_test[mask], y_pred[mask]).ravel()) == 4 else 0)

                results[f'age_{label}'] = {
                    'n': int(mask.sum()),
                    'accuracy': float(acc),
                    'sensitivity': float(sens),
                    'specificity': float(spec)
                }

                logger.info(f"  {label:15s} (n={mask.sum():3d}): "
                          f"Acc={acc:.3f}, Sens={sens:.3f}, Spec={spec:.3f}")

    return results


def visualiser_roc_curve(model, X_test, y_test, output_dir):
    """Visualise la courbe ROC."""
    logger.info("\n" + "="*70)
    logger.info("COURBE ROC")
    logger.info("="*70)

    # Prédictions probabilités
    if hasattr(model, 'predict_proba'):
        y_proba = model.predict_proba(X_test)[:, 1]

        # Calculer ROC curve
        fpr, tpr, thresholds = roc_curve(y_test, y_proba)
        auc = roc_auc_score(y_test, y_proba)

        # Plot
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(fpr, tpr, color='darkorange', lw=2,
               label=f'ROC curve (AUC = {auc:.3f})')
        ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--',
               label='Chance (AUC = 0.5)')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('Taux Faux Positifs (1 - Spécificité)', fontsize=12)
        ax.set_ylabel('Taux Vrais Positifs (Sensibilité)', fontsize=12)
        ax.set_title('Courbe ROC - Détection Diabète Type 1', fontsize=14, pad=15)
        ax.legend(loc="lower right", fontsize=11)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        output_file = output_dir / 'roc_curve.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"✓ Courbe ROC sauvegardée: {output_file.name}")
        logger.info(f"  - AUC = {auc:.4f}")

        return auc
    else:
        logger.warning("⚠ Modèle ne supporte pas predict_proba, skip ROC curve")
        return None


def generer_rapport_validation(metrics, ci_results, subgroup_results, output_dir):
    """Génère rapport de validation complet."""
    logger.info("\n" + "="*70)
    logger.info("GÉNÉRATION RAPPORT VALIDATION")
    logger.info("="*70)

    # Sauvegarder JSON
    report = {
        'clinical_metrics': metrics,
        'confidence_intervals': ci_results,
        'subgroup_analysis': subgroup_results
    }

    report_file = output_dir / 'validation_report.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    logger.info(f"\n✓ Rapport JSON: {report_file.name}")

    # Rapport texte résumé
    summary_file = output_dir / 'validation_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("RAPPORT DE VALIDATION CLINIQUE\n")
        f.write("Détection précoce Diabète Type 1 - Populations camerounaises\n")
        f.write("="*70 + "\n\n")

        f.write("1. PERFORMANCES GLOBALES\n")
        f.write("-" * 70 + "\n")
        f.write(f"Accuracy:    {metrics['accuracy']:.4f}\n")
        f.write(f"Sensibilité: {metrics['sensitivity']:.4f} "
               f"[{ci_results['sensitivity']['ci_lower']:.3f}, "
               f"{ci_results['sensitivity']['ci_upper']:.3f}]\n")
        f.write(f"Spécificité: {metrics['specificity']:.4f} "
               f"[{ci_results['specificity']['ci_lower']:.3f}, "
               f"{ci_results['specificity']['ci_upper']:.3f}]\n")
        f.write(f"PPV:         {metrics['ppv']:.4f}\n")
        f.write(f"NPV:         {metrics['npv']:.4f}\n")
        if metrics['roc_auc']:
            f.write(f"ROC-AUC:     {metrics['roc_auc']:.4f}\n")

        f.write("\n2. INTERPRÉTATION CLINIQUE\n")
        f.write("-" * 70 + "\n")

        sens = metrics['sensitivity']
        spec = metrics['specificity']

        if sens >= 0.90:
            f.write(f"✓ Excellente sensibilité ({sens:.1%}): Peu de cas DT1 manqués\n")
        elif sens >= 0.80:
            f.write(f"✓ Bonne sensibilité ({sens:.1%}): Acceptable pour dépistage\n")
        else:
            f.write(f"⚠ Sensibilité modérée ({sens:.1%}): Risque cas manqués\n")

        if spec >= 0.90:
            f.write(f"✓ Excellente spécificité ({spec:.1%}): Peu de faux positifs\n")
        elif spec >= 0.80:
            f.write(f"✓ Bonne spécificité ({spec:.1%}): Acceptable pour screening\n")
        else:
            f.write(f"⚠ Spécificité modérée ({spec:.1%}): Nombreux faux positifs\n")

        f.write("\n3. BIOMARQUEURS CLÉS\n")
        f.write("-" * 70 + "\n")
        f.write("- ANP32A-IT1: Surexpression associée DT1\n")
        f.write("- ESCO2: Sous-expression associée DT1\n")
        f.write("- NBPF1: Marqueur complémentaire\n")

        f.write("\n4. RECOMMANDATIONS\n")
        f.write("-" * 70 + "\n")
        f.write("• Validation prospective requise sur cohortes réelles\n")
        f.write("• Intégration données cliniques (HbA1c, C-peptide, auto-Ac)\n")
        f.write("• Étude coût-efficacité pour implémentation Cameroun\n")
        f.write("• Formation personnel soignant interprétation résultats\n")

    logger.info(f"✓ Rapport texte: {summary_file.name}")


def main():
    """Pipeline complet de validation."""
    logger.info("="*70)
    logger.info("SCRIPT 06: VALIDATION CLINIQUE")
    logger.info("="*70)

    # Chemins
    output_dir = Path(__file__).parent.parent / 'validation'
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Chargement
    model, X_test, y_test, df_full = charger_modele_et_donnees()

    # 2. Prédictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

    # 3. Métriques cliniques
    metrics = calculer_metriques_cliniques(y_test, y_pred, y_proba)

    # 4. Intervalles confiance
    ci_results = bootstrap_confidence_intervals(model, X_test, y_test, n_iterations=1000)

    # 5. Analyse sous-groupes
    subgroup_results = analyser_sous_groupes(model, X_test, y_test, df_full)

    # 6. Courbe ROC
    visualiser_roc_curve(model, X_test, y_test, output_dir)

    # 7. Rapport final
    generer_rapport_validation(metrics, ci_results, subgroup_results, output_dir)

    logger.info("\n" + "="*70)
    logger.info("✅ SCRIPT 06 TERMINÉ AVEC SUCCÈS")
    logger.info("="*70)
    logger.info("\n🎉 PIPELINE COMPLET TERMINÉ!")
    logger.info("   Tous les résultats sont disponibles dans 2_DONNEES/")


if __name__ == "__main__":
    main()
