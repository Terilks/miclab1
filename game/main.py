import os

import pygame

pygame.init()

tile_map = [
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '0', '0', '', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', ''],
    ['', '0', '0', '0', '0', '', '', '', '', '', '', '', '0', '0', ''],
    ['', '0', '0', '0', '', '', '', '0', '0', '0', '0', '0', '0', 'C', ''],
    ['', 'P', '0', '0', '', 'E', '0', '0', '0', '0', '0', '0', '0', '0', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
]

GRID_SIZE_X = 15
GRID_SIZE_Y = 7

TILE_SIZE = 64

WIDTH = GRID_SIZE_X * TILE_SIZE
HEIGHT = GRID_SIZE_Y * TILE_SIZE

FPS = 60

SPRITES_DIR = os.path.join(os.path.dirname(__file__), "sprites")
WATER_FILE = os.path.join(SPRITES_DIR, "water_sprite.png")
GRASS_FILE = os.path.join(SPRITES_DIR, "grass.png")
CHARACTER_FILE = os.path.join(SPRITES_DIR, "character1.png")
STAR_FILE = os.path.join(SPRITES_DIR, "star.png")
DOOR_FILE = os.path.join(SPRITES_DIR, "door.png")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labadabadapdap 1")
clock = pygame.time.Clock()

def load_image(path):
    try:
        img = pygame.image.load(path)
    except Exception as e:
        raise SystemExit(f"Не удалось загрузить изображение {path}: {e}")
    # если есть альфа — используем convert_alpha, иначе convert
    try:
        return pygame.transform.scale(img.convert_alpha(), (TILE_SIZE, TILE_SIZE))
    except Exception:
        return pygame.transform.scale(img.convert(), (TILE_SIZE, TILE_SIZE))


water_surf = load_image(WATER_FILE)
grass_surf = load_image(GRASS_FILE)
character_surf = load_image(CHARACTER_FILE)
star_surf = load_image(STAR_FILE)
door_surf = load_image(DOOR_FILE)

background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
for y in range(0, HEIGHT, TILE_SIZE):
    for x in range(0, WIDTH, TILE_SIZE):
        background.blit(water_surf, (x, y))

player_x = player_y = None
for y, row in enumerate(tile_map):
    for x, cell in enumerate(row):
        if cell == 'P':
            player_x, player_y = x, y
            tile_map[y][x] = '0'
            break
    if player_x is not None:
        break

running = True

score = 0
font = pygame.font.SysFont(None, 24)

while running:
    dt = clock.tick(FPS)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            dx = dy = 0
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                dy = -1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                dy = 1
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                dx = 1

            if dx != 0 or dy != 0:
                new_x = player_x + dx
                new_y = player_y + dy

                if 0 <= new_x < GRID_SIZE_X and 0 <= new_y < GRID_SIZE_Y:
                    target = tile_map[new_y][new_x]
                    if target == '0':
                        player_x, player_y = new_x, new_y
                    if target == 'C':
                        player_x, player_y = new_x, new_y
                        score += 1
                        tile_map[new_y][new_x] = '0'
                    if target == 'E' and score > 0:
                        player_x, player_y = new_x, new_y
                        running = False

    screen.blit(background, (0, 0))

    for y, row in enumerate(tile_map):
        for x, cell in enumerate(row):
            if cell == '0':
                screen.blit(grass_surf, (x * TILE_SIZE, y * TILE_SIZE))
            elif cell == 'C':
                screen.blit(grass_surf, (x * TILE_SIZE, y * TILE_SIZE))
                screen.blit(star_surf, (x * TILE_SIZE, y * TILE_SIZE))
            elif cell == 'E':
                screen.blit(grass_surf, (x * TILE_SIZE, y * TILE_SIZE))
                screen.blit(door_surf, (x * TILE_SIZE, y * TILE_SIZE))

    screen.blit(character_surf, (player_x * TILE_SIZE, player_y * TILE_SIZE))

    score_surf = font.render(f"Звезд: {score}", True, (0, 0, 0))
    screen.blit(score_surf, (8, 8))

    pygame.display.flip()

pygame.quit()