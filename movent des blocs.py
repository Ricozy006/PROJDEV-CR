# Code trouvé sur internet


import pygame

pygame.init()
L, H = 800, 600
fenetre = pygame.display.set_mode((L, H))

# position du cube
x, y = 100, H//2
vx = 5  # vitesse horizontale

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # déplace le cube
    x += vx

    # rebond sur les bords
    if x <= 0 or x >= L-20:
        vx = -vx

    # affichage
    fenetre.fill((0,0,0))
    pygame.draw.rect(fenetre, (200,0,0), (x, y, 20, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
