import pygame as pg

from app.assets import *
from app.config import *

from app.helpers import button_pressed

# ============ LAYOUT ============
def _get_starting_screen_layout():
    """create rects for the start screen"""
    # start and settings buttons
    settings_button_size = start_button.get_height()
    total_width = start_button.get_width() + settings_button_size + PADDING_SMALL
    start_x = WIDTH // 2 - total_width // 2
    settings_x = start_x + start_button.get_width() + PADDING_SMALL
    start_rect = start_button.get_rect(topleft=(start_x, START_BUTTONS_Y))
    settings_rect = pg.Rect(settings_x, START_BUTTONS_Y, settings_button_size, settings_button_size)

    # title render and rect
    title_text = TITLE.render("Night at The Museum", True, WHITE)
    title_rect = title_text.get_rect(midtop=(WIDTH // 2, START_TITLE_Y))

    # start text render and rect
    start_text = SUBTITLE.render("START", True, BROWN)
    start_text_rect = start_text.get_rect(center=start_rect.center)

    # settings icon rect
    settings_icon_size = int(settings_rect.width * 0.7)
    settings_icon = pg.transform.scale(icon_settings, (settings_icon_size, settings_icon_size))
    settings_icon_rect = settings_icon.get_rect(center=settings_rect.center)
    
    return {
        "start_button_rect": start_rect,
        "settings_button_rect": settings_rect,
        "title_text": title_text,
        "start_text": start_text,
        "settings_icon": settings_icon,
        "settings_icon_rect": settings_icon_rect,
        "title_rect": title_rect,
        "start_text_rect": start_text_rect,
    }

# ============ RENDERING ============
def render(screen):
    screen.blit(background, (0, 0))

    layout = _get_starting_screen_layout()

    screen.blit(layout["title_text"], layout["title_rect"])
    screen.blit(start_button, layout["start_button_rect"])
    screen.blit(pg.transform.scale(generic_button, layout["settings_button_rect"].size), layout["settings_button_rect"])
    screen.blit(layout["start_text"], layout["start_text_rect"])
    screen.blit(layout["settings_icon"], layout["settings_icon_rect"])

# ============ EVENT HANDLING ============
def handle_events(event: pg.event.Event):        
    settings_layout = _get_starting_screen_layout()

    if button_pressed(event, settings_layout["start_button_rect"]):
        return "game"

    if button_pressed(event, settings_layout["settings_button_rect"]):
        return "settings"

    return "starting_screen"

__all__ = ["render", "handle_events"]
