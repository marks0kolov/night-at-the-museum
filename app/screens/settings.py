import pygame as pg

from app.assets import *
from app.config import *

from app.helpers import button_pressed

# ============ SETTINGS VALUES ============
DIFFICULY_BUTTONS = {
    "easy": difficuly_easy_button,
    "medium": difficuly_medium_button,
    "hard": difficuly_hard_button,
}
SETTINGS_SUBHEADINGS = ("Difficuly", "Name", "Audio")

# ============ INPUT FIELD LOGIC ============
class SettingsCursor:
    def __init__(self):
        self.col = 0
        self.scroll_px = 0

    def update_scroll(self, rect: pg.Rect, settings_name):
        cursor_x = BODY.size(settings_name[:self.col])[0]
        visible_width = rect.w - PADDING_BIG
        if cursor_x - self.scroll_px > visible_width:
            self.scroll_px = cursor_x - visible_width
        elif cursor_x - self.scroll_px < 0:
            self.scroll_px = cursor_x
        self.scroll_px = max(0, self.scroll_px)

settings_cursor = SettingsCursor()

def _handle_settings_name_keydown(event: pg.event.Event, field_rect: pg.Rect, settings_name, settings_cursor):
    """handle a key being pressed if the name is currently being typed in"""
    if event.key == pg.K_BACKSPACE:
        if settings_cursor.col > 0:
            settings_name = settings_name[:settings_cursor.col - 1] + settings_name[settings_cursor.col:]
            settings_cursor.col -= 1
    elif event.key == pg.K_RIGHT:
        if settings_cursor.col < len(settings_name):
            settings_cursor.col += 1
    elif event.key == pg.K_LEFT:
        if settings_cursor.col > 0:
            settings_cursor.col -= 1
    elif event.unicode:
        settings_name = settings_name[:settings_cursor.col] + event.unicode + settings_name[settings_cursor.col:]
        settings_cursor.col += 1
    elif event.key == pg.K_RETURN:
        pass

    settings_cursor.update_scroll(field_rect, settings_name)
    return settings_name

# ============ LAYOUT ============
def _get_settings_layout():
    """calculate and return all the rectangles and rendered text needed to draw the settings screen"""
    #! some ai was used when writing this function, however, all the comments were written by me and i reviewed every single line. 
    #! just come on, there's no way i'd be wasting my time on this.
    window_rect = settings_window.get_rect(center=(WIDTH // 2, HEIGHT // 2)) # create the settings window in the center
    close_rect = close_button.get_rect(center=(window_rect.left + 10, window_rect.top + 10)) # create close button
    
    # create title text and rect
    title_y = window_rect.top + SETTINGS_TITLE_Y_OFFSET
    title_text = HEADING.render("Settings", True, BROWN)
    title_rect = title_text.get_rect(midtop=(window_rect.centerx, title_y))

    # outline safe content area
    inner_left = window_rect.left + SETTINGS_BORDER + SETTINGS_SIDE_PADDING // 2
    inner_right = window_rect.right - SETTINGS_BORDER - SETTINGS_SIDE_PADDING // 2
    bottom_padding = SETTINGS_BORDER
    column_gap = SETTINGS_COLUMN_GAP + 8
    content_top = title_rect.bottom + SETTINGS_CONTENT_TOP_GAP
    content_height = window_rect.bottom - content_top - bottom_padding

    # split space into 2 columns with a gap in between
    left_width = (inner_right - inner_left - column_gap) // 2
    right_width = left_width
    left_rect = pg.Rect(inner_left, content_top, left_width, content_height)
    right_rect = pg.Rect(left_rect.right + column_gap, content_top, right_width, content_height)

    # outline gaps inside columns
    section_gap = SETTINGS_SECTION_GAP
    name_height = SETTINGS_NAME_SECTION_HEIGHT
    audio_height = right_rect.height - name_height - section_gap

    # player name input rect
    name_section_rect = pg.Rect(right_rect.left, right_rect.top, right_rect.width, name_height)
    # audio control rect
    audio_section_rect = pg.Rect(right_rect.left, name_section_rect.bottom + section_gap, right_rect.width, audio_height)

    # vertical space between section titles and corresponding content
    section_title_gap = SETTINGS_SECTION_TITLE_GAP
    # position for each title
    section_lefts = {
        "Difficuly": left_rect.left + SETTINGS_TEXT_OFFSET_X,
        "Name": name_section_rect.left + SETTINGS_TEXT_OFFSET_X - 16,
        "Audio": audio_section_rect.left + SETTINGS_TEXT_OFFSET_X,
    }
    section_tops = {
        "Difficuly": left_rect.top - PADDING_SMALL,
        "Name": name_section_rect.top - PADDING_SMALL,
        "Audio": audio_section_rect.top - PADDING_SMALL // 2 + 17,
    }

    # render subheading text and rect for each section
    subheadings = {}
    for text in SETTINGS_SUBHEADINGS:
        surface = SUBTITLE.render(text, True, BROWN)
        rect = surface.get_rect(topleft=(section_lefts[text], section_tops[text]))
        subheadings[text.lower()] = {
            "surface": surface,
            "rect": rect,
        }

    # outline difficuly buttons boundaries
    difficuly_buttons_top = subheadings["difficuly"]["rect"].bottom + section_title_gap
    difficuly_buttons_bottom = left_rect.bottom - PADDING_SMALL
    difficuly_buttons_height = difficuly_buttons_bottom - difficuly_buttons_top
    difficuly_gap = SETTINGS_DIFFICULY_GAP
    difficuly_button_height = max(1, (difficuly_buttons_height - difficuly_gap * 2) // 3)

    # create each difficuly button's rect
    difficuly_rects = {}
    current_top = difficuly_buttons_top
    for difficuly in DIFFICULY_BUTTONS:
        # fill any leftovers by stretching the last button
        if difficuly == "hard":
            button_height = difficuly_buttons_bottom - current_top
        else:
            button_height = difficuly_button_height
        difficuly_rects[difficuly] = pg.Rect(left_rect.left, current_top, left_rect.width, button_height)
        current_top += button_height + difficuly_gap

    # create text field
    field_rect = pg.Rect(
        name_section_rect.left,
        subheadings["name"]["rect"].bottom + section_title_gap,
        name_section_rect.width,
        TEXT_FIELD_HEIGHT,
    )
    # create submit button
    submit_rect = pg.Rect(
        name_section_rect.left,
        field_rect.bottom + PADDING_SMALL - 10,
        name_section_rect.width,
        96,
    )

    # outline audio buttons borders
    audio_buttons_top = subheadings["audio"]["rect"].bottom + section_title_gap - 17
    audio_button_size = min(
        (audio_section_rect.width - PADDING_SMALL) // 2,
        audio_section_rect.bottom - audio_buttons_top,
    )
    # SFX button
    sound_rect = pg.Rect(audio_section_rect.left, audio_buttons_top, audio_button_size, audio_button_size)
    # music button
    music_rect = pg.Rect(sound_rect.right + PADDING_SMALL, audio_buttons_top, audio_button_size, audio_button_size)

    # return every rect and text created
    return {
        "window_rect": window_rect,
        "close_rect": close_rect,
        "title_rect": title_rect,
        "title_text": title_text,
        "difficuly_rects": difficuly_rects,
        "subheadings": subheadings,
        "buttons": {
            "sound": sound_rect,
            "music": music_rect,
        },
        "name_field_rect": field_rect,
        "submit_rect": submit_rect,
    }
    # phew

# ============ RENDERING ============
def _render_settings_text_field(screen, field_rect: pg.Rect, settings_name, settings_cursor):
    """render the text field and cursor for the name input in settings"""
    screen.blit(pg.transform.scale(name_input_field, field_rect.size), field_rect)

    rendered_text = BODY.render(settings_name, True, BROWN)

    clip_rect = screen.get_clip()
    screen.set_clip(field_rect.inflate(-PADDING_SMALL, 0))

    text_x = field_rect.x + PADDING_SMALL - settings_cursor.scroll_px
    screen.blit(rendered_text, (text_x, field_rect.y + (field_rect.height - rendered_text.get_height()) // 2))

    if (pg.time.get_ticks() // 500) % 2 == 0:
        cursor_x = field_rect.x + PADDING_SMALL + BODY.size(settings_name[:settings_cursor.col])[0] - settings_cursor.scroll_px
        cursor_h = BODY.get_height()
        cursor_y = field_rect.y + (field_rect.height - cursor_h) // 2
        pg.draw.rect(screen, BROWN, (cursor_x, cursor_y, 3, cursor_h), border_radius=2)

    screen.set_clip(clip_rect)

def _render_audio_button(screen, rect: pg.Rect, icon: pg.Surface, enabled: bool):
    """render button for toggling sound or music in settings"""
    screen.blit(pg.transform.scale(generic_button, rect.size), rect)

    icon_size = int(min(rect.width, rect.height) * 0.7)
    icon_surface = pg.transform.scale(icon, (icon_size, icon_size))
    icon_rect = icon_surface.get_rect(center=rect.center)
    screen.blit(icon_surface, icon_rect)

    if not enabled:
        off_size = int(min(rect.width, rect.height) * 0.9)
        off_surface = pg.transform.scale(icon_off, (off_size, off_size))
        off_rect = off_surface.get_rect(center=rect.center)
        screen.blit(off_surface, off_rect)

def render(screen, selected_difficuly, settings_name, sound_fx_enabled, music_enabled):
    """get the layout from _get_settings_layout and render the settings menu using it"""
    layout = _get_settings_layout()

    screen.blit(settings_window, layout["window_rect"])
    screen.blit(close_button, layout["close_rect"])
    screen.blit(layout["title_text"], layout["title_rect"])

    for subheading in layout["subheadings"].values():
        screen.blit(subheading["surface"], subheading["rect"])

    for difficuly, rect in layout["difficuly_rects"].items():
        button_image = DIFFICULY_BUTTONS[difficuly]["selected" if selected_difficuly == difficuly else "unselected"]
        screen.blit(pg.transform.scale(button_image, rect.size), rect)

        difficuly_text = SUBTITLE.render(difficuly.upper(), True, WHITE)
        text_rect = difficuly_text.get_rect(center=rect.center)
        screen.blit(difficuly_text, text_rect)

    _render_settings_text_field(screen, layout["name_field_rect"], settings_name, settings_cursor)
    screen.blit(pg.transform.scale(submit_name_button, layout["submit_rect"].size), layout["submit_rect"])
    _render_audio_button(screen, layout["buttons"]["sound"], icon_sfx, sound_fx_enabled)
    _render_audio_button(screen, layout["buttons"]["music"], icon_music, music_enabled)

# ============ HANDLE EVENTS ============
def handle_events(event: pg.event.Event, selected_difficuly, settings_name, sound_fx_enabled, music_enabled):
    state = "settings"
    layout = _get_settings_layout()

    if button_pressed(event, layout["close_rect"]):
        state = "starting_screen"

    for difficuly, rect in layout["difficuly_rects"].items():
        if button_pressed(event, rect):
            selected_difficuly = difficuly

    if button_pressed(event, layout["buttons"]["sound"]):
        sound_fx_enabled = not sound_fx_enabled

    if button_pressed(event, layout["buttons"]["music"]):
        if music_enabled:
            pg.mixer.music.pause()
        else:
            pg.mixer.music.unpause()
        music_enabled = not music_enabled

    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            state = "starting_screen"
        else:
            settings_name = _handle_settings_name_keydown(event, layout["name_field_rect"], settings_name, settings_cursor)

    return state, selected_difficuly, settings_name, sound_fx_enabled, music_enabled

__all__ = ["render", "handle_events"]
