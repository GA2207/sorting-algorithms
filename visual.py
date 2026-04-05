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

COULEURS_ALGOS = [
    (231, 76, 60),
    (230, 126, 34),
    (241, 196, 15),
    (46, 204, 113),
    (52, 152, 219),
    (155, 89, 182),
    (26, 188, 156),
]


def valeur_vers_couleur(valeur, maximum):
    """Convertit une valeur en couleur HSV (teinte basee sur la valeur)."""
    teinte = valeur / maximum
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


# ======================== FONCTIONS DE DESSIN ========================

def dessiner_cercle(screen, arr, maximum, titre=""):
    """Dessine les elements sous forme de cercle de couleurs."""
    screen.fill(NOIR)
    n = len(arr)

    for i in range(n):
        angle = (2 * math.pi * i / n) - math.pi / 2
        x_ext = CENTRE[0] + RAYON_CERCLE * math.cos(angle)
        y_ext = CENTRE[1] + RAYON_CERCLE * math.sin(angle)
        couleur = valeur_vers_couleur(arr[i], maximum)
        pygame.draw.line(screen, couleur, CENTRE, (int(x_ext), int(y_ext)), 3)

    if titre:
        font = pygame.font.SysFont("Arial", 24, bold=True)
        texte = font.render(titre, True, BLANC)
        screen.blit(texte, texte.get_rect(center=(LARGEUR // 2, 30)))

    pygame.display.flip()


def dessiner_barres(screen, arr, maximum, titre=""):
    """Dessine les elements sous forme de barres verticales colorees."""
    screen.fill(NOIR)
    n = len(arr)
    marge = 50
    zone_largeur = LARGEUR - 2 * marge
    zone_hauteur = HAUTEUR - 120
    largeur_barre = max(1, zone_largeur // n)

    for i in range(n):
        hauteur = int((arr[i] / maximum) * zone_hauteur)
        x = marge + i * largeur_barre
        y = HAUTEUR - 60 - hauteur
        couleur = valeur_vers_couleur(arr[i], maximum)
        pygame.draw.rect(screen, couleur, (x, y, max(1, largeur_barre - 1), hauteur))

    if titre:
        font = pygame.font.SysFont("Arial", 24, bold=True)
        texte = font.render(titre, True, BLANC)
        screen.blit(texte, texte.get_rect(center=(LARGEUR // 2, 30)))

    pygame.display.flip()


def dessiner_bouton_retour(screen):
    """Dessine un bouton 'Retour au menu' en bas de l'ecran."""
    font = pygame.font.SysFont("Arial", 20, bold=True)
    texte = font.render("Retour au menu (Appuyez R)", True, NOIR)
    rect = texte.get_rect(center=(LARGEUR // 2, HAUTEUR - 40))
    bouton_rect = rect.inflate(30, 16)
    pygame.draw.rect(screen, GRIS, bouton_rect, border_radius=8)
    pygame.draw.rect(screen, BLANC, bouton_rect, 2, border_radius=8)
    screen.blit(texte, rect)
    pygame.display.flip()
    return bouton_rect


def attendre_retour(screen, en_cours_ref):
    """Attend que l'utilisateur appuie sur R ou clique sur le bouton retour."""
    bouton_rect = dessiner_bouton_retour(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours_ref[0] = False
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and bouton_rect.collidepoint(event.pos):
                return


# ======================== ALGORITHMES VISUELS (CERCLE) ========================

def visual_selection_sort(arr, screen, maximum, titre, draw_func):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        draw_func(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    return True


def visual_bubble_sort(arr, screen, maximum, titre, draw_func):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        draw_func(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        if not swapped:
            break
    return True


def visual_insertion_sort(arr, screen, maximum, titre, draw_func):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        draw_func(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    return True


def visual_merge_sort(arr, screen, maximum, titre, draw_func):
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

        draw_func(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    return merge_sort_rec(arr, 0, len(arr))


def visual_quick_sort(arr, screen, maximum, titre, draw_func):
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

        draw_func(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if not quick_sort_rec(debut, j):
            return False
        if not quick_sort_rec(i, fin):
            return False
        return True

    return quick_sort_rec(0, len(arr) - 1)


def visual_heap_sort(arr, screen, maximum, titre, draw_func):
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
        draw_func(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    return True


def visual_comb_sort(arr, screen, maximum, titre, draw_func):
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

        draw_func(screen, arr, maximum, titre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    return True


# ======================== DICTIONNAIRE ========================

VISUAL_ALGORITHMS = {
    "1": ("Tri par selection", visual_selection_sort),
    "2": ("Tri a bulles", visual_bubble_sort),
    "3": ("Tri par insertion", visual_insertion_sort),
    "4": ("Tri fusion", visual_merge_sort),
    "5": ("Tri rapide", visual_quick_sort),
    "6": ("Tri par tas", visual_heap_sort),
    "7": ("Tri a peigne", visual_comb_sort),
}


# ======================== BENCHMARK GRAPHIQUE ========================

def benchmark_graphique(screen):
    """Lance les 7 algos, chronometre chacun et affiche un diagramme en barres."""
    from sorting import ALGORITHMS as SORT_ALGORITHMS

    NB_BENCH = 10000
    grosse_liste = [random.randint(1, 100000) for _ in range(NB_BENCH)]

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

    resultats.sort(key=lambda x: x[1])
    dessiner_diagramme_barres(screen, resultats, f"Comparaison des performances ({NB_BENCH} elements)")
    return True


def courbes_multi_tailles(screen):
    """Benchmark sur plusieurs tailles et affiche les courbes d'evolution."""
    from sorting import ALGORITHMS as SORT_ALGORITHMS

    tailles = [100, 500, 1000, 2000, 5000]

    screen.fill(NOIR)
    font = pygame.font.SysFont("Arial", 28, bold=True)
    texte = font.render("Benchmark multi-tailles en cours...", True, BLANC)
    screen.blit(texte, texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 2)))
    pygame.display.flip()

    # resultats[nom_algo] = [(taille, temps), ...]
    resultats = {}
    for key, (name, sort_func) in SORT_ALGORITHMS.items():
        resultats[name] = []

    for taille in tailles:
        grosse_liste = [random.randint(1, 100000) for _ in range(taille)]
        for key, (name, sort_func) in SORT_ALGORITHMS.items():
            liste_copie = grosse_liste.copy()
            start = time.time()
            sort_func(liste_copie)
            temps = time.time() - start
            resultats[name].append((taille, temps))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

    # ======================== DESSINER LES COURBES ========================
    screen.fill(NOIR)

    font_titre = pygame.font.SysFont("Arial", 24, bold=True)
    font_label = pygame.font.SysFont("Arial", 13)
    font_legende = pygame.font.SysFont("Arial", 14, bold=True)

    titre = font_titre.render("Evolution du temps selon la taille de la liste", True, BLANC)
    screen.blit(titre, titre.get_rect(center=(LARGEUR // 2, 30)))

    marge_gauche = 90
    marge_droite = 180
    marge_haut = 70
    marge_bas = 80
    zone_largeur = LARGEUR - marge_gauche - marge_droite
    zone_hauteur = HAUTEUR - marge_haut - marge_bas

    # axes
    pygame.draw.line(screen, BLANC, (marge_gauche, marge_haut), (marge_gauche, marge_haut + zone_hauteur), 2)
    pygame.draw.line(screen, BLANC, (marge_gauche, marge_haut + zone_hauteur), (marge_gauche + zone_largeur, marge_haut + zone_hauteur), 2)

    # trouver le temps max pour l'echelle
    temps_max = max(t for points in resultats.values() for _, t in points)
    taille_max = max(tailles)

    # graduations axe Y
    nb_grad_y = 5
    for i in range(nb_grad_y + 1):
        y = marge_haut + zone_hauteur - int(zone_hauteur * i / nb_grad_y)
        val = temps_max * i / nb_grad_y
        pygame.draw.line(screen, (50, 50, 50), (marge_gauche, y), (marge_gauche + zone_largeur, y), 1)
        label = font_label.render(f"{val:.3f}s", True, GRIS)
        screen.blit(label, (marge_gauche - label.get_width() - 8, y - 8))

    # graduations axe X
    for taille in tailles:
        x = marge_gauche + int((taille / taille_max) * zone_largeur)
        pygame.draw.line(screen, (50, 50, 50), (x, marge_haut), (x, marge_haut + zone_hauteur), 1)
        label = font_label.render(str(taille), True, GRIS)
        screen.blit(label, label.get_rect(center=(x, marge_haut + zone_hauteur + 20)))

    # label axes
    label_x = font_label.render("Nombre d'elements", True, GRIS)
    screen.blit(label_x, label_x.get_rect(center=(marge_gauche + zone_largeur // 2, marge_haut + zone_hauteur + 50)))

    label_y = font_label.render("Temps (secondes)", True, GRIS)
    label_y_rot = pygame.transform.rotate(label_y, 90)
    screen.blit(label_y_rot, (10, marge_haut + zone_hauteur // 2 - label_y_rot.get_height() // 2))

    # dessiner les courbes
    algo_names = list(resultats.keys())
    for idx, name in enumerate(algo_names):
        couleur = COULEURS_ALGOS[idx % len(COULEURS_ALGOS)]
        points_ecran = []
        for taille, temps in resultats[name]:
            x = marge_gauche + int((taille / taille_max) * zone_largeur)
            y = marge_haut + zone_hauteur - int((temps / temps_max) * zone_hauteur) if temps_max > 0 else marge_haut + zone_hauteur
            points_ecran.append((x, y))

        # tracer la ligne
        if len(points_ecran) >= 2:
            pygame.draw.lines(screen, couleur, False, points_ecran, 3)

        # tracer les points
        for pt in points_ecran:
            pygame.draw.circle(screen, couleur, pt, 5)

        # legende a droite
        y_legende = marge_haut + 10 + idx * 25
        pygame.draw.line(screen, couleur, (marge_gauche + zone_largeur + 15, y_legende + 6), (marge_gauche + zone_largeur + 35, y_legende + 6), 3)
        legende = font_legende.render(name, True, couleur)
        screen.blit(legende, (marge_gauche + zone_largeur + 40, y_legende))

    pygame.display.flip()
    return True


def dessiner_diagramme_barres(screen, resultats, titre_text):
    """Dessine un diagramme en barres a partir des resultats."""
    screen.fill(NOIR)

    font_titre = pygame.font.SysFont("Arial", 26, bold=True)
    font_label = pygame.font.SysFont("Arial", 14, bold=True)
    font_valeur = pygame.font.SysFont("Arial", 13)

    titre = font_titre.render(titre_text, True, BLANC)
    screen.blit(titre, titre.get_rect(center=(LARGEUR // 2, 40)))

    marge_gauche = 80
    marge_droite = 40
    marge_haut = 90
    marge_bas = 120
    zone_largeur = LARGEUR - marge_gauche - marge_droite
    zone_hauteur = HAUTEUR - marge_haut - marge_bas

    pygame.draw.line(screen, BLANC, (marge_gauche, marge_haut), (marge_gauche, marge_haut + zone_hauteur), 2)
    pygame.draw.line(screen, BLANC, (marge_gauche, marge_haut + zone_hauteur), (marge_gauche + zone_largeur, marge_haut + zone_hauteur), 2)

    temps_max = max(t for _, t in resultats)
    nb_algos = len(resultats)
    largeur_barre = zone_largeur // nb_algos - 16

    nb_grad = 5
    for i in range(nb_grad + 1):
        y = marge_haut + zone_hauteur - int(zone_hauteur * i / nb_grad)
        val = temps_max * i / nb_grad
        pygame.draw.line(screen, (60, 60, 60), (marge_gauche, y), (marge_gauche + zone_largeur, y), 1)
        label = font_valeur.render(f"{val:.3f}s", True, GRIS)
        screen.blit(label, (marge_gauche - label.get_width() - 8, y - 8))

    for i, (name, temps) in enumerate(resultats):
        x = marge_gauche + i * (zone_largeur // nb_algos) + 8
        hauteur_barre = int((temps / temps_max) * zone_hauteur) if temps_max > 0 else 0
        y = marge_haut + zone_hauteur - hauteur_barre

        couleur = COULEURS_ALGOS[i % len(COULEURS_ALGOS)]
        pygame.draw.rect(screen, couleur, (x, y, largeur_barre, hauteur_barre), border_radius=4)

        val_texte = font_valeur.render(f"{temps:.4f}s", True, BLANC)
        screen.blit(val_texte, val_texte.get_rect(center=(x + largeur_barre // 2, y - 14)))

        mots = name.split()
        for j, mot in enumerate(mots):
            mot_texte = font_label.render(mot, True, couleur)
            screen.blit(mot_texte, mot_texte.get_rect(center=(x + largeur_barre // 2, marge_haut + zone_hauteur + 20 + j * 18)))

    label_y = font_label.render("Temps (secondes)", True, GRIS)
    label_y_rot = pygame.transform.rotate(label_y, 90)
    screen.blit(label_y_rot, (10, marge_haut + zone_hauteur // 2 - label_y_rot.get_height() // 2))

    pygame.display.flip()


# ======================== MENU ========================

def afficher_menu(screen):
    """Affiche le menu de selection sur la fenetre pygame."""
    screen.fill(NOIR)
    font_titre = pygame.font.SysFont("Arial", 32, bold=True)
    font_option = pygame.font.SysFont("Arial", 22)
    font_section = pygame.font.SysFont("Arial", 18)

    titre = font_titre.render("Les Papyrus de Heron - Visualisation", True, BLANC)
    screen.blit(titre, titre.get_rect(center=(LARGEUR // 2, 60)))

    # section visualisation cercle
    section1 = font_section.render("--- Visualisation cercle (appuyez C puis le numero) ---", True, GRIS)
    screen.blit(section1, section1.get_rect(center=(LARGEUR // 2, 120)))

    for key, (name, _) in VISUAL_ALGORITHMS.items():
        y = 130 + int(key) * 35
        texte = font_option.render(f"  {key}. {name}", True, BLANC)
        screen.blit(texte, (250, y))

    # section visualisation barres
    section2 = font_section.render("--- Visualisation barres (appuyez B puis le numero) ---", True, GRIS)
    screen.blit(section2, section2.get_rect(center=(LARGEUR // 2, 410)))

    info_barres = font_option.render("  Meme algos, vue en barres verticales", True, (52, 152, 219))
    screen.blit(info_barres, (200, 440))

    # section benchmark
    section3 = font_section.render("--- Benchmarks ---", True, GRIS)
    screen.blit(section3, section3.get_rect(center=(LARGEUR // 2, 500)))

    bench1 = font_option.render("  8. Comparaison des performances", True, (46, 204, 113))
    screen.blit(bench1, (250, 530))

    bench2 = font_option.render("  9. Courbes multi-tailles", True, (46, 204, 113))
    screen.blit(bench2, (250, 565))

    quitter = font_option.render("  0. Quitter", True, (255, 100, 100))
    screen.blit(quitter, (250, 630))

    pygame.display.flip()


# ======================== BOUCLE PRINCIPALE ========================

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Les Papyrus de Heron - Visualisation des tris")

    en_cours = [True]
    mode = None  # "cercle" ou "barres"

    while en_cours[0]:
        afficher_menu(screen)
        mode = None

        choix = None
        while choix is None and en_cours[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    en_cours[0] = False
                    choix = "0"
                elif event.type == pygame.KEYDOWN:
                    touche = event.unicode
                    if touche == "c":
                        mode = "cercle"
                    elif touche == "b":
                        mode = "barres"
                    elif touche in ("8", "9", "0"):
                        choix = touche
                    elif touche in VISUAL_ALGORITHMS and mode:
                        choix = touche

        if choix == "0" or not en_cours[0]:
            break

        # benchmark diagramme en barres
        if choix == "8":
            result = benchmark_graphique(screen)
            if result:
                attendre_retour(screen, en_cours)
            continue

        # courbes multi-tailles
        if choix == "9":
            result = courbes_multi_tailles(screen)
            if result:
                attendre_retour(screen, en_cours)
            continue

        # tri visuel
        if choix in VISUAL_ALGORITHMS and mode:
            arr = list(range(1, NB_ELEMENTS + 1))
            random.shuffle(arr)
            maximum = NB_ELEMENTS
            nom, sort_func = VISUAL_ALGORITHMS[choix]

            draw_func = dessiner_cercle if mode == "cercle" else dessiner_barres

            draw_func(screen, arr, maximum, f"{nom} - Etat initial")
            time.sleep(1)

            start_time = time.time()
            resultat = sort_func(arr, screen, maximum, nom, draw_func)
            temps_tri = time.time() - start_time

            if resultat:
                draw_func(screen, arr, maximum, f"{nom} - Trie en {temps_tri:.4f}s")
                attendre_retour(screen, en_cours)

    pygame.quit()


if __name__ == "__main__":
    main()
