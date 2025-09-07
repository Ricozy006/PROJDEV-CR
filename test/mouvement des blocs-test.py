"""
Nom du projet : Rue en Folie - Grille et obstacles
Auteur       : Rafael Rico et Luca Giubbilei
Date         : 02/09/2025
Version      : 1.0
Description  : jeu pour tester les mouvements des blocs
"""

# Généré par chatGPT

import pygame
import random

pygame.init()
L, H = 800, 600
fenetre = pygame.display.set_mode((800, 600))

# Paramètres
num_cubes = 5      # nombre de cubes
cube_size = 40     # longueur et largeur d'un cube
lanes = [100, 200, 300, 400]  # positions des lignes (y)

# Création des cubes : liste de dictionnaires
cubes = []
for i in range(num_cubes):
    cube = {
        "x": random.randint(0, L - cube_size),        # position horizontale aléatoire
        "y": random.choice(lanes),                     # position verticale sur une ligne aléatoire
        "vx": random.choice([-1, 1]) * random.randint(1,8)  # vitesse horizontale aléatoire (droite ou gauche)
    }
    cubes.append(cube)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement des cubes
    for cube in cubes:
        cube["x"] += cube["vx"]

        # Bouclage à l'écran (comme dans Crossy Road)
        if cube["vx"] > 0 and cube["x"] > L:
            cube["x"] = -cube_size
        elif cube["vx"] < 0 and cube["x"] < -cube_size:
            cube["x"] = L

    # Fenêtre
    fenetre.fill((50, 150, 50))  # fond vert
    for cube in cubes:
        pygame.draw.rect(fenetre, (200, 0, 0), (cube["x"], cube["y"], cube_size, cube_size))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()