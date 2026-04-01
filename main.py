import random
import time
from sorting import ALGORITHMS


def get_user_list():
    """Demande a l'utilisateur de saisir une liste de nombres reels."""
    while True:
        raw = input("\nEntrez une liste de nombres reels separes par des espaces :\n> ")
        try:
            lst = [float(x) for x in raw.strip().split()]
            if not lst:
                print("Erreur : la liste ne peut pas etre vide.")
                continue
            return lst
        except ValueError:
            print("Erreur : veuillez entrer uniquement des nombres valides.")


def choose_algorithm():
    """Affiche le menu et retourne le choix de l'utilisateur."""
    print("\n========================================")
    print("   Les Papyrus de Heron")
    print("   Outil de tri automatise")
    print("========================================")
    print("\nChoisissez un algorithme de tri :\n")
    for key, (name, _) in ALGORITHMS.items():
        print(f"  {key}. {name}")
    print(f"  8. Comparer les performances")
    print(f"  0. Quitter")
    print()

    while True:
        choice = input("Votre choix : ").strip()
        if choice == "0":
            return None
        if choice == "8":
            return "benchmark"
        if choice in ALGORITHMS:
            return choice
        print("Choix invalide. Reessayez.")


def display_result(name, original, sorted_list):
    """Affiche l'input et le resultat trie."""
    print(f"\n--- {name} ---")
    print(f"  Input  : {original}")
    print(f"  Output : {sorted_list}")


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
        # chaque algo recoit sa propre copie de la liste
        liste_copie = grosse_liste.copy()
        try:
            print(f"\nLancement du {name}...")
            start_time = time.time()
            sort_func(liste_copie)
            temps = time.time() - start_time
            resultats[name] = temps
            print(f"  Termine en : {temps:.6f} secondes")
        except NotImplementedError:
            print(f"  [!] Non implemente")

    # VERDICT
    if resultats:
        print("\n========================================")
        print("   Le verdict")
        print("========================================\n")

        # trier les resultats du plus rapide au plus lent
        classement = sorted(resultats.items(), key=lambda x: x[1])

        for i, (name, temps) in enumerate(classement, 1):
            print(f"  {i}. {name} : {temps:.6f} secondes")

        plus_rapide = classement[0]
        plus_lent = classement[-1]

        if plus_rapide[1] > 0:
            ratio = plus_lent[1] / plus_rapide[1]
            print(f"\n  {plus_rapide[0]} est environ {ratio:.0f}x plus rapide que {plus_lent[0]}")


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

        name, sort_func = ALGORITHMS[choice]
        lst = get_user_list()

        try:
            sorted_list = sort_func(lst)
            display_result(name, lst, sorted_list)
        except NotImplementedError as e:
            print(f"\n[!] {e}")

        input("\nAppuyez sur Entree pour continuer...")


if __name__ == "__main__":
    main()
