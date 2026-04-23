# ============ IMPORTS ============
import pygame as pg
from assets import *
from config import *

# ============ INIT ============
pg.init()
pg.mixer.init()

# ============ LOGIC ============
# ~~~~~~ PLAYER ~~~~~~
class Player:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.rotation = 0
        self.bag_size = "big"
        self.image = player_images[self.bag_size]

player = Player()

# ~~~~~~ CONFIGURABLE VALUES IN SETTINGS ~~~~~~ # todo: create json
selected_difficuly = "medium"
settings_name = ""
sound_fx_enabled = True
music_enabled = True

# ~~~~~~ SIZES ~~~~~~ # todo: move this somewhere else
DIFFICULY_BUTTONS = {
    "easy": difficuly_easy_button,
    "medium": difficuly_medium_button,
    "hard": difficuly_hard_button,
}
SETTINGS_SUBHEADINGS = ("Difficuly", "Name", "Audio")

# ~~~~~~ INPUT FIELD ~~~~~~
class SettingsCursor:
    def __init__(self):
        self.col = 0
        self.scroll_px = 0

    def update_scroll(self, rect: pg.Rect):
        cursor_x = BODY.size(settings_name[:self.col])[0]
        visible_width = rect.w - PADDING_BIG
        if cursor_x - self.scroll_px > visible_width:
            self.scroll_px = cursor_x - visible_width
        elif cursor_x - self.scroll_px < 0:
            self.scroll_px = cursor_x
        self.scroll_px = max(0, self.scroll_px)

settings_cursor = SettingsCursor()

# ============ FUNCTIONS ============ # todo: split into multiple files

# -------- HELPERS --------
def _button_pressed(event: pg.event.Event, button_rect: pg.Rect):
    """check if a button is from an event and it's rectangle"""
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if button_rect.collidepoint(event.pos):
            return True
    return False

def _set_state(new_state: str):
    """set game state"""
    global state
    state = new_state

# -------- STARTING SCREEEN --------
# ~~~~~~ LAYOUT ~~~~~~
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

# ~~~~~~ RENDERING ~~~~~~
def render_starting_screen():
    screen.blit(background, (0, 0))

    layout = _get_starting_screen_layout()

    screen.blit(layout["title_text"], layout["title_rect"])
    screen.blit(start_button, layout["start_button_rect"])
    screen.blit(pg.transform.scale(generic_button, layout["settings_button_rect"].size), layout["settings_button_rect"])
    screen.blit(layout["start_text"], layout["start_text_rect"])
    screen.blit(layout["settings_icon"], layout["settings_icon_rect"])

# -------- GAME --------
# ~~~~~~ LAYOUT ~~~~~~
def _get_grid_layout():
    """calculate the current grid size and room size from the selected difficuly"""
    grid_w, grid_h = GRID_SIZES[selected_difficuly]
    room_width = (GRID_PIXEL_WIDTH - (grid_w + 1) * PADDING_SMALL) // grid_w
    room_height = (GRID_PIXEL_HEIGHT - (grid_h + 1) * PADDING_SMALL) // grid_h
    room_size = max(1, min(room_width, room_height))
    return {
        "grid_w": grid_w,
        "grid_h": grid_h,
        "room_size": room_size,
    }

# ~~~~~~ RENDERING ~~~~~~
def _render_grid():
    """"render game grid of rooms"""
    grid_layout = _get_grid_layout()
    room_surface = pg.transform.scale(room, (grid_layout["room_size"], grid_layout["room_size"]))
    for i in range(grid_layout["grid_w"]):
        for j in range(grid_layout["grid_h"]):
            x = GRID_OFFSET_X + PADDING_SMALL + i * (grid_layout["room_size"] + PADDING_SMALL)
            y = GRID_OFFSET_Y + PADDING_SMALL + j * (grid_layout["room_size"] + PADDING_SMALL)
            screen.blit(room_surface, (x, y))

def _render_player():
    """render player based on current position and rotation"""
    grid_layout = _get_grid_layout()
    sprite_size = max(1, grid_layout["room_size"] - PADDING_BIG)
    image = pg.transform.scale(player.image, (sprite_size, sprite_size))
    rotated_image = pg.transform.rotate(image, player.rotation)
    clamped_x = min(player.pos_x, grid_layout["grid_w"] - 1)
    clamped_y = min(player.pos_y, grid_layout["grid_h"] - 1)
    x = GRID_OFFSET_X + PADDING_SMALL + clamped_x * (grid_layout["room_size"] + PADDING_SMALL)
    y = GRID_OFFSET_Y + PADDING_SMALL + clamped_y * (grid_layout["room_size"] + PADDING_SMALL)
    player_rect = rotated_image.get_rect(center=(x + grid_layout["room_size"] // 2, y + grid_layout["room_size"] // 2))
    screen.blit(rotated_image, player_rect)

def render_game():
    """collect all rendering helpers into one render func for the entire game screen"""
    screen.blit(background, (0, 0))

    _render_grid()
    _render_player()

# -------- SETTINGS MENU --------
# ~~~~~~ LAYOUT ~~~~~~
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

# ~~~~~~ RENDERING ~~~~~~
def _render_audio_button(rect: pg.Rect, icon: pg.Surface, enabled: bool):
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

def render_settings_window():
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

    _render_settings_text_field(layout["name_field_rect"])
    screen.blit(pg.transform.scale(submit_name_button, layout["submit_rect"].size), layout["submit_rect"])
    _render_audio_button(layout["buttons"]["sound"], icon_sfx, sound_fx_enabled)
    _render_audio_button(layout["buttons"]["music"], icon_music, music_enabled)

# ~~~~~~ TEXT INPUT ~~~~~~
def _render_settings_text_field(field_rect: pg.Rect):
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

def _handle_settings_name_keydown(event: pg.event.Event, field_rect: pg.Rect):
    """handle a key being pressed if the name is currently being typed in"""
    global settings_name

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

    settings_cursor.update_scroll(field_rect)

# -------- GAME LOOP --------
def handle_events():
    global state, selected_difficuly, sound_fx_enabled, music_enabled
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False

        if state == "starting_screen":
            settings_layout = _get_starting_screen_layout()

            if _button_pressed(event, settings_layout["start_button_rect"]):
                _set_state("game")

            if _button_pressed(event, settings_layout["settings_button_rect"]):
                _set_state("settings")

        elif state == "settings":
            layout = _get_settings_layout()

            if _button_pressed(event, layout["close_rect"]):
                _set_state("starting_screen")

            for difficuly, rect in layout["difficuly_rects"].items():
                if _button_pressed(event, rect):
                    selected_difficuly = difficuly

            if _button_pressed(event, layout["buttons"]["sound"]):
                sound_fx_enabled = not sound_fx_enabled

            if _button_pressed(event, layout["buttons"]["music"]):
                if music_enabled:
                    pg.mixer.music.pause()
                else:
                    pg.mixer.music.unpause()
                music_enabled = not music_enabled

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    _set_state("starting_screen")
                else:
                    _handle_settings_name_keydown(event, layout["name_field_rect"])

        elif state == "game":
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                _set_state("starting_screen")

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

    match state:
        case "starting_screen":
            render_starting_screen()
        case "game":
            render_game()
        case "settings":
            render_starting_screen()
            render_settings_window()

    pg.display.flip()
    clock.tick(10)