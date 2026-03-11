import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

# Configuration
input_path = '2_DONNEES/processed/dataset_clean.csv'
output_path = '2_DONNEES/processed/dataset_features.csv'

print("Chargement des données nettoyées...")
df = pd.read_csv(input_path)

# 1. Feature Engineering
print("Création de nouvelles features...")
# Ratio ESCO2 / ANP32A_IT1 (éviter division par 0)
df['ratio_esco2_anp32a'] = df['ESCO2'] / (df['ANP32A_IT1'] + 1e-5)

# Groupes d'âge
bins = [0, 18, 30, 100]
labels = ['enfant', 'jeune', 'adulte']
df['age_groupe'] = pd.cut(df['age'], bins=bins, labels=labels)

# 2. Encodage One-Hot
print("Encodage One-Hot...")
categorical_cols = ['sexe', 'region', 'age_groupe']
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# 3. Normalisation (StandardScaler)
# Attention : Théoriquement, le fit du scaler doit se faire sur le TRAIN set uniquement pour éviter le data leakage.
# Cependant, dans cette étape pédagogique "Feature Engineering" global, on montre comment transformer.
# Pour le pipeline scikit-learn rigoureux, on utiliserait un Pipeline ou ColumnTransformer.
# Ici, pour générer un fichier "dataset_features.csv" prêt à l'emploi selon le plan, on scale tout.
# MAIS C'EST UNE MAUVAISE PRATIQUE DE PRODUCTION.
# On va plutôt laisser les données brutes numériques pour le scaling post-split ou scaler ici si c'est pour l'exercice.
# Suivons la méthodologie du fichier `demarche_methodologique_sorelle.md` qui dit :
# "Important : Faire sur train uniquement, appliquer sur test".
# Donc ce script ne devrait PAS scaler globalement s'il veut être rigoureux.
# Mais la tâche 9.5 dit "Générer dataset_features.csv" après normalization.
# Pour rester simple et suivre la Tâche 9.3 du md qui scale tout le df pour l'exemple (ligne 483), je vais le faire ici
# mais ajouter un commentaire d'avertissement.

print("Normalisation des variables numériques...")
numeric_features = ['age', 'IMC', 'glycemie_jeun', 'HbA1c', 'ANP32A_IT1', 'ESCO2', 'NBPF1', 'ratio_esco2_anp32a']
scaler = StandardScaler()
# Note: On convertit en float pour éviter les warnings
df_encoded[numeric_features] = scaler.fit_transform(df_encoded[numeric_features].astype(float))

# Sauvegarde
print(f"Dimensions finales avec features : {df_encoded.shape}")
df_encoded.to_csv(output_path, index=False)
print(f"Fichier sauvegardé : {output_path}")
