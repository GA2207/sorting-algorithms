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
    print(f"  0. Quitter")
    print()

    while True:
        choice = input("Votre choix : ").strip()
        if choice == "0":
            return None
        if choice in ALGORITHMS:
            return choice
        print("Choix invalide. Reessayez.")


def display_result(name, original, sorted_list):
    """Affiche l'input et le resultat trie."""
    print(f"\n--- {name} ---")
    print(f"  Input  : {original}")
    print(f"  Output : {sorted_list}")


def main():
    while True:
        choice = choose_algorithm()
        if choice is None:
            print("\nAu revoir !")
            break

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
