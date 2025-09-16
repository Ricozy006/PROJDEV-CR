"""
Nom du projet : Rue en Folie - Grille et obstacles
Auteur       : Rafael Rico et Luca Giubbilei
Date         : 02/09/2025
Version      : 2.0
Description  : Jeu Python avec joueur sur grille et cubes obstacles en mouvement,
               connexion utilisateur avec SQLite et leaderboard.
"""

import pygame
import random
import time
from test import db

pygame.init()
db.init_db()  # Initialisation DB

# ---------------- Fenêtre ----------------
LARGEUR_FENETRE, HAUTEUR_FENETRE = 800, 600
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Rue en Folie - Grille et Obstacles")

# ---------------- Couleurs ----------------
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
ROUGE = (200, 0, 0)
VERT = (50, 150, 50)
GRIS = (200, 200, 200)
NOIR = (0, 0, 0)

# ---------------- Grille ----------------
TAILLE_CASE = 50
COLONNES = LARGEUR_FENETRE // TAILLE_CASE
LIGNES = HAUTEUR_FENETRE // TAILLE_CASE


# ===================================================
# Classe InputBox (saisie texte)
# ===================================================
class InputBox:
    def __init__(self, x, y, w, h, is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLANC
        self.text = ''
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False
        self.is_password = is_password

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            display_text = '*' * len(self.text) if self.is_password else self.text
            self.txt_surface = self.font.render(display_text, True, self.color)
        return None

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


# ===================================================
# Écran login / register
# ===================================================
def login_screen():
    font = pygame.font.Font(None, 40)

    username_box = InputBox(300, 150, 200, 40)
    password_box = InputBox(300, 220, 200, 40, is_password=True)
    input_boxes = [username_box, password_box]

    login_btn = pygame.Rect(250, 300, 120, 50)
    register_btn = pygame.Rect(430, 300, 120, 50)

    error_msg = ""
    user_id = None
    running = True
    while running:
        fenetre.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_btn.collidepoint(event.pos):
                    user_id = db.login(username_box.text, password_box.text)
                    if user_id:
                        running = False
                    else:
                        error_msg = "❌ Login échoué"
                elif register_btn.collidepoint(event.pos):
                    user_id = db.create_user(username_box.text, password_box.text)
                    if user_id:
                        running = False
                    else:
                        error_msg = "⚠️ Username déjà pris"

        # Labels
        fenetre.blit(font.render("Username:", True, BLANC), (150, 155))
        fenetre.blit(font.render("Password:", True, BLANC), (150, 225))

        # Dessiner champs
        for box in input_boxes:
            box.draw(fenetre)

        # Boutons
        pygame.draw.rect(fenetre, (0, 200, 0), login_btn)
        pygame.draw.rect(fenetre, (0, 0, 200), register_btn)
        fenetre.blit(font.render("Login", True, BLANC), (login_btn.x + 20, login_btn.y + 10))
        fenetre.blit(font.render("Register", True, BLANC), (register_btn.x + 5, register_btn.y + 10))

        # Message d’erreur
        if error_msg:
            fenetre.blit(font.render(error_msg, True, ROUGE), (200, 380))

        pygame.display.flip()
    return user_id


# ===================================================
# Écran leaderboard
# ===================================================
def leaderboard_screen():
    fenetre.fill(NOIR)
    font = pygame.font.Font(None, 48)
    title = font.render("🏆 Leaderboard 🏆", True, (255, 215, 0))
    fenetre.blit(title, (LARGEUR_FENETRE // 2 - title.get_width() // 2, 50))

    highscores = db.get_highscores(5)
    font_small = pygame.font.Font(None, 36)
    y = 150
    for i, (name, score) in enumerate(highscores, start=1):
        text = font_small.render(f"{i}. {name} - {score}", True, BLANC)
        fenetre.blit(text, (LARGEUR_FENETRE // 2 - text.get_width() // 2, y))
        y += 50

    instr = font_small.render("Appuyez sur ESPACE pour quitter", True, GRIS)
    fenetre.blit(instr, (LARGEUR_FENETRE // 2 - instr.get_width() // 2, 500))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


# ===================================================
# Jeu principal
# ===================================================
def play_game(user_id):
    player_col, player_row = COLONNES // 2, LIGNES - 1

    # Obstacles
    lanes = [2, 4, 6, 8, 10]
    lane_y = [row * TAILLE_CASE for row in lanes]
    num_cubes = 7
    cube_size = 50
    cubes = []
    for i in range(num_cubes):
        lane = random.choice(lane_y)
        vx = random.choice([-1, 1]) * random.randint(3, 6)
        x = random.randint(0, LARGEUR_FENETRE - cube_size)
        cubes.append({"x": x, "y": lane, "vx": vx})

    clock = pygame.time.Clock()
    running = True
    move_cooldown = 0
    move_delay = 150
    start_time = time.time()

    while running:
        dt = clock.tick(60)
        move_cooldown -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Déplacement joueur
        keys = pygame.key.get_pressed()
        if move_cooldown <= 0:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_row = max(0, player_row - 1)
                move_cooldown = move_delay
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_row = min(LIGNES - 1, player_row + 1)
                move_cooldown = move_delay
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_col = max(0, player_col - 1)
                move_cooldown = move_delay
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_col = min(COLONNES - 1, player_col + 1)
                move_cooldown = move_delay

        # Déplacement obstacles
        for cube in cubes:
            cube["x"] += cube["vx"]
            if cube["vx"] > 0 and cube["x"] > LARGEUR_FENETRE:
                cube["x"] = -cube_size
            elif cube["vx"] < 0 and cube["x"] < -cube_size:
                cube["x"] = LARGEUR_FENETRE

        # Collision
        player_rect = pygame.Rect(player_col * TAILLE_CASE, player_row * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
        collision = any(player_rect.colliderect(pygame.Rect(c["x"], c["y"], cube_size, cube_size)) for c in cubes)
        if collision:
            elapsed = int(time.time() - start_time)
            db.save_score(user_id, elapsed)
            running = False

        # Affichage
        fenetre.fill(VERT)
        for i in range(COLONNES):
            for j in range(LIGNES):
                pygame.draw.rect(fenetre, GRIS, (i * TAILLE_CASE, j * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)
        for cube in cubes:
            pygame.draw.rect(fenetre, ROUGE, (cube["x"], cube["y"], cube_size, cube_size))
        pygame.draw.rect(fenetre, BLEU, (player_col * TAILLE_CASE, player_row * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

        # Score affiché en temps réel
        font = pygame.font.Font(None, 36)
        elapsed = int(time.time() - start_time)
        score_text = font.render(f"Score: {elapsed}", True, BLANC)
        fenetre.blit(score_text, (10, 10))

        pygame.display.flip()


# ===================================================
# Main
# ===================================================
if __name__ == "__main__":
    user_id = login_screen()
    if user_id:
        play_game(user_id)
        leaderboard_screen()
    pygame.quit()
