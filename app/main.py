# ============ IMPORTS ============
import pygame as pg
import random
from assets import *
from config import *

# ============ INIT ============
pg.init()

# ============ LOGIC ============
class Player:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.rotation = 0
        self.bag_size = "big"
        self.image = player_images[self.bag_size]

player = Player()

# ============ FUNCTIONS ============

# -------- HELPERS --------
def _check_button_press(event: pg.event.Event, button_rect: pg.Rect):
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if button_rect.collidepoint(event.pos):
            return True
    return False

# -------- RENDER --------
def _get_start_screen_buttons_positions():
    total_width = start_button.get_width() + settings_button.get_width() + PADDING_SMALL
    start_x = WIDTH // 2 - total_width // 2
    settings_x = start_x + start_button.get_width() + PADDING_SMALL

    start_rect = start_button.get_rect(topleft=(start_x, HEIGHT * 0.5))
    settings_rect = settings_button.get_rect(topleft=(settings_x, HEIGHT * 0.5))
    return start_rect, settings_rect

def render_grid():
    for i in range(GRID_W):
        for j in range(GRID_H):
            x = GRID_OFFSET_X + PADDING_SMALL + i * (ROOM_SIZE + PADDING_SMALL)
            y = GRID_OFFSET_Y + PADDING_SMALL + j * (ROOM_SIZE + PADDING_SMALL)
            screen.blit(room, (x, y))

def render_player():
    rotated_image = pg.transform.rotate(player.image, player.rotation)
    x = GRID_OFFSET_X + PADDING_SMALL + player.pos_x * (ROOM_SIZE + PADDING_SMALL)
    y = GRID_OFFSET_Y + PADDING_SMALL + player.pos_y * (ROOM_SIZE + PADDING_SMALL)
    player_rect = rotated_image.get_rect(center=(x + ROOM_SIZE // 2, y + ROOM_SIZE // 2))
    screen.blit(rotated_image, player_rect)

def render_starting_screen():
    screen.blit(background, (0, 0))

    title_text = HEADING.render("Night at The Museum", True, (255, 255, 255))
    title_rect = title_text.get_rect(midtop=(WIDTH // 2, HEIGHT * 0.34))
    start_rect, settings_rect = _get_start_screen_buttons_positions()

    screen.blit(title_text, title_rect)
    screen.blit(start_button, start_rect)
    screen.blit(settings_button, settings_rect)

# -------- GAME LOOP --------
def check_events():
    global state
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False  
        start_rect, _ = _get_start_screen_buttons_positions()

        if _check_button_press(event, start_rect):
            state = "game"

    return True

def render_game():
    screen.blit(background, (0, 0))

    render_grid()
    render_player()

# ============ MAIN SCREEN ============

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Night at The Museum")
clock = pg.time.Clock()

# ============ MAIN LOOP ============

running = True
state = "starting_screen"
while running:
    running = check_events()

    match state:
        case "starting_screen":
            render_starting_screen()
        case "game":
            render_game()

    pg.display.flip()
    clock.tick(10)

# ============ CLEANUP ============
