#!/usr/bin/env python3
"""Listing artwork for the Dismantle Electronics Fix mod.

The mod is about small electronics and a screwdriver, so the artwork draws
the devices, the screwdriver and the scrap they turn into.

Builds the 256x256 cover (the square image on the right of the Workshop page)
and the 1280x720 gallery images (the carousel below it). Both are uploaded
from the Workshop web UI, never through the mod content.

Usage:
    python3 -m toolbox.art.electronics [mod/repo/path]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from toolbox.drawing import (AMBER, BORDER, PANEL, PANEL_BORDER, RED, RED_BG,
                             STEEL, STEEL_SHADE, TEXT_BRIGHT, TEXT_DIM, GREEN,
                             GREEN_BG, BG_BOTTOM, BG_TOP, Canvas, frame,
                             write_png)
from toolbox.art.shared import (BANNER_EDGE, COPPER, GLASS, GLASS_LIGHT, PLASTIC,
                                SHADOW, STEEL_DARK, STEEL_LIGHT, STEEL_MID,
                                WOOD, WOOD_DARK, WOOD_LIGHT, WOOD_LINE,
                                background, caption, footer, heading, spiffo)

GALLERY_WIDTH, GALLERY_HEIGHT = 1280, 720
COVER = 256
MARGIN = 64


def _fondo(width, alto):
    return background(Canvas(width, alto, BG_BOTTOM), width, alto)


def _heading(canvas, text, scale=6, y=48):
    heading(canvas, text, scale, y, MARGIN)


def _footer(canvas, text, scale=3, y=596):
    footer(canvas, text, scale, y, MARGIN)


# --------------------------------------------------------------------------- #
# The devices
# --------------------------------------------------------------------------- #

def auriculares(canvas, x, y, escala=1):
    """A pair of headphones: the band and the two cups."""
    ancho = 70 * escala
    alto = 60 * escala
    grosor = max(2, 5 * escala)

    # the band
    canvas.ellipse(x + ancho // 2, y + alto // 3, ancho // 2 - 6 * escala,
                    alto // 2, STEEL_MID)
    canvas.ellipse(x + ancho // 2, y + alto // 3, ancho // 2 - 12 * escala,
                    alto // 2 - 6 * escala, BG_TOP)
    # the cups
    cup_w = 18 * escala
    cup_h = 26 * escala
    canvas.rectangle(x, y + alto // 3, cup_w, cup_h, STEEL_DARK)
    canvas.rectangle(x + ancho - cup_w, y + alto // 3, cup_w, cup_h, STEEL_DARK)
    canvas.ellipse(x + cup_w // 2, y + alto // 3 + cup_h // 2, cup_w // 2,
                    cup_h // 2, STEEL_MID)
    canvas.ellipse(x + ancho - cup_w // 2, y + alto // 3 + cup_h // 2, cup_w // 2,
                    cup_h // 2, STEEL_MID)
    # the pads
    canvas.rectangle(x + 3 * escala, y + alto // 3 + 4 * escala, 4 * escala,
                     cup_h - 8 * escala, GLASS)
    canvas.rectangle(x + ancho - cup_w + 3 * escala, y + alto // 3 + 4 * escala,
                     4 * escala, cup_h - 8 * escala, GLASS)
    return ancho, alto


def telefono(canvas, x, y, escala=1):
    """A cordless phone: the body, the screen and the keypad."""
    ancho = 26 * escala
    alto = 52 * escala

    canvas.rectangle(x, y, ancho, alto, STEEL_DARK)
    canvas.rectangle(x + 2 * escala, y + 2 * escala, ancho - 4 * escala,
                     alto - 4 * escala, STEEL_MID)
    # screen
    canvas.rectangle(x + 4 * escala, y + 5 * escala, ancho - 8 * escala,
                     12 * escala, GLASS)
    canvas.rectangle(x + 6 * escala, y + 7 * escala, (ancho - 12) // 2, 3 * escala,
                     GLASS_LIGHT)
    # keypad
    for fila in range(3):
        for columna in range(3):
            canvas.rectangle(x + 4 * escala + columna * 6 * escala,
                             y + 21 * escala + fila * 7 * escala,
                             4 * escala, 4 * escala, STEEL_DARK)
    return ancho, alto


def auriculares_boton(canvas, x, y, escala=1):
    """A pair of earbuds: the two buds and their case."""
    for i in range(2):
        bx = x + i * 22 * escala
        canvas.circle(bx + 8 * escala, y + 8 * escala, 8 * escala, PLASTIC)
        canvas.circle(bx + 8 * escala, y + 8 * escala, 4 * escala, GLASS_LIGHT)
        canvas.rectangle(bx + 6 * escala, y + 14 * escala, 4 * escala,
                         12 * escala, PLASTIC)
    return 44 * escala, 26 * escala


def destornillador(canvas, x, y, escala=1, diagonal=False):
    """A screwdriver: handle, shaft and tip."""
    largo = 92 * escala
    grosor = 7 * escala

    if diagonal:
        canvas.line(x, y, x + largo, y - largo // 2, grosor, STEEL)
        canvas.line(x, y, x + largo, y - largo // 2, grosor // 2, STEEL_SHADE)
        # handle
        canvas.rectangle(x - 12 * escala, y - 5 * escala, 26 * escala,
                         11 * escala, AMBER)
        canvas.rectangle(x - 12 * escala, y - 5 * escala, 26 * escala,
                         3 * escala, COPPER)
    else:
        canvas.rectangle(x, y, 30 * escala, grosor, AMBER)
        canvas.rectangle(x, y, 30 * escala, 3 * escala, COPPER)
        canvas.rectangle(x + 30 * escala, y, largo - 30 * escala, grosor, STEEL)
        canvas.rectangle(x + largo - 8 * escala, y, 8 * escala, grosor, STEEL_SHADE)
    return largo, grosor


def chatarra(canvas, x, y, escala=1):
    """A pile of electronics scrap: small irregular chips."""
    piezas = [(0, 0, 18, 8), (14, 6, 16, 9), (4, 12, 14, 8),
              (20, 16, 12, 7), (-4, 8, 10, 7), (12, 0, 10, 6)]
    for dx, dy, w, h in piezas:
        canvas.rectangle(x + dx * escala, y + dy * escala, w * escala, h * escala,
                         COPPER)
        canvas.rectangle(x + dx * escala, y + dy * escala, w * escala, 2 * escala,
                         (222, 172, 110))
    return 40 * escala, 24 * escala


# --------------------------------------------------------------------------- #
# Cover (256x256)
# --------------------------------------------------------------------------- #

def build_cover(destino):
    lienzo = _fondo(COVER, COVER)

    heading(lienzo, "DISMANTLE", 2, 8, 10)
    lienzo.text_centered(COVER // 2, 30, "ELECTRONICS FIX", 2, TEXT_BRIGHT)

    # the scene: a phone being taken apart with a screwdriver
    destornillador(lienzo, 150, 150, escala=1, diagonal=True)
    telefono(lienzo, 44, 92, escala=2)
    auriculares(lienzo, 108, 46, escala=1)

    # the scrap that comes out of it
    chatarra(lienzo, 40, 196, escala=1)

    frame(lienzo, 3)
    write_png(lienzo, destino)
    return destino


# --------------------------------------------------------------------------- #
# Gallery (1280x720)
# --------------------------------------------------------------------------- #

def _image_bug():
    canvas = _fondo(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "THE BUG", scale=6, y=48)

    # the animation happens
    destornillador(canvas, 300, 430, escala=2, diagonal=True)
    telefono(canvas, 700, 260, escala=3)
    caption(canvas, "The animation plays, the device moves...", 3, 480)

    # and nothing comes out
    canvas.panel(MARGIN, 540, GALLERY_WIDTH - 2 * MARGIN, 90, fondo=RED_BG,
                 borde=RED, grosor=2)
    canvas.text(MARGIN + 24, 566, "BUT THE OUTPUT NEVER RESOLVES", 4, RED)
    canvas.text(MARGIN + 24, 602, "THE RECIPE FAILS AND THE DEVICE IS NEVER CONSUMED", 3, TEXT_DIM)

    _footer(canvas, "Build 42.21, measured on a dedicated server.", y=648)
    return canvas


def _image_why():
    canvas = _fondo(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "WHY IT HAPPENS", scale=6, y=48)

    # the mapper, drawn as a table with one row that cannot be matched
    x0, y0 = MARGIN, 170
    canvas.panel(x0, y0, GALLERY_WIDTH - 2 * MARGIN, 200)
    canvas.text(x0 + 30, y0 + 24, "THE OUTPUT MAPPER", 4, AMBER)
    canvas.text(x0 + 30, y0 + 62, "AMPLIFIER        <- SPEAKER", 3, TEXT_DIM)
    canvas.text(x0 + 30, y0 + 90, "ELECTRONICS SCRAP <- CD PLAYER", 3, TEXT_DIM)
    canvas.text(x0 + 30, y0 + 118, "MOTION SENSOR    <- HOME ALARM", 3, TEXT_DIM)
    canvas.text(x0 + 30, y0 + 146, "RECEIVER         <- REMOTE", 3, TEXT_DIM)
    canvas.text(x0 + 30, y0 + 174, "NO FALLBACK ENTRY", 3, RED)

    canvas.text(MARGIN, 400, "NO MATCH FOUND", 4, AMBER)
    canvas.text(MARGIN, 440, "THE OUTPUT COMES BACK NULL, THE RECIPE IS", 3, TEXT_DIM)
    canvas.text(MARGIN, 464, "MARKED AS FAILED, AND THE ITEM IS NEVER CONSUMED", 3, TEXT_DIM)

    _footer(canvas, "Every other mapper in the game base has a default entry. This one does not.", y=648)
    return canvas


def _image_fix():
    canvas = _fondo(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "THE FIX", scale=6, y=48)

    # the devices
    auriculares(canvas, MARGIN + 40, 200, escala=2)
    telefono(canvas, MARGIN + 260, 170, escala=2)
    auriculares_boton(canvas, MARGIN + 380, 220, escala=2)

    # the screwdriver and the scrap
    destornillador(canvas, MARGIN + 620, 320, escala=2, diagonal=True)
    chatarra(canvas, MARGIN + 900, 250, escala=3)

    canvas.text(MARGIN, 430, "A NEW RECIPE: DISMANTLE PORTABLE ELECTRONICS", 4, GREEN)
    canvas.text(MARGIN, 470, "PHONES, PAGERS, HEADPHONES AND EARBUDS, PLUS A SCREWDRIVER", 3, TEXT_DIM)
    canvas.text(MARGIN, 494, "THE MAPPER HAS A DEFAULT ENTRY, SO THE OUTPUT ALWAYS RESOLVES", 3, TEXT_DIM)

    _footer(canvas, "A mod cannot replace a vanilla recipe, so this one adds its own.", y=648)
    return canvas


def build_gallery(destino):
    for name, canvas in (("1-the-bug", _image_bug()),
                         ("2-why-it-happens", _image_why()),
                         ("3-the-fix", _image_fix())):
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
