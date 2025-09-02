

import pygame
import random

pygame.init()
L, H = 800, 600
fenetre = pygame.display.set_mode((L, H))

# Parameters
num_cubes = 5      # number of moving cubes
cube_size = 40      # width and height
lanes = [100, 200, 300, 400, 500]  # y positions for lanes

# Create cubes: list of dictionaries
cubes = []
for i in range(num_cubes):
    cube = {
        "x": random.randint(0, L - cube_size),
        "y": random.choice(lanes),
        "vx": random.choice([-1, 1]) * random.randint(3, 8)
    }
    cubes.append(cube)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move cubes
    for cube in cubes:
        cube["x"] += cube["vx"]

        # Wrap around screen (like Crossy Road)
        if cube["vx"] > 0 and cube["x"] > L:
            cube["x"] = -cube_size
        elif cube["vx"] < 0 and cube["x"] < -cube_size:
            cube["x"] = L

    # Draw everything
    fenetre.fill((50, 150, 50))  # green background
    for cube in cubes:
        pygame.draw.rect(fenetre, (200, 0, 0), (cube["x"], cube["y"], cube_size, cube_size))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
