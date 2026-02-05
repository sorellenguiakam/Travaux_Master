import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, roc_curve)

import joblib

# Ensure output directory exists
output_dir = '../5_RAPPORTS/figures'
model_dir = '../2_DONNEES/models'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(model_dir, exist_ok=True)

# Load data
print("Loading data...")
try:
    df = pd.read_csv('../2_DONNEES/processed/dataset_clean.csv')
    print("Data loaded successfully.")
except FileNotFoundError:
    print("Error: Dataset not found at ../2_DONNEES/processed/dataset_clean.csv")
    exit(1)

features = ['age', 'IMC', 'glycemie_jeun', 'HbA1c', 'ANP32A_IT1', 'ESCO2', 'NBPF1']
X = df[features]
y = df['diagnostic']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")

# 1. XGBoost Base
print("Training XGBoost Base...")
xgb_base = XGBClassifier(
    n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric='logloss'
)
xgb_base.fit(X_train, y_train)
y_pred_xgb = xgb_base.predict(X_test)
y_proba_xgb = xgb_base.predict_proba(X_test)[:, 1]

# 2. XGBoost Balanced
print("Training XGBoost Balanced...")
n_neg = (y_train == 0).sum()
n_pos = (y_train == 1).sum()
scale_pos_weight = n_neg / n_pos

xgb_balanced = XGBClassifier(
    n_estimators=100, max_depth=6, learning_rate=0.1,
    scale_pos_weight=scale_pos_weight, random_state=42, eval_metric='logloss'
)
xgb_balanced.fit(X_train, y_train)
y_pred_xgb_bal = xgb_balanced.predict(X_test)
y_proba_xgb_bal = xgb_balanced.predict_proba(X_test)[:, 1]

# 3. LightGBM
print("Training LightGBM...")
lgbm = LGBMClassifier(
    n_estimators=100, max_depth=6, learning_rate=0.1,
    class_weight='balanced', random_state=42, verbose=-1
)
lgbm.fit(X_train, y_train)
y_pred_lgbm = lgbm.predict(X_test)
y_proba_lgbm = lgbm.predict_proba(X_test)[:, 1]

# 4. RF + SMOTE
print("Training RF + SMOTE...")
smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

rf_smote = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf_smote.fit(X_train_sm, y_train_sm)
y_pred_rf_smote = rf_smote.predict(X_test)
y_proba_rf_smote = rf_smote.predict_proba(X_test)[:, 1]

# Metrics Collection
models = [
    ('XGBoost base', y_pred_xgb, y_proba_xgb),
    ('XGBoost balanced', y_pred_xgb_bal, y_proba_xgb_bal),
    ('LightGBM', y_pred_lgbm, y_proba_lgbm),
    ('RF + SMOTE', y_pred_rf_smote, y_proba_rf_smote)
]

metrics_data = []
for name, y_pred, y_proba in models:
    metrics_data.append({
        'Modèle': name,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'F1-score': f1_score(y_test, y_pred),
        'AUC-ROC': roc_auc_score(y_test, y_proba)
    })

results_df = pd.DataFrame(metrics_data)

# Plots
plt.style.use('seaborn-v0_8-darkgrid')

# 1. Comparison Bar Chart
print("Generating Comparison Plot...")
fig, ax = plt.subplots(figsize=(12, 6))
metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1-score']
x = np.arange(len(metrics_to_plot))
width = 0.2

for i, row in results_df.iterrows():
    ax.bar(x + i*width, row[metrics_to_plot], width, label=row['Modèle'], alpha=0.8)

ax.set_xlabel('Métrique', fontsize=12)
ax.set_ylabel('Score', fontsize=12)
ax.set_title('Comparaison des modèles avancés (Semaine 4)', fontsize=14, fontweight='bold')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(metrics_to_plot)
ax.legend(loc='lower right')
ax.set_ylim(0, 1.1)
plt.savefig(f'{output_dir}/week4_comparaison_modeles.png', bbox_inches='tight', dpi=300)
plt.close()

# 2. ROC Curves
print("Generating ROC Curve Plot...")
plt.figure(figsize=(10, 8))
for name, _, y_proba in models:
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.plot(fpr, tpr, linewidth=2, label=f'{name}')

plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Hasard')
plt.xlabel('Taux de Faux Positifs', fontsize=12)
plt.ylabel('Taux de Vrais Positifs', fontsize=12)
plt.title('Courbes ROC - Modèles Avancés', fontsize=14, fontweight='bold')
plt.legend(loc='lower right')
plt.grid(alpha=0.3)
plt.savefig(f'{output_dir}/week4_roc_curves.png', bbox_inches='tight', dpi=300)
plt.close()

# 3. Feature Importance (XGBoost Balanced)
print("Generating Feature Importance Plot...")
importances = xgb_balanced.feature_importances_
feature_imp_df = pd.DataFrame({
    'Feature': features,
    'Importance': importances
}).sort_values('Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_imp_df, palette='viridis')
plt.title('Importance des variables (XGBoost Balanced)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{output_dir}/week4_feature_importance.png', bbox_inches='tight', dpi=300)
plt.close()

# 4. Save best models
print("Saving models...")
joblib.dump(xgb_balanced, f'{model_dir}/xgboost_balanced.joblib')
joblib.dump(rf_smote, f'{model_dir}/rf_smote.joblib')
joblib.dump(lgbm, f'{model_dir}/lightgbm.joblib')

print(f"Figures generated successfully in {output_dir}")
print(f"Models saved successfully in {model_dir}")
print(results_df)
