import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import shap
import os
from sklearn.model_selection import train_test_split

# Configuration
MODEL_PATH = '../2_DONNEES/models/xgboost_balanced.joblib'
DATA_PATH = '../2_DONNEES/processed/dataset_clean.csv'
OUTPUT_DIR = '../5_RAPPORTS/figures'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load Data
print("Loading data...")
df = pd.read_csv(DATA_PATH)
features = ['age', 'IMC', 'glycemie_jeun', 'HbA1c', 'ANP32A_IT1', 'ESCO2', 'NBPF1']
X = df[features]
y = df['diagnostic']

# Use same split as training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Data loaded: {len(X_test)} test samples")

# 2. Load Model
print(f"Loading model from {MODEL_PATH}...")
try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded: {type(model).__name__}")
    
    # Fix for SHAP issue with XGBoost 1.6+ where base_score might be a list or string
    # SHAP expects a float
    try:
        booster = model.get_booster()
        base_score = booster.save_config()
        # No easy way to modify config string, but we can set the attribute on the sklearn wrapper if SHAP uses that
        # Actually SHAP creates TreeEnsemble from booster.
        # Let's try to reload the model with specific parameters if possible or just use the booster directly
        model_byte = model.get_booster()
    except Exception as e:
        print(f"Warning during model inspection: {e}")

except FileNotFoundError:
    print(f"Error: Model not found at {MODEL_PATH}")
    exit(1)

# 3. Calculate SHAP Values
# 3. Calculate SHAP Values
print("Calculating SHAP values...")
shap_obj = None

try:
    print("Attempting TreeExplainer...")
    explainer = shap.TreeExplainer(model)
    # Try the modern API first
    shap_obj = explainer(X_test)
except Exception as e:
    print(f"TreeExplainer failed: {e}")
    print("Falling back to PermutationExplainer (model-agnostic)...")
    
    # Needs prediction function
    predictions = model.predict_proba
    # Background dataset
    background = shap.maskers.Independent(X_train, max_samples=100)
    explainer = shap.PermutationExplainer(predictions, background)
    
    # Calculate SHAP values
    shap_obj = explainer(X_test)

# Handle binary classification case
# shap_obj.values might be (samples, features, classes)
if len(shap_obj.shape) == 3:
    # We want the positive class (index 1) for plotting
    # But we need to keep the Explanation object structure
    shap_values = shap_obj.values[:, :, 1]
    # Creates a new Explanation object for just the positive class
    shap_explanation = shap.Explanation(
        values=shap_values,
        base_values=shap_obj.base_values[:, 1] if len(shap_obj.base_values.shape) > 1 else shap_obj.base_values,
        data=shap_obj.data,
        feature_names=features
    )
else:
    shap_explanation = shap_obj
    shap_values = shap_obj.values

print(f"SHAP values calculated. Shape: {shap_values.shape}")

# 4. Generate & Save Plots

# A. SHAP Summary Plot (Global Importance - Bar)
print("Generating Summary Plot (Bar)...")
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_test, plot_type="bar", show=False, feature_names=features)
plt.title('Importance Globale des Features (SHAP)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/week5_shap_importance.png', dpi=300, bbox_inches='tight')
plt.close()

# B. SHAP Beeswarm Plot (Global Impact)
print("Generating Beeswarm Plot...")
plt.figure(figsize=(10, 8))
shap.summary_plot(shap_values, X_test, show=False, feature_names=features)
plt.title('Impact des Features sur le Risque DT1', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/week5_shap_beeswarm.png', dpi=300, bbox_inches='tight')
plt.close()

# C. Local Explanation (Waterfall) for a Positive Patient (DT1)
y_pred = model.predict(X_test)
true_positives = np.where((y_test == 1) & (y_pred == 1))[0]

if len(true_positives) > 0:
    patient_idx = true_positives[0]
    print(f"Generating Waterfall Plot for Patient index {patient_idx}...")
    
    # Use the Explanation object directly
    plt.figure(figsize=(10, 6))
    shap.waterfall_plot(shap_explanation[patient_idx], show=False)
    plt.title(f'Explication Locale (Patient DT1 détecté)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/week5_shap_waterfall.png', dpi=300, bbox_inches='tight')
    plt.close()
else:
    print("Warning: No True Positive found in test set for Waterfall plot.")

# D. SHAP Dependence Plots
print("Generating SHAP Dependence Plots...")
top_features = ['glycemie_jeun', 'HbA1c', 'ESCO2']
for feature in top_features:
    if feature in features:
        plt.figure(figsize=(8, 6))
        shap.dependence_plot(feature, shap_values, X_test, show=False, feature_names=features)
        plt.title(f'SHAP Dependence: {feature}', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/week5_shap_dependence_{feature}.png', dpi=300, bbox_inches='tight')
        plt.close()

# 5. LIME Analysis
print("Generating LIME Explanation...")
try:
    import lime
    import lime.lime_tabular
    
    explainer_lime = lime.lime_tabular.LimeTabularExplainer(
        X_train.values,
        feature_names=features,
        class_names=['Sain', 'DT1'],
        mode='classification'
    )
    
    if len(true_positives) > 0:
        patient_idx = true_positives[0]
        # LIME expects a function that returns probabilities
        exp = explainer_lime.explain_instance(
            X_test.iloc[patient_idx].values,
            model.predict_proba,
            num_features=10
        )
        
        # Save LIME figure
        plt.figure(figsize=(10, 6))
        exp.as_pyplot_figure()
        plt.title(f'LIME Explanation for Patient {patient_idx}', fontsize=12, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/week5_lime_patient_explanation.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✅ LIME figure generated.")
        
except ImportError:
    print("⚠️ LIME not installed. Skipping LIME analysis.")
except Exception as e:
    print(f"⚠️ Error during LIME analysis: {e}")

# 6. Partial Dependence Plots (PDP)
print("Generating Partial Dependence Plots...")
from sklearn.inspection import PartialDependenceDisplay

features_to_plot = ['ESCO2', 'ANP32A_IT1', 'NBPF1', 'HbA1c']
# Check which features exist in dataset
valid_features = [f for f in features_to_plot if f in features]

if valid_features:
    fig, ax = plt.subplots(figsize=(12, 4 * ((len(valid_features) + 1) // 2)))
    display = PartialDependenceDisplay.from_estimator(
        model,
        X_test,
        valid_features,
        kind="average",
        ax=ax
    )
    plt.suptitle('Partial Dependence Plots', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/week5_partial_dependence.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ PDP figure generated.")


print(f"✅ All SHAP/LIME/PDP figures generated in {OUTPUT_DIR}")
