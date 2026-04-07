import random
import time
import threading
import csv
import os
from sorting import ALGORITHMS, Stats


def get_user_list():
    """Demande un nombre N et genere une liste de N elements aleatoires entre 0 et N."""
    while True:
        raw = input("\nEntrez un nombre N (genere une liste de N elements entre 0 et N) :\n> ").strip()
        try:
            n = int(raw)
            if n <= 0:
                print("Erreur : N doit etre un entier strictement positif.")
                continue
            lst = [random.randint(0, n) for _ in range(n)]
            print(f"  Liste generee : {lst if n <= 30 else str(lst[:20]) + f'... ({n} elements)'}")
            return lst
        except ValueError:
            print("Erreur : veuillez entrer un entier valide.")


def get_order():
    """Demande a l'utilisateur l'ordre de tri."""
    print("\n  1. Croissant")
    print("  2. Decroissant")
    while True:
        choix = input("  Ordre de tri : ").strip()
        if choix == "1":
            return False
        if choix == "2":
            return True
        print("  Choix invalide.")


def is_already_sorted(lst):
    """Verifie si la liste est deja triee (croissant ou decroissant)."""
    if all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1)):
        return "croissant"
    if all(lst[i] >= lst[i + 1] for i in range(len(lst) - 1)):
        return "decroissant"
    return None


def choose_algorithm():
    """Affiche le menu et retourne le choix de l'utilisateur."""
    print("\n========================================")
    print("   Les Papyrus de Heron")
    print("   Outil de tri automatise")
    print("========================================")
    print("\nChoisissez une option :\n")
    for key, (name, _) in ALGORITHMS.items():
        print(f"  {key}. {name}")
    print(f"  8. Comparer les performances")
    print(f"  9. Benchmark multithreading")
    print(f"  0. Quitter")
    print()

    while True:
        choice = input("Votre choix : ").strip()
        if choice == "0":
            return None
        if choice == "8":
            return "benchmark"
        if choice == "9":
            return "multithread"
        if choice in ALGORITHMS:
            return choice
        print("Choix invalide. Reessayez.")


def display_result(name, original, sorted_list, stats=None):
    """Affiche l'input et le resultat trie."""
    print(f"\n--- {name} ---")
    print(f"  Input  : {original}")
    print(f"  Output : {sorted_list}")
    if stats:
        print(f"  Comparaisons : {stats.comparaisons}")
        print(f"  Echanges     : {stats.echanges}")


def export_csv(resultats, taille, filename="benchmark_results.csv"):
    """Exporte les resultats du benchmark dans un fichier CSV."""
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithme", "Temps (secondes)", "Taille de la liste"])
        for name, temps in resultats:
            writer.writerow([name, f"{temps:.6f}", taille])
    print(f"\n  Resultats exportes dans : {filepath}")


def benchmark():
    """Compare les performances des algorithmes sur une grosse liste."""
    print("\n========================================")
    print("   Benchmark - Comparaison des performances")
    print("========================================")

    taille = 10000
    grosse_liste = [random.randint(1, 100000) for _ in range(taille)]
    print(f"\nListe generee : {taille} elements aleatoires")

    resultats = {}

    for key, (name, sort_func) in ALGORITHMS.items():
        liste_copie = grosse_liste.copy()
        stats = Stats()
        print(f"\nLancement du {name}...")
        start_time = time.time()
        sort_func(liste_copie, stats)
        temps = time.time() - start_time
        resultats[name] = (temps, stats)
        print(f"  Termine en : {temps:.6f} secondes | {stats}")

    # VERDICT
    if resultats:
        print("\n========================================")
        print("   Le verdict")
        print("========================================\n")

        classement = sorted(resultats.items(), key=lambda x: x[1][0])

        for i, (name, (temps, stats)) in enumerate(classement, 1):
            print(f"  {i}. {name} : {temps:.6f}s | Comp: {stats.comparaisons} | Ech: {stats.echanges}")

        plus_rapide = classement[0]
        plus_lent = classement[-1]

        if plus_rapide[1][0] > 0:
            ratio = plus_lent[1][0] / plus_rapide[1][0]
            print(f"\n  {plus_rapide[0]} est environ {ratio:.0f}x plus rapide que {plus_lent[0]}")

        # export CSV
        export = input("\n  Exporter en CSV ? (o/n) : ").strip().lower()
        if export == "o":
            export_csv([(name, temps) for name, (temps, _) in classement], taille)


def benchmark_multithread():
    """Lance tous les algorithmes en parallele avec des threads."""
    print("\n========================================")
    print("   Benchmark Multithreading")
    print("   Tous les algorithmes en parallele")
    print("========================================")

    taille = 10000
    grosse_liste = [random.randint(1, 100000) for _ in range(taille)]
    print(f"\nListe generee : {taille} elements aleatoires")

    resultats = {}
    lock = threading.Lock()

    def trier(name, sort_func, liste):
        start_time = time.time()
        sort_func(liste)
        temps = time.time() - start_time
        with lock:
            resultats[name] = temps

    threads = []
    for key, (name, sort_func) in ALGORITHMS.items():
        liste_copie = grosse_liste.copy()
        t = threading.Thread(target=trier, args=(name, sort_func, liste_copie))
        threads.append((name, t))

    print(f"\nLancement de {len(threads)} threads en parallele...")
    start_total = time.time()

    for name, t in threads:
        t.start()
        print(f"  -> Thread {name} demarre")

    for name, t in threads:
        t.join()

    temps_total = time.time() - start_total

    # VERDICT
    print("\n========================================")
    print("   Resultats")
    print("========================================\n")

    classement = sorted(resultats.items(), key=lambda x: x[1])

    for i, (name, temps) in enumerate(classement, 1):
        print(f"  {i}. {name} : {temps:.6f} secondes")

    print(f"\n  Temps total (parallele) : {temps_total:.6f} secondes")

    temps_sequentiel = sum(t for _, t in classement)
    print(f"  Temps cumule (sequentiel) : {temps_sequentiel:.6f} secondes")

    if temps_total > 0:
        speedup = temps_sequentiel / temps_total
        print(f"  Speedup multithreading : x{speedup:.2f}")

    # export CSV
    export = input("\n  Exporter en CSV ? (o/n) : ").strip().lower()
    if export == "o":
        export_csv(classement, taille, "benchmark_multithread.csv")


def main():
    while True:
        choice = choose_algorithm()
        if choice is None:
            print("\nAu revoir !")
            break

        if choice == "benchmark":
            benchmark()
            input("\nAppuyez sur Entree pour continuer...")
            continue

        if choice == "multithread":
            benchmark_multithread()
            input("\nAppuyez sur Entree pour continuer...")
            continue

        name, sort_func = ALGORITHMS[choice]
        lst = get_user_list()

        # verification si la liste est deja triee
        deja_trie = is_already_sorted(lst)
        if deja_trie:
            print(f"\n  [Info] La liste est deja triee en ordre {deja_trie}.")

        # choix de l'ordre
        reverse = get_order()

        # compteur d'operations
        stats = Stats()
        sorted_list = sort_func(lst, stats)

        # inverser si decroissant
        if reverse:
            sorted_list = sorted_list[::-1]

        display_result(name, lst, sorted_list, stats)

        input("\nAppuyez sur Entree pour continuer...")


if __name__ == "__main__":
    main()
