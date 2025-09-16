import pygame, random

pygame.init()
WIDTH, HEIGHT = 900, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autoroute de cubes")
clock = pygame.time.Clock()

NUM_CUBES = 15
CUBE_SIZE = 40
LANES = [100, 145, 250, 320, 420]

# Définir la vitesse par voie (positive = droite, négative = gauche)
lane_speeds = {
    100: 5,
    145: -3,
    250: 8,
    320: -6,
    420: 4
}


cubes = []
for _ in range(NUM_CUBES):
    y = random.choice(LANES)
    x = random.randint(0, WIDTH - CUBE_SIZE)
    vx = lane_speeds[y]
    cubes.append({"x": x, "y": y, "vx": vx, "stop_time": 0})


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    for c in cubes:
        current_time = pygame.time.get_ticks()

        # Si le cube est en pause (moins d'une seconde écoulée depuis stop_time)
        if current_time - c["stop_time"] < 1000:
            continue  # Cube attend, ne bouge pas

        # Bouge le cube
        c["x"] += c["vx"]

        # Si cube sort à droite
        if c["x"] > WIDTH:
            c["x"] = -CUBE_SIZE
            c["stop_time"] = current_time  # Pause 1 sec avant de repartir

        # Si cube sort à gauche
        elif c["x"] < -CUBE_SIZE:
            c["x"] = WIDTH
            c["stop_time"] = current_time  # Pause 1 sec avant de repartir

    screen.fill((50, 150, 50))

    for lane_y in LANES:
        pygame.draw.rect(screen, (20, 20, 20), (0, lane_y - CUBE_SIZE//2, WIDTH, CUBE_SIZE))

    for c in cubes:
        pygame.draw.rect(screen, (200, 0, 0), (int(c["x"]), int(c["y"] - CUBE_SIZE//2), CUBE_SIZE, CUBE_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
