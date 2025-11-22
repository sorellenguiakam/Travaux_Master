#!/usr/bin/env python3
"""
Script de téléchargement automatique des articles scientifiques
Télécharge les articles Open Access gratuits pour le projet DT1 Cameroun
"""

import requests
import os
import time
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent / "PDF_references"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Liste des articles à télécharger (Open Access uniquement)
ARTICLES = [
    {
        'nom': 'Katte_2023_phenotype_T1D_Africa.pdf',
        'dossier': '1_DT1_Afrique',
        'url': 'https://www.frontiersin.org/articles/10.3389/fpubh.2023.1110013/pdf',
        'description': 'Phénotype du DT1 en Afrique subsaharienne'
    },
    {
        'nom': 'Zhang_2022_biomarkers_T1D.pdf',
        'dossier': '2_Biomarqueurs',
        'url': 'https://www.frontiersin.org/articles/10.3389/fgene.2022.942897/pdf',
        'description': 'Identification des biomarqueurs ANP32A-IT1, ESCO2, NBPF1'
    },
    {
        'nom': 'Lundberg_2017_SHAP.pdf',
        'dossier': '5_Interpretabilite',
        'url': 'https://arxiv.org/pdf/1705.07874.pdf',
        'description': 'SHAP - Unified Approach to Interpreting Model Predictions'
    },
    {
        'nom': 'Chen_2016_XGBoost.pdf',
        'dossier': '4_Algorithmes',
        'url': 'https://arxiv.org/pdf/1603.02754.pdf',
        'description': 'XGBoost: A Scalable Tree Boosting System'
    },
    {
        'nom': 'Ribeiro_2016_LIME.pdf',
        'dossier': '5_Interpretabilite',
        'url': 'https://arxiv.org/pdf/1602.04938.pdf',
        'description': 'LIME - Why Should I Trust You?'
    },
    {
        'nom': 'Chawla_2002_SMOTE.pdf',
        'dossier': '6_Methodologie',
        'url': 'https://arxiv.org/pdf/1106.1813.pdf',
        'description': 'SMOTE: Synthetic Minority Over-sampling Technique'
    },
    {
        'nom': 'Saito_2015_PrecisionRecall.pdf',
        'dossier': '6_Methodologie',
        'url': 'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0118432&type=printable',
        'description': 'Precision-Recall Plot More Informative than ROC'
    },
    {
        'nom': 'Ke_2017_LightGBM.pdf',
        'dossier': '4_Algorithmes',
        'url': 'https://papers.nips.cc/paper_files/paper/2017/file/6449f44a102fde848669bdd9eb6b76fa-Paper.pdf',
        'description': 'LightGBM: A Highly Efficient Gradient Boosting'
    },
    {
        'nom': 'Mensh_2017_Writing_Paper.pdf',
        'dossier': '6_Methodologie',
        'url': 'https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1005619&type=printable',
        'description': 'Ten Simple Rules for Writing a Scientific Paper'
    },
]

# Livres (PDFs gratuits)
LIVRES = [
    {
        'nom': 'Hastie_2009_ESL.pdf',
        'dossier': '7_Livres',
        'url': 'https://hastie.su.domains/ElemStatLearn/printings/ESLII_print12_toc.pdf',
        'description': 'Elements of Statistical Learning'
    },
    {
        'nom': 'James_2021_ISLR.pdf',
        'dossier': '7_Livres',
        'url': 'https://hastie.su.domains/ISLR2/ISLRv2_website.pdf',
        'description': 'Introduction to Statistical Learning with R'
    },
]

def telecharger_fichier(url, chemin_destination, description):
    """
    Télécharge un fichier depuis une URL

    Args:
        url: URL du fichier à télécharger
        chemin_destination: Chemin où sauvegarder le fichier
        description: Description de l'article

    Returns:
        bool: True si succès, False sinon
    """
    try:
        print(f"\n📥 Téléchargement: {description}")
        print(f"   URL: {url}")

        # Envoyer la requête
        response = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        response.raise_for_status()

        # Vérifier que c'est bien un PDF
        content_type = response.headers.get('content-type', '')
        if 'pdf' not in content_type.lower() and not url.endswith('.pdf'):
            print(f"   ⚠️  Attention: Le contenu n'est peut-être pas un PDF ({content_type})")

        # Créer le dossier si nécessaire
        chemin_destination.parent.mkdir(parents=True, exist_ok=True)

        # Sauvegarder le fichier
        with open(chemin_destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Vérifier la taille
        taille = chemin_destination.stat().st_size
        if taille < 1000:
            print(f"   ⚠️  Fichier suspect (trop petit: {taille} octets)")
            return False

        print(f"   ✅ Téléchargé: {chemin_destination.name} ({taille/1024:.1f} Ko)")
        return True

    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False
    except Exception as e:
        print(f"   ❌ Erreur inattendue: {str(e)}")
        return False

def telecharger_tous():
    """
    Télécharge tous les articles de la liste
    """
    print("="*70)
    print("📚 TÉLÉCHARGEMENT DES ARTICLES SCIENTIFIQUES")
    print("="*70)
    print(f"\nRépertoire de destination: {BASE_DIR}")

    # Créer la structure de dossiers
    for dossier in ['1_DT1_Afrique', '2_Biomarqueurs', '3_ML_Sante',
                    '4_Algorithmes', '5_Interpretabilite', '6_Methodologie', '7_Livres']:
        (BASE_DIR / dossier).mkdir(parents=True, exist_ok=True)

    # Télécharger les articles
    succes = 0
    echecs = 0

    print(f"\n{'='*70}")
    print(f"📄 ARTICLES SCIENTIFIQUES ({len(ARTICLES)} à télécharger)")
    print(f"{'='*70}")

    for article in ARTICLES:
        chemin = BASE_DIR / article['dossier'] / article['nom']

        # Vérifier si déjà téléchargé
        if chemin.exists():
            taille = chemin.stat().st_size
            print(f"\n✓ Déjà présent: {article['nom']} ({taille/1024:.1f} Ko)")
            succes += 1
            continue

        # Télécharger
        if telecharger_fichier(article['url'], chemin, article['description']):
            succes += 1
        else:
            echecs += 1

        # Pause pour ne pas surcharger les serveurs
        time.sleep(2)

    # Télécharger les livres
    print(f"\n{'='*70}")
    print(f"📚 LIVRES ({len(LIVRES)} à télécharger)")
    print(f"{'='*70}")

    for livre in LIVRES:
        chemin = BASE_DIR / livre['dossier'] / livre['nom']

        if chemin.exists():
            taille = chemin.stat().st_size
            print(f"\n✓ Déjà présent: {livre['nom']} ({taille/1024:.1f} Ko)")
            succes += 1
            continue

        if telecharger_fichier(livre['url'], chemin, livre['description']):
            succes += 1
        else:
            echecs += 1

        time.sleep(2)

    # Résumé
    total = len(ARTICLES) + len(LIVRES)
    print(f"\n{'='*70}")
    print(f"📊 RÉSUMÉ DU TÉLÉCHARGEMENT")
    print(f"{'='*70}")
    print(f"✅ Réussis: {succes}/{total}")
    print(f"❌ Échecs:  {echecs}/{total}")

    if echecs > 0:
        print(f"\n⚠️  Articles non téléchargés:")
        print(f"   - Vérifier la connexion internet")
        print(f"   - Certains liens peuvent avoir changé")
        print(f"   - Télécharger manuellement depuis liens_bibliographie.md")

    print(f"\n📁 Fichiers sauvegardés dans: {BASE_DIR}")
    print(f"\n{'='*70}")

def lister_fichiers():
    """
    Liste tous les fichiers PDF présents
    """
    print("\n📋 FICHIERS PDF PRÉSENTS:\n")

    for dossier in sorted(BASE_DIR.glob("*/")):
        if dossier.is_dir():
            pdfs = list(dossier.glob("*.pdf"))
            if pdfs:
                print(f"\n📁 {dossier.name}/ ({len(pdfs)} fichiers)")
                for pdf in sorted(pdfs):
                    taille = pdf.stat().st_size / 1024
                    print(f"   ✓ {pdf.name} ({taille:.1f} Ko)")

if __name__ == "__main__":
    import sys

    # Vérifier que requests est installé
    try:
        import requests
    except ImportError:
        print("❌ Erreur: Le module 'requests' n'est pas installé")
        print("   Installez-le avec: pip install requests")
        sys.exit(1)

    # Télécharger tous les articles
    telecharger_tous()

    # Lister les fichiers présents
    lister_fichiers()

    print("\n🎉 Script terminé!")
    print("\n💡 Prochaines étapes:")
    print("   1. Vérifier que les PDFs sont lisibles")
    print("   2. Importer dans Zotero pour gestion bibliographique")
    print("   3. Télécharger manuellement les articles payants via bibliothèque universitaire")
