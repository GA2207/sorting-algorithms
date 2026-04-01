# ACTE I : La force brute - Le tri par sélection
"""C'est l'algo naif : on parcourt toute la liste pour trouver le plus petit element,
on l'echange avec le 1er element non trie, et ainsi de suite.
Il utilise des boucles imbriquees : pour N elements, il fait N^2 iterations."""

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # on suppose que le 1er element non trie est le min
        min_idx = i

        # cherche le plus petit dans le reste de la liste
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        # on permute les 2 elements
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# ACTE II : La methode classique - Le tri a bulles
"""On compare chaque paire d'elements adjacents et on les echange
s'ils sont dans le mauvais ordre. A chaque passage, le plus grand
element "remonte" comme une bulle vers la fin de la liste."""

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # si l'element actuel est plus grand que le suivant, on echange
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # si aucun echange n'a eu lieu, la liste est deja triee
        if not swapped:
            break
    return arr


# ACTE III : L'approche du joueur de cartes - Le tri par insertion
"""Comme quand on trie des cartes dans sa main : on prend chaque element
et on l'insere a sa bonne place dans la partie deja triee de la liste."""

def insertion_sort(arr):
    for i in range(1, len(arr)):
        # on prend l'element a inserer
        key = arr[i]
        j = i - 1

        # on decale les elements plus grands vers la droite
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        # on insere l'element a sa place
        arr[j + 1] = key
    return arr

