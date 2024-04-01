import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
import pandas as pd

# Lire les données depuis un fichier CSV
df = pd.read_csv('resultats_tests.csv')

# Supposons que le CSV a les colonnes spécifiées lors de l'écriture du fichier
entropies_initiales = df['EntropieInitiale'].tolist()
scores = df['Score'].tolist()
comparaisons = df['Comparaisons'].tolist()
deplacements = df['Deplacements'].tolist()

# Tracé
plt.figure(figsize=(12, 8))

# Nuages de points pour les comparaisons et les déplacements
plt.scatter(entropies_initiales, comparaisons, color='blue', alpha=0.5, label='Comparaisons')
plt.scatter(entropies_initiales, deplacements, color='orange', alpha=0.5, label='Déplacements')

# Ajout des scores sous forme de nuage de points
plt.scatter(entropies_initiales, scores, color='green', alpha=0.5, label='Scores')

# Ajout de lignes de tendance LOWESS
comparaisons_tendance = lowess(comparaisons, entropies_initiales, frac=0.1)
deplacements_tendance = lowess(deplacements, entropies_initiales, frac=0.1)
scores_tendance = lowess(scores, entropies_initiales, frac=0.1)

plt.plot(comparaisons_tendance[:, 0], comparaisons_tendance[:, 1], 'r--', label='Tendance Comparaisons')
plt.plot(deplacements_tendance[:, 0], deplacements_tendance[:, 1], 'b--', label='Tendance Déplacements')
plt.plot(scores_tendance[:, 0], scores_tendance[:, 1], 'g--', label='Tendance Scores')

# Configuration du graphique
plt.xlabel('Entropie Initiale')
plt.ylabel('Valeurs')
plt.title('Comparaisons, Déplacements et Scores en fonction de l\'Entropie Initiale')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
