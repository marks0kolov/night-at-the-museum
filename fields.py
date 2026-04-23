import pygame as pg

pg.init()

#############  - VARIABLES -  #############

# -------- colors -------- #

# surface
SURF_LIGHT = (29, 29, 29)
SURF_DARK = (24, 24, 24)

# text
TEXT_PRIM = (225, 225, 225)
TEXT_SEC = (110, 118, 129)

# semantic
COLOR_BLUE = (0, 200, 255)

# -------- fonts -------- #

BODY = pg.font.Font("assets/JetBrainsMono.ttf", 32)
CHAR_W = BODY.size("M")[0]

# -------- logic -------- #

class Cursor:
    def __init__(self):
        self.col = 0
        self.scroll_x = 0
        self.field = 0
        
    def _get_curr_field_len(self):
        return len(fields[self.field].text)
    
    def update_scroll(self):
        max_visible = max(1, (fields[self.field].rect.w - 10) // CHAR_W)
        self.scroll_x = max(0, self.col - max_visible)
    
    def move(self, direction: str):
        match direction:
            case "r":
                if self.col < self._get_curr_field_len():
                    self.col += 1
            case "l":
                if self.col > 0:
                    self.col -= 1
            case "u":
                if self.field > 0:
                    self.field -= 1
                    self.col = min(self._get_curr_field_len(), self.col)
            case "d":
                if self.field < len(fields) - 1:
                    self.field += 1
                    self.col = min(self._get_curr_field_len(), self.col)
        self.update_scroll()

cursor = Cursor()


class Field:
    def __init__(self, index: int, rect: pg.Rect | tuple[int, int, int, int]):
        self.index = index
        self.rect = pg.Rect(rect) if isinstance(rect, tuple) else rect
        self.text = ""

fields = [
    Field(0, (100, 100, 500, 50)),
    Field(2, (765, 450, 500, 50)),
]

#############  - FUNCS -  #############

def render_text():
    for field in fields:
        text = BODY.render(field.text, True, TEXT_PRIM)
        x = field.rect.x + 5
        if field.index == cursor.field:
            x -= cursor.scroll_x * CHAR_W

        global_clip = screen.get_clip()
        screen.set_clip(field.rect)
        screen.blit(text, (x, field.rect.y + 5))
        screen.set_clip(global_clip)

def render_cursor():
    if (pg.time.get_ticks() // 500) % 2 == 0:
        current_field = fields[cursor.field]
        pg.draw.rect(
            screen,
            TEXT_PRIM,
            (
                current_field.rect.x + (cursor.col - cursor.scroll_x) * CHAR_W + 7,
                current_field.rect.y + 7,
                5,
                32,
            ),
        )

#############  - MAIN SCREEN -  #############

screen = pg.display.set_mode((1550, 950))
pg.display.set_caption("textFields")

#############  - MAIN LOOP -  #############

clock = pg.time.Clock()
pg.key.set_repeat(400, 40)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                if cursor.col > 0:
                    text = fields[cursor.field].text
                    fields[cursor.field].text = text[:cursor.col - 1] + text[cursor.col:]
                    cursor.col -= 1
                    cursor.update_scroll()
            
            elif event.key == pg.K_RETURN:
                pass
            
            elif event.key == pg.K_RIGHT:
                cursor.move("r")
            elif event.key == pg.K_LEFT:
                cursor.move("l")
            elif event.key == pg.K_DOWN:
                cursor.move("d")
            elif event.key == pg.K_UP:
                cursor.move("u")

            elif event.key == pg.K_TAB:
                cursor.field = (cursor.field + 1) % len(fields)
                cursor.col = len(fields[cursor.field].text)
                cursor.update_scroll()
            
            elif event.unicode:
                text = fields[cursor.field].text
                fields[cursor.field].text = text[:cursor.col] + event.unicode + text[cursor.col:]
                cursor.col += 1
                cursor.update_scroll()
                

    screen.fill(SURF_DARK)

    for field in fields:
        pg.draw.rect(screen, SURF_LIGHT, field.rect)
        pg.draw.rect(screen, COLOR_BLUE, field.rect, 3)

    render_text()
    render_cursor()

    pg.display.flip()

    clock.tick(60)

pg.quit()
