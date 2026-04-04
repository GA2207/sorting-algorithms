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


# === Algorithmes a implementer par Lukas ===

def merge_sort(arr):
    """Tri fusion - Merge Sort (Lukas)"""
    raise NotImplementedError("A implementer par Lukas")


def quick_sort(arr):
    """Tri rapide - Quick Sort (Lukas)"""
    raise NotImplementedError("A implementer par Lukas")


# ACTE VI : L'arbre du savoir - Le tri par tas
"""On transforme la liste en un arbre binaire special (tas max) ou chaque parent
est plus grand que ses enfants. On extrait le plus grand element (la racine),
on le place a la fin, puis on reconstruit le tas avec le reste.
Complexite : O(N log N)"""

def heap_sort(arr):
    n = len(arr)

    # on construit le tas max (heapify) a partir du dernier noeud parent
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)

    # on extrait les elements un par un du tas
    for i in range(n - 1, 0, -1):
        # le plus grand element (racine) va a la fin
        arr[0], arr[i] = arr[i], arr[0]
        # on reconstruit le tas sur la partie non triee
        _heapify(arr, i, 0)

    return arr


def _heapify(arr, n, i):
    """Maintient la propriete du tas max : le parent est toujours plus grand que ses enfants."""
    plus_grand = i
    gauche = 2 * i + 1
    droite = 2 * i + 2

    # verifie si l'enfant gauche est plus grand que le parent
    if gauche < n and arr[gauche] > arr[plus_grand]:
        plus_grand = gauche

    # verifie si l'enfant droit est plus grand que le plus grand actuel
    if droite < n and arr[droite] > arr[plus_grand]:
        plus_grand = droite

    # si le plus grand n'est pas le parent, on echange et on continue
    if plus_grand != i:
        arr[i], arr[plus_grand] = arr[plus_grand], arr[i]
        _heapify(arr, n, plus_grand)


# ACTE VII : Le peigne magique - Le tri a peigne
"""Amelioration du tri a bulles : au lieu de comparer des elements adjacents (ecart = 1),
on commence avec un grand ecart qu'on reduit progressivement par un facteur de 1.3.
Cela permet de deplacer les petits elements en fin de liste (les "tortues") plus vite.
Complexite : O(N^2 / 2^p) en moyenne, meilleur que le tri a bulles classique"""

def comb_sort(arr):
    n = len(arr)
    # l'ecart initial est la taille de la liste
    ecart = n
    # facteur de reduction de l'ecart
    retrecissement = 1.3
    trie = False

    while not trie:
        # on reduit l'ecart
        ecart = int(ecart / retrecissement)
        if ecart <= 1:
            ecart = 1
            trie = True

        # on compare les elements avec l'ecart actuel
        i = 0
        while i + ecart < n:
            if arr[i] > arr[i + ecart]:
                arr[i], arr[i + ecart] = arr[i + ecart], arr[i]
                trie = False
            i += 1

    return arr


ALGORITHMS = {
    "1": ("Tri par selection", selection_sort),
    "2": ("Tri a bulles", bubble_sort),
    "3": ("Tri par insertion", insertion_sort),
    "4": ("Tri fusion", merge_sort),
    "5": ("Tri rapide", quick_sort),
    "6": ("Tri par tas", heap_sort),
    "7": ("Tri a peigne", comb_sort),
}
