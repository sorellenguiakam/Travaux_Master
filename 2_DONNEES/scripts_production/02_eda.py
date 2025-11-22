#!/usr/bin/env python3
"""
Script 02: Analyse Exploratoire Données (EDA)
Visualisations et statistiques descriptives

Auteure: Sorelle
Encadrant: Dr. Jean-Pierre TCHAPET
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Style plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100

def charger_dataset():
    """Charge le dataset généré par script 01."""
    data_file = Path(__file__).parent.parent / 'raw' / 'dataset_dt1_cameroun.csv'

    if not data_file.exists():
        logger.error(f"❌ Fichier introuvable: {data_file}")
        logger.error("   Exécutez d'abord: python 01_generer_dataset.py")
        raise FileNotFoundError(data_file)

    df = pd.read_csv(data_file)
    logger.info(f"✓ Dataset chargé: {df.shape[0]} patients, {df.shape[1]} variables")
    return df


def statistiques_descriptives(df):
    """Affiche statistiques descriptives."""
    logger.info("\n" + "="*70)
    logger.info("STATISTIQUES DESCRIPTIVES")
    logger.info("="*70)

    # Répartition diagnostic
    logger.info(f"\nRépartition diagnostic:")
    logger.info(f"  - DT1: {df['diagnostic_dt1'].sum()} ({df['diagnostic_dt1'].mean()*100:.1f}%)")
    logger.info(f"  - Sains: {(~df['diagnostic_dt1'].astype(bool)).sum()} ({(1-df['diagnostic_dt1'].mean())*100:.1f}%)")

    # Statistiques numériques
    logger.info(f"\nStatistiques variables numériques:")
    logger.info(df.describe().T[['mean', 'std', 'min', 'max']])


def visualisations(df, output_dir='../processed/figures'):
    """Crée visualisations EDA."""
    output_path = Path(__file__).parent.parent / output_dir
    output_path.mkdir(parents=True, exist_ok=True)

    logger.info(f"\nGénération visualisations dans: {output_path}")

    # 1. Distribution biomarqueurs par diagnostic
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    biomarqueurs = ['anp32a_it1', 'esco2', 'nbpf1']

    for i, bio in enumerate(biomarqueurs):
        df[df['diagnostic_dt1']==0][bio].hist(ax=axes[i], bins=30, alpha=0.5, label='Sains', color='blue')
        df[df['diagnostic_dt1']==1][bio].hist(ax=axes[i], bins=30, alpha=0.5, label='DT1', color='red')
        axes[i].set_xlabel(bio)
        axes[i].set_ylabel('Fréquence')
        axes[i].legend()
        axes[i].set_title(f'Distribution {bio.upper()}')

    plt.tight_layout()
    plt.savefig(output_path / '01_distributions_biomarqueurs.png', dpi=300, bbox_inches='tight')
    plt.close()
    logger.info("  ✓ 01_distributions_biomarqueurs.png")

    # 2. Matrice corrélations
    features_numeriques = df.select_dtypes(include=[np.number]).columns.tolist()
    features_numeriques.remove('diagnostic_dt1')  # Exclure target

    fig, ax = plt.subplots(figsize=(12, 10))
    corr = df[features_numeriques].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    plt.title('Matrice de Corrélations - Features Numériques', fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(output_path / '02_matrice_correlations.png', dpi=300, bbox_inches='tight')
    plt.close()
    logger.info("  ✓ 02_matrice_correlations.png")

    # 3. Boxplots comparaison DT1 vs Sains
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.ravel()

    features_cliniques = ['hba1c', 'glycemie_jeun', 'cpeptide', 'anp32a_it1', 'esco2', 'nbpf1']

    for i, feat in enumerate(features_cliniques):
        df.boxplot(column=feat, by='diagnostic_dt1', ax=axes[i])
        axes[i].set_xlabel('Diagnostic (0=Sain, 1=DT1)')
        axes[i].set_ylabel(feat)
        axes[i].set_title(f'{feat}')
        plt.sca(axes[i])
        plt.xticks([1, 2], ['Sain', 'DT1'])

    plt.suptitle('')  # Enlever titre automatique
    plt.tight_layout()
    plt.savefig(output_path / '03_boxplots_comparaison.png', dpi=300, bbox_inches='tight')
    plt.close()
    logger.info("  ✓ 03_boxplots_comparaison.png")

    logger.info(f"\nTotal: 3 figures générées")


def main():
    """Pipeline EDA."""
    logger.info("="*70)
    logger.info("SCRIPT 02: ANALYSE EXPLORATOIRE DONNÉES (EDA)")
    logger.info("="*70)

    # Chargement
    df = charger_dataset()

    # Statistiques
    statistiques_descriptives(df)

    # Visualisations
    visualisations(df)

    logger.info("\n" + "="*70)
    logger.info("✅ SCRIPT 02 TERMINÉ AVEC SUCCÈS")
    logger.info("="*70)
    logger.info("Prochaine étape: python 03_preprocessing.py")


if __name__ == "__main__":
    main()
