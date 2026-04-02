import sys

# Augmenter la recursivite pour eviter que le quick sort plante
sys.setrecursionlimit(50000)


# ACTE I : La force brute - Le tri par selection
"""C'est l'algo naif : on parcourt toute la liste pour trouver le plus petit element,
on l'echange avec le 1er element non trie, et ainsi de suite.
Il utilise des boucles imbriquees : pour N elements, il fait N^2 iterations.
Complexite : O(N^2)"""

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
element "remonte" comme une bulle vers la fin de la liste.
Complexite : O(N^2)"""

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
et on l'insere a sa bonne place dans la partie deja triee de la liste.
Complexite : O(N^2)"""

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


# ACTE IV : Diviser pour regner - Le tri fusion
"""On divise la liste en deux moities, on trie chaque moitie recursivement,
puis on fusionne les deux moities triees en une seule liste ordonnee.
C'est un algo stable et performant dans tous les cas.
Complexite : O(N log N)"""

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # on divise la liste en deux moities
    milieu = len(arr) // 2
    gauche = arr[:milieu]
    droite = arr[milieu:]

    # on trie chaque moitie recursivement
    gauche = merge_sort(gauche)
    droite = merge_sort(droite)

    # on fusionne les deux moities triees
    i = j = k = 0
    while i < len(gauche) and j < len(droite):
        if gauche[i] <= droite[j]:
            arr[k] = gauche[i]
            i += 1
        else:
            arr[k] = droite[j]
            j += 1
        k += 1

    # on copie les elements restants
    while i < len(gauche):
        arr[k] = gauche[i]
        i += 1
        k += 1

    while j < len(droite):
        arr[k] = droite[j]
        j += 1
        k += 1

    return arr


# ACTE V : Le pivot decisif - Le tri rapide
"""Concept : on choisit un element (le pivot), on place tous les elements
plus petits a sa gauche et plus grands a sa droite.
Le pivot est a sa place definitive, puis on s'appelle soi-meme
(recursivite) sur la sous-liste de gauche et de droite.
Complexite : O(N log N) en moyenne, O(N^2) au pire cas
Exemple pire cas : liste deja triee [1, 2, 3, 4, 5] avec pivot = 1er element,
chaque appel ne separe qu'un seul element -> N niveaux x N comparaisons = N^2"""

def quick_sort(arr):
    # condition d'arret : une liste vide ou 1 element est deja triee
    if len(arr) <= 1:
        return arr

    # on choisit notre pivot (l'element du milieu)
    pivot = arr[len(arr) // 2]

    # on divise la liste en 3 groupes
    gauche = [x for x in arr if x < pivot]
    milieu = [x for x in arr if x == pivot]
    droite = [x for x in arr if x > pivot]

    # on rappelle la fonction sur les sous-listes
    return quick_sort(gauche) + milieu + quick_sort(droite)


# === Algorithmes a implementer par HIBA ===

def heap_sort(arr):
    """Tri par tas - Heap Sort (HIBA)"""
    raise NotImplementedError("A implementer par HIBA")


def comb_sort(arr):
    """Tri a peigne - Comb Sort (HIBA)"""
    raise NotImplementedError("A implementer par HIBA")


ALGORITHMS = {
    "1": ("Tri par selection", selection_sort),
    "2": ("Tri a bulles", bubble_sort),
    "3": ("Tri par insertion", insertion_sort),
    "4": ("Tri fusion", merge_sort),
    "5": ("Tri rapide", quick_sort),
    "6": ("Tri par tas", heap_sort),
    "7": ("Tri a peigne", comb_sort),
}
