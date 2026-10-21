#!/usr/bin/env python3
"""Listing artwork for the Katana Sharpening mod.

Builds the 256x256 cover (the square image on the right of the Workshop page)
and the 1280x720 gallery images (the carousel below it). Both are uploaded
from the Workshop web UI, never through the mod content.

Usage:
    python3 -m toolbox.art.katana [mod/repo/path]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from toolbox.drawing import (STEEL, STEEL_SHADE, AMBER, BORDER, BG_BOTTOM,
                            BG_TOP, WOOD, PANEL, PANEL_BORDER, STONE,
                            STONE_TOP, RED, RED_BG, TEXT_BRIGHT,
                            TEXT_DIM, GREEN, GREEN_BG, Canvas,
                            write_png, frame, katana, whetstone)
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


def _etiqueta(canvas, x, y, text, color, fondo, scale=3):
    width = canvas.text_width(text, scale) + 24
    canvas.panel(x, y, width, 7 * scale + 20, fondo=fondo, borde=color, grosor=2)
    canvas.text(x + 12, y + 10, text, scale, color)
    return width


# --------------------------------------------------------------------------- #
# Cover (256x256)
# --------------------------------------------------------------------------- #

def build_cover(destino):
    lienzo = _fondo(COVER, COVER)

    heading(lienzo, "KATANA SHARPENING", 2, 8, 10)

    # the scene: the katana and the mascot with a whetstone
    katana(lienzo, 26, 196, 186, 62, scale=2)
    spiffo(lienzo, 148, 118, 74, holding="stone")
    whetstone(lienzo, 30, 200, 84, 22)

    caption(lienzo, ["NOW YOU CAN", "SHARPEN IT"], 2, 216, 34)

    write_png(lienzo, destino)
    return destino


# --------------------------------------------------------------------------- #
# Gallery (1280x720)
# --------------------------------------------------------------------------- #

def _image_bug():
    canvas = _fondo(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "WHY IT COULD NOT BE SHARPENED", 6)

    # left panel: the vanilla recipe
    canvas.panel(MARGIN, 180, 520, 380)
    canvas.text(MARGIN + 28, 206, "VANILLA RECIPE", 4, TEXT_BRIGHT)
    canvas.text(MARGIN + 28, 248, "SHARPEN BLADE", 5, AMBER)
    canvas.text(MARGIN + 28, 306, "NEEDS AN ITEM WITH THE TAG:", 3, TEXT_DIM)
    _etiqueta(canvas, MARGIN + 28, 340, "base:sharpenable", GREEN, GREEN_BG, 4)
    canvas.text(MARGIN + 28, 420, "WHETSTONE OR FILE", 3, TEXT_DIM)
    canvas.text(MARGIN + 28, 470, "NO KATANA ITEM HAS THIS", 3, TEXT_DIM)
    canvas.text(MARGIN + 28, 496, "TAG IN THE VANILLA FILE", 3, TEXT_DIM)

    canvas.text(600, 320, "→", 12, AMBER)

    # right panel: the katana tags
    canvas.panel(696, 180, 520, 380)
    canvas.text(724, 206, "THE KATANA (VANILLA)", 4, TEXT_BRIGHT)
    canvas.text(724, 248, "TAGS:", 5, AMBER)
    _etiqueta(canvas, 724, 306, "base:ignorezombiedensity", TEXT_DIM, PANEL, 3)
    _etiqueta(canvas, 724, 350, "base:hasmetal", TEXT_DIM, PANEL, 3)
    _etiqueta(canvas, 724, 394, "base:fullblade", TEXT_DIM, PANEL, 3)
    canvas.panel(724, 446, 460, 42, fondo=RED_BG, borde=RED, grosor=2)
    canvas.text(738, 458, "MISSING base:sharpenable", 3, RED)

    _footer(canvas,
         "The katana is the only long blade in the game without that tag: the machete, "
         "the sword, the knives and the axes all have it. That is why it could never "
         "be sharpened.",
         y=584)
    return canvas


def _image_damage():
    canvas = _fondo(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "THE EDGE SCALES THE DAMAGE", 6)

    canvas.panel(MARGIN, 180, 700, 120)
    canvas.text(MARGIN + 28, 206, "DAMAGE PER HIT", 4, TEXT_BRIGHT)
    canvas.text(MARGIN + 28, 252, "BASE X (SHARPNESS + 1) / 2", 4, AMBER)

    width = 520
    canvas.text(MARGIN, 340, "PRISTINE EDGE (1.0)", 4, TEXT_BRIGHT)
    canvas.rectangle(MARGIN, 378, width, 34, PANEL)
    canvas.rectangle(MARGIN + 3, 381, width - 6, 28, GREEN)
    canvas.text(MARGIN + width + 28, 380, "100%", 5, GREEN)

    canvas.text(MARGIN, 452, "DULL EDGE (0.0)", 4, TEXT_BRIGHT)
    canvas.rectangle(MARGIN, 490, width, 34, PANEL)
    canvas.rectangle(MARGIN + 3, 493, (width - 6) // 2, 28, (120, 86, 60))
    canvas.text(MARGIN + width + 28, 492, "50%", 5, (196, 140, 88))

    canvas.panel(800, 180, 416, 380)
    canvas.text_centered(1008, 214, "CANNOT BE SHARPENED", 3, RED)
    whetstone(canvas, 836, 452, 250, 62)
    katana(canvas, 856, 498, 1146, 292, scale=3)
    canvas.text_centered(1008, 518, "THE EDGE DULLS AND", 2, TEXT_DIM)
    canvas.text_centered(1008, 536, "CANNOT BE RESTORED", 2, TEXT_DIM)

    _footer(canvas,
         "The edge dulls with every hit, and with no way to sharpen it the katana kept "
         "hitting for half damage.", y=584)
    return canvas


def _image_changes():
    canvas = _fondo(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "WHAT THE MOD DOES", 7)

    rows = [
        ("1", "ADDS base:sharpenable",
         "The katana shows up in the vanilla Sharpen Blade recipe, so the edge can "
         "be restored."),
        ("2", "CONDITIONMAX 10 > 13",
         "Same value as the sword and the machete: it lasts more hits between "
         "sharpenings and breaks less often."),
        ("3", "CONDITIONLOWERCHANCEONEIN 15 > 20",
         "Every hit has a lower chance of damaging the weapon, same as the sword."),
    ]

    y = 170
    for number, heading, detail in rows:
        canvas.panel(MARGIN, y, GALLERY_WIDTH - 2 * MARGIN, 128)
        canvas.circle(MARGIN + 54, y + 64, 30, GREEN_BG)
        canvas.circle(MARGIN + 54, y + 64, 27, PANEL)
        canvas.text_centered(MARGIN + 54, y + 51, number, 6, GREEN)
        canvas.text(MARGIN + 120, y + 26, heading, 4, AMBER)
        canvas.text_block(MARGIN + 120, y + 74, detail, 3, TEXT_DIM,
                                 GALLERY_WIDTH - 2 * MARGIN - 160)
        y += 144

    _footer(canvas,
         "Afterwards: Sharpen Blade (whetstone) + katana > Save. "
         "The katana hits for 100% again.", y=628)
    return canvas


def build_gallery(destino):
    for name, canvas in (("1-the-bug", _image_bug()),
                           ("2-the-damage", _image_damage()),
                           ("3-what-it-does", _image_changes())):
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
