import sys

# Augmenter la recursivite pour eviter que le quick sort plante
sys.setrecursionlimit(50000)


# ======================== COMPTEUR D'OPERATIONS ========================

class Stats:
    """Compteur de comparaisons et d'echanges pour analyser la complexite."""
    def __init__(self):
        self.comparaisons = 0
        self.echanges = 0

    def reset(self):
        self.comparaisons = 0
        self.echanges = 0

    def __repr__(self):
        return f"Comparaisons: {self.comparaisons}, Echanges: {self.echanges}"


# ======================== ALGORITHMES DE TRI ========================

# ACTE I : La force brute - Le tri par selection
"""C'est l'algo naif : on parcourt toute la liste pour trouver le plus petit element,
on l'echange avec le 1er element non trie, et ainsi de suite.
Il utilise des boucles imbriquees : pour N elements, il fait N^2 iterations.
Complexite : O(N^2)"""

def selection_sort(arr, stats=None):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if stats:
                stats.comparaisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if stats:
            stats.echanges += 1
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# ACTE II : La methode classique - Le tri a bulles
"""On compare chaque paire d'elements adjacents et on les echange
s'ils sont dans le mauvais ordre. A chaque passage, le plus grand
element "remonte" comme une bulle vers la fin de la liste.
Complexite : O(N^2)"""

def bubble_sort(arr, stats=None):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if stats:
                stats.comparaisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                if stats:
                    stats.echanges += 1
                swapped = True
        if not swapped:
            break
    return arr


# ACTE III : L'approche du joueur de cartes - Le tri par insertion
"""Comme quand on trie des cartes dans sa main : on prend chaque element
et on l'insere a sa bonne place dans la partie deja triee de la liste.
Complexite : O(N^2)"""

def insertion_sort(arr, stats=None):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            if stats:
                stats.comparaisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                if stats:
                    stats.echanges += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
    return arr


# ACTE IV : Diviser pour regner - Le tri fusion
"""On divise la liste en deux moities, on trie chaque moitie recursivement,
puis on fusionne les deux moities triees en une seule liste ordonnee.
C'est un algo stable et performant dans tous les cas.
Complexite : O(N log N)"""

def merge_sort(arr, stats=None):
    if len(arr) <= 1:
        return arr

    milieu = len(arr) // 2
    gauche = arr[:milieu]
    droite = arr[milieu:]

    gauche = merge_sort(gauche, stats)
    droite = merge_sort(droite, stats)

    i = j = k = 0
    while i < len(gauche) and j < len(droite):
        if stats:
            stats.comparaisons += 1
        if gauche[i] <= droite[j]:
            arr[k] = gauche[i]
            i += 1
        else:
            arr[k] = droite[j]
            j += 1
        if stats:
            stats.echanges += 1
        k += 1

    while i < len(gauche):
        arr[k] = gauche[i]
        if stats:
            stats.echanges += 1
        i += 1
        k += 1

    while j < len(droite):
        arr[k] = droite[j]
        if stats:
            stats.echanges += 1
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

def quick_sort(arr, stats=None):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    gauche = []
    milieu = []
    droite = []
    for x in arr:
        if stats:
            stats.comparaisons += 1
        if x < pivot:
            gauche.append(x)
        elif x == pivot:
            milieu.append(x)
        else:
            droite.append(x)

    return quick_sort(gauche, stats) + milieu + quick_sort(droite, stats)


# ACTE VI : L'arbre du savoir - Le tri par tas
"""On transforme la liste en un arbre binaire special (tas max) ou chaque parent
est plus grand que ses enfants. On extrait le plus grand element (la racine),
on le place a la fin, puis on reconstruit le tas avec le reste.
Complexite : O(N log N)"""

def heap_sort(arr, stats=None):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i, stats)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        if stats:
            stats.echanges += 1
        _heapify(arr, i, 0, stats)

    return arr


def _heapify(arr, n, i, stats=None):
    plus_grand = i
    gauche = 2 * i + 1
    droite = 2 * i + 2

    if gauche < n:
        if stats:
            stats.comparaisons += 1
        if arr[gauche] > arr[plus_grand]:
            plus_grand = gauche

    if droite < n:
        if stats:
            stats.comparaisons += 1
        if arr[droite] > arr[plus_grand]:
            plus_grand = droite

    if plus_grand != i:
        arr[i], arr[plus_grand] = arr[plus_grand], arr[i]
        if stats:
            stats.echanges += 1
        _heapify(arr, n, plus_grand, stats)


# ACTE VII : Le peigne magique - Le tri a peigne
"""Amelioration du tri a bulles : au lieu de comparer des elements adjacents (ecart = 1),
on commence avec un grand ecart qu'on reduit progressivement par un facteur de 1.3.
Cela permet de deplacer les petits elements en fin de liste (les "tortues") plus vite.
Complexite : O(N^2 / 2^p) en moyenne, meilleur que le tri a bulles classique"""

def comb_sort(arr, stats=None):
    n = len(arr)
    ecart = n
    retrecissement = 1.3
    trie = False

    while not trie:
        ecart = int(ecart / retrecissement)
        if ecart <= 1:
            ecart = 1
            trie = True

        i = 0
        while i + ecart < n:
            if stats:
                stats.comparaisons += 1
            if arr[i] > arr[i + ecart]:
                arr[i], arr[i + ecart] = arr[i + ecart], arr[i]
                if stats:
                    stats.echanges += 1
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
