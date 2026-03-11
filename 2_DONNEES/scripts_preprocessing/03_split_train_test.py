import pandas as pd
import os
from sklearn.model_selection import train_test_split

# Configuration
input_path = '2_DONNEES/processed/dataset_features.csv'
output_dir = '2_DONNEES/processed'

print("Chargement du dataset avec features...")
df = pd.read_csv(input_path)

# Séparation Features (X) et Target (y)
target_col = 'diagnostic'
X = df.drop(target_col, axis=1)
y = df[target_col]

print(f"Totale samples: {len(df)}")
print(f"Distribution cible: \n{y.value_counts(normalize=True)}")

# Split Stratifié
# 60% Train, 20% Val, 20% Test
# D'abord 80% Train+Val, 20% Test
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Puis 75% de Train+Val -> 60% du total (0.75 * 0.8 = 0.6)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp)

print(f"Train shapes: X={X_train.shape}, y={y_train.shape}")
print(f"Val shapes: X={X_val.shape}, y={y_val.shape}")
print(f"Test shapes: X={X_test.shape}, y={y_test.shape}")

# Sauvegarde
print("Sauvegarde des fichiers...")
X_train.to_csv(os.path.join(output_dir, 'X_train.csv'), index=False)
y_train.to_csv(os.path.join(output_dir, 'y_train.csv'), index=False)

X_val.to_csv(os.path.join(output_dir, 'X_val.csv'), index=False)
y_val.to_csv(os.path.join(output_dir, 'y_val.csv'), index=False)

X_test.to_csv(os.path.join(output_dir, 'X_test.csv'), index=False)
y_test.to_csv(os.path.join(output_dir, 'y_test.csv'), index=False)

print("Terminé.")
