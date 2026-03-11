import pandas as pd
import numpy as np
import os
from sklearn.impute import SimpleImputer

# Configuration
input_path = '2_DONNEES/raw/dataset_dt1_cameroun_synthetic.csv'
output_dir = '2_DONNEES/processed'
output_path = os.path.join(output_dir, 'dataset_clean.csv')

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(output_dir, exist_ok=True)

print("Chargement des données...")
df = pd.read_csv(input_path)
print(f"Dimensions initiales : {df.shape}")

# 1. Gestion des valeurs manquantes
print("Gestion des valeurs manquantes...")
# Pour les variables numériques : Imputation par la médiane
numeric_cols = df.select_dtypes(include=[np.number]).columns
imputer = SimpleImputer(strategy='median')
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

# Pour les variables catégorielles : Imputation par le mode (si nécessaire, ici pas de missing dans l'exemple mais sécu)
categorical_cols = df.select_dtypes(exclude=[np.number]).columns
if len(categorical_cols) > 0:
    cat_imputer = SimpleImputer(strategy='most_frequent')
    df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

# 2. Gestion des Outliers (Capping à Q1-1.5*IQR et Q3+1.5*IQR)
print("Gestion des outliers...")
for col in ['ANP32A_IT1', 'ESCO2', 'NBPF1', 'glycemie_jeun', 'HbA1c', 'IMC', 'age']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # On ne supprime pas, on cape (winsorization) pour garder les données
    df[col] = np.clip(df[col], lower_bound, upper_bound)

# 3. Standardisation des formats
print("Standardisation des formats...")
if 'sexe' in df.columns:
    df['sexe'] = df['sexe'].str.strip().str.upper()
if 'region' in df.columns:
    df['region'] = df['region'].str.strip().str.title()

print(f"Dimensions finales : {df.shape}")
df.to_csv(output_path, index=False)
print(f"Fichier sauvegardé : {output_path}")
