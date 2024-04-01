def tri_fusion(tableau):
    if len(tableau) > 1:
        milieu = len(tableau) // 2
        gauche = tableau[:milieu]
        droite = tableau[milieu:]

        comparaisons_gauche, deplacements_gauche, gauche = tri_fusion(gauche)
        comparaisons_droite, deplacements_droite, droite = tri_fusion(droite)

        fusionne, comparaisons_fusion, deplacements_fusion = fusionner(gauche, droite)

        comparaisons = comparaisons_gauche + comparaisons_droite + comparaisons_fusion
        deplacements = deplacements_gauche + deplacements_droite + deplacements_fusion

        return comparaisons, deplacements, fusionne
    else:
        return 0, 0, tableau

def fusionner(gauche, droite):
    resultat = []
    i = j = 0
    comparaisons = deplacements = 0

    while i < len(gauche) and j < len(droite):
        comparaisons += 1
        if gauche[i] < droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
        deplacements += 1

    while i < len(gauche):
        resultat.append(gauche[i])
        i += 1
        deplacements += 1

    while j < len(droite):
        resultat.append(droite[j])
        j += 1
        deplacements += 1

    return resultat, comparaisons, deplacements

# Exemple d'utilisation
if __name__ == "__main__":
    tableau = [8, 6, 4, 3, 2, 1, 9, 5, 7]
    comparaisons, deplacements, tableau_trie = tri_fusion(tableau)
    print(f"Tableau trié : {tableau_trie}")
    print(f"Nombre de comparaisons : {comparaisons}")
    print(f"Nombre de déplacements : {deplacements}")
