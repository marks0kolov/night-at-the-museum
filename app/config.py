import pygame as pg
from pathlib import Path

pg.init()
# ============ DISPLAY SIZE ============
display = pg.display.Info()
SCREEN_RATIO = 1.4
SCREEN_COVERAGE = 0.8

DISPLAY_WIDTH, DISPLAY_HEIGHT = display.current_w, display.current_h

# ============ SCREEN SIZE AND INTERNAL PADDING ============
MAX_WIDTH = int(DISPLAY_WIDTH * SCREEN_COVERAGE)
MAX_HEIGHT = int(DISPLAY_HEIGHT * SCREEN_COVERAGE)
WIDTH = min(MAX_WIDTH, int(MAX_HEIGHT * SCREEN_RATIO))
HEIGHT = int(WIDTH / SCREEN_RATIO)

PADDING_SMALL = WIDTH // 70
PADDING_BIG = WIDTH // 24

# ============ ROOM GRID ============
GRID_W, GRID_H = 6, 4
ROOM_SIZE = min(
    (WIDTH - (GRID_W + 1) * PADDING_SMALL) // GRID_W,
    (HEIGHT - (GRID_H + 1) * PADDING_SMALL) // GRID_H,
)
GRID_PIXEL_WIDTH = GRID_W * ROOM_SIZE + (GRID_W + 1) * PADDING_SMALL
GRID_PIXEL_HEIGHT = GRID_H * ROOM_SIZE + (GRID_H + 1) * PADDING_SMALL
GRID_OFFSET_X = (WIDTH - GRID_PIXEL_WIDTH) // 2
GRID_OFFSET_Y = (HEIGHT - GRID_PIXEL_HEIGHT) // 2

# ============ PATHS ============
ASSETS_PATH = Path("./assets")
IMAGES_PATH = ASSETS_PATH / "images"
FONTS_PATH = ASSETS_PATH / "fonts"

# ============ FONTS ============
BODY = pg.font.Font(FONTS_PATH / "NotoSerifGeorgian.ttf", max(16, WIDTH // 90))
HEADING = pg.font.Font(FONTS_PATH / "UnifrakturMaguntia.ttf", max(64, WIDTH // 10))
