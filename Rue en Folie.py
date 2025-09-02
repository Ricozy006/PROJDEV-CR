"""
Nom du projet : Rue en Folie - Grille et obstacles
Auteur       : Rafael Rico et Luca Giubbilei
Date         : 02/09/2025
Version      : 1.0
Description  : Jeu Python avec joueur sur grille et cubes obstacles en mouvement
"""

import pygame
import random

pygame.init()

# ---------------- Fenêtre ----------------
LARGEUR_FENETRE, HAUTEUR_FENETRE = 800, 600
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Rue en Folie - Grille et Obstacles")

# ---------------- Couleurs ----------------
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
ROUGE = (200, 0, 0)
VERT = (50, 150, 50)
GRIS = (200, 200, 200)

# ---------------- Grille ----------------
TAILLE_CASE = 50
COLONNES = LARGEUR_FENETRE // TAILLE_CASE
LIGNES = HAUTEUR_FENETRE // TAILLE_CASE

# Position initiale du joueur (en cases)
player_col, player_row = COLONNES // 2, LIGNES - 1

# ---------------- Lanes pour obstacles ----------------
lanes = [2, 4, 6, 8, 10]  # ligne sur la grille
lane_y = [row * TAILLE_CASE for row in lanes]

# ---------------- Cubes obstacles ----------------
num_cubes = 7
cube_size = 50
cubes = []
for i in range(num_cubes):
    lane = random.choice(lane_y)
    vx = random.choice([-1, 1]) * random.randint(3, 6)
    x = random.randint(0, LARGEUR_FENETRE - cube_size)
    cubes.append({"x": x, "y": lane, "vx": vx})

# ---------------- Boucle principale ----------------
clock = pygame.time.Clock()
running = True
move_cooldown = 0
move_delay = 150  # ms entre chaque mouvement joueur

while running:
    dt = clock.tick(60)
    move_cooldown -= dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Déplacement joueur bloc par bloc ---
    keys = pygame.key.get_pressed()
    if move_cooldown <= 0:
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_row = max(0, player_row - 1)
            move_cooldown = move_delay
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_row = min(LIGNES - 1, player_row + 1)
            move_cooldown = move_delay
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_col = max(0, player_col - 1)
            move_cooldown = move_delay
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_col = min(COLONNES - 1, player_col + 1)
            move_cooldown = move_delay

    # --- Déplacement cubes ---
    for cube in cubes:
        cube["x"] += cube["vx"]
        # Wrap around
        if cube["vx"] > 0 and cube["x"] > LARGEUR_FENETRE:
            cube["x"] = -cube_size
        elif cube["vx"] < 0 and cube["x"] < -cube_size:
            cube["x"] = LARGEUR_FENETRE

    # --- Détection collision ---
    player_rect = pygame.Rect(player_col*TAILLE_CASE, player_row*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
    collision = any(player_rect.colliderect(pygame.Rect(c["x"], c["y"], cube_size, cube_size)) for c in cubes)
    if collision:
        print("Collision ! Game Over.")
        running = False

    # --- Affichage ---
    fenetre.fill(VERT)

    # Dessiner grille
    for i in range(COLONNES):
        for j in range(LIGNES):
            pygame.draw.rect(fenetre, GRIS, (i*TAILLE_CASE, j*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)

    # Dessiner cubes obstacles
    for cube in cubes:
        pygame.draw.rect(fenetre, ROUGE, (cube["x"], cube["y"], cube_size, cube_size))

    # Dessiner joueur
    pygame.draw.rect(fenetre, BLEU, (player_col*TAILLE_CASE, player_row*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
##
    pygame.display.flip()

pygame.quit()
