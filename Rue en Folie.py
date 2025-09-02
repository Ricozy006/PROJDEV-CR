"""
Nom du projet : Rue en Folie - Smooth Cars No Overlap Fixed
Auteur       : Rafael Rico et Luca Giubbilei
Date         : 02/09/2025
Version      : 1.6
Description  : Jeu Python avec routes, voitures lisses, joueur bloc par bloc, et voitures qui ne se chevauchent jamais
"""

import pygame
import random

pygame.init()

# Fenêtre de jeu
L, H = 800, 600
fenetre = pygame.display.set_mode((L, H))
pygame.display.set_caption("Rue en Folie - Smooth Cars No Overlap")

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

# Création des voitures avec distance minimale entre elles
cubes = []
min_gap = 2 * cell_size  # distance minimale entre voitures sur la même lane
for row in lanes:
    num_cars = random.randint(2, 4)
    direction = random.choice([-1, 1])
    speeds = [random.uniform(2, 6) for _ in range(num_cars)]
    # Répartir les voitures avec un espacement minimal
    positions = [i * (L // num_cars) for i in range(num_cars)]
    random.shuffle(positions)
    for i in range(num_cars):
        cubes.append({
            "x": positions[i],
            "row": row,
            "vx": direction * speeds[i]
        })

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
    for row in lanes:
        # Extraire les voitures de cette lane
        lane_cars = [c for c in cubes if c["row"] == row]
        for car in lane_cars:
            car["x"] += car["vx"]
            # Wrap-around
            if car["vx"] > 0 and car["x"] > L:
                car["x"] = -cell_size
            elif car["vx"] < 0 and car["x"] < -cell_size:
                car["x"] = L

        # Vérifier et corriger chevauchement minimal
        lane_cars.sort(key=lambda c: c["x"])
        for i in range(len(lane_cars)):
            next_i = (i + 1) % len(lane_cars)
            car = lane_cars[i]
            next_car = lane_cars[next_i]
            gap = (next_car["x"] - car["x"]) % L
            if gap < min_gap:
                # Ajuster la voiture suivante pour maintenir l'écart minimal
                if car["vx"] > 0:
                    next_car["x"] = (car["x"] + min_gap) % L
                else:
                    car["x"] = (next_car["x"] + min_gap) % L

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
