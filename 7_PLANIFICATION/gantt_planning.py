#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GÉNÉRATION DU DIAGRAMME DE GANTT
Projet: Détection précoce DT1 Cameroun
Étudiante: Sorelle - Master 2 Biophysique
Période: Novembre 2025 - Mai 2026 (6 mois)
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Configuration
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'DejaVu Sans'

# Définir les tâches et leurs durées
# Format: (Nom, Date début, Durée en jours, Catégorie)
date_debut = datetime(2025, 11, 22)  # Date actuelle

taches = [
    # PHASE 1: INSTALLATION ET PRISE EN MAIN (Semaines 1-2)
    ("1.1 Installation environnement Python", date_debut, 2, "Installation"),
    ("1.2 Découverte des notebooks", date_debut + timedelta(days=2), 3, "Installation"),
    ("1.3 Import bibliographie dans Zotero", date_debut + timedelta(days=3), 4, "Installation"),

    # PHASE 2: APPRENTISSAGE ML (Semaines 1-7)
    ("2.1 Semaine 1: Python + ML de base", date_debut + timedelta(days=0), 7, "Apprentissage"),
    ("2.2 Semaine 2: Exploration données", date_debut + timedelta(days=7), 7, "Apprentissage"),
    ("2.3 Semaine 3: Modèles simples", date_debut + timedelta(days=14), 7, "Apprentissage"),
    ("2.4 Semaines 4-5: Modèles avancés", date_debut + timedelta(days=21), 14, "Apprentissage"),
    ("2.5 Semaine 6: Optimisation", date_debut + timedelta(days=35), 7, "Apprentissage"),
    ("2.6 Semaine 7: Interprétabilité", date_debut + timedelta(days=42), 7, "Apprentissage"),

    # PHASE 3: LECTURES BIBLIOGRAPHIQUES (Parallèle)
    ("3.1 Lecture articles DT1 Afrique", date_debut + timedelta(days=7), 21, "Bibliographie"),
    ("3.2 Lecture articles ML médical", date_debut + timedelta(days=14), 21, "Bibliographie"),
    ("3.3 Lecture articles techniques", date_debut + timedelta(days=28), 21, "Bibliographie"),

    # PHASE 4: DÉVELOPPEMENT APPLICATION (Semaines 8-10)
    ("4.1 Tests application Streamlit", date_debut + timedelta(days=49), 7, "Application"),
    ("4.2 Ajout fonctionnalités", date_debut + timedelta(days=56), 7, "Application"),
    ("4.3 Finalisation interface", date_debut + timedelta(days=63), 7, "Application"),

    # PHASE 5: RÉDACTION MÉMOIRE (Semaines 8-20)
    ("5.1 Rédaction Introduction", date_debut + timedelta(days=49), 14, "Rédaction"),
    ("5.2 Rédaction État de l'art", date_debut + timedelta(days=56), 21, "Rédaction"),
    ("5.3 Rédaction Méthodologie", date_debut + timedelta(days=70), 21, "Rédaction"),
    ("5.4 Génération résultats + figures", date_debut + timedelta(days=84), 14, "Rédaction"),
    ("5.5 Rédaction Résultats", date_debut + timedelta(days=91), 14, "Rédaction"),
    ("5.6 Rédaction Discussion", date_debut + timedelta(days=98), 14, "Rédaction"),
    ("5.7 Rédaction Conclusion + Abstract", date_debut + timedelta(days=105), 7, "Rédaction"),

    # PHASE 6: RÉVISION ET FINALISATION (Semaines 18-22)
    ("6.1 Relecture et corrections", date_debut + timedelta(days=119), 14, "Finalisation"),
    ("6.2 Mise en page finale", date_debut + timedelta(days=126), 7, "Finalisation"),
    ("6.3 Impression et reliure", date_debut + timedelta(days=133), 3, "Finalisation"),
    ("6.4 Dépôt mémoire", date_debut + timedelta(days=136), 1, "Finalisation"),

    # PHASE 7: SOUTENANCE (Semaines 23-24)
    ("7.1 Préparation slides", date_debut + timedelta(days=140), 7, "Soutenance"),
    ("7.2 Répétitions", date_debut + timedelta(days=147), 7, "Soutenance"),
    ("7.3 SOUTENANCE", date_debut + timedelta(days=154), 1, "Soutenance"),
]

# Créer un DataFrame
df = pd.DataFrame(taches, columns=['Tâche', 'Début', 'Durée', 'Catégorie'])
df['Fin'] = df.apply(lambda x: x['Début'] + timedelta(days=x['Durée']), axis=1)

# Définir les couleurs par catégorie
couleurs = {
    'Installation': '#FF6B6B',
    'Apprentissage': '#4ECDC4',
    'Bibliographie': '#45B7D1',
    'Application': '#FFA07A',
    'Rédaction': '#98D8C8',
    'Finalisation': '#F7DC6F',
    'Soutenance': '#BB8FCE'
}

# Créer le diagramme
fig, ax = plt.subplots(figsize=(18, 12))

# Tracer les barres
for idx, row in df.iterrows():
    ax.barh(idx, row['Durée'], left=mdates.date2num(row['Début']),
            height=0.6, color=couleurs[row['Catégorie']],
            edgecolor='black', linewidth=0.5, alpha=0.8)

    # Ajouter le nom de la tâche
    ax.text(mdates.date2num(row['Début']) - 2, idx, row['Tâche'],
            va='center', ha='right', fontsize=9, fontweight='bold')

    # Ajouter la durée à la fin
    ax.text(mdates.date2num(row['Fin']) + 1, idx, f"{int(row['Durée'])}j",
            va='center', ha='left', fontsize=8)

# Configuration des axes
ax.set_yticks(range(len(df)))
ax.set_yticklabels([])
ax.set_ylim(-1, len(df))

# Formatter l'axe des dates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.DayLocator())

# Rotation des dates
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Grille
ax.grid(True, axis='x', alpha=0.3, linestyle='--')
ax.axhline(y=6.5, color='red', linestyle='--', linewidth=2, alpha=0.5)  # Fin apprentissage
ax.axhline(y=9.5, color='orange', linestyle='--', linewidth=2, alpha=0.5)  # Fin lectures
ax.axhline(y=12.5, color='green', linestyle='--', linewidth=2, alpha=0.5)  # Fin application

# Légende
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=couleurs[cat], edgecolor='black', label=cat)
                   for cat in couleurs.keys()]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10,
          title='Catégories', framealpha=0.9)

# Titres et labels
ax.set_xlabel('Date (2025-2026)', fontsize=12, fontweight='bold')
ax.set_title('DIAGRAMME DE GANTT - Projet Master 2\n' +
             'Détection précoce du Diabète Type 1 au Cameroun\n' +
             'Étudiante: Sorelle | Encadrant: Dr. TCHAPET NJAFA Jean-Pierre',
             fontsize=14, fontweight='bold', pad=20)

# Ajouter des annotations pour les jalons
jalons = [
    (date_debut + timedelta(days=49), "Fin apprentissage ML"),
    (date_debut + timedelta(days=70), "Début rédaction intensive"),
    (date_debut + timedelta(days=119), "Début révisions"),
    (date_debut + timedelta(days=154), "SOUTENANCE")
]

for date_jalon, texte in jalons:
    ax.axvline(x=mdates.date2num(date_jalon), color='red',
               linestyle=':', linewidth=1.5, alpha=0.6)

# Statistiques en bas
stats_text = f"""
DURÉE TOTALE: {(df['Fin'].max() - date_debut).days} jours (~{(df['Fin'].max() - date_debut).days // 7} semaines)
PHASES: 7 | TÂCHES: {len(df)} | DATE DÉBUT: {date_debut.strftime('%d/%m/%Y')} | DATE FIN: {df['Fin'].max().strftime('%d/%m/%Y')}
"""
fig.text(0.5, 0.02, stats_text, ha='center', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.subplots_adjust(bottom=0.08)

# Sauvegarder
plt.savefig('7_PLANIFICATION/gantt_planning.png', dpi=300, bbox_inches='tight')
plt.savefig('7_PLANIFICATION/gantt_planning.pdf', bbox_inches='tight')
print("✅ Diagramme de Gantt créé:")
print("   - 7_PLANIFICATION/gantt_planning.png")
print("   - 7_PLANIFICATION/gantt_planning.pdf")

# Créer aussi un fichier CSV du planning
df[['Tâche', 'Début', 'Fin', 'Durée', 'Catégorie']].to_csv(
    '7_PLANIFICATION/planning_details.csv', index=False, encoding='utf-8'
)
print("   - 7_PLANIFICATION/planning_details.csv")

plt.show()
