"""
Nom du projet : Rue en Folie - Lanes Smooth Cars No Overlap
Auteur       : Rafael Rico et Luca Giubbilei
Date         : 02/09/2025
Version      : 1.5
Description  : Jeu Python avec routes, voitures lisses, joueur bloc par bloc, et voitures qui ne se chevauchent pas
"""

import pygame
import random

pygame.init()

# Fenêtre de jeu
L, H = 800, 600
fenetre = pygame.display.set_mode((L, H))
pygame.display.set_caption("Rue en Folie - No Car Overlap")

# Couleurs
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
ROUGE = (200, 0, 0)
VERT = (50, 150, 50)
GRIS = (100, 100, 100)

# Paramètres grille
cell_size = 50
cols = L // cell_size
rows = H // cell_size

# Lignes de routes (où les voitures circulent)
lanes = [2, 4, 6, 8, 10]

# Cubes obstacles (voitures) - pas de chevauchement
cubes = []
for row in lanes:
    num_cars = random.randint(2, 4)
    spacing = L // num_cars  # espace minimum entre les voitures
    for i in range(num_cars):
        vx = random.choice([-1, 1]) * random.uniform(2, 6)
        x = i * spacing
        cubes.append({"x": x, "row": row, "vx": vx})

# Spawn joueur en position sûre
safe = False
while not safe:
    player_pos = [cols // 2, rows - 1]
    safe = all(player_pos[0]*cell_size != int(c["x"]) or player_pos[1] != c["row"] for c in cubes)

clock = pygame.time.Clock()
running = True
move_cooldown = 0
move_delay = 150

while running:
    dt = clock.tick(60)
    move_cooldown -= dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement joueur bloc par bloc
    touches = pygame.key.get_pressed()
    if move_cooldown <= 0:
        if touches[pygame.K_UP] or touches[pygame.K_w]:
            player_pos[1] -= 1
            move_cooldown = move_delay
        elif touches[pygame.K_DOWN] or touches[pygame.K_s]:
            player_pos[1] += 1
            move_cooldown = move_delay
        elif touches[pygame.K_LEFT] or touches[pygame.K_a]:
            player_pos[0] -= 1
            move_cooldown = move_delay
        elif touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            player_pos[0] += 1
            move_cooldown = move_delay

    # Limites grille
    player_pos[0] = max(0, min(cols - 1, player_pos[0]))
    player_pos[1] = max(0, min(rows - 1, player_pos[1]))

    # Déplacement des voitures (smooth) sans chevauchement
    for cube in cubes:
        cube["x"] += cube["vx"]
        if cube["vx"] > 0 and cube["x"] > L:
            cube["x"] = -cell_size
        elif cube["vx"] < 0 and cube["x"] < -cell_size:
            cube["x"] = L

    # Détection collision
    collision = any(player_pos[0]*cell_size == int(c["x"]) and player_pos[1] == c["row"] for c in cubes)
    if collision:
        print("Collision ! Game Over.")
        running = False

    # Vérifier victoire
    if player_pos[1] <= 0:
        print("Bravo ! Vous avez traversé la rue !")
        running = False

    # Affichage
    fenetre.fill(VERT)

    # Dessiner routes
    for row in lanes:
        pygame.draw.rect(fenetre, GRIS, (0, row*cell_size, L, cell_size))

    # Dessiner grille
    for i in range(cols):
        for j in range(rows):
            pygame.draw.rect(fenetre, BLANC, (i * cell_size, j * cell_size, cell_size, cell_size), 1)

    # Dessiner joueur
    pygame.draw.rect(fenetre, BLEU, (player_pos[0]*cell_size, player_pos[1]*cell_size, cell_size, cell_size))

    # Dessiner voitures
    for cube in cubes:
        pygame.draw.rect(fenetre, ROUGE, (cube["x"], cube["row"]*cell_size, cell_size, cell_size))

    pygame.display.flip()

pygame.quit()
