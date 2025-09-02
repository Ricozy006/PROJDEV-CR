"""
Nom du projet : mouvement du joueur
Auteur       : Rafael Rico et Luca Giubbilei
Date         : 02/09/2025
Version      : 1.0
Description  : Petit jeu en Python où vous devez traverser des obstacles sans être touché
"""

import pygame

pygame.init()

# fênetre de jeu
fenetre = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Rue en Folie")

# les couleurs
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)

# le carré
x, y = 300, 200
taille = 50
vitesse = 5

clock = pygame.time.Clock()
en_cours = True

while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    # touches pour les movements (générée par ChatGPT )
    touches = pygame.key.get_pressed()

    if touches[pygame.K_UP] or touches[pygame.K_w]:
        y -= vitesse
    if touches[pygame.K_DOWN] or touches[pygame.K_s]:
        y += vitesse
    if touches[pygame.K_LEFT] or touches[pygame.K_a]:
        x -= vitesse
    if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
        x += vitesse

    # affichage
    fenetre.fill(BLANC)
    pygame.draw.rect(fenetre, BLEU, (x, y, taille, taille))
    pygame.display.flip()
    clock.tick(40)

pygame.quit()
