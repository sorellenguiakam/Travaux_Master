import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score
import joblib
import os

# Configuration
DATA_PATH = '2_DONNEES/processed/dataset_clean.csv'
MODEL_DIR = '4_MODELES/models'
MODEL_PATH = os.path.join(MODEL_DIR, 'final_model.pkl')
FEATURES_PATH = os.path.join(MODEL_DIR, 'features.pkl')

FEATURES = ['age', 'IMC', 'glycemie_jeun', 'HbA1c', 'ANP32A_IT1', 'ESCO2', 'NBPF1']
TARGET = 'diagnostic'

def train():
    print("Chargement des données...")
    if not os.path.exists(DATA_PATH):
        print(f"Erreur: Le fichier {DATA_PATH} n'existe pas.")
        return

    df = pd.read_csv(DATA_PATH)
    
    # Vérification des colonnes
    missing_cols = [col for col in FEATURES if col not in df.columns]
    if missing_cols:
        print(f"Erreur: Colonnes manquantes dans le CSV : {missing_cols}")
        return

    X = df[FEATURES]
    y = df[TARGET]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Calcul scale_pos_weight pour déséquilibre
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

    # Configuration du modèle (inspiré du notebook Semaine 6)
    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        eval_metric='logloss',
        random_state=42,
        use_label_encoder=False
    )

    print("Entraînement du modèle XGBoost...")
    model.fit(X_train, y_train)

    # Évaluation rapide
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    print(f"Modèle entraîné. Accuracy: {acc:.2%}, Recall: {rec:.2%}")

    # Sauvegarde
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(FEATURES, FEATURES_PATH)
    print(f"Modèle sauvegardé dans : {MODEL_PATH}")
    print(f"Liste des features sauvegardée dans : {FEATURES_PATH}")

if __name__ == "__main__":
    train()
