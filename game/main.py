import os

import pygame

pygame.init()

GRID_SIZE_X = 13
GRID_SIZE_Y = 7

TILE_SIZE = 64

WIDTH = GRID_SIZE_X * TILE_SIZE
HEIGHT = GRID_SIZE_Y * TILE_SIZE

FPS = 60

SPRITES_DIR = os.path.join(os.path.dirname(__file__), "sprites")
WATER_FILE = os.path.join(SPRITES_DIR, "water_sprite.png")

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

TILE_WATER = "water"

running = True
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(water_surf, (7 * TILE_SIZE, 3 * TILE_SIZE))

    pygame.display.flip()

pygame.quit()