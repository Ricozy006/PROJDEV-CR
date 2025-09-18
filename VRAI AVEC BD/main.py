import pygame, sys, time
import db  # notre db1.py MySQL/HeidiSQL

pygame.init()

# ----------- Constantes -----------
WIDTH, HEIGHT = 600, 400
WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (255,0,0)
FONT = pygame.font.Font(None, 32)

# ----------- InputBox pour login/register -----------
class InputBox:
    def __init__(self, x, y, w, h, text='', password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.password = password

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render('*'*len(self.text) if self.password else self.text, True, self.color)
        return None

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# ----------- Login/Register screen -----------
def login_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Login / Register")

    username_box = InputBox(200, 100, 200, 32)
    password_box = InputBox(200, 150, 200, 32, password=True)
    message = ''

    login_button = pygame.Rect(200, 200, 80, 32)
    register_button = pygame.Rect(320, 200, 80, 32)

    clock = pygame.time.Clock()
    user_id = None
    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            username_box.handle_event(event)
            password_box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.collidepoint(event.pos):
                    uid = db.login(username_box.text, password_box.text)
                    if uid:
                        user_id = uid
                        running = False
                    else:
                        message = 'Login failed!'
                if register_button.collidepoint(event.pos):
                    uid = db.create_user(username_box.text, password_box.text)b
                    if uid:
                        user_id = db.login(username_box.text, password_box.text)
                        running = False
                    else:
                        message = 'Username already exists!'

        # Draw
        username_box.draw(screen)
        password_box.draw(screen)
        pygame.draw.rect(screen, BLACK, login_button, 2)
        pygame.draw.rect(screen, BLACK, register_button, 2)
        screen.blit(FONT.render("Login", True, BLACK), (login_button.x+5, login_button.y+5))
        screen.blit(FONT.render("Register", True, BLACK), (register_button.x+5, register_button.y+5))
        if message:
            screen.blit(FONT.render(message, True, RED), (200, 250))
        pygame.display.flip()
        clock.tick(30)
    return user_id

# ----------- Leaderboard screen -----------
def leaderboard_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Leaderboard")
    scores = db.get_highscores(5)
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(WHITE)
        y = 50
        screen.blit(FONT.render("Leaderboard (Top 5)", True, BLACK), (180, 10))
        for username, score in scores:
            screen.blit(FONT.render(f"{username} : {score}", True, BLACK), (220, y))
            y += 40
        screen.blit(FONT.render("Press SPACE to quit", True, RED), (180, HEIGHT-50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
        pygame.display.flip()
        clock.tick(30)

# ----------- Game logic simple Crossy Road ----------
def run_game(user_id):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Crossy Road")
    clock = pygame.time.Clock()
    player = pygame.Rect(WIDTH//2, HEIGHT-40, 30, 30)
    obstacles = [pygame.Rect(0, 100, 50, 30), pygame.Rect(200, 200, 50, 30)]
    start_time = time.time()
    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.x -= 5
        if keys[pygame.K_RIGHT]: player.x += 5
        if keys[pygame.K_UP]: player.y -= 5
        if keys[pygame.K_DOWN]: player.y += 5

        # Move obstacles
        for obs in obstacles:
            obs.y += 3
            if obs.y > HEIGHT: obs.y = -30

        # Collision check
        if any(player.colliderect(obs) for obs in obstacles):
            elapsed = int(time.time() - start_time)
            db.save_score(user_id, elapsed)
            running = False

        # Draw
        pygame.draw.rect(screen, (0,0,255), player)
        for obs in obstacles:
            pygame.draw.rect(screen, (255,0,0), obs)
        score = int(time.time() - start_time)
        screen.blit(FONT.render(f"Score: {score}", True, BLACK), (10,10))

        pygame.display.flip()
        clock.tick(30)

# ----------- Main -----------
def main():
    user_id = login_screen()
    run_game(user_id)
    leaderboard_screen()
    pygame.quit()

if __name__ == "__main__":
    main()
