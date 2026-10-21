#!/usr/bin/env python3
"""Listing artwork for the Perk Descriptions mod.

Builds the 256x256 cover (the square image on the right of the Workshop page)
and the 1280x720 gallery images (the carousel below it). Both are uploaded
from the Workshop web UI, never through the mod content.

Usage:
    python3 -m toolbox.art.perks [mod/repo/path]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from toolbox.drawing import (AMBER, BORDER, BG_BOTTOM, BG_TOP, PANEL,
                            PANEL_BORDER, RED, RED_BG, TEXT_BRIGHT,
                            TEXT_DIM, GREEN, GREEN_BG, Canvas,
                            write_png, frame)
from toolbox.art.shared import (BANNER_EDGE, WOOD_DARK, WOOD_LIGHT, WOOD_LINE,
                                background, caption, footer, heading, spiffo)

GALLERY_WIDTH, GALLERY_HEIGHT = 1280, 720
COVER = 256
MARGIN = 64


def _fondo(width, alto):
    return background(Canvas(width, alto, WOOD_DARK), width, alto)


def _heading(canvas, text, scale=6, y=48):
    heading(canvas, text, scale, y, MARGIN)


def _footer(canvas, text, scale=3, y=596):
    footer(canvas, text, scale, y, MARGIN)


def _tooltip(canvas, x, y, width, alto, name, lineas, color, fondo=PANEL,
             name_scale=5, line_scale=3):
    """Mockup of a skill tooltip."""
    canvas.panel(x, y, width, alto, fondo=fondo, borde=color, grosor=3)
    canvas.text(x + 20, y + 18, name, name_scale, TEXT_BRIGHT)
    rule = y + 18 + 7 * name_scale + 8
    canvas.rectangle(x + 20, rule, width - 40, 3, color)
    for i, line in enumerate(lineas):
        canvas.text(x + 20, rule + 16 + i * (7 * line_scale + 8), line, line_scale, color)
    return y + alto


# --------------------------------------------------------------------------- #
# Cover (256x256)
# --------------------------------------------------------------------------- #

def build_cover(destino):
    lienzo = _fondo(COVER, COVER)

    heading(lienzo, "PERK DESCRIPTIONS", 2, 8, 10)

    # the scene: the fixed tooltip and the mascot reading it
    _tooltip(lienzo, 8, 52, 168, 142, "AXE",
             ["CHOP TREES", "AND GATHER", "WOOD"], GREEN, GREEN_BG,
             name_scale=4, line_scale=2)
    spiffo(lienzo, 184, 130, 60)

    caption(lienzo, ["REAL DESCRIPTIONS,", "IN EVERY LANGUAGE"], 2, 200, 46)

    write_png(lienzo, destino)
    return destino


# --------------------------------------------------------------------------- #
# Gallery (1280x720)
# --------------------------------------------------------------------------- #

def _image_bug():
    canvas = _fondo(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "THE VANILLA BUG", 6)

    canvas.text(MARGIN, 180, "WITHOUT THE MOD", 4, RED)
    _tooltip(canvas, MARGIN, 220, 520, 280, "AXE",
             ["IGUI_perks_Carpinteria", "_Description"], RED, RED_BG)
    canvas.text(MARGIN + 24, 420, "THE RAW KEY IS SHOWN", 3, RED)
    canvas.text(MARGIN + 24, 450, "INSTEAD OF THE TEXT", 3, RED)

    canvas.text(696, 180, "WITH THE MOD", 4, GREEN)
    _tooltip(canvas, 696, 220, 520, 280, "AXE",
             ["YOU CAN USE THE AXE TO", "CHOP TREES AND GATHER",
              "WOOD MORE EFFICIENTLY."], GREEN, GREEN_BG)

    _footer(canvas,
         "The engine builds the tooltip key from the TRANSLATED skill name, but "
         "the game only ships the descriptions under the ENGLISH name. In any "
         "other language the key does not exist and the raw text is shown.", y=560)
    return canvas


def _image_how():
    canvas = _fondo(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "HOW IT FIXES IT", 6)

    width = 360
    steps = [
        ("1", "TRANSLATED NAME",
         "The engine asks for the key",
         ["IGUI_perks_Carpinteria", "_Description"]),
        ("2", "TO ENGLISH",
         "The mod translates it",
         ["Perks.Carpentry", "-> Carpentry"]),
        ("3", "CORRECT KEY",
         "That key exists, already",
         ["IGUI_perks_Carpentry", "_Description"]),
    ]

    x = MARGIN
    for i, (number, name, detail, keys) in enumerate(steps):
        canvas.panel(x, 190, width, 330)
        canvas.circle(x + 44, 240, 26, GREEN_BG)
        canvas.circle(x + 44, 240, 23, PANEL)
        canvas.text_centered(x + 44, 229, number, 5, GREEN)
        canvas.text(x + 24, 290, name, 3, AMBER)
        canvas.text_block(x + 24, 330, detail, 3, TEXT_DIM, width - 48)
        for j, key in enumerate(keys):
            canvas.text(x + 24, 448 + j * 30, key, 2, GREEN)
        if i < 2:
            canvas.text(x + width + 6, 330, "→", 4, AMBER)
        x += width + 36

    _footer(canvas,
         "A single file, no translations copied: the text you see is the game own, "
         "so if The Indie Stone improves a description, you see the improvement.", y=570)
    return canvas


def _image_coverage():
    canvas = _fondo(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "WHAT IT COVERS", 7)

    data = [
        ("35", ["SKILLS", "VANILLA"],
         ["Axe, Carpentry,", "Cooking, Sneaking,", "First Aid and more."]),
        ("28", ["LANGUAGES", "SUPPORTED"],
         ["One single file.", "The right key is", "resolved at", "runtime."]),
        ("1", ["FILE"],
         ["Overrides the game", "tooltip and nothing", "else: it can be", "removed mid game."]),
    ]

    x = MARGIN
    width = 360
    for number, name, detail in data:
        canvas.panel(x, 190, width, 340)
        canvas.text_centered(x + width // 2, 212, number, 10, AMBER)
        for j, line in enumerate(name):
            canvas.text_centered(x + width // 2, 300 + j * 28, line, 3, TEXT_BRIGHT)
        canvas.rectangle(x + 40, 366, width - 80, 3, BORDER)
        for j, line in enumerate(detail):
            canvas.text(x + 30, 388 + j * 30, line, 3, TEXT_DIM)
        x += width + 36

    _footer(canvas,
         "Skills added by other mods keep their original behaviour, and the mod can be "
         "removed at any time without leaving a trace in the save.",
         y=570)
    return canvas


def build_gallery(destino):
    for name, canvas in (("1-the-bug", _image_bug()),
                           ("2-how-it-works", _image_how()),
                           ("3-coverage", _image_coverage())):
        write_png(canvas, os.path.join(destino, f"{name}.png"))
    return destino


def main():
    raiz = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    workshop = os.path.join(raiz, "workshop")
    os.makedirs(os.path.join(workshop, "gallery"), exist_ok=True)
    build_cover(os.path.join(workshop, "preview.png"))
    build_gallery(os.path.join(workshop, "gallery"))
    print(f"listing artwork written to {workshop}")


if __name__ == "__main__":
    main()
