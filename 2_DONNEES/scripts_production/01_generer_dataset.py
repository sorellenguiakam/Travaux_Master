#!/usr/bin/env python3
"""
Script 01: Génération Dataset Synthétique - Diabète Type 1
Création de 1000 patients camerounais avec biomarqueurs génétiques

Auteure: Sorelle
Master 2 Physique - Université de Yaoundé I
Encadrant: Dr. Jean-Pierre TCHAPET (jean-pierre.tchapet@facsciences-uy1.cm)
"""

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Seed pour reproductibilité
np.random.seed(42)

def generer_patients_synthetiques(n_patients=1000, prevalence_dt1=0.15):
    """
    Génère dataset synthétique de patients camerounais.

    Parameters
    ----------
    n_patients : int
        Nombre de patients à générer (défaut: 1000)
    prevalence_dt1 : float
        Proportion de cas DT1 positifs (défaut: 0.15 = 15%)

    Returns
    -------
    pd.DataFrame
        Dataset avec données démographiques, cliniques et génétiques
    """
    logger.info(f"Génération de {n_patients} patients (prévalence DT1: {prevalence_dt1*100}%)")

    n_dt1 = int(n_patients * prevalence_dt1)
    n_sains = n_patients - n_dt1

    # Diagnostic (variable cible)
    diagnostic = np.concatenate([
        np.ones(n_dt1, dtype=int),   # DT1 positifs
        np.zeros(n_sains, dtype=int)  # Sains
    ])

    # ===================================================================
    # 1. DONNÉES DÉMOGRAPHIQUES
    # ===================================================================

    # Âge (ans) - DT1 souvent diagnostiqué chez enfants/adolescents
    age_dt1 = np.random.normal(loc=12, scale=5, size=n_dt1)  # Pic ~12 ans
    age_sains = np.random.normal(loc=15, scale=8, size=n_sains)
    age = np.concatenate([age_dt1, age_sains])
    age = np.clip(age, 1, 40).astype(int)  # Limiter 1-40 ans

    # Sexe (0=Féminin, 1=Masculin) - léger biais masculin pour DT1
    sexe_dt1 = np.random.binomial(1, 0.55, size=n_dt1)  # 55% garçons
    sexe_sains = np.random.binomial(1, 0.50, size=n_sains)  # 50% neutre
    sexe = np.concatenate([sexe_dt1, sexe_sains])

    # IMC (kg/m²) - DT1 souvent plus maigres
    imc_dt1 = np.random.normal(loc=18, scale=2.5, size=n_dt1)
    imc_sains = np.random.normal(loc=21, scale=3, size=n_sains)
    imc = np.concatenate([imc_dt1, imc_sains])
    imc = np.clip(imc, 12, 35)

    # Antécédents familiaux diabète (0=Non, 1=Oui)
    atcd_dt1 = np.random.binomial(1, 0.30, size=n_dt1)  # 30% avec antécédents
    atcd_sains = np.random.binomial(1, 0.05, size=n_sains)  # 5% seulement
    antecedents_familiaux = np.concatenate([atcd_dt1, atcd_sains])

    # ===================================================================
    # 2. DONNÉES CLINIQUES
    # ===================================================================

    # HbA1c (%) - Hémoglobine glyquée (marqueur glycémie long terme)
    # Normal: <5.7%, Pré-diabète: 5.7-6.4%, Diabète: ≥6.5%
    hba1c_dt1 = np.random.normal(loc=9.5, scale=2.0, size=n_dt1)  # Élevé
    hba1c_sains = np.random.normal(loc=5.2, scale=0.4, size=n_sains)  # Normal
    hba1c = np.concatenate([hba1c_dt1, hba1c_sains])
    hba1c = np.clip(hba1c, 4.0, 15.0)

    # Glycémie à jeun (mmol/L)
    # Normal: 3.9-5.5, Pré-diabète: 5.6-6.9, Diabète: ≥7.0
    glycemie_dt1 = np.random.normal(loc=12.0, scale=3.0, size=n_dt1)
    glycemie_sains = np.random.normal(loc=5.0, scale=0.5, size=n_sains)
    glycemie_jeun = np.concatenate([glycemie_dt1, glycemie_sains])
    glycemie_jeun = np.clip(glycemie_jeun, 3.0, 25.0)

    # C-peptide (pmol/L) - marqueur production insuline endogène
    # Faible chez DT1 (destruction cellules β pancréatiques)
    cpeptide_dt1 = np.random.normal(loc=100, scale=50, size=n_dt1)  # Bas
    cpeptide_sains = np.random.normal(loc=600, scale=150, size=n_sains)  # Normal
    cpeptide = np.concatenate([cpeptide_dt1, cpeptide_sains])
    cpeptide = np.clip(cpeptide, 10, 1500)

    # Auto-anticorps (0=Absent, 1=Présent)
    # 40-80% DT1 auto-immuns ont anticorps (ICA, GAD, IA-2)
    # Formes idiopathiques (20-60% en Afrique) = absence anticorps
    anticorps_dt1 = np.random.binomial(1, 0.60, size=n_dt1)  # 60% positifs
    anticorps_sains = np.random.binomial(1, 0.01, size=n_sains)  # 1% faux positifs
    auto_anticorps = np.concatenate([anticorps_dt1, anticorps_sains])

    # ===================================================================
    # 3. BIOMARQUEURS GÉNÉTIQUES (Cœur du projet)
    # ===================================================================

    # Expression biomarqueurs candidats (valeurs normalisées log2)
    # Basé sur littérature: ANP32A-IT1, ESCO2, NBPF1

    # ANP32A-IT1 (lncRNA) - surexprimé chez DT1
    anp32a_dt1 = np.random.normal(loc=2.5, scale=0.8, size=n_dt1)  # Élevé
    anp32a_sains = np.random.normal(loc=0.5, scale=0.6, size=n_sains)  # Bas
    anp32a_it1 = np.concatenate([anp32a_dt1, anp32a_sains])
    anp32a_it1 = np.clip(anp32a_it1, -2, 5)

    # ESCO2 (Establishment of Sister Chromatid Cohesion 2) - sous-exprimé chez DT1
    esco2_dt1 = np.random.normal(loc=-1.5, scale=0.7, size=n_dt1)  # Bas
    esco2_sains = np.random.normal(loc=0.8, scale=0.5, size=n_sains)  # Normal
    esco2 = np.concatenate([esco2_dt1, esco2_sains])
    esco2 = np.clip(esco2, -4, 3)

    # NBPF1 (Neuroblastoma Breakpoint Family 1) - surexprimé chez DT1
    nbpf1_dt1 = np.random.normal(loc=1.8, scale=0.9, size=n_dt1)  # Élevé
    nbpf1_sains = np.random.normal(loc=-0.3, scale=0.6, size=n_sains)  # Bas
    nbpf1 = np.concatenate([nbpf1_dt1, nbpf1_sains])
    nbpf1 = np.clip(nbpf1, -3, 4)

    # Biomarqueurs additionnels (pour robustesse modèle)
    # HLA-DQB1 (Human Leukocyte Antigen) - risque génétique
    hla_dqb1_dt1 = np.random.binomial(1, 0.70, size=n_dt1)  # 70% ont allèle risque
    hla_dqb1_sains = np.random.binomial(1, 0.25, size=n_sains)  # 25% population générale
    hla_dqb1_risque = np.concatenate([hla_dqb1_dt1, hla_dqb1_sains])

    # IL-10 (Interleukine-10) - cytokine anti-inflammatoire, souvent basse chez DT1
    il10_dt1 = np.random.normal(loc=3.0, scale=1.0, size=n_dt1)  # Bas
    il10_sains = np.random.normal(loc=6.0, scale=1.5, size=n_sains)  # Normal
    il10 = np.concatenate([il10_dt1, il10_sains])
    il10 = np.clip(il10, 0.5, 12)

    # TNF-alpha (Tumor Necrosis Factor) - pro-inflammatoire, élevé chez DT1
    tnf_alpha_dt1 = np.random.normal(loc=25, scale=8, size=n_dt1)  # Élevé
    tnf_alpha_sains = np.random.normal(loc=10, scale=4, size=n_sains)  # Normal
    tnf_alpha = np.concatenate([tnf_alpha_dt1, tnf_alpha_sains])
    tnf_alpha = np.clip(tnf_alpha, 2, 60)

    # ===================================================================
    # 4. ASSEMBLY DATASET
    # ===================================================================

    # Mélanger pour éviter biais ordre
    indices = np.random.permutation(n_patients)

    df = pd.DataFrame({
        # Identifiant
        'patient_id': [f'CAM_{i:04d}' for i in range(n_patients)],

        # Démographique
        'age': age[indices],
        'sexe': sexe[indices],  # 0=F, 1=M
        'imc': imc[indices],
        'antecedents_familiaux': antecedents_familiaux[indices],

        # Clinique
        'hba1c': hba1c[indices],
        'glycemie_jeun': glycemie_jeun[indices],
        'cpeptide': cpeptide[indices],
        'auto_anticorps': auto_anticorps[indices],

        # Biomarqueurs génétiques (cibles principales)
        'anp32a_it1': anp32a_it1[indices],
        'esco2': esco2[indices],
        'nbpf1': nbpf1[indices],

        # Biomarqueurs additionnels
        'hla_dqb1_risque': hla_dqb1_risque[indices],
        'il10': il10[indices],
        'tnf_alpha': tnf_alpha[indices],

        # Variable cible (à prédire)
        'diagnostic_dt1': diagnostic[indices]  # 0=Sain, 1=DT1
    })

    logger.info(f"Dataset généré: {df.shape[0]} patients, {df.shape[1]} variables")
    logger.info(f"Répartition: {df['diagnostic_dt1'].sum()} DT1 ({df['diagnostic_dt1'].mean()*100:.1f}%), "
                f"{(~df['diagnostic_dt1'].astype(bool)).sum()} Sains")

    return df


def sauvegarder_dataset(df, output_dir='../raw'):
    """
    Sauvegarde dataset avec métadonnées.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset à sauvegarder
    output_dir : str
        Répertoire de sortie
    """
    output_path = Path(__file__).parent.parent / output_dir
    output_path.mkdir(parents=True, exist_ok=True)

    # Fichier CSV principal
    csv_file = output_path / 'dataset_dt1_cameroun.csv'
    df.to_csv(csv_file, index=False)
    logger.info(f"✓ Dataset sauvegardé: {csv_file}")
    logger.info(f"  Taille: {csv_file.stat().st_size / 1024:.1f} KB")

    # Métadonnées
    metadata = {
        'date_generation': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'n_patients': len(df),
        'n_features': df.shape[1] - 2,  # Exclure patient_id et diagnostic
        'prevalence_dt1': df['diagnostic_dt1'].mean(),
        'features': df.columns.tolist(),
        'description': {
            'patient_id': 'Identifiant unique patient',
            'age': 'Âge (années)',
            'sexe': 'Sexe (0=Féminin, 1=Masculin)',
            'imc': 'Indice Masse Corporelle (kg/m²)',
            'antecedents_familiaux': 'Antécédents familiaux diabète (0/1)',
            'hba1c': 'Hémoglobine glyquée (%)',
            'glycemie_jeun': 'Glycémie à jeun (mmol/L)',
            'cpeptide': 'C-peptide (pmol/L)',
            'auto_anticorps': 'Présence auto-anticorps (0/1)',
            'anp32a_it1': 'Expression ANP32A-IT1 (log2)',
            'esco2': 'Expression ESCO2 (log2)',
            'nbpf1': 'Expression NBPF1 (log2)',
            'hla_dqb1_risque': 'Allèle HLA-DQB1 risque (0/1)',
            'il10': 'Interleukine-10 (pg/mL)',
            'tnf_alpha': 'TNF-alpha (pg/mL)',
            'diagnostic_dt1': 'Diagnostic DT1 (0=Sain, 1=DT1)'
        }
    }

    metadata_file = output_path / 'dataset_metadata.txt'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("MÉTADONNÉES DATASET DIABÈTE TYPE 1 - CAMEROUN\n")
        f.write("="*70 + "\n\n")
        f.write(f"Date génération: {metadata['date_generation']}\n")
        f.write(f"Nombre patients: {metadata['n_patients']}\n")
        f.write(f"Nombre features: {metadata['n_features']}\n")
        f.write(f"Prévalence DT1: {metadata['prevalence_dt1']*100:.1f}%\n\n")
        f.write("="*70 + "\n")
        f.write("DESCRIPTION VARIABLES\n")
        f.write("="*70 + "\n\n")
        for var, desc in metadata['description'].items():
            f.write(f"{var:25s}: {desc}\n")

    logger.info(f"✓ Métadonnées sauvegardées: {metadata_file}")


def afficher_statistiques(df):
    """Affiche statistiques descriptives du dataset."""
    logger.info("\n" + "="*70)
    logger.info("STATISTIQUES DATASET")
    logger.info("="*70)

    # Statistiques globales
    logger.info(f"\nNombre total patients: {len(df)}")
    logger.info(f"  - DT1 positifs: {df['diagnostic_dt1'].sum()} ({df['diagnostic_dt1'].mean()*100:.1f}%)")
    logger.info(f"  - Sains: {(~df['diagnostic_dt1'].astype(bool)).sum()} ({(1-df['diagnostic_dt1'].mean())*100:.1f}%)")

    # Comparaison DT1 vs Sains (moyennes)
    logger.info("\nComparaison DT1 vs Sains (moyennes):")
    logger.info(f"{'Variable':<20s} {'DT1':>10s} {'Sains':>10s} {'Différence':>12s}")
    logger.info("-" * 55)

    for col in ['age', 'imc', 'hba1c', 'glycemie_jeun', 'cpeptide',
                'anp32a_it1', 'esco2', 'nbpf1', 'il10', 'tnf_alpha']:
        dt1_mean = df[df['diagnostic_dt1']==1][col].mean()
        sains_mean = df[df['diagnostic_dt1']==0][col].mean()
        diff = dt1_mean - sains_mean
        logger.info(f"{col:<20s} {dt1_mean:>10.2f} {sains_mean:>10.2f} {diff:>12.2f}")

    # Valeurs manquantes
    logger.info(f"\nValeurs manquantes: {df.isnull().sum().sum()} (attendu: 0)")


def main():
    """Pipeline principal."""
    logger.info("="*70)
    logger.info("SCRIPT 01: GÉNÉRATION DATASET SYNTHÉTIQUE DT1")
    logger.info("="*70)

    # Génération
    df = generer_patients_synthetiques(n_patients=1000, prevalence_dt1=0.15)

    # Statistiques
    afficher_statistiques(df)

    # Sauvegarde
    sauvegarder_dataset(df, output_dir='../raw')

    logger.info("\n" + "="*70)
    logger.info("✅ SCRIPT 01 TERMINÉ AVEC SUCCÈS")
    logger.info("="*70)
    logger.info(f"\nProchaine étape: python 02_eda.py")


if __name__ == "__main__":
    main()
