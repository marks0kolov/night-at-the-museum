import pygame as pg

def button_pressed(event: pg.event.Event, button_rect: pg.Rect):
    """check if a button is pressed from an event and it's rectangle"""
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if button_rect.collidepoint(event.pos):
            return True
    return False