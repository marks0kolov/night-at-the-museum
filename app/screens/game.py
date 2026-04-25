import pygame as pg
import random

from app.assets import *
from app.config import *
from app.museum import ARTIFACT_SCORE, GEM_SCORE, generate_museum, solve_museum

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
museum = None
turn = 0
gem_image_by_room = {}
artifact_image_by_room = {}

ARROW_ROTATIONS = {
    (1, 0): 0,
    (1, 1): -45,
    (0, 1): -90,
    (-1, 1): -135,
    (-1, 0): 180,
    (-1, -1): 135,
    (0, -1): 90,
    (1, -1): 45,
} # there's 100% a better way to do this

# ============ LOGIC ============

def reset_game(selected_difficulty):
    """reset the player and generate a fresh museum"""
    global museum, turn, gem_image_by_room, artifact_image_by_room

    player.pos_x = 0
    player.pos_y = 0
    player.rotation = 0
    player.visited_rooms = {(0, 0)}
    turn = 0
    museum = generate_museum(selected_difficulty)
    gem_image_by_room = {room_pos: random.choice(gem_images) for room_pos in museum["gems"]}
    artifact_image_by_room = {room_pos: random.choice(artifact_images) for room_pos in museum["artifacts"]}

def _get_current_guard_rooms():
    """return the rooms currently occupied by guards"""
    occupied_rooms = set()

    for cycle in museum["guards"]:
        if cycle:
            occupied_rooms.add(cycle[turn % len(cycle)])

    return occupied_rooms

def get_player_score():
    """calculate the score collected on the player's current path"""
    score = 0

    for room_pos in player.visited_rooms:
        if room_pos in museum["gems"]:
            score += GEM_SCORE
        if room_pos in museum["artifacts"]:
            score += ARTIFACT_SCORE

    return score

def get_max_score(selected_difficulty):
    """calculate the best score possible for the current museum"""
    return solve_museum(selected_difficulty, museum)

# ============ LAYOUT ============

def _get_grid_layout(selected_difficulty):
    """calculate the current grid size and room size from the selected difficulty"""
    grid_w, grid_h = GRID_SIZES[selected_difficulty]
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

def _get_room_center(grid_layout, room_pos):
    """return the center point of a room"""
    x = grid_layout["grid_left"] + room_pos[0] * (grid_layout["room_size"] + PADDING_SMALL)
    y = grid_layout["grid_top"] + room_pos[1] * (grid_layout["room_size"] + PADDING_SMALL)

    return (x + grid_layout["room_size"] // 2, y + grid_layout["room_size"] // 2)

def _get_rotation(dx, dy, default_angle=0):
    """turn a one-step direction into a sprite rotation"""
    if dx == 0 and dy == 0:
        return default_angle

    return ARROW_ROTATIONS[(dx, dy)]

def _get_guard_rotation(dx, dy):
    """turn a one-step direction into a guard rotation"""
    if dx == 0 and dy == 0:
        return 0

    return _get_rotation(dx, dy, 0) + 90

# ============ RENDER ============

def _render_grid(screen, grid_layout):
    """"render game grid of rooms"""
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

def _render_collectibles(screen, grid_layout):
    """render gems and artifacts"""
    item_size = max(1, int(grid_layout["room_size"] * 0.45))

    # render gems
    for room_pos in sorted(museum["gems"]):
        image = pg.transform.scale(gem_image_by_room[room_pos], (item_size, item_size))

        x = grid_layout["grid_left"] + room_pos[0] * (grid_layout["room_size"] + PADDING_SMALL)
        y = grid_layout["grid_top"] + room_pos[1] * (grid_layout["room_size"] + PADDING_SMALL)

        rect = image.get_rect(center=(x + grid_layout["room_size"] // 2, y + grid_layout["room_size"] // 2))
        
        screen.blit(image, rect)

    # render artifacts
    for room_pos in sorted(museum["artifacts"]):
        image = pg.transform.scale(artifact_image_by_room[room_pos], (item_size * 1.3, item_size * 1.3))

        x = grid_layout["grid_left"] + room_pos[0] * (grid_layout["room_size"] + PADDING_SMALL)
        y = grid_layout["grid_top"] + room_pos[1] * (grid_layout["room_size"] + PADDING_SMALL)

        rect = image.get_rect(center=(x + grid_layout["room_size"] // 2, y + grid_layout["room_size"] // 2))

        screen.blit(image, rect)

def _render_guard_paths(screen, grid_layout):
    """render each guard cycle using arrows between rooms"""
    arrow_length = max(PADDING_SMALL * 4, int(grid_layout["room_size"] * 0.5))
    arrow_thick = max(PADDING_SMALL, int(grid_layout["room_size"] * 0.2))

    for cycle in museum["guards"]:
        if len(cycle) <= 1:
            continue

        next_index = turn % len(cycle)

        for i, start_room in enumerate(cycle):
            next_room = cycle[(i + 1) % len(cycle)]

            start_center = _get_room_center(grid_layout, start_room)
            next_center = _get_room_center(grid_layout, next_room)

            arrow_image = arrow_default if i == next_index else arrow_dimmed
            arrow_surface = pg.transform.scale(arrow_image, (arrow_length, arrow_thick))

            dx = next_room[0] - start_room[0]
            dy = next_room[1] - start_room[1]

            angle = _get_rotation(dx, dy)
            rotated_arrow = pg.transform.rotate(arrow_surface, angle)

            arrow_rect = rotated_arrow.get_rect(center=((start_center[0] + next_center[0]) // 2, (start_center[1] + next_center[1]) // 2))
            screen.blit(rotated_arrow, arrow_rect)

def _render_guards(screen, grid_layout):
    """render guards at their current positions in the cycle"""
    guard_size = max(1, int(grid_layout["room_size"] * 0.6))
    guard_surface = pg.transform.scale(guard_image, (guard_size, guard_size))

    for cycle in museum["guards"]:
        if not cycle:
            continue

        current_index = turn % len(cycle)
        room_pos = cycle[current_index]

        next_room = cycle[(current_index + 1) % len(cycle)]
        dx = next_room[0] - room_pos[0]
        dy = next_room[1] - room_pos[1]
        angle = _get_guard_rotation(dx, dy)
        rotated_guard = pg.transform.rotate(guard_surface, angle)

        guard_rect = rotated_guard.get_rect(center=_get_room_center(grid_layout, room_pos))
        screen.blit(rotated_guard, guard_rect)

def _render_player(screen, grid_layout):
    """render player based on current position and rotation"""
    sprite_size = max(1, grid_layout["room_size"] - PADDING_BIG)
    image = pg.transform.scale(player.image, (sprite_size, sprite_size))
    rotated_image = pg.transform.rotate(image, player.rotation)

    clamped_x = min(player.pos_x, grid_layout["grid_w"] - 1)
    clamped_y = min(player.pos_y, grid_layout["grid_h"] - 1)

    x = grid_layout["grid_left"] + clamped_x * (grid_layout["room_size"] + PADDING_SMALL)
    y = grid_layout["grid_top"] + clamped_y * (grid_layout["room_size"] + PADDING_SMALL)

    player_rect = rotated_image.get_rect(center=(x + grid_layout["room_size"] // 2, y + grid_layout["room_size"] // 2))
    screen.blit(rotated_image, player_rect)

def render(screen, selected_difficulty):
    """collect all rendering helpers into one render func for the entire game screen"""
    grid_layout = _get_grid_layout(selected_difficulty)

    screen.blit(background, (0, 0))

    _render_grid(screen, grid_layout)
    _render_guard_paths(screen, grid_layout)
    _render_collectibles(screen, grid_layout)
    _render_guards(screen, grid_layout)
    _render_player(screen, grid_layout)

# ============ EVENT HANDLING ============

def handle_events(event: pg.event.Event, selected_difficulty):
    global turn

    if event.type == pg.KEYDOWN:
        grid_layout = _get_grid_layout(selected_difficulty)
        moved = False

        match event.key:
            case pg.K_RIGHT:
                if player.pos_x < grid_layout["grid_w"] - 1:
                    player.pos_x += 1
                    player.rotation = 90
                    moved = True
            case pg.K_DOWN:
                if player.pos_y < grid_layout["grid_h"] - 1:
                    player.pos_y += 1
                    player.rotation = 0
                    moved = True

        if moved:
            player.visited_rooms.add((player.pos_x, player.pos_y))
            turn += 1

            if (player.pos_x, player.pos_y) in _get_current_guard_rooms():
                return "game_over"

            if (player.pos_x, player.pos_y) == (grid_layout["grid_w"] - 1, grid_layout["grid_h"] - 1):
                return "game_end"
    
    return "game"

__all__ = ["render", "handle_events", "reset_game", "get_player_score", "get_max_score"]
