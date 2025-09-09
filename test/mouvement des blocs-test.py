import pygame, random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autoroute de cubes")
clock = pygame.time.Clock()

# --- paramètres faciles à modifier ---
NUM_CUBES = 4 #nombres de cubes
CUBE_SIZE = 40
LANES = [100, 145, 250, 320, 420]   # positions centrales (y) des "bandes" (voies) la bonne distance serrait de 45
LANE_HEIGHT = CUBE_SIZE    # hauteur de chaque bande noire
# --------------------------------------

# Création des cubes : chaque cube a x, y (centre de la voie) et vx (vitesse)
cubes = []
for _ in range(NUM_CUBES):
    y = random.choice(LANES)
    x = random.randint(1, WIDTH - CUBE_SIZE)
    vx = random.choice([-1, 1]) * random.randint(1, 6)
    cubes.append({"x": x, "y": y, "vx": vx})

running = True
while running:
    # 1) gestion des événements (fenêtre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2) mise à jour des positions (déplacement + bouclage à l'écran)
    for c in cubes:
        c["x"] += c["vx"]
        # si dépasse la droite -> réapparaît à gauche (et vice-versa)
        if c["vx"] > 0 and c["x"] > WIDTH:
            c["x"] = -CUBE_SIZE
        elif c["vx"] < 0 and c["x"] < -CUBE_SIZE:
            c["x"] = WIDTH

    # 3) dessin
    screen.fill((50, 150, 50))  # fond vert (herbe)

    # dessiner chaque "voie" noire (autoroute)
    for lane_y in LANES:
        lane_rect = pygame.Rect(0, lane_y - LANE_HEIGHT // 2, WIDTH, LANE_HEIGHT)
        pygame.draw.rect(screen, (20, 20, 20), lane_rect)  # couleur noire/gris foncé

        # petites lignes centrales en pointillés (optionnel)
        dash_w = 40
        gap = 20
        # for x in range(0, WIDTH, dash_w + gap):
        #     dash_rect = pygame.Rect(x, lane_y - 3, dash_w, 6)
        #     pygame.draw.rect(screen, (255, 215, 0), dash_rect)  # jaune (marquage)

    # dessiner les cubes (on centre verticalement le carré sur la voie)
    for c in cubes:
        rect = pygame.Rect(int(c["x"]), int(c["y"] - CUBE_SIZE // 2), CUBE_SIZE, CUBE_SIZE)
        pygame.draw.rect(screen, (200, 0, 0), rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()