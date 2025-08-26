import pygame
import sys
import random
from PIL import Image
import sqlite3

# ------------------ DATABASE ------------------
conn = sqlite3.connect("crossy_cat.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    score INTEGER
)
""")
conn.commit()

# ------------------ PYGAME SETUP ------------------
pygame.init()
TILE_SIZE = 80
PLAYABLE_WIDTH = 8
GRID_WIDTH = PLAYABLE_WIDTH + 2
WIDTH, HEIGHT = GRID_WIDTH * TILE_SIZE, 9 * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crossy Cat")
clock = pygame.time.Clock()

# ------------------ COLORS ------------------
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
ROAD_GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN_BTN = (0, 200, 0)
GRAY_BTN = (100, 100, 100)

# ------------------ GIF LOADER ------------------
def load_gif(filename, size):
    pil_image = Image.open(filename)
    frames = []
    try:
        while True:
            frame = pil_image.copy().convert("RGBA")
            frame = frame.resize(size, Image.NEAREST)
            mode = frame.mode
            data = frame.tobytes()
            py_image = pygame.image.fromstring(data, frame.size, mode)
            frames.append(py_image)
            pil_image.seek(pil_image.tell() + 1)
    except EOFError:
        pass
    return frames

cat_frames = {
    "up": load_gif("catup.gif", (TILE_SIZE, TILE_SIZE)),
    "down": load_gif("catdown.gif", (TILE_SIZE, TILE_SIZE)),
    "left": load_gif("catleft.gif", (TILE_SIZE, TILE_SIZE)),
    "right": load_gif("catright.gif", (TILE_SIZE, TILE_SIZE)),
}

# ------------------ CAR IMAGES ------------------
def load_car_images():
    car_files = ["car1.png", "car2.png"]
    cars = []
    for f in car_files:
        img = pygame.image.load(f).convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        cars.append(img)
    return cars

car_images = load_car_images()
cars = []

# ------------------ WORLD ------------------
world = {}
row_types = {}
row_directions = {}

def get_row_type(row):
    if row not in row_types:
        r = random.random()
        if r < 0.2:
            row_types[row] = "road"
            row_directions[row] = random.choice(["left", "right"])
        else:
            row_types[row] = "land"
    return row_types[row]

def get_tile(row, col):
    if col == 0 or col == GRID_WIDTH - 1:
        return "wall"
    row_type = get_row_type(row)
    if row_type == "road":
        return "road"
    else:
        if (row, col) not in world:
            if random.random() < 0.1:
                world[(row, col)] = "tree"
            else:
                world[(row, col)] = "empty"
        return world[(row, col)]

def draw_grid(camera_y):
    start_row = camera_y // TILE_SIZE
    end_row = (camera_y + HEIGHT) // TILE_SIZE + 1
    for row in range(start_row, end_row):
        row_type = get_row_type(row)
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(
                col * TILE_SIZE,
                row * TILE_SIZE - camera_y,
                TILE_SIZE, TILE_SIZE
            )
            if row_type == "road":
                pygame.draw.rect(screen, ROAD_GRAY, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect, 1)
            tile = get_tile(row, col)
            if tile == "tree":
                pygame.draw.rect(screen, BROWN, rect.inflate(-30, -30))
                pygame.draw.circle(screen, GREEN, rect.center, TILE_SIZE//3)
            elif tile == "wall":
                pygame.draw.rect(screen, BLACK, rect)

# ------------------ CARS ------------------
def spawn_cars(camera_y):
    start_row = (camera_y // TILE_SIZE) - 2
    end_row = ((camera_y + HEIGHT) // TILE_SIZE) + 2
    for row in range(start_row, end_row):
        if get_row_type(row) == "road":
            if not any(car["row"] == row for car in cars):
                if random.random() < 0.1:
                    direction = row_directions[row]
                    base_img = random.choice(car_images)
                    if direction == "left":
                        car_img = base_img
                        x = WIDTH + random.randint(0, 3) * TILE_SIZE
                    else:
                        car_img = pygame.transform.flip(base_img, True, False)
                        x = -TILE_SIZE - random.randint(0, 3) * TILE_SIZE
                    y = row * TILE_SIZE - camera_y
                    cars.append({
                        "rect": pygame.Rect(x, y, TILE_SIZE, TILE_SIZE),
                        "row": row,
                        "dir": direction,
                        "speed": random.randint(4, 7),
                        "image": car_img
                    })

def update_cars(camera_y):
    for car in cars[:]:
        if car["dir"] == "left":
            car["rect"].x -= car["speed"]
        else:
            car["rect"].x += car["speed"]
        car["rect"].y = car["row"] * TILE_SIZE - camera_y
        if car["rect"].right < -200 or car["rect"].left > WIDTH + 200:
            cars.remove(car)
        else:
            screen.blit(car["image"], (car["rect"].x, car["rect"].y))

# ------------------ USERNAME GUI ------------------
def get_username():
    username = ""
    active = False
    font = pygame.font.SysFont(None, 50)
    button_font = pygame.font.SysFont(None, 40)
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 25, 300, 50)
    start_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50)
    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if start_button.collidepoint(event.pos) and username.strip() != "":
                    return username.strip()
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN and username.strip() != "":
                    return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
        color = (0, 0, 0) if active else (150, 150, 150)
        pygame.draw.rect(screen, color, input_box, 3)
        txt_surface = font.render(username, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, GREEN_BTN, start_button)
        btn_text = button_font.render("Start Game", True, WHITE)
        screen.blit(btn_text, (start_button.x + 10, start_button.y + 10))
        label = font.render("Enter your username:", True, BLACK)
        screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - 100))
        pygame.display.flip()
        clock.tick(60)

# ------------------ GAME OVER GUI ------------------
def game_over_screen(score):
    font = pygame.font.SysFont(None, 80)
    button_font = pygame.font.SysFont(None, 40)
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)

    while True:
        screen.fill(WHITE)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.draw.rect(screen, GREEN_BTN, play_button)
        play_text = button_font.render("Play Again", True, WHITE)
        screen.blit(play_text, (play_button.x + 20, play_button.y + 10))

        pygame.draw.rect(screen, GRAY_BTN, quit_button)
        quit_text = button_font.render("Quit", True, WHITE)
        screen.blit(quit_text, (quit_button.x + 60, quit_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conn.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return True
                if quit_button.collidepoint(event.pos):
                    conn.close()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

# ------------------ GAME LOOP ------------------
def main():
    global cars
    username = get_username()
    while True:  # loop to allow play again
        player_row, player_col = 5, GRID_WIDTH // 2
        frame_index = 0
        frame_timer = 0
        ANIM_SPEED = 8
        score = 0
        visited_rows = set([player_row])
        direction = "down"
        cars = []

        running = True
        while running:
            screen.fill(WHITE)
            # --- Input ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    conn.close()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    new_row, new_col = player_row, player_col
                    if event.key == pygame.K_UP:
                        new_row -= 1
                        direction = "up"
                    if event.key == pygame.K_DOWN:
                        new_row += 1
                        direction = "down"
                    if event.key == pygame.K_LEFT:
                        new_col -= 1
                        direction = "left"
                    if event.key == pygame.K_RIGHT:
                        new_col += 1
                        direction = "right"
                    if get_tile(new_row, new_col) not in ("tree", "wall"):
                        player_row, player_col = new_row, new_col
                        if player_row not in visited_rows:
                            visited_rows.add(player_row)
                            score += 1

            camera_y = player_row * TILE_SIZE - HEIGHT // 2 + TILE_SIZE // 2
            draw_grid(camera_y)
            spawn_cars(camera_y)
            update_cars(camera_y)

            # Collision
            player_rect = pygame.Rect(player_col * TILE_SIZE,
                                      player_row * TILE_SIZE - camera_y,
                                      TILE_SIZE, TILE_SIZE)
            if any(player_rect.colliderect(car["rect"]) for car in cars):
                # Save score
                c.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (username, score))
                conn.commit()
                if game_over_screen(score):
                    break  # restart game loop

            # Player animation
            frame_timer += 1
            if frame_timer >= ANIM_SPEED:
                frame_index = (frame_index + 1) % len(cat_frames[direction])
                frame_timer = 0
            frame = cat_frames[direction][frame_index]
            screen.blit(frame, (player_col * TILE_SIZE, player_row * TILE_SIZE - camera_y))

            # Draw score
            font = pygame.font.SysFont(None, 40)
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()
