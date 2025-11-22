"""
TITRE: Nettoyage et préparation des données DT1 Cameroun
OBJECTIF: Nettoyer le dataset brut, gérer valeurs manquantes, détecter outliers
INPUTS: dataset_dt1_cameroun_synthetic.csv
OUTPUTS: dataset_clean.csv
DURÉE ESTIMÉE: <1 minute
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("🧹 NETTOYAGE DES DONNÉES - PROJET DT1 CAMEROUN")
print("=" * 70)

# === CHARGEMENT ===
print("\n📂 Étape 1/6: Chargement des données...")
df = pd.read_csv('../raw/dataset_dt1_cameroun_synthetic.csv')
print(f"   ✅ {df.shape[0]} lignes, {df.shape[1]} colonnes chargées")

# === INSPECTION ===
print("\n🔍 Étape 2/6: Inspection initiale...")
print(f"\n   Valeurs manquantes:")
missing = df.isnull().sum()
for col in missing[missing > 0].index:
    print(f"      {col}: {missing[col]} ({missing[col]/len(df)*100:.1f}%)")

# === IMPUTATION ===
print("\n🔧 Étape 3/6: Imputation des valeurs manquantes...")
imputer = SimpleImputer(strategy='median')
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols.remove('diagnostic')  # Ne pas imputer la variable cible

df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
print(f"   ✅ Imputation par médiane effectuée")

# === OUTLIERS ===
print("\n📊 Étape 4/6: Détection des outliers (méthode IQR)...")
outliers_count = 0
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
    if outliers > 0:
        print(f"      {col}: {outliers} outliers détectés")
        outliers_count += outliers

print(f"   Total: {outliers_count} outliers (conservés pour analyse)")

# === ENCODAGE ===
print("\n🔤 Étape 5/6: Encodage des variables catégorielles...")
df['sexe_encoded'] = df['sexe'].map({'M': 0, 'F': 1})
df = pd.get_dummies(df, columns=['region'], drop_first=True)
print(f"   ✅ Encodage terminé ({len(df.columns)} colonnes au total)")

# === SAUVEGARDE ===
print("\n💾 Étape 6/6: Sauvegarde...")
df.to_csv('../processed/dataset_clean.csv', index=False)
print(f"   ✅ Sauvegardé: ../processed/dataset_clean.csv")

print("\n" + "=" * 70)
print("✨ NETTOYAGE TERMINÉ!")
print("=" * 70)
