import pygame
import sys
import random
from PIL import Image

# --- Function to load GIF frames into Pygame ---
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

# --- Pygame setup ---
pygame.init()
TILE_SIZE = 80
PLAYABLE_WIDTH = 8  # playable tiles in the middle
GRID_WIDTH = PLAYABLE_WIDTH + 2  # add 1 wall tile on each side
WIDTH, HEIGHT = GRID_WIDTH * TILE_SIZE, 9 * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Load cat GIFs for each direction ---
cat_frames = {
    "up": load_gif("catup.gif", (TILE_SIZE, TILE_SIZE)),
    "down": load_gif("catdown.gif", (TILE_SIZE, TILE_SIZE)),
    "left": load_gif("catleft.gif", (TILE_SIZE, TILE_SIZE)),
    "right": load_gif("catright.gif", (TILE_SIZE, TILE_SIZE)),
}

player_row, player_col = 5, GRID_WIDTH // 2  # start near center
frame_index = 0
frame_timer = 0
ANIM_SPEED = 8
score = 0
farthest_row = player_row

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
ROAD_COLOR = (50, 50, 50)
CAR_COLOR = (200, 0, 0)

# Font
font = pygame.font.SysFont("Arial", 32, bold=True)

# --- World data ---
world = {}
row_types = {}
row_directions = {}  # road rows: left or right
cars = []  # active cars

# --- World generation ---
def get_row_type(row):
    if row not in row_types:
        if random.random() < 0.15:
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
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(
                col * TILE_SIZE,
                row * TILE_SIZE - camera_y,
                TILE_SIZE, TILE_SIZE
            )
            pygame.draw.rect(screen, GRAY, rect, 1)

            tile = get_tile(row, col)
            if tile == "tree":
                pygame.draw.rect(screen, BROWN, rect.inflate(-30, -30))
                pygame.draw.circle(screen, GREEN, rect.center, TILE_SIZE // 3)
            elif tile == "wall":
                pygame.draw.rect(screen, BLACK, rect)
            elif tile == "road":
                pygame.draw.rect(screen, ROAD_COLOR, rect)

def spawn_cars(camera_y):
    """Spawn cars randomly on visible road rows."""
    start_row = camera_y // TILE_SIZE
    end_row = (camera_y + HEIGHT) // TILE_SIZE + 1

    for row in range(start_row, end_row):
        if get_row_type(row) == "road":
            if random.random() < 0.03:  # slightly higher spawn chance
                direction = row_directions[row]

                # Decide if car spawns at side or anywhere on road
                if random.random() < 0.5:
                    # normal: spawn at edge
                    if direction == "left":
                        x = WIDTH
                    else:
                        x = -TILE_SIZE
                else:
                    # new: spawn somewhere along the road
                    x = random.randint(TILE_SIZE, WIDTH - TILE_SIZE)

                y = row * TILE_SIZE - camera_y
                cars.append({
                    "rect": pygame.Rect(x, y, TILE_SIZE, TILE_SIZE),
                    "row": row,
                    "dir": direction,
                    "speed": random.randint(4, 7)
                })

def update_cars(camera_y):
    """Move and draw cars."""
    global running
    for car in cars[:]:
        row_offset = car["row"] * TILE_SIZE - camera_y
        car["rect"].y = row_offset  # adjust Y position with camera
        if car["dir"] == "left":
            car["rect"].x -= car["speed"]
        else:
            car["rect"].x += car["speed"]

        # remove cars that move off screen
        if car["rect"].right < 0 or car["rect"].left > WIDTH:
            cars.remove(car)
            continue

        pygame.draw.rect(screen, CAR_COLOR, car["rect"])

        # collision check with player
        player_rect = pygame.Rect(
            player_col * TILE_SIZE,
            player_row * TILE_SIZE - camera_y,
            TILE_SIZE, TILE_SIZE
        )
        if car["row"] == player_row and car["rect"].colliderect(player_rect):
            game_over()

# --- Game Over ---
def game_over():
    global running
    over_text = font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# --- Direction tracker ---
direction = "down"

def main():
    global player_row, player_col, frame_index, frame_timer, direction, score, farthest_row, running
    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
                    if player_row < farthest_row:
                        score += 1
                        farthest_row = player_row

        # Camera follows vertically
        camera_y = player_row * TILE_SIZE - HEIGHT // 2 + TILE_SIZE // 2

        # Draw world
        draw_grid(camera_y)

        # Cars
        spawn_cars(camera_y)
        update_cars(camera_y)

        # Animation
        frame_timer += 1
        if frame_timer >= ANIM_SPEED:
            frame_index = (frame_index + 1) % len(cat_frames[direction])
            frame_timer = 0
        frame = cat_frames[direction][frame_index]

        # Draw player
        screen.blit(
            frame,
            (player_col * TILE_SIZE, player_row * TILE_SIZE - camera_y)
        )

        # Score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
