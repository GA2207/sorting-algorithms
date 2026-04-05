import unittest
import random
from sorting import (
    selection_sort, bubble_sort, insertion_sort,
    merge_sort, quick_sort, heap_sort, comb_sort, Stats
)

ALGOS = [
    ("selection_sort", selection_sort),
    ("bubble_sort", bubble_sort),
    ("insertion_sort", insertion_sort),
    ("merge_sort", merge_sort),
    ("quick_sort", quick_sort),
    ("heap_sort", heap_sort),
    ("comb_sort", comb_sort),
]


class TestSortingAlgorithms(unittest.TestCase):

    def test_liste_vide(self):
        """Chaque algo doit retourner une liste vide sans erreur."""
        for name, func in ALGOS:
            with self.subTest(algo=name):
                self.assertEqual(func([]), [])

    def test_un_element(self):
        """Une liste avec un seul element est deja triee."""
        for name, func in ALGOS:
            with self.subTest(algo=name):
                self.assertEqual(func([42]), [42])

    def test_liste_deja_triee(self):
        """Une liste deja triee doit rester identique."""
        lst = [1, 2, 3, 4, 5]
        for name, func in ALGOS:
            with self.subTest(algo=name):
                self.assertEqual(func(lst.copy()), [1, 2, 3, 4, 5])

    def test_liste_triee_inverse(self):
        """Une liste triee a l'envers doit etre correctement triee."""
        lst = [5, 4, 3, 2, 1]
        for name, func in ALGOS:
            with self.subTest(algo=name):
                self.assertEqual(func(lst.copy()), [1, 2, 3, 4, 5])

    def test_doublons(self):
        """Les doublons doivent etre correctement geres."""
        lst = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        attendu = sorted(lst)
        for name, func in ALGOS:
            with self.subTest(algo=name):
                self.assertEqual(func(lst.copy()), attendu)

    def test_elements_identiques(self):
        """Une liste avec tous les elements identiques."""
        lst = [7, 7, 7, 7, 7]
        for name, func in ALGOS:
            with self.subTest(algo=name):
                self.assertEqual(func(lst.copy()), [7, 7, 7, 7, 7])

    def test_nombres_negatifs(self):
        """Les nombres negatifs doivent etre correctement tries."""
        lst = [3, -1, -5, 2, 0, -3, 4]
        attendu = sorted(lst)
        for name, func in ALGOS:
            with self.subTest(algo=name):
                self.assertEqual(func(lst.copy()), attendu)

    def test_nombres_reels(self):
        """Les nombres a virgule doivent etre correctement tries."""
        lst = [3.14, 1.41, 2.71, 0.57, 1.73]
        attendu = sorted(lst)
        for name, func in ALGOS:
            with self.subTest(algo=name):
                result = func(lst.copy())
                for a, b in zip(result, attendu):
                    self.assertAlmostEqual(a, b)

    def test_grosse_liste_aleatoire(self):
        """Verification sur une grande liste aleatoire (1000 elements)."""
        lst = [random.randint(-10000, 10000) for _ in range(1000)]
        attendu = sorted(lst)
        for name, func in ALGOS:
            with self.subTest(algo=name):
                self.assertEqual(func(lst.copy()), attendu)

    def test_deux_elements(self):
        """Liste de deux elements dans le mauvais ordre."""
        for name, func in ALGOS:
            with self.subTest(algo=name):
                self.assertEqual(func([2, 1]), [1, 2])

    def test_stats_compteur(self):
        """Le compteur d'operations doit fonctionner correctement."""
        lst = [5, 3, 1, 4, 2]
        for name, func in ALGOS:
            with self.subTest(algo=name):
                stats = Stats()
                func(lst.copy(), stats)
                self.assertGreater(stats.comparaisons, 0)
                # quick_sort ne fait pas d'echanges directs (il cree de nouvelles listes)
                if name != "quick_sort":
                    self.assertGreater(stats.echanges, 0)


if __name__ == "__main__":
    unittest.main()
