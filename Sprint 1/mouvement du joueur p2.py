"""
Nom du projet : mouvement du joueur (Version grille)
Auteur       : Rafael Rico et Luca Giubbilei
Date         : 02/09/2025
Version      : 1.1
Description  : Jeu en Python avec grille visible et mouvement du joueur case par case
"""

import pygame

pygame.init()

# Configuration de la fenêtre
LARGEUR_FENETRE, HAUTEUR_FENETRE = 600, 400
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Rue en Folie - Grille")

# Couleurs
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
GRIS = (200, 200, 200)

# Taille de la grille
TAILLE_CASE = 50
COLONNES = LARGEUR_FENETRE // TAILLE_CASE
LIGNES = HAUTEUR_FENETRE // TAILLE_CASE

# Position initiale (en cases)
x_case, y_case = COLONNES // 2, LIGNES // 2

clock = pygame.time.Clock()
en_cours = True

while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    # Déplacement du joueur
    touches = pygame.key.get_pressed()
    if touches[pygame.K_UP] or touches[pygame.K_w]:
        y_case = max(0, y_case - 1)
    if touches[pygame.K_DOWN] or touches[pygame.K_s]:
        y_case = min(LIGNES - 1, y_case + 1)
    if touches[pygame.K_LEFT] or touches[pygame.K_a]:
        x_case = max(0, x_case - 1)
    if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
        x_case = min(COLONNES - 1, x_case + 1)

    # Affichage
    fenetre.fill(BLANC)

    # Dessiner la grille
    for i in range(COLONNES):
        for j in range(LIGNES):
            pygame.draw.rect(
                fenetre, GRIS,
                (i * TAILLE_CASE, j * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE),
                1  # largeur du contour
            )

    # Dessiner le joueur
    pygame.draw.rect(
        fenetre,
        BLEU,
        (x_case * TAILLE_CASE, y_case * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
    )

    pygame.display.flip()
    clock.tick(10)  # vitesse de déplacement

pygame.quit()
