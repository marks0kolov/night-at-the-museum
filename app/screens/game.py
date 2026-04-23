import pygame as pg

from app.assets import *
from app.config import *

# ============ PLAYER LOGIC ============
class Player:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.rotation = 0
        self.bag_size = "big"
        self.image = player_images[self.bag_size]
        self.visited_rooms = {(0, 0)}

player = Player()

# ============ LAYOUT ============
def _get_grid_layout(selected_difficuly):
    """calculate the current grid size and room size from the selected difficuly"""
    grid_w, grid_h = GRID_SIZES[selected_difficuly]
    room_size = (WIDTH - PADDING_SMALL * 2 - (grid_w - 1) * PADDING_SMALL) // grid_w
    
    grid_width = grid_w * room_size + (grid_w - 1) * PADDING_SMALL
    grid_height = grid_h * room_size + (grid_h - 1) * PADDING_SMALL

    grid_left = (WIDTH - grid_width) // 2
    grid_top = HEIGHT - PADDING_SMALL - grid_height

    return {
        "grid_w": grid_w,
        "grid_h": grid_h,
        "room_size": room_size,
        "grid_left": grid_left,
        "grid_top": grid_top,
    }

def _render_grid(screen, selected_difficuly):
    """"render game grid of rooms"""
    grid_layout = _get_grid_layout(selected_difficuly)
    
    room_surface = pg.transform.scale(room_default, (grid_layout["room_size"], grid_layout["room_size"]))
    dark_room_surface = pg.transform.scale(room_darkened, (grid_layout["room_size"], grid_layout["room_size"]))
    
    for i in range(grid_layout["grid_w"]):
        for j in range(grid_layout["grid_h"]):
            x = grid_layout["grid_left"] + i * (grid_layout["room_size"] + PADDING_SMALL)
            y = grid_layout["grid_top"] + j * (grid_layout["room_size"] + PADDING_SMALL)

            current_room = room_surface if (i, j) in player.visited_rooms else dark_room_surface
            screen.blit(current_room, (x, y))

            if (i, j) == (grid_layout["grid_w"] - 1, grid_layout["grid_h"] - 1):
                final_mark = pg.transform.scale(icon_final_mark, (grid_layout["room_size"] * 0.7, grid_layout["room_size"] * 0.7))
                final_mark_rect = final_mark.get_rect(center=(x + grid_layout["room_size"] // 2, y + grid_layout["room_size"] // 2))
                screen.blit(final_mark, final_mark_rect)

def _render_player(screen, selected_difficuly):
    """render player based on current position and rotation"""
    grid_layout = _get_grid_layout(selected_difficuly)

    sprite_size = max(1, grid_layout["room_size"] - PADDING_BIG)
    image = pg.transform.scale(player.image, (sprite_size, sprite_size))
    rotated_image = pg.transform.rotate(image, player.rotation)

    clamped_x = min(player.pos_x, grid_layout["grid_w"] - 1)
    clamped_y = min(player.pos_y, grid_layout["grid_h"] - 1)

    x = grid_layout["grid_left"] + clamped_x * (grid_layout["room_size"] + PADDING_SMALL)
    y = grid_layout["grid_top"] + clamped_y * (grid_layout["room_size"] + PADDING_SMALL)

    player_rect = rotated_image.get_rect(center=(x + grid_layout["room_size"] // 2, y + grid_layout["room_size"] // 2))
    screen.blit(rotated_image, player_rect)

def render(screen, selected_difficuly):
    """collect all rendering helpers into one render func for the entire game screen"""
    screen.blit(background, (0, 0))

    _render_grid(screen, selected_difficuly)
    _render_player(screen, selected_difficuly)

# ============ EVENT HANDLING ============
def handle_events(event: pg.event.Event, selected_difficuly):
    if event.type == pg.KEYDOWN:
        grid_layout = _get_grid_layout(selected_difficuly)

        match event.key:
            case pg.K_ESCAPE:
                return "starting_screen"

            case pg.K_RIGHT:
                player.pos_x = min(player.pos_x + 1, grid_layout["grid_w"] - 1)
                player.rotation = 90
                player.visited_rooms.add((player.pos_x, player.pos_y))
            case pg.K_DOWN:
                player.pos_y = min(player.pos_y + 1, grid_layout["grid_h"] - 1)
                player.rotation = 0
                player.visited_rooms.add((player.pos_x, player.pos_y))
    

    return None

__all__ = ["render", "handle_events"]
