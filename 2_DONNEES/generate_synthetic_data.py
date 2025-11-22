"""
TITRE: Génération de Données Synthétiques pour le Projet DT1 Cameroun
OBJECTIF: Créer un dataset réaliste de patients avec biomarqueurs pour entraînement ML
OUTPUTS: dataset_dt1_cameroun_synthetic.csv dans 2_DONNEES/raw/
DURÉE ESTIMÉE: <1 minute
AUTEUR: Dr. TCHAPET NJAFA Jean-Pierre / Claude 4.5
DATE: Novembre 2025
"""

# === IMPORTS ===
import numpy as np  # Génération nombres aléatoires
import pandas as pd  # Manipulation données
from datetime import datetime  # Horodatage
import os  # Gestion fichiers

# Fixer la graine pour reproductibilité
np.random.seed(42)

# === CONFIGURATION ===
CONFIG = {
    'n_patients': 1000,  # Nombre total de patients
    'prevalence_dt1': 0.25,  # 25% de patients DT1+ (réaliste pour étude ciblée)
    'output_path': 'raw/dataset_dt1_cameroun_synthetic.csv'
}

print("=" * 70)
print("🔬 GÉNÉRATION DE DONNÉES SYNTHÉTIQUES - PROJET DT1 CAMEROUN")
print("=" * 70)

# === GÉNÉRATION DES DONNÉES ===

print(f"\n📊 Configuration:")
print(f"   - Nombre de patients: {CONFIG['n_patients']}")
print(f"   - Prévalence DT1+: {CONFIG['prevalence_dt1']*100}%")

# Calcul nombre de patients par classe
n_dt1_positif = int(CONFIG['n_patients'] * CONFIG['prevalence_dt1'])
n_dt1_negatif = CONFIG['n_patients'] - n_dt1_positif

print(f"   - Patients DT1+: {n_dt1_positif}")
print(f"   - Patients DT1-: {n_dt1_negatif}")

# === GÉNÉRATION IDENTIFIANTS ===
print("\n🆔 Génération des identifiants...")
ids = [f"PAT{str(i).zfill(4)}" for i in range(1, CONFIG['n_patients'] + 1)]

# === GÉNÉRATION DÉMOGRAPHIE ===
print("👥 Génération des données démographiques...")

# Âge: Distribution réaliste (pic jeunes adultes pour DT1)
ages = np.concatenate([
    np.random.normal(25, 8, n_dt1_positif),  # DT1+: plus jeunes (moyenne 25 ans)
    np.random.normal(35, 12, n_dt1_negatif)  # DT1-: plus âgés (moyenne 35 ans)
])
ages = np.clip(ages, 5, 70).astype(int)  # Limiter entre 5 et 70 ans

# Sexe: Distribution équilibrée avec légère prédominance masculine DT1+
sexes_dt1_pos = np.random.choice(['M', 'F'], n_dt1_positif, p=[0.55, 0.45])
sexes_dt1_neg = np.random.choice(['M', 'F'], n_dt1_negatif, p=[0.48, 0.52])
sexes = np.concatenate([sexes_dt1_pos, sexes_dt1_neg])

# Région: Principales villes du Cameroun
regions = np.random.choice(
    ['Yaoundé', 'Douala', 'Bafoussam', 'Garoua', 'Bamenda', 'Maroua', 'Ngaoundéré'],
    CONFIG['n_patients'],
    p=[0.30, 0.25, 0.15, 0.10, 0.08, 0.07, 0.05]  # Proportions réalistes
)

# === GÉNÉRATION BIOMARQUEURS (CLÉS POUR LA DÉTECTION) ===
print("🧬 Génération des biomarqueurs génétiques...")

# ANP32A-IT1: Régulation immunitaire
# DT1+: valeurs plus élevées (moyenne 4.5)
# DT1-: valeurs plus basses (moyenne 2.0)
anp32a_dt1_pos = np.random.lognormal(mean=1.3, sigma=0.5, size=n_dt1_positif)
anp32a_dt1_neg = np.random.lognormal(mean=0.5, sigma=0.6, size=n_dt1_negatif)
anp32a = np.concatenate([anp32a_dt1_pos, anp32a_dt1_neg])
anp32a = np.clip(anp32a, 0.5, 10.0)  # Limiter plage réaliste

# ESCO2: Régulation cycle cellulaire
# DT1+: valeurs élevées (moyenne 6.0)
# DT1-: valeurs basses (moyenne 2.5)
esco2_dt1_pos = np.random.lognormal(mean=1.6, sigma=0.45, size=n_dt1_positif)
esco2_dt1_neg = np.random.lognormal(mean=0.7, sigma=0.55, size=n_dt1_negatif)
esco2 = np.concatenate([esco2_dt1_pos, esco2_dt1_neg])
esco2 = np.clip(esco2, 1.0, 15.0)

# NBPF1: Expression cellules pancréatiques
# DT1+: valeurs modérément élevées (moyenne 3.5)
# DT1-: valeurs basses (moyenne 1.8)
nbpf1_dt1_pos = np.random.lognormal(mean=1.1, sigma=0.5, size=n_dt1_positif)
nbpf1_dt1_neg = np.random.lognormal(mean=0.4, sigma=0.6, size=n_dt1_negatif)
nbpf1 = np.concatenate([nbpf1_dt1_pos, nbpf1_dt1_neg])
nbpf1 = np.clip(nbpf1, 0.8, 8.0)

# === BIOMARQUEURS ADDITIONNELS (pour enrichir le dataset) ===
print("🔬 Génération des biomarqueurs additionnels...")

# Glycémie à jeun (mmol/L): Élevée chez DT1+
glycemie_dt1_pos = np.random.normal(10.5, 2.5, n_dt1_positif)  # Hyperglycémie
glycemie_dt1_neg = np.random.normal(5.0, 0.8, n_dt1_negatif)   # Normale
glycemie = np.concatenate([glycemie_dt1_pos, glycemie_dt1_neg])
glycemie = np.clip(glycemie, 3.0, 20.0)

# HbA1c (%) : Élevée chez DT1+
hba1c_dt1_pos = np.random.normal(9.5, 1.8, n_dt1_positif)  # >6.5% = diabète
hba1c_dt1_neg = np.random.normal(5.2, 0.5, n_dt1_negatif)  # Normale
hba1c = np.concatenate([hba1c_dt1_pos, hba1c_dt1_neg])
hba1c = np.clip(hba1c, 4.0, 14.0)

# IMC (kg/m²): DT1+ souvent plus minces
imc_dt1_pos = np.random.normal(21.5, 3.0, n_dt1_positif)
imc_dt1_neg = np.random.normal(25.0, 4.5, n_dt1_negatif)
imc = np.concatenate([imc_dt1_pos, imc_dt1_neg])
imc = np.clip(imc, 15.0, 40.0)

# Antécédents familiaux diabète (0=non, 1=oui)
antecedents_dt1_pos = np.random.choice([0, 1], n_dt1_positif, p=[0.6, 0.4])  # 40% ont antécédents
antecedents_dt1_neg = np.random.choice([0, 1], n_dt1_negatif, p=[0.85, 0.15])  # 15% ont antécédents
antecedents = np.concatenate([antecedents_dt1_pos, antecedents_dt1_neg])

# === VARIABLE CIBLE (DIAGNOSTIC) ===
diagnostic = np.concatenate([
    np.ones(n_dt1_positif, dtype=int),   # 1 = DT1+
    np.zeros(n_dt1_negatif, dtype=int)   # 0 = DT1-
])

# === CRÉATION DU DATAFRAME ===
print("\n📋 Création du DataFrame...")

df = pd.DataFrame({
    'ID_patient': ids,
    'age': ages,
    'sexe': sexes,
    'region': regions,
    'IMC': np.round(imc, 2),
    'glycemie_jeun': np.round(glycemie, 2),
    'HbA1c': np.round(hba1c, 2),
    'antecedents_familiaux': antecedents,
    'ANP32A_IT1': np.round(anp32a, 3),
    'ESCO2': np.round(esco2, 3),
    'NBPF1': np.round(nbpf1, 3),
    'diagnostic': diagnostic
})

# === MÉLANGER LES DONNÉES (shuffle) ===
print("🔀 Mélange des données...")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# === AJOUTER QUELQUES VALEURS MANQUANTES RÉALISTES ===
print("🕳️  Ajout de valeurs manquantes réalistes (2-5%)...")

# Simuler valeurs manquantes (certains biomarqueurs non mesurés)
n_missing_anp32a = int(0.03 * CONFIG['n_patients'])  # 3% manquant
n_missing_nbpf1 = int(0.02 * CONFIG['n_patients'])   # 2% manquant
n_missing_hba1c = int(0.05 * CONFIG['n_patients'])   # 5% manquant

missing_indices_anp32a = np.random.choice(df.index, n_missing_anp32a, replace=False)
missing_indices_nbpf1 = np.random.choice(df.index, n_missing_nbpf1, replace=False)
missing_indices_hba1c = np.random.choice(df.index, n_missing_hba1c, replace=False)

df.loc[missing_indices_anp32a, 'ANP32A_IT1'] = np.nan
df.loc[missing_indices_nbpf1, 'NBPF1'] = np.nan
df.loc[missing_indices_hba1c, 'HbA1c'] = np.nan

# === STATISTIQUES DESCRIPTIVES ===
print("\n" + "=" * 70)
print("📊 STATISTIQUES DESCRIPTIVES DU DATASET")
print("=" * 70)

print(f"\n📈 Distribution de la variable cible:")
print(df['diagnostic'].value_counts())
print(f"\n   Proportion DT1+: {df['diagnostic'].mean()*100:.1f}%")
print(f"   Proportion DT1-: {(1-df['diagnostic'].mean())*100:.1f}%")

print(f"\n🧮 Statistiques biomarqueurs clés:")
for col in ['ANP32A_IT1', 'ESCO2', 'NBPF1']:
    print(f"\n   {col}:")
    print(f"      DT1+ - Moyenne: {df[df['diagnostic']==1][col].mean():.3f}, Écart-type: {df[df['diagnostic']==1][col].std():.3f}")
    print(f"      DT1- - Moyenne: {df[df['diagnostic']==0][col].mean():.3f}, Écart-type: {df[df['diagnostic']==0][col].std():.3f}")

print(f"\n🕳️  Valeurs manquantes:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# === SAUVEGARDE ===
print("\n" + "=" * 70)
print("💾 SAUVEGARDE DU DATASET")
print("=" * 70)

# Créer dossier si n'existe pas
os.makedirs('raw', exist_ok=True)

# Sauvegarder
df.to_csv(CONFIG['output_path'], index=False, encoding='utf-8')

print(f"\n✅ Dataset sauvegardé: {CONFIG['output_path']}")
print(f"   - Taille fichier: {os.path.getsize(CONFIG['output_path']) / 1024:.1f} KB")
print(f"   - Nombre de lignes: {len(df)}")
print(f"   - Nombre de colonnes: {len(df.columns)}")

# === VALIDATION FINALE ===
print("\n🔍 Validation du fichier sauvegardé...")
df_test = pd.read_csv(CONFIG['output_path'])
assert len(df_test) == CONFIG['n_patients'], "❌ Erreur: nombre de lignes incorrect"
assert len(df_test.columns) == len(df.columns), "❌ Erreur: nombre de colonnes incorrect"
print("✅ Validation réussie!")

print("\n" + "=" * 70)
print("✨ GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
print("=" * 70)
print("\n📝 Prochaines étapes:")
print("   1. Charger le dataset: pd.read_csv('2_DONNEES/raw/dataset_dt1_cameroun_synthetic.csv')")
print("   2. Explorer les données (notebook Semaine 2)")
print("   3. Nettoyer et préparer (scripts preprocessing)")
print("\n" + "=" * 70)
