def selection_sort(lst):
    """Tri par selection - Selection Sort"""
    arr = lst.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def bubble_sort(lst):
    """Tri a bulles - Bubble Sort"""
    arr = lst.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def insertion_sort(lst):
    """Tri par insertion - Insertion Sort"""
    arr = lst.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# === Algorithmes a implementer par les autres membres ===

def merge_sort(lst):
    """Tri fusion - Merge Sort (Personne 2)"""
    raise NotImplementedError("A implementer par Personne 2")


def quick_sort(lst):
    """Tri rapide - Quick Sort (Personne 2)"""
    raise NotImplementedError("A implementer par Personne 2")


def heap_sort(lst):
    """Tri par tas - Heap Sort (Personne 3)"""
    raise NotImplementedError("A implementer par Personne 3")


def comb_sort(lst):
    """Tri a peigne - Comb Sort (Personne 3)"""
    raise NotImplementedError("A implementer par Personne 3")


ALGORITHMS = {
    "1": ("Tri par selection", selection_sort),
    "2": ("Tri a bulles", bubble_sort),
    "3": ("Tri par insertion", insertion_sort),
    "4": ("Tri fusion", merge_sort),
    "5": ("Tri rapide", quick_sort),
    "6": ("Tri par tas", heap_sort),
    "7": ("Tri a peigne", comb_sort),
}
