import pygame as pg
from config import WIDTH, HEIGHT, IMAGES_PATH, FONTS_PATH, ROOM_SIZE, PADDING_BIG

# ============ IMAGES ============
# ~~~~~~ HELPERS ~~~~~~
def _load_image(path, size=None):
    try:
        img = pg.image.load(path)
    except Exception as e:
        print(f"Error: image not found at path {path}")
        return None
    
    if size:
        img = pg.transform.scale(img, size)
    return img

# ~~~~~~ SIZES ~~~~~~
START_BUTTON_WIDTH = int(WIDTH * 0.4)
START_BUTTON_HEIGHT = int(START_BUTTON_WIDTH / 3)
SETTINGS_BUTTON_SIZE = START_BUTTON_HEIGHT

# ~~~~~~ IMAGES ~~~~~~
start_button = _load_image(IMAGES_PATH / "button.start.png", (START_BUTTON_WIDTH, START_BUTTON_HEIGHT))
settings_button = _load_image(IMAGES_PATH / "button.settings.png", (SETTINGS_BUTTON_SIZE, SETTINGS_BUTTON_SIZE))

background = _load_image(IMAGES_PATH / "background.png", (WIDTH, HEIGHT))
room = _load_image(IMAGES_PATH / "room.png", (ROOM_SIZE, ROOM_SIZE))

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

for k in player_images:
    player_images[k] = pg.transform.scale(player_images[k], (ROOM_SIZE - PADDING_BIG, ROOM_SIZE - PADDING_BIG))

# ============ FONTS ============
BODY = pg.font.Font(FONTS_PATH / "NotoSerifGeorgian.ttf", max(16, WIDTH // 90))
HEADING = pg.font.Font(FONTS_PATH / "UnifrakturMaguntia.ttf", max(64, WIDTH // 10))
