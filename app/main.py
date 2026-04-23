import pygame as pg
from app.assets import *
from app.config import *
from app.screens.settings import handle_events as handle_settings_events, render as render_settings
from app.screens.game import handle_events as handle_game_events, render as render_game
from app.screens.starting import handle_events as handle_starting_events, render as render_starting

# ============ INIT ============
pg.init()
pg.mixer.init()

# ============ LOGIC ============
# ~~~~~~ CONFIGURABLE VALUES IN SETTINGS ~~~~~~ # todo: create json
selected_difficuly = "medium"
settings_name = ""
sfx_enabled = True
music_enabled = True

# ============ GAME LOOP FUNCS ============ 

def render():
    match state:
        case "starting_screen":
            render_starting(screen)
        case "game":
            render_game(screen, selected_difficuly)
        case "settings":
            render_starting(screen)
            render_settings(screen, selected_difficuly, settings_name, sfx_enabled, music_enabled)

def handle_events():
    global state, selected_difficuly, settings_name, sfx_enabled, music_enabled
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if state == "starting_screen":
            new_state = handle_starting_events(event)
            if new_state:
                state = new_state

        elif state == "settings":
            state, selected_difficuly, settings_name, sfx_enabled, music_enabled = handle_settings_events(
                event,
                selected_difficuly,
                settings_name,
                sfx_enabled,
                music_enabled,
            )

        elif state == "game":
            new_state = handle_game_events(event, selected_difficuly)
            if new_state:
                state = new_state

    return True

# ============ MAIN SCREEN ============

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Night at The Museum")
clock = pg.time.Clock()
pg.key.set_repeat(400, 40)

# ============ MAIN LOOP ============

running = True
state = "starting_screen"
pg.mixer.music.play(-1)
while running:
    running = handle_events()

    render()

    pg.display.flip()
    clock.tick(10)
