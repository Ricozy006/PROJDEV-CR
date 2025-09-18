import pygame
import random
import sys

pygame.init()

# Configuration de la fenêtre
LARGEUR, HAUTEUR = 900, 1000
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Autoroute du poulet")
clock = pygame.time.Clock()

# Taille d'une case
TAILLE_CASE = 50
NB_CASES_LARGEUR = LARGEUR // TAILLE_CASE
NB_CASES_HAUTEUR = HAUTEUR // TAILLE_CASE

# Nombre de voies (routes)
NB_VOIES = 7

# Position des voies (en cases Y)
# On espace les voies avec une case d'herbe entre chaque route
VOIES = [2 + i * 2 for i in range(NB_VOIES)]

# Vitesse des voitures par voie (en cases par seconde)
vitesses_voies = {}
for voie in VOIES:
    v = 0
    while v == 0:
        v = random.choice([-2, -1, 1, 2])
    vitesses_voies[voie] = v

# Chargement des images (assurez-vous qu'elles sont dans le dossier)
try:
    poulet_img = pygame.image.load("poulet_img.png").convert_alpha()
    poulet_img = pygame.transform.scale(poulet_img, (TAILLE_CASE, TAILLE_CASE))

    voiture_droite_img = pygame.image.load("car_right.png").convert_alpha()
    voiture_droite_img = pygame.transform.scale(voiture_droite_img, (TAILLE_CASE, TAILLE_CASE))

    voiture_gauche_img = pygame.image.load("car_left.png").convert_alpha()
    voiture_gauche_img = pygame.transform.scale(voiture_gauche_img, (TAILLE_CASE, TAILLE_CASE))
except Exception as e:
    print("Erreur chargement images :", e)
    pygame.quit()
    sys.exit()

# Position du joueur (en cases)
joueur_x = NB_CASES_LARGEUR // 2
joueur_y = NB_CASES_HAUTEUR - 1

# Liste des voitures : chaque voiture est [x_case (float), y_case (int), vitesse (cases/sec)]
voitures = []

# Fonction pour créer des voitures aléatoires sur les voies sans chevauchement initial
def creer_voitures():
    voitures.clear()
    for voie in VOIES:
        nb_voitures_voie = random.randint(2, 4)
        positions_occupees = []
        for _ in range(nb_voitures_voie):
            # Trouver une position x libre sur la voie (en cases flottantes)
            essais = 0
            while True:
                x = random.uniform(0, NB_CASES_LARGEUR)
                # Vérifier qu'aucune voiture n'est trop proche (distance > 1.5 cases)
                if all(abs(x - pos) > 1.5 for pos in positions_occupees):
                    positions_occupees.append(x)
                    break
                essais += 1
                if essais > 100:  # éviter boucle infinie
                    break
            vitesse = vitesses_voies[voie]
            voitures.append([x, voie, vitesse])

creer_voitures()

# Police pour texte
font = pygame.font.SysFont(None, 40)

score = 0
game_over = False

def dessiner_texte(texte, x, y, couleur=(255, 255, 255)):
    img = font.render(texte, True, couleur)
    screen.blit(img, (x, y))

def reset():
    global joueur_x, joueur_y, score, game_over, vitesses_voies
    joueur_x = NB_CASES_LARGEUR // 2
    joueur_y = NB_CASES_HAUTEUR - 1
    score = 0
    game_over = False
    # Réinitialiser vitesses
    for voie in VOIES:
        v = 0
        while v == 0:
            v = random.choice([-2, -1, 1, 2])
        vitesses_voies[voie] = v
    creer_voitures()

while True:
    dt = clock.tick(60) / 1000  # secondes écoulées depuis la dernière frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset()
            if not game_over:
                if event.key == pygame.K_LEFT:
                    joueur_x = max(0, joueur_x - 1)
                elif event.key == pygame.K_RIGHT:
                    joueur_x = min(NB_CASES_LARGEUR - 1, joueur_x + 1)
                elif event.key == pygame.K_UP:
                    joueur_y = max(0, joueur_y - 1)
                elif event.key == pygame.K_DOWN:
                    joueur_y = min(NB_CASES_HAUTEUR - 1, joueur_y + 1)

    if not game_over:
        # Déplacer les voitures
        for voiture in voitures:
            voiture[0] += voiture[2] * dt
            # Rebouclage à l'écran avec gestion anti-chevauchement
            if voiture[2] > 0 and voiture[0] > NB_CASES_LARGEUR:
                voiture[0] = -1
            elif voiture[2] < 0 and voiture[0] < -1:
                voiture[0] = NB_CASES_LARGEUR

        # Empêcher les voitures de se chevaucher en ajustant leur position si trop proches
        for voie in VOIES:
            voitures_voie = [v for v in voitures if v[1] == voie]
            voitures_voie.sort(key=lambda v: v[0])
            for i in range(len(voitures_voie) - 1):
                dist = voitures_voie[i+1][0] - voitures_voie[i][0]
                if dist < 1.5:  # moins de 1.5 cases d'écart
                    # Décaler la voiture suivante pour éviter chevauchement
                    voitures_voie[i+1][0] = voitures_voie[i][0] + 1.5
            # Remettre à jour dans la liste principale
            idx = 0
            for i, v in enumerate(voitures):
                if v[1] == voie:
                    voitures[i] = voitures_voie[idx]
                    idx += 1

        # Vérifier collision joueur-voiture
        joueur_rect = pygame.Rect(joueur_x * TAILLE_CASE, joueur_y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
        for voiture in voitures:
            voiture_rect = pygame.Rect(int(voiture[0] * TAILLE_CASE), voiture[1] * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            if joueur_rect.colliderect(voiture_rect):
                game_over = True
                break

        # Si joueur atteint le haut, augmenter score et remettre en bas
        if joueur_y == 0:
            score += 1
            joueur_y = NB_CASES_HAUTEUR - 1
            # Augmenter légèrement la vitesse des voitures
            for voie in VOIES:
                v = vitesses_voies[voie]
                if v > 0:
                    vitesses_voies[voie] = min(v + 0.5, 5)
                else:
                    vitesses_voies[voie] = max(v - 0.5, -5)
            # Mettre à jour les vitesses des voitures
            for voiture in voitures:
                voie = voiture[1]
                voiture[2] = vitesses_voies[voie]

    # Dessin du fond (herbe + routes séparées par herbe)
    screen.fill((50, 150, 50))  # herbe de fond
    for voie in VOIES:
        pygame.draw.rect(screen, (40, 40, 40), (0, voie * TAILLE_CASE, LARGEUR, TAILLE_CASE))

    # Dessiner voitures
    for voiture in voitures:
        img = voiture_droite_img if voiture[2] > 0 else voiture_gauche_img
        screen.blit(img, (int(voiture[0] * TAILLE_CASE), voiture[1] * TAILLE_CASE))

    # Dessiner joueur
    screen.blit(poulet_img, (joueur_x * TAILLE_CASE, joueur_y * TAILLE_CASE))

    # Afficher score
    dessiner_texte(f"Score : {score}", 10, 10)

    # Message game over
    if game_over:
        dessiner_texte("GAME OVER ! Appuyez sur R pour rejouer", LARGEUR // 6, HAUTEUR // 2, (255, 0, 0))

    pygame.display.flip()
