import pygame as pg
from app.config import WIDTH, HEIGHT, IMAGES_PATH, FONTS_PATH, MUSIC_PATH

# ============ COLORS ============
WHITE = (255, 255, 255)
BROWN = (42, 29, 18)

# ============ HELPERS ============

def _load_image(path, size=None):
    try:
        img = pg.image.load(path)
    except Exception:
        print(f"Error: image not found at path {path}")
        exit()
    
    if size:
        img = pg.transform.scale(img, size)
    return img

def _load_audio(path):
    try:
        audio = pg.mixer.Sound(path)
    except Exception:
        print(f"Error: audio not found at path {path}")
        exit()
    return audio

# ============ IMAGES ============
# ~~~~~~ SIZES ~~~~~~
START_BUTTON_SIZE = (450, 150)
SETTINGS_BUTTON_SIZE = START_BUTTON_SIZE[1]
SETTINGS_WINDOW_SIZE = (960, 680)
DIFFICULY_BUTTON_SIZE = (320, 116)
TOGGLE_BUTTON_SIZE = (176, 176)

# ~~~~~~ IMAGES ~~~~~~
start_button = _load_image(IMAGES_PATH / "button.start.png", START_BUTTON_SIZE)
icon_settings = _load_image(IMAGES_PATH / "icon.settings.png")

settings_window = _load_image(IMAGES_PATH / "settings_window.png", SETTINGS_WINDOW_SIZE)

name_input_field = _load_image(IMAGES_PATH / "name_input_field.png")
submit_name_button = _load_image(IMAGES_PATH / "button.submit_name.png")

close_button = _load_image(IMAGES_PATH / "button.close.png", (80, 80))

generic_button = _load_image(IMAGES_PATH / "button.generic.png", TOGGLE_BUTTON_SIZE)

icon_sfx = _load_image(IMAGES_PATH / "icon.sfx.png")
icon_music = _load_image(IMAGES_PATH / "icon.music.png")
icon_off = _load_image(IMAGES_PATH / "icon.off.png")

difficuly_easy_button = {
    "selected": _load_image(IMAGES_PATH / "button.level.easy.selected.png", DIFFICULY_BUTTON_SIZE),
    "unselected": _load_image(IMAGES_PATH / "button.level.easy.unselected.png", DIFFICULY_BUTTON_SIZE)
}
difficuly_medium_button = {
    "selected": _load_image(IMAGES_PATH / "button.level.medium.selected.png", DIFFICULY_BUTTON_SIZE),
    "unselected": _load_image(IMAGES_PATH / "button.level.medium.unselected.png", DIFFICULY_BUTTON_SIZE)
}
difficuly_hard_button = {
    "selected": _load_image(IMAGES_PATH / "button.level.hard.selected.png", DIFFICULY_BUTTON_SIZE),
    "unselected": _load_image(IMAGES_PATH / "button.level.hard.unselected.png", DIFFICULY_BUTTON_SIZE)
}

background = _load_image(IMAGES_PATH / "background.png", (WIDTH, HEIGHT))
room_default = _load_image(IMAGES_PATH / "room.default.png")
room_darkened = _load_image(IMAGES_PATH / "room.darkened.png")
icon_final_mark = _load_image(IMAGES_PATH / "icon.final_mark.png")

player_images = dict(
    zip(
        ["big", "medium", "small"],
        map(
            _load_image,
            [
                IMAGES_PATH / "sprite.thief.big_bag.png",
                IMAGES_PATH / "sprite.thief.medium_bag.png",
                IMAGES_PATH / "sprite.thief.small_bag.png"
            ]
        )
    )
)

# ============ AUDIO ============

try:
    music = pg.mixer.music.load(MUSIC_PATH / "background.mp3")
except Exception:
    print(f"Error: music not found at path {MUSIC_PATH / "background.mp3"}")
    exit()

# ============ FONTS ============

TITLE = pg.font.Font(FONTS_PATH / "UnifrakturMaguntia.ttf", 118)
HEADING = pg.font.Font(FONTS_PATH / "UnifrakturMaguntia.ttf", 72)

SUBTITLE = pg.font.Font(FONTS_PATH / "NotoSerifGeorgian.ttf", 55)
BODY = pg.font.Font(FONTS_PATH / "NotoSerifGeorgian.ttf", 25)
