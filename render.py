#!/usr/bin/env python3
"""Render entry.png — newspaper front page, 1024x1024, drawn with Pillow.

No external assets and no network access. Run from this directory:
    python3 render.py          # writes entry.png beside this file

The six stories are the verified events of Monday, 23 November 2026
(each checked against two or more sources dated that day).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 48
CONTENT_W = W - 2 * MARGIN  # 928

BLACK = (0, 0, 0)
DARK_GRAY = (51, 51, 51)
WHITE = (255, 255, 255)
RED = (139, 26, 26)  # the only accent colour: dark red

FONT_DIR = "/usr/share/fonts/truetype/liberation/"


def load_font(name, size):
    """Load one Liberation font at the given point size."""
    return ImageFont.truetype(FONT_DIR + name, size)


# Fixed type scale for the page.
F_TITLE = load_font("LiberationSans-Bold.ttf", 64)
F_DATE = load_font("LiberationSans-Bold.ttf", 40)
F_SUBLINE = load_font("LiberationSans-Italic.ttf", 30)
F_NUM = load_font("LiberationSans-Bold.ttf", 46)
F_CHIP = load_font("LiberationSans-Bold.ttf", 18)
F_FOOT = load_font("LiberationSans-Regular.ttf", 26)

STORIES = [
    ("WAR", "Ukraine sinks Russian warship off Libya",
     "Zelenskyy: 7 sea drones sank corvette Merkury"),
    ("MARKETS", "KOSPI sinks 3.3% as AI rout deepens",
     "Seoul hits 10-month low; Samsung, SK hynix fall"),
    ("CLIMATE", "COP31 fallout: blame game begins",
     "Calls for minister Bowen to quit after collapse"),
    ("SPORT", "UK to host 2035 Women's World Cup",
     "FIFA confirms; first World Cup there since 1966"),
    ("EUROPE", "Belgium airports shut in national strike",
     "Airspace closed 7am-9pm; 60,000 passengers hit"),
    ("WAR", "Russian strikes kill 11 near Kyiv",
     "Teenager among dead; boy pulled alive from rubble"),
]


def fit_font(d, text, font_name, start_size, max_w, min_size=24):
    """Largest size (from start_size down) at which text fits max_w."""
    size = start_size
    while size > min_size:
        f = load_font(font_name, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return load_font(font_name, min_size)


def draw_header(d):
    """Masthead: title, date, tagline, and the double rule below."""
    d.text((MARGIN, 36), "THE WORLD IN ONE DAY", font=F_TITLE, fill=BLACK)
    d.text((MARGIN, 122), "MONDAY, 23 NOVEMBER 2026", font=F_DATE, fill=RED)
    d.text((MARGIN, 178), "World news in one image", font=F_SUBLINE, fill=DARK_GRAY)
    # thick black rule + thin red rule
    d.rectangle([MARGIN, 232, W - MARGIN, 236], fill=BLACK)
    d.rectangle([MARGIN, 242, W - MARGIN, 244], fill=RED)


def draw_story(d, index, chip, head, sub):
    """One numbered story block: number, category chip, headline, subline."""
    y = 262 + index * 116
    d.text((MARGIN, y + 8), str(index + 1), font=F_NUM, fill=RED)
    tx = MARGIN + 62
    chip_w = int(d.textlength(chip, font=F_CHIP)) + 26
    chip_h = 30
    d.rounded_rectangle([tx, y + 4, tx + chip_w, y + 4 + chip_h],
                        radius=6, fill=RED)
    d.text((tx + 13, y + 4 + 6), chip, font=F_CHIP, fill=WHITE)
    text_w = W - MARGIN - tx
    f_head = fit_font(d, head, "LiberationSans-Bold.ttf", 40, text_w)
    f_sub = fit_font(d, sub, "LiberationSans-Regular.ttf", 28, text_w)
    d.text((tx, y + 40), head, font=f_head, fill=BLACK)
    d.text((tx, y + 82), sub, font=f_sub, fill=DARK_GRAY)


def draw_footer(d):
    """Centred footer line naming the day a second time."""
    footer = "23 November 2026 — six stories that defined the day"
    fw = d.textlength(footer, font=F_FOOT)
    d.text(((W - fw) / 2, 970), footer, font=F_FOOT, fill=BLACK)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    draw_header(d)
    for i, (chip, head, sub) in enumerate(STORIES):
        draw_story(d, i, chip, head, sub)
    draw_footer(d)
    img.save("entry.png", "PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
