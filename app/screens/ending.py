import pygame as pg

from app.assets import *
from app.config import *
from app.helpers import *

# ============ LAYOUT ============

def _get_game_over_layout():
    window_rect = ending_gameover_window.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    title_y = window_rect.top + 80
    title_text = TITLE.render("Game Over!", True, WHITE)
    title_rect = title_text.get_rect(midtop=(WIDTH // 2, title_y))

    subtitle_y = title_rect.bottom + 5
    subtitle_text = BODY.render("A guard caught you!", True, WHITE)
    subtitle_rect = subtitle_text.get_rect(midtop=(WIDTH // 2, subtitle_y))

    # buttons
    buttons_y = subtitle_rect.bottom + 25
    total_buttons_width = generic_button.get_width() * 2 + 50
    buttons_left = WIDTH // 2 - total_buttons_width // 2

    # back button
    back_button_rect = generic_button.get_rect(topleft=(buttons_left, buttons_y))
    back_icon_rect = back_icon.get_rect(center=back_button_rect.center)

    # restart button
    restart_x = back_button_rect.right + 50
    restart_button_rect = generic_button.get_rect(topleft=(restart_x, buttons_y))
    restart_icon_rect = restart_icon.get_rect(center=restart_button_rect.center)

    return {
        "window_rect": window_rect,
        "title_text": title_text,
        "title_rect": title_rect,
        "subtitle_text": subtitle_text,
        "subtitle_rect": subtitle_rect,
        "back_button_rect": back_button_rect,
        "back_icon_rect": back_icon_rect,
        "restart_button_rect": restart_button_rect,
        "restart_icon_rect": restart_icon_rect,
    }

def _get_ending_window(percent):
    if percent < 20:
        return ending_charcoal_window
    if percent < 60:
        return ending_bronze_window
    if percent < 90:
        return ending_silver_window
    return ending_gold_window

def _get_ending_layout(score, max_score):
    percent = 100 if max_score == 0 else round(score / max_score * 100)
    window_image = _get_ending_window(percent)
    window_rect = window_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    title_y = window_rect.top + 80
    title_text = TITLE.render(f"{percent}%", True, WHITE)
    title_rect = title_text.get_rect(midtop=(WIDTH // 2, title_y))

    subtitle_y = title_rect.bottom + 5
    subtitle_text_comment = "Better luck next time!" if percent < 20 else "You can do better!" if percent < 60 else "Great job!" if percent < 90 else "Excellent!" if percent < 100 else "Perfect!"
    subtitle_text = BODY.render(f"{score}/{max_score} score: {subtitle_text_comment}, ", True, WHITE)
    subtitle_rect = subtitle_text.get_rect(midtop=(WIDTH // 2, subtitle_y))

    # buttons
    buttons_y = subtitle_rect.bottom + 25
    total_buttons_width = generic_button.get_width() * 2 + 50
    buttons_left = WIDTH // 2 - total_buttons_width // 2

    # back button
    back_button_rect = generic_button.get_rect(topleft=(buttons_left, buttons_y))
    back_icon_rect = back_icon.get_rect(center=back_button_rect.center)

    # restart button
    restart_x = back_button_rect.right + 50
    restart_button_rect = generic_button.get_rect(topleft=(restart_x, buttons_y))
    restart_icon_rect = restart_icon.get_rect(center=restart_button_rect.center)

    return {
        "window_image": window_image,
        "window_rect": window_rect,
        "title_text": title_text,
        "title_rect": title_rect,
        "subtitle_text": subtitle_text,
        "subtitle_rect": subtitle_rect,
        "back_button_rect": back_button_rect,
        "back_icon_rect": back_icon_rect,
        "restart_button_rect": restart_button_rect,
        "restart_icon_rect": restart_icon_rect,
    }

# ============ RENDER ============

def render_game_over(screen):
    layout = _get_game_over_layout()
    screen.blit(ending_gameover_window, layout["window_rect"])
    screen.blit(layout["title_text"], layout["title_rect"])
    screen.blit(layout["subtitle_text"], layout["subtitle_rect"])
    screen.blit(generic_button, layout["back_button_rect"])
    screen.blit(back_icon, layout["back_icon_rect"])
    screen.blit(generic_button, layout["restart_button_rect"])
    screen.blit(restart_icon, layout["restart_icon_rect"])

def render_ending(screen, score, max_score):
    layout = _get_ending_layout(score, max_score)
    screen.blit(layout["window_image"], layout["window_rect"])
    screen.blit(layout["title_text"], layout["title_rect"])
    screen.blit(layout["subtitle_text"], layout["subtitle_rect"])
    screen.blit(generic_button, layout["back_button_rect"])
    screen.blit(back_icon, layout["back_icon_rect"])
    screen.blit(generic_button, layout["restart_button_rect"])
    screen.blit(restart_icon, layout["restart_icon_rect"])

# ============ EVENT HANDLING ============

def handle_events(event: pg.event.Event, state="game_over", score=0, max_score=0):
    if state == "game_end":
        layout = _get_ending_layout(score, max_score)
    else:
        layout = _get_game_over_layout()

    if button_pressed(event, layout["back_button_rect"]):
        return "starting_screen"

    if button_pressed(event, layout["restart_button_rect"]):
        return "game"

    return state

__all__ = ["render_game_over", "render_ending", "handle_events"]
