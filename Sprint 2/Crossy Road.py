# Projet : Base de données et crossy Road
# Auteur : Luca Giubbilei et Rafael Rico
# Date : 13.03.2024
# Note : Certaines parties de la logique du jeu ont été aidées par ChatGPT

from tkinter import *
from tkinter import messagebox
import sqlite3
import os
import pygame
import random
import sys
username1 = ""  # variable globale pour stocker le nom de l'utilisateur connecté



# --- CONFIGURATION DE LA FENÊTRE PRINCIPALE TKINTER ---
root = Tk()
root.title("Login")

width = 300
height = 150

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# on centre la fenêtre à l'écran
x = (screen_width - width) // 2
y = (screen_height - height) // 5
root.geometry(f"{width}x{height}+{x}+{y}")



# --- BASE DE DONNÉES ---
def create_database():

    conn = sqlite3.connect('login_db.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tusers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            top_score INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()



# --- INSCRIPTION ---
def register():

    global username1
    username = entry_username.get()
    password = entry_password.get()
    username1 = username
    if username and password:
        conn = sqlite3.connect('login_db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tusers WHERE username=?', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Erreur", "Nom d'utilisateur déjà pris, choisissez-en un autre.")
        else:
            cursor.execute('INSERT INTO tusers (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Inscription", "Bienvenue ! Votre inscription a été réussie.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer un nom d'utilisateur et un mot de passe.")



# --- SAUVEGARDE DU SCORE ---
def sauvegarder_score(username, score):

    conn = sqlite3.connect('login_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT top_score FROM tusers WHERE username=?", (username,))
    result = cursor.fetchone()
    if result:
        top_score = result[0]
        if score > top_score:
            cursor.execute("UPDATE tusers SET top_score=?, score=? WHERE username=?", (score, score, username))
        else:
            cursor.execute("UPDATE tusers SET score=? WHERE username=?", (score, username))
    conn.commit()
    conn.close()



# --- OUVRIR LE JEU PYGAME ---
def open_game():

    global username1
    root.destroy()  # fermer la fenêtre Tkinter avant de lancer le jeu

    pygame.init()
    LARGEUR, HAUTEUR = 900, 1000
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Autoroute du poulet")
    clock = pygame.time.Clock()

    TAILLE_CASE = 50
    NB_CASES_LARGEUR = LARGEUR // TAILLE_CASE
    NB_CASES_HAUTEUR = HAUTEUR // TAILLE_CASE

    NB_VOIES = 7
    VOIES = [2 + i * 2 for i in range(NB_VOIES)]  # positions des voies sur la grille



    # On attribue une vitesse aléatoire à chaque voie (ne peut pas être 0)
    vitesses_voies = {}
    for voie in VOIES:
        v = 0
        while v == 0:
            v = random.choice([-2, -1, 1, 2])
        vitesses_voies[voie] = v



    # --- CHARGEMENT DES IMAGES ---
    try:
        poulet_img = pygame.image.load("poulet_img.png").convert_alpha()
        poulet_img = pygame.transform.scale(poulet_img, (TAILLE_CASE, TAILLE_CASE))

        voiture_droite_img = pygame.image.load("car_right.png").convert_alpha()
        voiture_droite_img = pygame.transform.scale(voiture_droite_img, (TAILLE_CASE, TAILLE_CASE))

        voiture_gauche_img = pygame.image.load("car_left.png").convert_alpha()
        voiture_gauche_img = pygame.transform.scale(voiture_gauche_img, (TAILLE_CASE, TAILLE_CASE))
    except Exception as e:
        pygame.quit()
        sys.exit()

    joueur_x = NB_CASES_LARGEUR // 2
    joueur_y = NB_CASES_HAUTEUR - 1
    voitures = []



    # --- CRÉATION DES VOITURES ---
    def creer_voitures():
        """Positionne les voitures sur les voies en évitant qu'elles se superposent."""
        voitures.clear()
        for voie in VOIES:
            nb_voitures_voie = random.randint(2, 4)
            positions_occupees = []
            for _ in range(nb_voitures_voie):
                essais = 0
                while True:
                    x = random.uniform(0, NB_CASES_LARGEUR)
                    if all(abs(x - pos) > 1.5 for pos in positions_occupees):
                        positions_occupees.append(x)
                        break
                    essais += 1
                    if essais > 100:
                        break
                vitesse = vitesses_voies[voie]
                voitures.append([x, voie, vitesse])

    creer_voitures()
    font = pygame.font.SysFont(None, 40)
    score = 0
    game_over = False

    def dessiner_texte(texte, x, y, couleur=(255, 255, 255)):
        """Petit utilitaire pour afficher du texte à l'écran."""
        img = font.render(texte, True, couleur)
        screen.blit(img, (x, y))

    def reset():
        """Réinitialise le jeu après un game over."""
        nonlocal joueur_x, joueur_y, score, game_over, vitesses_voies
        joueur_x = NB_CASES_LARGEUR // 2
        joueur_y = NB_CASES_HAUTEUR - 1
        score = 0
        game_over = False
        for voie in VOIES:
            v = 0
            while v == 0:
                v = random.choice([-2, -1, 1, 2])
            vitesses_voies[voie] = v
        creer_voitures()



    # --- BOUCLE PRINCIPALE DU JEU --- (ChatGPT)
    while True:
        dt = clock.tick(60) / 1000  # delta time pour que le mouvement soit fluide
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sauvegarder_score(username1, score)
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
            # Déplacement des voitures (ChatGPT)
            for voiture in voitures:
                voiture[0] += voiture[2] * dt
                if voiture[2] > 0 and voiture[0] > NB_CASES_LARGEUR:
                    voiture[0] = -1
                elif voiture[2] < 0 and voiture[0] < -1:
                    voiture[0] = NB_CASES_LARGEUR



            # Eviter que les voitures se superposent sur la même voie (ChatGPT)
            for voie in VOIES:
                voitures_voie = [v for v in voitures if v[1] == voie]
                voitures_voie.sort(key=lambda v: v[0])
                for i in range(len(voitures_voie) - 1):
                    dist = voitures_voie[i+1][0] - voitures_voie[i][0]
                    if dist < 1.5:
                        voitures_voie[i+1][0] = voitures_voie[i][0] + 1.5
                idx = 0
                for i, v in enumerate(voitures):
                    if v[1] == voie:
                        voitures[i] = voitures_voie[idx]
                        idx += 1



            # Détection de collision (ChatGPT)
            joueur_rect = pygame.Rect(joueur_x * TAILLE_CASE, joueur_y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            for voiture in voitures:
                voiture_rect = pygame.Rect(int(voiture[0] * TAILLE_CASE), voiture[1] * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
                if joueur_rect.colliderect(voiture_rect):
                    game_over = True
                    sauvegarder_score(username1, score)
                    break



            # Si le joueur atteint le haut de l'écran
            if joueur_y == 0:
                score += 1
                joueur_y = NB_CASES_HAUTEUR - 1
                # Augmentation progressive de la vitesse
                for voie in VOIES:
                    v = vitesses_voies[voie]
                    if v > 0:
                        vitesses_voies[voie] = min(v + 0.5, 5)
                    else:
                        vitesses_voies[voie] = max(v - 0.5, -5)
                for voiture in voitures:
                    voie = voiture[1]
                    voiture[2] = vitesses_voies[voie]



        # --- DESSIN À L'ÉCRAN ---
        screen.fill((50, 150, 50))  # couleur herbe
        for voie in VOIES:
            pygame.draw.rect(screen, (40, 40, 40), (0, voie * TAILLE_CASE, LARGEUR, TAILLE_CASE))  # routes

        for voiture in voitures:
            img = voiture_droite_img if voiture[2] > 0 else voiture_gauche_img
            screen.blit(img, (int(voiture[0] * TAILLE_CASE), voiture[1] * TAILLE_CASE))

        screen.blit(poulet_img, (joueur_x * TAILLE_CASE, joueur_y * TAILLE_CASE))
        dessiner_texte(f"Score : {score}", 10, 10)

        if game_over:
            dessiner_texte("GAME OVER ! Appuyez sur R pour rejouer", LARGEUR // 6, HAUTEUR // 2, (255, 0, 0))

        pygame.display.flip()



# --- CONNEXION ---
def login():
    """Permet à l'utilisateur de se connecter et d'ouvrir le jeu si les identifiants sont corrects."""
    global username1
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        conn = sqlite3.connect('login_db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tusers WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        if user:
            username1 = username
            messagebox.showinfo("Connexion réussie", f"Bienvenue, {username}!")
            open_game()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect ou le compte n'existe pas.")
    else:
        messagebox.showerror("Erreur", "Le nom d'utilisateur et le mot de passe sont requis.")



# --- INITIALISATION ---
create_database()

# --- INTERFACE TKINTER ---
frame_main = Frame(root, padx=20, pady=20)
frame_main.pack(fill="both", expand=True)

frame_user = Frame(frame_main)
frame_user.pack(fill="x", pady=5)

label_user = Label(frame_user, text="Username :", font=("Helvetica", 11), width=10, anchor='w')
label_user.pack(side=LEFT)

entry_username = Entry(frame_user, font=("Helvetica", 11))
entry_username.pack(side=LEFT, fill="x", expand=True)
entry_username.focus()

frame_password = Frame(frame_main)
frame_password.pack(fill="x", pady=5)

label_password = Label(frame_password, text="Password :", font=("Helvetica", 11), width=10, anchor='w')
label_password.pack(side=LEFT)

entry_password = Entry(frame_password, show="*", font=("Helvetica", 11))
entry_password.pack(side=LEFT, fill="x", expand=True)

frame_buttons = Frame(frame_main)
frame_buttons.pack(pady=5)

button_register = Button(frame_buttons, text="S'inscrire", width=15, command=register)
button_register.pack(side=LEFT, padx=10, pady=5)

button_login = Button(frame_buttons, text="Se connecter", width=15, command=login)
button_login.pack(side=LEFT, padx=10, pady=3)

root.mainloop()
