import pygame
import random
import math
import sys
import time

# ======================== CONFIGURATION ========================
LARGEUR = 800
HAUTEUR = 800
FPS = 60
NB_ELEMENTS = 100
RAYON_CERCLE = 300
CENTRE = (LARGEUR // 2, HAUTEUR // 2)

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (180, 180, 180)


def valeur_vers_couleur(valeur, maximum):
    """Convertit une valeur en couleur HSV (teinte basee sur la valeur)."""
    teinte = valeur / maximum
    # conversion HSV -> RGB (saturation = 1, valeur = 1)
    r, g, b = hsv_to_rgb(teinte, 1.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))


def hsv_to_rgb(h, s, v):
    """Conversion HSV vers RGB."""
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    if i == 0: return v, t, p
    if i == 1: return q, v, p
    if i == 2: return p, v, t
    if i == 3: return p, q, v
    if i == 4: return t, p, v
    if i == 5: return v, p, q


def dessiner_cercle(screen, arr, maximum, titre=""):
    """Dessine les elements sous forme de cercle de couleurs."""
    screen.fill(NOIR)
    n = len(arr)

    for i in range(n):
        # angle de chaque element sur le cercle
        angle = (2 * math.pi * i / n) - math.pi / 2
        # position exterieure du segment
        x_ext = CENTRE[0] + RAYON_CERCLE * math.cos(angle)
        y_ext = CENTRE[1] + RAYON_CERCLE * math.sin(angle)

        couleur = valeur_vers_couleur(arr[i], maximum)

        # dessiner une ligne du centre vers l'exterieur
        pygame.draw.line(screen, couleur, CENTRE, (int(x_ext), int(y_ext)), 3)

    # afficher le titre de l'algorithme
    if titre:
        font = pygame.font.SysFont("Arial", 24, bold=True)
        texte = font.render(titre, True, BLANC)
        rect = texte.get_rect(center=(LARGEUR // 2, 30))
        screen.blit(texte, rect)

    pygame.display.flip()


def dessiner_bouton_retour(screen):
    """Dessine un bouton 'Retour au menu' en bas de l'ecran."""
    font = pygame.font.SysFont("Arial", 20, bold=True)
    texte = font.render("Retour au menu (Appuyez R)", True, NOIR)
    rect = texte.get_rect(center=(LARGEUR // 2, HAUTEUR - 40))
    # fond du bouton
    bouton_rect = rect.inflate(30, 16)
    pygame.draw.rect(screen, GRIS, bouton_rect, border_radius=8)
    pygame.draw.rect(screen, BLANC, bouton_rect, 2, border_radius=8)
    screen.blit(texte, rect)
    pygame.display.flip()
    return bouton_rect


# ======================== ALGORITHMES VISUELS ========================
# Chaque algo appelle dessiner_cercle() a chaque etape pour montrer le tri

def visual_selection_sort(arr, screen, maximum, titre):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        dessiner_cercle(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    return True


def visual_bubble_sort(arr, screen, maximum, titre):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        dessiner_cercle(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        if not swapped:
            break
    return True


def visual_insertion_sort(arr, screen, maximum, titre):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        dessiner_cercle(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    return True


def visual_merge_sort(arr, screen, maximum, titre):
    def merge_sort_rec(arr, debut, fin):
        if fin - debut <= 1:
            return True
        milieu = (debut + fin) // 2
        if not merge_sort_rec(arr, debut, milieu):
            return False
        if not merge_sort_rec(arr, milieu, fin):
            return False

        gauche = arr[debut:milieu]
        droite = arr[milieu:fin]
        i = j = 0
        k = debut
        while i < len(gauche) and j < len(droite):
            if gauche[i] <= droite[j]:
                arr[k] = gauche[i]
                i += 1
            else:
                arr[k] = droite[j]
                j += 1
            k += 1
        while i < len(gauche):
            arr[k] = gauche[i]
            i += 1
            k += 1
        while j < len(droite):
            arr[k] = droite[j]
            j += 1
            k += 1

        dessiner_cercle(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    return merge_sort_rec(arr, 0, len(arr))


def visual_quick_sort(arr, screen, maximum, titre):
    def quick_sort_rec(debut, fin):
        if debut >= fin:
            return True
        pivot = arr[(debut + fin) // 2]
        i, j = debut, fin
        while i <= j:
            while arr[i] < pivot:
                i += 1
            while arr[j] > pivot:
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1

        dessiner_cercle(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if not quick_sort_rec(debut, j):
            return False
        if not quick_sort_rec(i, fin):
            return False
        return True

    return quick_sort_rec(0, len(arr) - 1)


def visual_heap_sort(arr, screen, maximum, titre):
    n = len(arr)

    def heapify(n, i):
        plus_grand = i
        g = 2 * i + 1
        d = 2 * i + 2
        if g < n and arr[g] > arr[plus_grand]:
            plus_grand = g
        if d < n and arr[d] > arr[plus_grand]:
            plus_grand = d
        if plus_grand != i:
            arr[i], arr[plus_grand] = arr[plus_grand], arr[i]
            heapify(n, plus_grand)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
        dessiner_cercle(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    return True


def visual_comb_sort(arr, screen, maximum, titre):
    n = len(arr)
    ecart = n
    trie = False

    while not trie:
        ecart = int(ecart / 1.3)
        if ecart <= 1:
            ecart = 1
            trie = True

        i = 0
        while i + ecart < n:
            if arr[i] > arr[i + ecart]:
                arr[i], arr[i + ecart] = arr[i + ecart], arr[i]
                trie = False
            i += 1

        dessiner_cercle(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    return True


# ======================== MENU ET BOUCLE PRINCIPALE ========================

VISUAL_ALGORITHMS = {
    "1": ("Tri par selection", visual_selection_sort),
    "2": ("Tri a bulles", visual_bubble_sort),
    "3": ("Tri par insertion", visual_insertion_sort),
    "4": ("Tri fusion", visual_merge_sort),
    "5": ("Tri rapide", visual_quick_sort),
    "6": ("Tri par tas", visual_heap_sort),
    "7": ("Tri a peigne", visual_comb_sort),
}


def benchmark_graphique(screen):
    """Lance les 7 algos, chronometre chacun et affiche un diagramme en barres."""
    from sorting import ALGORITHMS as SORT_ALGORITHMS

    NB_BENCH = 10000
    grosse_liste = [random.randint(1, 100000) for _ in range(NB_BENCH)]

    # ecran de chargement
    screen.fill(NOIR)
    font = pygame.font.SysFont("Arial", 28, bold=True)
    texte = font.render("Benchmark en cours...", True, BLANC)
    screen.blit(texte, texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 2)))
    pygame.display.flip()

    resultats = []
    for key, (name, sort_func) in SORT_ALGORITHMS.items():
        liste_copie = grosse_liste.copy()
        start = time.time()
        sort_func(liste_copie)
        temps = time.time() - start
        resultats.append((name, temps))
        # garder pygame reactif
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

    # trier du plus rapide au plus lent
    resultats.sort(key=lambda x: x[1])

    # ======================== DESSINER LE GRAPHIQUE ========================
    screen.fill(NOIR)

    font_titre = pygame.font.SysFont("Arial", 26, bold=True)
    font_label = pygame.font.SysFont("Arial", 14, bold=True)
    font_valeur = pygame.font.SysFont("Arial", 13)

    titre = font_titre.render(f"Comparaison des performances ({NB_BENCH} elements)", True, BLANC)
    screen.blit(titre, titre.get_rect(center=(LARGEUR // 2, 40)))

    # zone du graphique
    marge_gauche = 80
    marge_droite = 40
    marge_haut = 90
    marge_bas = 120
    zone_largeur = LARGEUR - marge_gauche - marge_droite
    zone_hauteur = HAUTEUR - marge_haut - marge_bas

    # axes
    pygame.draw.line(screen, BLANC, (marge_gauche, marge_haut), (marge_gauche, marge_haut + zone_hauteur), 2)
    pygame.draw.line(screen, BLANC, (marge_gauche, marge_haut + zone_hauteur), (marge_gauche + zone_largeur, marge_haut + zone_hauteur), 2)

    temps_max = max(t for _, t in resultats)
    nb_algos = len(resultats)
    largeur_barre = zone_largeur // nb_algos - 16

    # couleurs pour chaque barre
    couleurs_barres = [
        (231, 76, 60),
        (230, 126, 34),
        (241, 196, 15),
        (46, 204, 113),
        (52, 152, 219),
        (155, 89, 182),
        (26, 188, 156),
    ]

    # graduations sur l'axe Y
    nb_grad = 5
    for i in range(nb_grad + 1):
        y = marge_haut + zone_hauteur - int(zone_hauteur * i / nb_grad)
        val = temps_max * i / nb_grad
        pygame.draw.line(screen, (60, 60, 60), (marge_gauche, y), (marge_gauche + zone_largeur, y), 1)
        label = font_valeur.render(f"{val:.3f}s", True, GRIS)
        screen.blit(label, (marge_gauche - label.get_width() - 8, y - 8))

    # barres
    for i, (name, temps) in enumerate(resultats):
        x = marge_gauche + i * (zone_largeur // nb_algos) + 8
        hauteur_barre = int((temps / temps_max) * zone_hauteur) if temps_max > 0 else 0
        y = marge_haut + zone_hauteur - hauteur_barre

        couleur = couleurs_barres[i % len(couleurs_barres)]
        pygame.draw.rect(screen, couleur, (x, y, largeur_barre, hauteur_barre), border_radius=4)

        # valeur au dessus de la barre
        val_texte = font_valeur.render(f"{temps:.4f}s", True, BLANC)
        screen.blit(val_texte, val_texte.get_rect(center=(x + largeur_barre // 2, y - 14)))

        # nom de l'algo en dessous (rotation simulee par multi-ligne)
        mots = name.split()
        for j, mot in enumerate(mots):
            mot_texte = font_label.render(mot, True, couleur)
            screen.blit(mot_texte, mot_texte.get_rect(center=(x + largeur_barre // 2, marge_haut + zone_hauteur + 20 + j * 18)))

    # label axe Y
    label_y = font_label.render("Temps (secondes)", True, GRIS)
    label_y_rot = pygame.transform.rotate(label_y, 90)
    screen.blit(label_y_rot, (10, marge_haut + zone_hauteur // 2 - label_y_rot.get_height() // 2))

    bouton_rect = dessiner_bouton_retour(screen)
    return bouton_rect


def afficher_menu(screen):
    """Affiche le menu de selection sur la fenetre pygame."""
    screen.fill(NOIR)
    font_titre = pygame.font.SysFont("Arial", 32, bold=True)
    font_option = pygame.font.SysFont("Arial", 22)

    titre = font_titre.render("Les Papyrus de Heron - Visualisation", True, BLANC)
    screen.blit(titre, titre.get_rect(center=(LARGEUR // 2, 80)))

    sous_titre = font_option.render("Choisissez un algorithme de tri :", True, GRIS)
    screen.blit(sous_titre, sous_titre.get_rect(center=(LARGEUR // 2, 140)))

    for key, (name, _) in VISUAL_ALGORITHMS.items():
        y = 200 + int(key) * 50
        texte = font_option.render(f"  {key}. {name}", True, BLANC)
        screen.blit(texte, (250, y))

    comparaison = font_option.render("  8. Comparaison des performances", True, (46, 204, 113))
    screen.blit(comparaison, (250, 200 + 8 * 50))

    quitter = font_option.render("  0. Quitter", True, (255, 100, 100))
    screen.blit(quitter, (250, 200 + 9 * 50))

    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Les Papyrus de Heron - Visualisation des tris")
    clock = pygame.time.Clock()

    en_cours = True
    while en_cours:
        afficher_menu(screen)

        choix = None
        while choix is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    en_cours = False
                    choix = "0"
                elif event.type == pygame.KEYDOWN:
                    touche = event.unicode
                    if touche in VISUAL_ALGORITHMS or touche in ("0", "8"):
                        choix = touche

        if choix == "0":
            break

        if choix == "8":
            bouton_rect = benchmark_graphique(screen)
            if bouton_rect is False:
                break
            attente = True
            while attente:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        en_cours = False
                        attente = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            attente = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if bouton_rect.collidepoint(event.pos):
                            attente = False
            continue

        # generer une liste aleatoire
        arr = list(range(1, NB_ELEMENTS + 1))
        random.shuffle(arr)
        maximum = NB_ELEMENTS

        nom, sort_func = VISUAL_ALGORITHMS[choix]

        # afficher l'etat initial
        dessiner_cercle(screen, arr, maximum, f"{nom} - Etat initial")
        time.sleep(1)

        # lancer le tri visuel avec chronometre
        start_time = time.time()
        resultat = sort_func(arr, screen, maximum, nom)
        temps_tri = time.time() - start_time

        if resultat:
            # afficher le resultat final avec le temps de tri
            dessiner_cercle(screen, arr, maximum, f"{nom} - Trie en {temps_tri:.4f}s")
            bouton_rect = dessiner_bouton_retour(screen)

            # attendre que l'utilisateur clique sur le bouton ou appuie sur R
            attente = True
            while attente:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        en_cours = False
                        attente = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            attente = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if bouton_rect.collidepoint(event.pos):
                            attente = False

    pygame.quit()


if __name__ == "__main__":
    main()
