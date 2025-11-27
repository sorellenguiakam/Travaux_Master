#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MODULE PREDICTION - PIPELINE DE PRÉDICTION SUR NOUVELLES DONNÉES
================================================================================

Ce module contient des fonctions pour charger un modèle sauvegardé et
effectuer des prédictions sur de nouvelles données (patients).

Auteur: Dr. TCHAPET NJAFA Jean-Pierre avec assistance Claude Code
Date: Novembre 2025
"""

import numpy as np
import pandas as pd
import joblib
import pickle
from pathlib import Path
import warnings


class PredicteurDT1:
    """
    Classe pour charger un modèle sauvegardé et effectuer des prédictions.
    """

    def __init__(self, dossier_modele='./models'):
        """
        Initialise le prédicteur en chargeant le modèle et les artefacts.

        Args:
            dossier_modele (str): Chemin vers le dossier contenant le modèle
        """
        self.dossier_modele = Path(dossier_modele)
        self.modele = None
        self.scaler = None
        self.feature_names = None

        self._charger_artefacts()

    def _charger_artefacts(self):
        """
        Charge le modèle, le scaler et les noms de features.
        """
        print("🔧 Chargement des artefacts du modèle...")

        # Charger le modèle
        chemin_modele_pkl = self.dossier_modele / 'final_model.pkl'
        chemin_modele_joblib = self.dossier_modele / 'final_model.joblib'

        if chemin_modele_pkl.exists():
            with open(chemin_modele_pkl, 'rb') as f:
                self.modele = pickle.load(f)
            print(f"✅ Modèle chargé: {chemin_modele_pkl}")
        elif chemin_modele_joblib.exists():
            self.modele = joblib.load(chemin_modele_joblib)
            print(f"✅ Modèle chargé: {chemin_modele_joblib}")
        else:
            raise FileNotFoundError(
                f"Aucun modèle trouvé dans {self.dossier_modele}. "
                "Vérifiez que 'final_model.pkl' ou 'final_model.joblib' existe."
            )

        # Charger le scaler (optionnel)
        chemin_scaler = self.dossier_modele / 'scaler.pkl'
        if chemin_scaler.exists():
            with open(chemin_scaler, 'rb') as f:
                self.scaler = pickle.load(f)
            print(f"✅ Scaler chargé: {chemin_scaler}")
        else:
            warnings.warn("Scaler non trouvé. Les données ne seront pas normalisées.")

        # Charger les noms de features
        chemin_features = self.dossier_modele / 'features.pkl'
        if chemin_features.exists():
            with open(chemin_features, 'rb') as f:
                self.feature_names = pickle.load(f)
            print(f"✅ Features chargées: {self.feature_names}")
        else:
            raise FileNotFoundError(
                f"Fichier features.pkl introuvable dans {self.dossier_modele}"
            )

    def preparer_donnees(self, data):
        """
        Prépare les données d'entrée pour la prédiction.

        Args:
            data (dict ou pd.DataFrame): Données du patient

        Returns:
            np.array: Données préparées pour le modèle
        """
        # Convertir en DataFrame si dict
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        elif isinstance(data, pd.DataFrame):
            data = data.copy()
        else:
            raise ValueError("data doit être un dict ou un DataFrame")

        # Vérifier que toutes les features requises sont présentes
        features_manquantes = [f for f in self.feature_names if f not in data.columns]
        if features_manquantes:
            raise ValueError(
                f"Features manquantes: {features_manquantes}. "
                f"Features requises: {self.feature_names}"
            )

        # Sélectionner les bonnes features dans le bon ordre
        X = data[self.feature_names].copy()

        # Normaliser si scaler disponible
        if self.scaler is not None:
            X = self.scaler.transform(X)

        return X

    def predire(self, data, retourner_proba=True):
        """
        Effectue une prédiction sur de nouvelles données.

        Args:
            data (dict ou pd.DataFrame): Données du patient
            retourner_proba (bool): Retourner les probabilités en plus

        Returns:
            dict: Résultat de la prédiction
        """
        # Préparer les données
        X = self.preparer_donnees(data)

        # Prédiction
        y_pred = self.modele.predict(X)

        # Probabilités
        y_proba = None
        if retourner_proba and hasattr(self.modele, 'predict_proba'):
            y_proba = self.modele.predict_proba(X)[:, 1]

        # Formater le résultat
        resultats = []
        for i in range(len(y_pred)):
            resultat = {
                'prediction': 'DT1+' if y_pred[i] == 1 else 'Sain',
                'classe_predite': int(y_pred[i]),
                'interpretation': self._interpreter_prediction(y_pred[i], y_proba[i] if y_proba is not None else None)
            }

            if y_proba is not None:
                resultat['probabilite_DT1'] = float(y_proba[i])
                resultat['probabilite_Sain'] = float(1 - y_proba[i])
                resultat['confiance'] = self._evaluer_confiance(y_proba[i])

            resultats.append(resultat)

        # Retourner un seul résultat si une seule prédiction
        if len(resultats) == 1:
            return resultats[0]

        return resultats

    def _interpreter_prediction(self, classe, proba=None):
        """
        Génère une interprétation textuelle de la prédiction.

        Args:
            classe (int): Classe prédite (0 ou 1)
            proba (float): Probabilité de DT1+

        Returns:
            str: Interprétation
        """
        if classe == 0:
            if proba is not None and proba < 0.1:
                return "Patient probablement sain. Risque de DT1 très faible."
            elif proba is not None and proba < 0.3:
                return "Patient sain avec faible risque de DT1. Surveillance de routine."
            else:
                return "Patient classé sain, mais surveiller les biomarqueurs."
        else:  # classe == 1
            if proba is not None and proba > 0.9:
                return "⚠️ RISQUE ÉLEVÉ DE DT1. Consultation endocrinologue URGENTE recommandée."
            elif proba is not None and proba > 0.7:
                return "⚠️ Risque modéré à élevé de DT1. Tests complémentaires recommandés."
            else:
                return "⚠️ Risque possible de DT1. Surveillance rapprochée recommandée."

    def _evaluer_confiance(self, proba):
        """
        Évalue le niveau de confiance de la prédiction.

        Args:
            proba (float): Probabilité de la classe positive

        Returns:
            str: Niveau de confiance
        """
        # Distance à la décision (0.5)
        distance = abs(proba - 0.5)

        if distance > 0.4:
            return "Très élevée"
        elif distance > 0.3:
            return "Élevée"
        elif distance > 0.2:
            return "Modérée"
        elif distance > 0.1:
            return "Faible"
        else:
            return "Très faible (incertain)"

    def predire_batch(self, fichier_csv, colonne_id='patient_id'):
        """
        Effectue des prédictions sur un fichier CSV de patients.

        Args:
            fichier_csv (str): Chemin vers le fichier CSV
            colonne_id (str): Nom de la colonne identifiant

        Returns:
            pd.DataFrame: DataFrame avec prédictions ajoutées
        """
        print(f"📊 Chargement des données: {fichier_csv}")
        df = pd.read_csv(fichier_csv)

        print(f"✅ {len(df)} patients chargés")

        # Effectuer les prédictions
        print("🔮 Prédictions en cours...")
        resultats = self.predire(df, retourner_proba=True)

        # Ajouter les résultats au DataFrame
        df['prediction'] = [r['prediction'] for r in resultats]
        df['classe_predite'] = [r['classe_predite'] for r in resultats]
        df['probabilite_DT1'] = [r['probabilite_DT1'] for r in resultats]
        df['confiance'] = [r['confiance'] for r in resultats]
        df['interpretation'] = [r['interpretation'] for r in resultats]

        print(f"✅ Prédictions terminées!")
        print(f"\n📊 Résumé:")
        print(df['prediction'].value_counts())

        return df

    def generer_rapport_patient(self, data, sauvegarder=None):
        """
        Génère un rapport détaillé pour un patient.

        Args:
            data (dict): Données du patient
            sauvegarder (str): Chemin pour sauvegarder le rapport (optionnel)

        Returns:
            str: Rapport formaté
        """
        # Effectuer la prédiction
        resultat = self.predire(data, retourner_proba=True)

        # Construire le rapport
        rapport = []
        rapport.append("=" * 80)
        rapport.append("RAPPORT DE PRÉDICTION - DÉTECTION PRÉCOCE DT1")
        rapport.append("=" * 80)
        rapport.append("")

        # Données du patient
        rapport.append("📋 DONNÉES DU PATIENT:")
        rapport.append("-" * 80)
        for feature in self.feature_names:
            if feature in data:
                rapport.append(f"  {feature}: {data[feature]}")
        rapport.append("")

        # Résultat de la prédiction
        rapport.append("🔮 RÉSULTAT DE LA PRÉDICTION:")
        rapport.append("-" * 80)
        rapport.append(f"  Diagnostic prédit: {resultat['prediction']}")

        if 'probabilite_DT1' in resultat:
            rapport.append(f"  Probabilité DT1+:  {resultat['probabilite_DT1']:.1%}")
            rapport.append(f"  Probabilité Sain:  {resultat['probabilite_Sain']:.1%}")
            rapport.append(f"  Confiance:         {resultat['confiance']}")

        rapport.append("")
        rapport.append("💡 INTERPRÉTATION:")
        rapport.append("-" * 80)
        rapport.append(f"  {resultat['interpretation']}")
        rapport.append("")

        # Avertissements
        rapport.append("⚠️ AVERTISSEMENTS IMPORTANTS:")
        rapport.append("-" * 80)
        rapport.append("  1. Cet outil est une AIDE au diagnostic, pas un remplacement")
        rapport.append("     de l'expertise médicale d'un endocrinologue.")
        rapport.append("  2. Ce modèle a été entraîné sur des données synthétiques.")
        rapport.append("  3. Une consultation médicale complète est INDISPENSABLE.")
        rapport.append("  4. Ne jamais prendre de décision thérapeutique basée")
        rapport.append("     uniquement sur ce résultat.")
        rapport.append("")
        rapport.append("=" * 80)

        rapport_texte = "\n".join(rapport)

        # Afficher
        print(rapport_texte)

        # Sauvegarder si demandé
        if sauvegarder:
            with open(sauvegarder, 'w', encoding='utf-8') as f:
                f.write(rapport_texte)
            print(f"\n✅ Rapport sauvegardé: {sauvegarder}")

        return rapport_texte


def exemple_utilisation():
    """
    Exemple d'utilisation du prédicteur.
    """
    print("=" * 80)
    print("EXEMPLE D'UTILISATION DU PRÉDICTEUR DT1")
    print("=" * 80)

    # Créer des données de test
    patient_test = {
        'age': 28,
        'sexe': 1,  # 1=Homme, 0=Femme
        'IMC': 24.5,
        'glycemie_jeun': 7.8,  # mmol/L (élevé)
        'ANP32A_IT1': 4.2,  # Biomarqueur élevé
        'ESCO2': 3.8,
        'NBPF1': 3.5,
        'antecedents_familiaux': 1,  # Oui
        'ethnie': 2  # Encodé
    }

    print("\n📋 Données du patient test:")
    for key, val in patient_test.items():
        print(f"  {key}: {val}")

    try:
        # Initialiser le prédicteur
        print("\n🔧 Initialisation du prédicteur...")
        predicteur = PredicteurDT1(dossier_modele='./models')

        # Effectuer la prédiction
        print("\n🔮 Prédiction en cours...")
        resultat = predicteur.predire(patient_test, retourner_proba=True)

        print("\n✅ Prédiction réussie!")
        print(f"\n📊 Résultat:")
        for key, val in resultat.items():
            print(f"  {key}: {val}")

        # Générer le rapport complet
        print("\n📄 Génération du rapport...")
        predicteur.generer_rapport_patient(patient_test)

    except FileNotFoundError as e:
        print(f"\n⚠️ Erreur: {e}")
        print("\nℹ️ Le modèle n'est pas encore entraîné.")
        print("   Exécutez d'abord: python pipeline_complet.py")


if __name__ == '__main__':
    """Point d'entrée pour tests."""

    exemple_utilisation()
