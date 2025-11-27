#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PIPELINE COMPLET - DÉTECTION PRÉCOCE DU DIABÈTE DE TYPE 1 (DT1) AU CAMEROUN
================================================================================

Ce script implémente le pipeline machine learning complet pour la détection
précoce du DT1 en utilisant des biomarqueurs génétiques (ANP32A-IT1, ESCO2,
NBPF1) et des facteurs cliniques dans le contexte camerounais.

PRIORITÉ MÉDICALE: Maximiser le Recall (sensibilité) pour minimiser les
faux négatifs, car manquer un patient DT1+ est plus grave qu'un faux positif.

Auteur: Dr. TCHAPET NJAFA Jean-Pierre avec assistance Claude Code
Date: Novembre 2025
Version: 1.0
"""

# ============================================================================
# IMPORTS
# ============================================================================
import os
import sys
import logging
import warnings
from pathlib import Path
from datetime import datetime
import argparse

# Data manipulation
import numpy as np
import pandas as pd
from scipy import stats

# Machine Learning
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

# Modèles ML
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb
import lightgbm as lgb

# Gestion du déséquilibre des classes
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

# Métriques d'évaluation
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report, roc_curve, auc
)

# Visualisation
import matplotlib.pyplot as plt
import seaborn as sns

# Interprétabilité
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    warnings.warn("SHAP non installé. Analyses d'interprétabilité désactivées.")

# Configuration
import yaml

# Sauvegarde modèles
import joblib
import pickle

# ============================================================================
# CONFIGURATION DU LOGGING
# ============================================================================
def setup_logging(log_dir='./logs', verbose=True):
    """
    Configure le système de logging pour le pipeline.

    Args:
        log_dir (str): Répertoire de sauvegarde des logs
        verbose (bool): Activer logs détaillés

    Returns:
        logger: Logger configuré
    """
    # Créer le répertoire de logs s'il n'existe pas
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Nom du fichier log avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(log_dir) / f"pipeline_{timestamp}.log"

    # Configuration du logger
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger('DT1_Pipeline')
    logger.info("=" * 80)
    logger.info("PIPELINE ML - DÉTECTION DT1 AU CAMEROUN")
    logger.info("=" * 80)

    return logger


# ============================================================================
# CHARGEMENT DE LA CONFIGURATION
# ============================================================================
def charger_configuration(config_path='config.yaml'):
    """
    Charge le fichier de configuration YAML.

    Args:
        config_path (str): Chemin vers config.yaml

    Returns:
        dict: Configuration chargée
    """
    logger = logging.getLogger('DT1_Pipeline')

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info(f"✅ Configuration chargée depuis {config_path}")
        logger.info(f"Version configuration: {config['version']['config']}")
        return config

    except FileNotFoundError:
        logger.error(f"❌ Fichier de configuration introuvable: {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"❌ Erreur de parsing YAML: {e}")
        sys.exit(1)


# ============================================================================
# CHARGEMENT ET PRÉTRAITEMENT DES DONNÉES
# ============================================================================
class PreprocesseurDonnees:
    """
    Classe pour gérer le prétraitement des données.
    Gère les valeurs manquantes, la normalisation, l'encodage et l'équilibrage.
    """

    def __init__(self, config):
        """
        Initialise le préprocesseur avec la configuration.

        Args:
            config (dict): Configuration du preprocessing
        """
        self.config = config
        self.logger = logging.getLogger('DT1_Pipeline.Preprocesseur')

        # Initialiser les transformateurs
        self.scaler = None
        self.imputer = None
        self.label_encoders = {}
        self.feature_names = None

    def charger_donnees(self, data_path):
        """
        Charge les données brutes depuis CSV.

        Args:
            data_path (str): Chemin vers le fichier CSV

        Returns:
            pd.DataFrame: Données chargées
        """
        try:
            df = pd.read_csv(data_path)
            self.logger.info(f"✅ Données chargées: {df.shape[0]} lignes, {df.shape[1]} colonnes")
            self.logger.info(f"Colonnes: {list(df.columns)}")
            return df

        except FileNotFoundError:
            self.logger.error(f"❌ Fichier de données introuvable: {data_path}")
            raise
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du chargement des données: {e}")
            raise

    def analyser_donnees(self, df):
        """
        Analyse exploratoire rapide des données.

        Args:
            df (pd.DataFrame): Données à analyser
        """
        self.logger.info("=" * 60)
        self.logger.info("ANALYSE EXPLORATOIRE DES DONNÉES")
        self.logger.info("=" * 60)

        # Statistiques descriptives
        self.logger.info(f"\n📊 Statistiques descriptives:\n{df.describe()}")

        # Valeurs manquantes
        valeurs_manquantes = df.isnull().sum()
        if valeurs_manquantes.sum() > 0:
            self.logger.warning(f"\n⚠️ Valeurs manquantes:\n{valeurs_manquantes[valeurs_manquantes > 0]}")
        else:
            self.logger.info("✅ Aucune valeur manquante détectée")

        # Distribution de la variable cible
        cible = self.config['features']['cible']
        if cible in df.columns:
            distribution = df[cible].value_counts()
            self.logger.info(f"\n🎯 Distribution de la variable cible '{cible}':\n{distribution}")

            # Calculer le ratio de déséquilibre
            ratio = distribution.min() / distribution.max()
            if ratio < 0.5:
                self.logger.warning(f"⚠️ Déséquilibre détecté (ratio: {ratio:.2f}). SMOTE sera appliqué.")
            else:
                self.logger.info(f"✅ Classes relativement équilibrées (ratio: {ratio:.2f})")

    def preparer_features(self, df):
        """
        Prépare les features et la variable cible.

        Args:
            df (pd.DataFrame): Données brutes

        Returns:
            tuple: (X, y, feature_names)
        """
        # Extraire les features depuis la configuration
        features_config = self.config['features']

        # Construire la liste de toutes les features
        all_features = []
        all_features.extend(features_config['biomarqueurs'])
        all_features.extend(features_config['cliniques'])
        all_features.extend(features_config['genetiques'])

        # Filtrer les features présentes dans le dataframe
        features_disponibles = [f for f in all_features if f in df.columns]
        features_manquantes = [f for f in all_features if f not in df.columns]

        if features_manquantes:
            self.logger.warning(f"⚠️ Features manquantes: {features_manquantes}")

        self.logger.info(f"✅ Features utilisées: {features_disponibles}")

        # Extraire X et y
        cible = features_config['cible']
        X = df[features_disponibles].copy()
        y = df[cible].copy()

        self.feature_names = features_disponibles

        return X, y, features_disponibles

    def gerer_valeurs_manquantes(self, X):
        """
        Gère les valeurs manquantes selon la stratégie configurée.

        Args:
            X (pd.DataFrame): Features avec possibles valeurs manquantes

        Returns:
            pd.DataFrame: Features sans valeurs manquantes
        """
        strategie = self.config['preprocessing']['gestion_valeurs_manquantes']

        if X.isnull().sum().sum() == 0:
            self.logger.info("✅ Aucune valeur manquante à traiter")
            return X

        self.logger.info(f"🔧 Gestion des valeurs manquantes: stratégie '{strategie}'")

        if strategie == 'drop':
            X_clean = X.dropna()
            lignes_supprimees = len(X) - len(X_clean)
            self.logger.info(f"Lignes supprimées: {lignes_supprimees}")
            return X_clean

        else:  # median ou mean
            self.imputer = SimpleImputer(strategy=strategie)
            X_imputed = self.imputer.fit_transform(X)
            X_clean = pd.DataFrame(X_imputed, columns=X.columns, index=X.index)
            self.logger.info(f"✅ Valeurs manquantes imputées avec stratégie '{strategie}'")
            return X_clean

    def normaliser_features(self, X_train, X_test):
        """
        Normalise les features numériques avec StandardScaler.

        Args:
            X_train (pd.DataFrame): Features d'entraînement
            X_test (pd.DataFrame): Features de test

        Returns:
            tuple: (X_train_scaled, X_test_scaled)
        """
        if not self.config['preprocessing']['normalisation']:
            self.logger.info("⏭️ Normalisation désactivée")
            return X_train, X_test

        self.logger.info("🔧 Normalisation des features avec StandardScaler")

        # Fit sur train, transform sur train et test
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Convertir en DataFrames
        X_train_scaled = pd.DataFrame(
            X_train_scaled,
            columns=X_train.columns,
            index=X_train.index
        )
        X_test_scaled = pd.DataFrame(
            X_test_scaled,
            columns=X_test.columns,
            index=X_test.index
        )

        self.logger.info("✅ Normalisation terminée")
        return X_train_scaled, X_test_scaled

    def equilibrer_classes(self, X_train, y_train):
        """
        Équilibre les classes avec SMOTE si activé.

        Args:
            X_train (pd.DataFrame): Features d'entraînement
            y_train (pd.Series): Labels d'entraînement

        Returns:
            tuple: (X_train_balanced, y_train_balanced)
        """
        if not self.config['preprocessing']['equilibrage_classes']:
            self.logger.info("⏭️ Équilibrage des classes désactivé")
            return X_train, y_train

        # Vérifier le déséquilibre
        distribution_avant = pd.Series(y_train).value_counts()
        self.logger.info(f"Distribution avant SMOTE:\n{distribution_avant}")

        ratio = self.config['preprocessing']['smote_ratio']
        self.logger.info(f"🔧 Application de SMOTE (sampling_strategy={ratio})")

        try:
            smote = SMOTE(
                sampling_strategy=ratio,
                random_state=self.config['preprocessing']['random_state']
            )
            X_balanced, y_balanced = smote.fit_resample(X_train, y_train)

            distribution_apres = pd.Series(y_balanced).value_counts()
            self.logger.info(f"Distribution après SMOTE:\n{distribution_apres}")
            self.logger.info("✅ Équilibrage terminé")

            return X_balanced, y_balanced

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'application de SMOTE: {e}")
            self.logger.warning("⚠️ Utilisation des données déséquilibrées")
            return X_train, y_train


# ============================================================================
# ENTRAÎNEMENT DES MODÈLES
# ============================================================================
class GestionnaireModeles:
    """
    Classe pour gérer l'entraînement et l'évaluation de plusieurs modèles ML.
    """

    def __init__(self, config):
        """
        Initialise le gestionnaire avec la configuration.

        Args:
            config (dict): Configuration des modèles
        """
        self.config = config
        self.logger = logging.getLogger('DT1_Pipeline.Modeles')
        self.modeles = {}
        self.resultats = {}
        self.meilleur_modele = None
        self.meilleur_score = 0

    def initialiser_modeles(self):
        """
        Initialise tous les modèles actifs depuis la configuration.
        """
        self.logger.info("=" * 60)
        self.logger.info("INITIALISATION DES MODÈLES ML")
        self.logger.info("=" * 60)

        config_modeles = self.config['modeles']

        # Régression Logistique
        if config_modeles['logistic_regression']['actif']:
            params = config_modeles['logistic_regression']['params']
            self.modeles['Logistic Regression'] = LogisticRegression(**params)
            self.logger.info("✅ Logistic Regression initialisée")

        # Random Forest
        if config_modeles['random_forest']['actif']:
            params = config_modeles['random_forest']['params']
            self.modeles['Random Forest'] = RandomForestClassifier(**params)
            self.logger.info("✅ Random Forest initialisé")

        # XGBoost
        if config_modeles['xgboost']['actif']:
            params = config_modeles['xgboost']['params']
            self.modeles['XGBoost'] = xgb.XGBClassifier(**params)
            self.logger.info("✅ XGBoost initialisé")

        # LightGBM
        if config_modeles['lightgbm']['actif']:
            params = config_modeles['lightgbm']['params']
            self.modeles['LightGBM'] = lgb.LGBMClassifier(**params)
            self.logger.info("✅ LightGBM initialisé")

        # SVM
        if config_modeles['svm']['actif']:
            params = config_modeles['svm']['params']
            self.modeles['SVM'] = SVC(probability=True, **params)
            self.logger.info("✅ SVM initialisé")

        # K-Nearest Neighbors
        if config_modeles['knn']['actif']:
            params = config_modeles['knn']['params']
            self.modeles['KNN'] = KNeighborsClassifier(**params)
            self.logger.info("✅ KNN initialisé")

        self.logger.info(f"\n📊 Total: {len(self.modeles)} modèles actifs")

    def entrainer_modeles(self, X_train, y_train, X_test, y_test):
        """
        Entraîne tous les modèles et évalue leurs performances.

        Args:
            X_train: Features d'entraînement
            y_train: Labels d'entraînement
            X_test: Features de test
            y_test: Labels de test
        """
        self.logger.info("=" * 60)
        self.logger.info("ENTRAÎNEMENT DES MODÈLES")
        self.logger.info("=" * 60)

        for nom_modele, modele in self.modeles.items():
            self.logger.info(f"\n🚀 Entraînement: {nom_modele}")

            try:
                # Entraînement
                debut = datetime.now()
                modele.fit(X_train, y_train)
                duree = (datetime.now() - debut).total_seconds()

                # Prédictions
                y_pred_train = modele.predict(X_train)
                y_pred_test = modele.predict(X_test)
                y_proba_test = modele.predict_proba(X_test)[:, 1]

                # Calculer les métriques
                metriques = self.calculer_metriques(y_test, y_pred_test, y_proba_test)
                metriques['duree_entrainement'] = duree
                metriques['accuracy_train'] = accuracy_score(y_train, y_pred_train)

                # Sauvegarder les résultats
                self.resultats[nom_modele] = {
                    'modele': modele,
                    'metriques': metriques,
                    'y_pred': y_pred_test,
                    'y_proba': y_proba_test
                }

                # Afficher les résultats
                self.afficher_resultats(nom_modele, metriques)

                # Vérifier si c'est le meilleur modèle (selon Recall)
                critere = self.config['sauvegarde']['critere_meilleur']
                score = metriques[critere]

                if score > self.meilleur_score:
                    self.meilleur_score = score
                    self.meilleur_modele = nom_modele
                    self.logger.info(f"🏆 Nouveau meilleur modèle! ({critere}={score:.4f})")

            except Exception as e:
                self.logger.error(f"❌ Erreur lors de l'entraînement de {nom_modele}: {e}")
                continue

        self.logger.info("\n" + "=" * 60)
        self.logger.info(f"🏆 MEILLEUR MODÈLE: {self.meilleur_modele}")
        self.logger.info(f"Score ({self.config['sauvegarde']['critere_meilleur']}): {self.meilleur_score:.4f}")
        self.logger.info("=" * 60)

    def calculer_metriques(self, y_true, y_pred, y_proba):
        """
        Calcule toutes les métriques d'évaluation.

        Args:
            y_true: Vraies étiquettes
            y_pred: Prédictions
            y_proba: Probabilités de prédiction

        Returns:
            dict: Métriques calculées
        """
        metriques = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_true, y_proba) if len(np.unique(y_true)) > 1 else 0.0
        }

        return metriques

    def afficher_resultats(self, nom_modele, metriques):
        """
        Affiche les résultats d'un modèle de manière formatée.

        Args:
            nom_modele (str): Nom du modèle
            metriques (dict): Métriques du modèle
        """
        self.logger.info(f"\n📊 Résultats {nom_modele}:")
        self.logger.info(f"  - Accuracy:  {metriques['accuracy']:.4f}")
        self.logger.info(f"  - Precision: {metriques['precision']:.4f}")
        self.logger.info(f"  - Recall:    {metriques['recall']:.4f} ⭐ (prioritaire)")
        self.logger.info(f"  - F1-Score:  {metriques['f1_score']:.4f}")
        self.logger.info(f"  - ROC-AUC:   {metriques['roc_auc']:.4f}")
        self.logger.info(f"  - Durée:     {metriques['duree_entrainement']:.2f}s")

        # Vérifier les seuils minimaux
        seuils = self.config['evaluation']['seuils']
        if metriques['recall'] < seuils['recall_minimum']:
            self.logger.warning(f"  ⚠️ Recall inférieur au seuil minimal ({seuils['recall_minimum']})")
        if metriques['accuracy'] < seuils['accuracy_minimum']:
            self.logger.warning(f"  ⚠️ Accuracy inférieure au seuil minimal ({seuils['accuracy_minimum']})")


# ============================================================================
# VISUALISATIONS
# ============================================================================
class GenerateurVisualisations:
    """
    Classe pour générer toutes les visualisations du projet.
    """

    def __init__(self, config):
        """
        Initialise le générateur avec la configuration.

        Args:
            config (dict): Configuration des visualisations
        """
        self.config = config
        self.logger = logging.getLogger('DT1_Pipeline.Visualisations')

        # Configuration matplotlib
        plt.style.use(config['visualisations']['style'])
        self.dpi = config['visualisations']['dpi']
        self.format_fig = config['visualisations']['format_figures']

        # Créer le dossier de figures
        self.dossier_figures = Path(config['donnees']['dossier_figures'])
        self.dossier_figures.mkdir(parents=True, exist_ok=True)

    def generer_toutes_visualisations(self, gestionnaire_modeles, X_test, y_test, feature_names):
        """
        Génère toutes les visualisations configurées.

        Args:
            gestionnaire_modeles: Gestionnaire de modèles avec résultats
            X_test: Features de test
            y_test: Labels de test
            feature_names: Noms des features
        """
        self.logger.info("=" * 60)
        self.logger.info("GÉNÉRATION DES VISUALISATIONS")
        self.logger.info("=" * 60)

        figures_a_generer = self.config['visualisations']['figures_a_generer']

        if 'matrice_confusion' in figures_a_generer:
            self.generer_matrices_confusion(gestionnaire_modeles, y_test)

        if 'courbe_roc' in figures_a_generer:
            self.generer_courbes_roc(gestionnaire_modeles, y_test)

        if 'importance_features' in figures_a_generer:
            self.generer_importance_features(gestionnaire_modeles, feature_names)

        self.logger.info(f"✅ Visualisations sauvegardées dans {self.dossier_figures}")

    def generer_matrices_confusion(self, gestionnaire_modeles, y_test):
        """
        Génère les matrices de confusion pour tous les modèles.

        Args:
            gestionnaire_modeles: Gestionnaire de modèles
            y_test: Labels de test
        """
        self.logger.info("📊 Génération des matrices de confusion...")

        n_modeles = len(gestionnaire_modeles.resultats)
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()

        for idx, (nom_modele, resultats) in enumerate(gestionnaire_modeles.resultats.items()):
            if idx >= len(axes):
                break

            y_pred = resultats['y_pred']
            cm = confusion_matrix(y_test, y_pred)

            sns.heatmap(
                cm,
                annot=True,
                fmt='d',
                cmap='Blues',
                ax=axes[idx],
                xticklabels=['Sain', 'DT1+'],
                yticklabels=['Sain', 'DT1+']
            )
            axes[idx].set_title(f'{nom_modele}\nRecall={resultats["metriques"]["recall"]:.3f}')
            axes[idx].set_ylabel('Vraie Classe')
            axes[idx].set_xlabel('Classe Prédite')

        # Masquer les axes non utilisés
        for idx in range(len(gestionnaire_modeles.resultats), len(axes)):
            axes[idx].axis('off')

        plt.tight_layout()
        chemin = self.dossier_figures / f'matrices_confusion.{self.format_fig}'
        plt.savefig(chemin, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        self.logger.info(f"  ✅ Matrices de confusion sauvegardées: {chemin}")

    def generer_courbes_roc(self, gestionnaire_modeles, y_test):
        """
        Génère les courbes ROC pour tous les modèles.

        Args:
            gestionnaire_modeles: Gestionnaire de modèles
            y_test: Labels de test
        """
        self.logger.info("📊 Génération des courbes ROC...")

        plt.figure(figsize=(10, 8))

        for nom_modele, resultats in gestionnaire_modeles.resultats.items():
            y_proba = resultats['y_proba']
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            auc_score = auc(fpr, tpr)

            plt.plot(fpr, tpr, label=f'{nom_modele} (AUC={auc_score:.3f})', linewidth=2)

        # Ligne diagonale de référence
        plt.plot([0, 1], [0, 1], 'k--', label='Chance (AUC=0.5)', linewidth=1)

        plt.xlabel('Taux de Faux Positifs (1 - Spécificité)', fontsize=12)
        plt.ylabel('Taux de Vrais Positifs (Sensibilité/Recall)', fontsize=12)
        plt.title('Courbes ROC - Comparaison des Modèles\nContexte Médical: Priorité au Recall', fontsize=14)
        plt.legend(loc='lower right')
        plt.grid(True, alpha=0.3)

        chemin = self.dossier_figures / f'courbes_roc.{self.format_fig}'
        plt.savefig(chemin, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        self.logger.info(f"  ✅ Courbes ROC sauvegardées: {chemin}")

    def generer_importance_features(self, gestionnaire_modeles, feature_names):
        """
        Génère les graphiques d'importance des features.

        Args:
            gestionnaire_modeles: Gestionnaire de modèles
            feature_names: Noms des features
        """
        self.logger.info("📊 Génération de l'importance des features...")

        # Sélectionner le meilleur modèle
        meilleur_nom = gestionnaire_modeles.meilleur_modele
        meilleur_modele = gestionnaire_modeles.resultats[meilleur_nom]['modele']

        # Extraire l'importance (si disponible)
        if hasattr(meilleur_modele, 'feature_importances_'):
            importances = meilleur_modele.feature_importances_
        elif hasattr(meilleur_modele, 'coef_'):
            importances = np.abs(meilleur_modele.coef_[0])
        else:
            self.logger.warning(f"  ⚠️ {meilleur_nom} ne supporte pas l'importance des features")
            return

        # Créer le graphique
        plt.figure(figsize=(10, 6))
        indices = np.argsort(importances)[::-1]

        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.xlabel('Features', fontsize=12)
        plt.ylabel('Importance', fontsize=12)
        plt.title(f'Importance des Features - {meilleur_nom}', fontsize=14)
        plt.tight_layout()

        chemin = self.dossier_figures / f'importance_features.{self.format_fig}'
        plt.savefig(chemin, dpi=self.dpi, bbox_inches='tight')
        plt.close()

        self.logger.info(f"  ✅ Importance des features sauvegardée: {chemin}")


# ============================================================================
# SAUVEGARDE DES MODÈLES
# ============================================================================
def sauvegarder_meilleur_modele(gestionnaire_modeles, preprocesseur, config):
    """
    Sauvegarde le meilleur modèle et les artefacts associés.

    Args:
        gestionnaire_modeles: Gestionnaire de modèles
        preprocesseur: Préprocesseur de données
        config: Configuration
    """
    logger = logging.getLogger('DT1_Pipeline')
    logger.info("=" * 60)
    logger.info("SAUVEGARDE DU MEILLEUR MODÈLE")
    logger.info("=" * 60)

    # Créer le dossier de sauvegarde
    dossier_modeles = Path(config['sauvegarde']['dossier_modeles'])
    dossier_modeles.mkdir(parents=True, exist_ok=True)

    # Récupérer le meilleur modèle
    meilleur_nom = gestionnaire_modeles.meilleur_modele
    meilleur_resultat = gestionnaire_modeles.resultats[meilleur_nom]
    meilleur_modele = meilleur_resultat['modele']
    metriques = meilleur_resultat['metriques']

    # Format de sauvegarde
    format_save = config['sauvegarde']['format']

    # Sauvegarder le modèle
    if format_save == 'pkl':
        chemin_modele = dossier_modeles / 'final_model.pkl'
        with open(chemin_modele, 'wb') as f:
            pickle.dump(meilleur_modele, f)
    else:  # joblib
        chemin_modele = dossier_modeles / 'final_model.joblib'
        joblib.dump(meilleur_modele, chemin_modele)

    logger.info(f"✅ Modèle sauvegardé: {chemin_modele}")

    # Sauvegarder le scaler
    if preprocesseur.scaler is not None:
        chemin_scaler = dossier_modeles / 'scaler.pkl'
        with open(chemin_scaler, 'wb') as f:
            pickle.dump(preprocesseur.scaler, f)
        logger.info(f"✅ Scaler sauvegardé: {chemin_scaler}")

    # Sauvegarder les noms de features
    chemin_features = dossier_modeles / 'features.pkl'
    with open(chemin_features, 'wb') as f:
        pickle.dump(preprocesseur.feature_names, f)
    logger.info(f"✅ Features sauvegardées: {chemin_features}")

    # Générer le rapport de performances
    chemin_rapport = dossier_modeles / 'rapport_modele_final.txt'
    with open(chemin_rapport, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RAPPORT DU MODÈLE FINAL - DÉTECTION PRÉCOCE DT1 AU CAMEROUN\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Modèle sélectionné: {meilleur_nom}\n")
        f.write(f"Critère de sélection: {config['sauvegarde']['critere_meilleur']}\n\n")
        f.write("PERFORMANCES SUR ENSEMBLE DE TEST:\n")
        f.write("-" * 80 + "\n")
        f.write(f"  - Accuracy:  {metriques['accuracy']:.4f}\n")
        f.write(f"  - Precision: {metriques['precision']:.4f}\n")
        f.write(f"  - Recall:    {metriques['recall']:.4f} ⭐ (métrique prioritaire)\n")
        f.write(f"  - F1-Score:  {metriques['f1_score']:.4f}\n")
        f.write(f"  - ROC-AUC:   {metriques['roc_auc']:.4f}\n\n")
        f.write("NOTES IMPORTANTES:\n")
        f.write("-" * 80 + "\n")
        f.write("1. CONTEXTE MÉDICAL: Le Recall (sensibilité) est prioritaire car manquer\n")
        f.write("   un patient DT1+ (faux négatif) est plus grave qu'un faux positif.\n\n")
        f.write("2. DONNÉES SYNTHÉTIQUES: Ce modèle a été entraîné sur des données\n")
        f.write("   synthétiques. Validation sur données réelles OBLIGATOIRE avant\n")
        f.write("   tout déploiement clinique.\n\n")
        f.write("3. ÉTHIQUE: Cet outil est une AIDE au diagnostic, pas un remplacement\n")
        f.write("   de l'expertise médicale.\n\n")
        f.write("=" * 80 + "\n")

    logger.info(f"✅ Rapport sauvegardé: {chemin_rapport}")
    logger.info("=" * 60)


# ============================================================================
# PIPELINE PRINCIPAL
# ============================================================================
def executer_pipeline(config_path='config.yaml'):
    """
    Exécute le pipeline ML complet.

    Args:
        config_path (str): Chemin vers le fichier de configuration
    """
    # 1. Configuration du logging
    logger = setup_logging(verbose=True)

    try:
        # 2. Chargement de la configuration
        config = charger_configuration(config_path)

        # 3. Prétraitement des données
        preprocesseur = PreprocesseurDonnees(config)

        # Charger les données
        data_path = config['donnees']['raw_data']
        df = preprocesseur.charger_donnees(data_path)

        # Analyse exploratoire
        preprocesseur.analyser_donnees(df)

        # Préparer features et cible
        X, y, feature_names = preprocesseur.preparer_features(df)

        # Gérer valeurs manquantes
        X = preprocesseur.gerer_valeurs_manquantes(X)

        # Split train/test
        test_size = config['preprocessing']['test_size']
        random_state = config['preprocessing']['random_state']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        logger.info(f"✅ Split train/test: {len(X_train)} / {len(X_test)} échantillons")

        # Normalisation
        X_train, X_test = preprocesseur.normaliser_features(X_train, X_test)

        # Équilibrage des classes
        X_train, y_train = preprocesseur.equilibrer_classes(X_train, y_train)

        # Sauvegarder les données prétraitées
        processed_path = config['donnees']['processed_data']
        Path(processed_path).parent.mkdir(parents=True, exist_ok=True)
        df_clean = pd.concat([X, y], axis=1)
        df_clean.to_csv(processed_path, index=False)
        logger.info(f"✅ Données prétraitées sauvegardées: {processed_path}")

        # 4. Entraînement des modèles
        gestionnaire = GestionnaireModeles(config)
        gestionnaire.initialiser_modeles()
        gestionnaire.entrainer_modeles(X_train, y_train, X_test, y_test)

        # 5. Visualisations
        visualisateur = GenerateurVisualisations(config)
        visualisateur.generer_toutes_visualisations(gestionnaire, X_test, y_test, feature_names)

        # 6. Sauvegarde du meilleur modèle
        if config['sauvegarde']['sauvegarder_meilleur_seulement']:
            sauvegarder_meilleur_modele(gestionnaire, preprocesseur, config)

        # 7. Résumé final
        logger.info("\n" + "=" * 80)
        logger.info("🎉 PIPELINE TERMINÉ AVEC SUCCÈS")
        logger.info("=" * 80)
        logger.info(f"🏆 Meilleur modèle: {gestionnaire.meilleur_modele}")
        logger.info(f"📊 Recall: {gestionnaire.meilleur_score:.4f}")
        logger.info(f"📁 Modèle sauvegardé dans: {config['sauvegarde']['dossier_modeles']}")
        logger.info(f"📊 Visualisations dans: {config['donnees']['dossier_figures']}")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"❌ ERREUR CRITIQUE: {e}")
        logger.exception("Détails de l'erreur:")
        sys.exit(1)


# ============================================================================
# POINT D'ENTRÉE
# ============================================================================
if __name__ == '__main__':
    # Parser les arguments
    parser = argparse.ArgumentParser(
        description='Pipeline ML pour détection précoce du Diabète de Type 1 au Cameroun'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Chemin vers le fichier de configuration YAML (défaut: config.yaml)'
    )

    args = parser.parse_args()

    # Exécuter le pipeline
    executer_pipeline(config_path=args.config)
