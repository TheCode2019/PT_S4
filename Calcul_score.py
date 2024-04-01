import random
import math
from tri_par_fusion import tri_fusion
import matplotlib.pyplot as plt


def generer_donnees(taille_echantillon, type_test):
    if type_test == 'vide':
        return []  # Retourne un ensemble de données vide
    elif type_test == 'un_element':
        return [(random.randint(0, 100), 0)]  # Retourne un ensemble avec un seul élément
    elif type_test == 'croissant':
        return [(i, i) for i in range(taille_echantillon)]  # Retourne un ensemble trié en ordre croissant
    elif type_test == 'decroissant':
        return [(i, taille_echantillon - i - 1) for i in range(taille_echantillon)]  # Retourne un ensemble trié en ordre décroissant
    elif type_test == 'aleatoire':
        return [(random.randint(0, taille_echantillon), i) for i in range(taille_echantillon)]  # Retourne un ensemble aléatoire
    elif type_test == 'chaine':
        return [(random.choice('abcdefghijklmnopqrstuvwxyz'), i) for i in range(taille_echantillon)]  # Retourne un ensemble de chaînes

def calculer_entropie(data):
    frequences = {}
    for element in data:
        frequences[element] = frequences.get(element, 0) + 1
    probabilites = [f / len(data) for f in frequences.values()]
    entropie = -sum(p * math.log2(p) for p in probabilites if p > 0)
    return entropie

def calculer_score(comparaisons, deplacements, entropie_initiale, entropie_finale, donnees_test):
    # Initialiser le score à 10
    score = 10
    
    # ajustement de score basé sur les comparaisons et déplacements
    score -= (comparaisons + deplacements) / (2 * len(donnees_test))
    
    # Ajuster le score en fonction de la réduction de l'entropie
    if entropie_finale < entropie_initiale:
        score += 1  # Bonus si l'entropie est réduite
    else:
        score -= 1  # Pénalité si l'entropie n'est pas réduite (ou est augmentée, ce qui est improbable)
    
    # S'assurer que le score est entre 1 et 10
    score = max(1, min(10, score))
    
    return round(score, 1)

def tester_stabilite_tri(tri_fonction, donnees_test):
    # Calculer l'entropie initiale
    entropie_initiale = calculer_entropie([val for val, _ in donnees_test])
    
    # Trier les données et récupérer le nombre de comparaisons et de déplacements
    comparaisons, deplacements, donnees_triees = tri_fonction(donnees_test)
    
    # Calculer l'entropie finale
    entropie_finale = calculer_entropie([val for val, _ in donnees_triees])
    
    # Calculer la note de stabilité et ajuster en fonction des comparaisons et déplacements
    score = calculer_score(comparaisons, deplacements, entropie_initiale, entropie_finale, donnees_test)
    
    return score, entropie_initiale, entropie_finale, comparaisons, deplacements

def ajuster_score_en_fonction_des_donnees(score, donnees_test):
    # Ajustements basés sur les caractéristiques des données
    if len(donnees_test) == 0:  # Tableau vide
        return 10
    if len(donnees_test) == 1:  # Tableau avec un seul élément
        return 10
    if all(donnees_test[i][0] == donnees_test[0][0] for i in range(len(donnees_test))):  # Données avec doublons uniquement
        return score - 0.5  # Ajustement léger pour les doublons
    if all(donnees_test[i][0] <= donnees_test[i + 1][0] for i in range(len(donnees_test) - 1)):  # Données déjà triées (croissant)
        return score + 0.5  # Bonus pour données déjà triées en ordre croissant
    if all(donnees_test[i][0] >= donnees_test[i + 1][0] for i in range(len(donnees_test) - 1)):  # Données déjà triées (décroissant)
        return score + 0.25  # Bonus pour données déjà triées en ordre décroissant
    
    return score  # Le score ajusté, s'il ne dépasse pas 10

def calculer_score(comparaisons, deplacements, entropie_initiale, entropie_finale, donnees_test):
    # Si l'ensemble de données est vide ou contient un seul élément, retourner un score parfait.
    if len(donnees_test) <= 1:
        return 10
    
    score = 10  # Score de base
    
    # Ajustement pour la performance, avec une vérification pour éviter la division par zéro.
    if len(donnees_test) > 1:
        penalite = (comparaisons + deplacements) / (10 * len(donnees_test))
        score -= penalite
    
    # Ajustement pour entropie
    if entropie_finale < entropie_initiale:
        score += 1  # Bonus si l'entropie est réduite
    else:
        score -= 1  # Pénalité si l'entropie n'est pas réduite
    
    # Applique d'autres ajustements basés sur les caractéristiques des données.
    score = ajuster_score_en_fonction_des_donnees(score, donnees_test)
    
    # S'assurer que le score est entre 1 et 10.
    return max(1, min(round(score, 1), 10))


def executer_tests_tri():
    taille_echantillon = int(input("Taille de l'échantillon: "))
    type_test = input("Type de test (vide, un_element, croissant, decroissant, aleatoire, chaine): ").lower()
    
    donnees_test = generer_donnees(taille_echantillon, type_test)

    if donnees_test is not None:  # Vérifier que generer_donnees n'a pas retourné None
        score, entropie_initiale, entropie_finale, comparaisons, deplacements = tester_stabilite_tri(tri_fonction=tri_fusion, donnees_test=donnees_test)
        
        # Affichage des résultats
        print(f"La note de stabilité pour le tri fusion est : {score}/10")
        print(f"Entropie initiale : {entropie_initiale}, Entropie finale : {entropie_finale}")
        print(f"Nombre de comparaisons : {comparaisons}, Nombre de déplacements : {deplacements}")
        
        # Enregistrement des résultats dans le premier fichier
        with open('donnees_tests.txt', 'a') as file:
            file.write(f"Taille de l'échantillon: {taille_echantillon}\n")
            file.write(f"Type de test: {type_test}\n")
            file.write(f"Données test: {donnees_test}\n")
            file.write(f"Score: {score}, Entropie initiale: {entropie_initiale}, Entropie finale: {entropie_finale}\n")
            file.write(f"Comparaisons: {comparaisons}, Déplacements: {deplacements}\n")
            file.write("----------------------------------------------------\n")

        # Enregistrement des résultats essentiels dans un deuxième fichier (par exemple, au format CSV)
        with open('resultats_tests.csv', 'a') as file_csv:
            # Écrire l'en-tête si le fichier est nouvellement créé ou vide
            if file_csv.tell() == 0:
                file_csv.write("Score,EntropieInitiale,EntropieFinale,Comparaisons,Deplacements\n")
            file_csv.write(f"{score},{entropie_initiale},{entropie_finale},{comparaisons},{deplacements}\n")

    else:
        print("Type de test non reconnu. Aucun test exécuté.")

if __name__ == "__main__":
    k = int(input("Combien de sets de données voulez-vous générer et enregistrer ? "))
    for n in range(k):
        executer_tests_tri()



 


