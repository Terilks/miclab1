import os

import pygame

pygame.init()

ALLOWED = {'0', '1', 'C', 'E', 'P'}


def load_map_txt(path):
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(__file__), path)

    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            rows.append(list(s))

    w = len(rows[0])
    if any(len(r) != w for r in rows):
        raise SystemExit("Строки карты разной длины.")

    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c not in ALLOWED:
                raise SystemExit(f"Недопустимый символ '{c}' в ({y},{x}).")

    p = sum(c == 'P' for r in rows for c in r)
    c = sum(c == 'C' for r in rows for c in r)
    e = sum(c == 'E' for r in rows for c in r)

    if p != 1:
        raise SystemExit("На карте должен быть ровно один P.")
    if c < 1:
        raise SystemExit("Должен быть хотя бы один C.")
    if e < 1:
        raise SystemExit("Должен быть хотя бы один E.")

    return rows


tile_map = load_map_txt("tile_map.txt")

GRID_SIZE_X = len(tile_map[0])
GRID_SIZE_Y = len(tile_map)

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
        return pygame.transform.scale(
            img.convert_alpha(),
            (TILE_SIZE, TILE_SIZE))
    except Exception:
        return pygame.transform.scale(img.convert(), (TILE_SIZE, TILE_SIZE))


water_surf = load_image(WATER_FILE)
grass_surf = load_image(GRASS_FILE)
character_surf = load_image(CHARACTER_FILE)
star_surf = load_image(STAR_FILE)
door_surf = load_image(DOOR_FILE)

BASE_DIR = 'right'

def make_lr(img, base_dir='right'):
    if base_dir == 'right':
        right = img
    elif base_dir == 'left':
        right = pygame.transform.flip(img, True, False)
    elif base_dir == 'up':
        right = pygame.transform.rotate(img, -90)
    elif base_dir == 'down':
        right = pygame.transform.rotate(img, 90)
    else:
        right = img
    left = pygame.transform.flip(right, True, False)
    return left, right

char_left, char_right = make_lr(character_surf, BASE_DIR)
facing_right = True

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
moves = 0

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
                        moves += 1
                    if target == 'C':
                        player_x, player_y = new_x, new_y
                        score += 1
                        tile_map[new_y][new_x] = '0'
                        moves += 1
                    if target == 'E' and score > 0:
                        player_x, player_y = new_x, new_y
                        moves += 1
                        running = False

                if dx == 1:
                    facing_right = True
                elif dx == -1:
                    facing_right = False

    for y, row in enumerate(tile_map):
        for x, cell in enumerate(row):
            if cell == '1':
                screen.blit(water_surf, (x * TILE_SIZE, y * TILE_SIZE))
            elif cell == '0':
                screen.blit(grass_surf, (x * TILE_SIZE, y * TILE_SIZE))
            elif cell == 'C':
                screen.blit(grass_surf, (x * TILE_SIZE, y * TILE_SIZE))
                screen.blit(star_surf, (x * TILE_SIZE, y * TILE_SIZE))
            elif cell == 'E':
                screen.blit(grass_surf, (x * TILE_SIZE, y * TILE_SIZE))
                screen.blit(door_surf, (x * TILE_SIZE, y * TILE_SIZE))

    screen.blit(char_right if facing_right else char_left,
                (player_x * TILE_SIZE, player_y * TILE_SIZE))

    score_surf = font.render(f"Звезд: {score}", True, (0, 0, 0))
    screen.blit(score_surf, (8, 8))

    moves_surf = font.render(f"Moves: {moves}", True, (0, 0, 0))
    screen.blit(moves_surf, (8, 410))

    pygame.display.flip()

pygame.quit()
