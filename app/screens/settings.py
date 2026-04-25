import pygame as pg

from app.assets import *
from app.config import *

from app.helpers import button_pressed

# ============ SETTINGS VALUES ============
DIFFICULTY_BUTTONS = {
    "easy": difficulty_easy_button,
    "medium": difficulty_medium_button,
    "hard": difficulty_hard_button,
}
SETTINGS_SUBHEADINGS = ("Difficulty", "Name", "Audio")

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
name_field_active = False
name_submitted = False
submit_selected_until = 0

SUBMIT_FLASH_MS = 300

def _handle_settings_name_keydown(event: pg.event.Event, field_rect: pg.Rect, settings_name, settings_cursor):
    """handle a key being pressed if the name is currently being typed in"""
    old_name = settings_name

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
    return settings_name, settings_name != old_name

def _move_cursor_to_end(field_rect: pg.Rect, settings_name):
    """put the text cursor at the end of the name field"""
    settings_cursor.col = len(settings_name)
    settings_cursor.update_scroll(field_rect, settings_name)

def _get_submit_button_image():
    """return the current submit button image"""
    if name_submitted:
        if pg.time.get_ticks() < submit_selected_until:
            return submit_name_buttons["selected"]
        return submit_name_buttons["dimmed"]

    return submit_name_buttons["default"]

# ============ LAYOUT ============
def _get_settings_layout():
    """calculate and return all the rectangles and rendered text needed to draw the settings screen"""
    window_rect = settings_window.get_rect(center=(WIDTH // 2, HEIGHT // 2)) # create the settings window in the center
    close_rect = close_button.get_rect(center=(window_rect.left + 10, window_rect.top + 10)) # create close button
    
    # create title text and rect
    title_y = window_rect.top + 66
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
        "Difficulty": left_rect.left + SETTINGS_TEXT_OFFSET_X,
        "Name": name_section_rect.left + SETTINGS_TEXT_OFFSET_X - 16,
        "Audio": audio_section_rect.left + SETTINGS_TEXT_OFFSET_X,
    }
    section_tops = {
        "Difficulty": left_rect.top - PADDING_SMALL,
        "Name": name_section_rect.top - PADDING_SMALL,
        "Audio": audio_section_rect.top - PADDING_SMALL // 2,
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

    # outline difficulty buttons boundaries
    difficulty_buttons_top = subheadings["difficulty"]["rect"].bottom + section_title_gap
    difficulty_buttons_bottom = left_rect.bottom - PADDING_SMALL
    difficulty_buttons_height = difficulty_buttons_bottom - difficulty_buttons_top
    difficulty_gap = SETTINGS_DIFFICULTY_GAP
    difficulty_button_height = max(1, (difficulty_buttons_height - difficulty_gap * 2) // 3)

    # create each difficulty button's rect
    difficulty_rects = {}
    current_top = difficulty_buttons_top
    for difficulty in DIFFICULTY_BUTTONS:
        # fill any leftovers by stretching the last button
        if difficulty == "hard":
            button_height = difficulty_buttons_bottom - current_top
        else:
            button_height = difficulty_button_height
        difficulty_rects[difficulty] = pg.Rect(left_rect.left, current_top, left_rect.width, button_height)
        current_top += button_height + difficulty_gap

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
        field_rect.bottom + PADDING_SMALL - 15,
        name_section_rect.width,
        80,
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
        "difficulty_rects": difficulty_rects,
        "subheadings": subheadings,
        "sound_button_rect": sound_rect,
        "music_button_rect": music_rect,
        "name_field_rect": field_rect,
        "submit_rect": submit_rect,
    }

# ============ RENDERING ============
def _render_settings_text_field(screen, field_rect: pg.Rect, settings_name, settings_cursor):
    """render the text field and cursor for the name input in settings"""
    screen.blit(pg.transform.scale(name_input_field, field_rect.size), field_rect)

    rendered_text = BODY.render(settings_name, True, BROWN)

    clip_rect = screen.get_clip()
    screen.set_clip(field_rect.inflate(-PADDING_SMALL, 0))

    text_x = field_rect.x + PADDING_SMALL - settings_cursor.scroll_px
    screen.blit(rendered_text, (text_x, field_rect.y + (field_rect.height - rendered_text.get_height()) // 2))

    if name_field_active and (pg.time.get_ticks() // 500) % 2 == 0:
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

def render(screen, selected_difficulty, settings_name, sound_fx_enabled, music_enabled):
    """get the layout from _get_settings_layout and render the settings menu using it"""
    layout = _get_settings_layout()

    screen.blit(settings_window, layout["window_rect"])
    screen.blit(close_button, layout["close_rect"])
    screen.blit(layout["title_text"], layout["title_rect"])

    for subheading in layout["subheadings"].values():
        screen.blit(subheading["surface"], subheading["rect"])

    for difficulty, rect in layout["difficulty_rects"].items():
        button_image = DIFFICULTY_BUTTONS[difficulty]["selected" if selected_difficulty == difficulty else "unselected"]
        screen.blit(pg.transform.scale(button_image, rect.size), rect)

        difficulty_text = SUBTITLE.render(difficulty.upper(), True, WHITE)
        text_rect = difficulty_text.get_rect(center=rect.center)
        screen.blit(difficulty_text, text_rect)

    _render_settings_text_field(screen, layout["name_field_rect"], settings_name, settings_cursor)
    screen.blit(pg.transform.scale(_get_submit_button_image(), layout["submit_rect"].size), layout["submit_rect"])
    _render_audio_button(screen, layout["sound_button_rect"], icon_sfx, sound_fx_enabled)
    _render_audio_button(screen, layout["music_button_rect"], icon_music, music_enabled)

# ============ HANDLE EVENTS ============
def handle_events(event: pg.event.Event, selected_difficulty, settings_name, sound_fx_enabled, music_enabled):
    global name_field_active, name_submitted, submit_selected_until

    state = "settings"
    layout = _get_settings_layout()

    if button_pressed(event, layout["close_rect"]):
        state = "starting_screen"
        name_field_active = False
    
    if button_pressed(event, layout["name_field_rect"]):
        name_field_active = True
        settings_cursor.col = len(settings_name)
        settings_cursor.update_scroll(layout["name_field_rect"], settings_name)
    elif button_pressed(event, layout["submit_rect"]):
        name_field_active = False

    for difficulty, rect in layout["difficulty_rects"].items():
        if button_pressed(event, rect):
            selected_difficulty = difficulty

    if button_pressed(event, layout["sound_button_rect"]):
        sound_fx_enabled = not sound_fx_enabled

    if button_pressed(event, layout["music_button_rect"]):
        if music_enabled:
            pg.mixer.music.pause()
        else:
            pg.mixer.music.unpause()
        music_enabled = not music_enabled

    if button_pressed(event, layout["submit_rect"]) and not name_submitted:
        name_submitted = True
        submit_selected_until = pg.time.get_ticks() + SUBMIT_FLASH_MS

    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            state = "starting_screen"
            name_field_active = False
        elif name_field_active:
            settings_name, name_changed = _handle_settings_name_keydown(event, layout["name_field_rect"], settings_name, settings_cursor)
            if name_changed:
                name_submitted = False
        else:
            pass

    return state, selected_difficulty, settings_name, sound_fx_enabled, music_enabled

__all__ = ["render", "handle_events"]
