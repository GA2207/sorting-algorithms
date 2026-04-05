# Les Papyrus de Héron - Sorting Algorithms

## Contexte

Dans l'effervescence de la ville égyptienne au Ier siècle apr. J.-C., se dressait la Grande Bibliothèque d'Alexandrie, tel un phare du savoir antique. Parmi les érudits arpentant les couloirs sacrés se trouvait Héron, un esprit brillant réputé pour ses prouesses en mathématiques, en mécanique et en ingénierie.

Un jour, Héron remarqua le désordre qui sévissait dans la Bibliothèque. Déterminé à rétablir l'ordre, il s'attela à la tâche en explorant différentes méthodes pour résoudre ce nouveau défi.

Ce projet consiste à lui venir en aide en implémentant 7 algorithmes de tri en Python, permettant d'automatiser l'organisation des papyrus contenant le savoir de l'humanité.

## Algorithmes implémentés

| # | Algorithme | Complexité | Statut |
|---|---|---|---|
| 1 | Tri par sélection | O(N²) | ✅ |
| 2 | Tri à bulles | O(N²) | ✅ |
| 3 | Tri par insertion | O(N²) | ✅ |
| 4 | Tri fusion | O(N log N) | ✅ |
| 5 | Tri rapide | O(N log N) en moyenne, O(N²) au pire cas | ✅ |
| 6 | Tri par tas | O(N log N) | ✅ |
| 7 | Tri à peigne | O(N² / 2^p) | ✅ |

## Utilisation

```bash
python main.py
```

Le programme affiche un menu permettant de :
1. Choisir un algorithme de tri
2. Saisir une liste de nombres réels
3. Visualiser l'input et le résultat trié
4. Comparer les performances de tous les algorithmes (option 8)

### Interface graphique

```bash
python visual.py
```

Lance une visualisation animée du tri sous forme de cercle de couleurs.

## Structure du projet

- `sorting.py` : Implémentation des 7 algorithmes de tri
- `main.py` : Script principal (menu, interaction utilisateur, benchmark)
- `visual.py` : Interface graphique de visualisation des tris
- `README.md` : Documentation du projet

## Analyse de performance

Benchmark réalisé sur une liste de **10 000 éléments aléatoires** (entiers de 1 à 100 000) :

| # | Algorithme | Temps d'exécution |
|---|---|---|
| 1 | Tri rapide | 0.009765 s |
| 2 | Tri fusion | 0.022077 s |
| 3 | Tri à peigne | 0.026028 s |
| 4 | Tri par tas | 0.038242 s |
| 5 | Tri par insertion | 2.290605 s |
| 6 | Tri par sélection | 2.792978 s |
| 7 | Tri à bulles | 5.621935 s |

Le tri rapide est environ **576x plus rapide** que le tri à bulles sur 10 000 éléments.

### Observations

- Les algorithmes en **O(N log N)** (tri rapide, tri fusion, tri par tas, tri à peigne) sont largement plus performants que les algorithmes en **O(N²)** (tri par sélection, tri à bulles, tri par insertion).
- Le **tri rapide** est le plus rapide grâce à sa stratégie de pivot qui divise efficacement la liste en sous-parties équilibrées.
- Le **tri à bulles** est le plus lent car il effectue de nombreuses comparaisons et échanges inutiles, même avec l'optimisation early stop.
- Le **tri par insertion** est le meilleur des O(N²) car il profite des sous-séquences déjà triées.
- Le **tri à peigne** rivalise avec les algorithmes O(N log N) grâce à son système d'écart décroissant qui élimine rapidement les "tortues" (petits éléments en fin de liste).

## Conclusion

Ce projet nous a permis de comprendre concrètement la différence entre les complexités algorithmiques. Sur le papier, O(N²) vs O(N log N) peut sembler abstrait, mais en pratique la différence est flagrante : sur 10 000 éléments, on passe de quelques millisecondes à plusieurs secondes.

Le tri rapide s'impose comme le meilleur choix dans la majorité des cas, ce qui explique pourquoi il est utilisé dans de nombreux langages de programmation (comme la fonction `sorted()` de Python qui utilise Timsort, un hybride entre tri fusion et tri par insertion).

Héron aurait certainement approuvé le tri rapide pour organiser les papyrus de la Grande Bibliothèque d'Alexandrie.
