#!/usr/bin/env python3
"""Listing artwork for the Cell Fridge mod.

Unlike the other mods, this one gets dedicated illustrations: the mod is a
physical object, so the artwork draws the object itself (a two door display
cooler) instead of diagrams made of boxes and labels.

Builds the 256x256 cover (the square image on the right of the Workshop page)
and the 1280x720 gallery images (the carousel below it). Both are uploaded from
the Workshop web UI, never through the mod content.

Usage:
    python3 -m toolbox.art.cellfridge [mod/repo/path]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from toolbox.drawing import (AMBER, BORDER, BG_BOTTOM, BG_TOP, PANEL, PANEL_BORDER,
                             RED, STEEL, STEEL_SHADE, TEXT_BRIGHT, TEXT_DIM, GREEN,
                             GREEN_BG, Canvas, frame, write_png)

GALLERY_WIDTH, GALLERY_HEIGHT = 1280, 720
COVER = 256
MARGIN = 64

# colours of the illustration
STEEL_LIGHT = (222, 228, 234)
STEEL_MID = (176, 186, 196)
STEEL_DARK = (116, 126, 136)
GLASS = (46, 62, 72)
GLASS_LIGHT = (92, 118, 132)
SHADOW = (22, 26, 30)
WOOD = (150, 108, 66)
COPPER = (198, 132, 68)
BOARD = (58, 96, 72)
PLASTIC = (206, 208, 210)
FOOD_RED = (186, 72, 60)
FOOD_GREEN = (104, 150, 78)
FOOD_YELLOW = (214, 178, 74)
FOOD_BLUE = (78, 116, 168)
FROZEN = (150, 190, 210)
WOOD_LIGHT = (108, 78, 50)
WOOD_DARK = (62, 44, 30)
WOOD_LINE = (48, 33, 22)
BANNER_WOOD = (86, 60, 38)
BANNER_EDGE = (146, 106, 62)


def _background(width, height):
    """A warm wooden wall, the way the shop interiors look in game."""
    canvas = Canvas(width, height, WOOD_DARK)
    canvas.vertical_gradient(WOOD_LIGHT, WOOD_DARK)
    plank = 26 if width == COVER else 40
    for y in range(0, height, plank):
        canvas.rectangle(0, y, width, 2, WOOD_LINE)
        canvas.rectangle(0, y + 2, width, 1, (78, 56, 38))
    frame(canvas, 4 if width == COVER else 6)
    return canvas


def _heading(canvas, text, scale=6, y=48):
    """A wooden sign board with the title, like the mod banners in game."""
    height = 7 * scale + 26
    width = canvas.width - 2 * MARGIN
    canvas.rectangle(MARGIN, y, width, height, BANNER_WOOD)
    canvas.rectangle(MARGIN, y, width, 4, BANNER_EDGE)
    canvas.rectangle(MARGIN, y + height - 4, width, 4, BANNER_EDGE)
    canvas.rectangle(MARGIN, y, 4, height, BANNER_EDGE)
    canvas.rectangle(MARGIN + width - 4, y, 4, height, BANNER_EDGE)
    canvas.text_centered(MARGIN + width // 2, y + 13, text, scale, AMBER)


def _footer(canvas, text, scale=3, y=596):
    canvas.rectangle(MARGIN, y - 24, canvas.width - 2 * MARGIN, 3, BORDER)
    canvas.text_block(MARGIN, y, text, scale, TEXT_DIM, canvas.width - 2 * MARGIN)



# --------------------------------------------------------------------------- #
# The mascot
# --------------------------------------------------------------------------- #

FUR = (214, 150, 92)
FUR_DARK = (176, 112, 62)
MASK = (58, 46, 42)
MUZZLE = (240, 224, 200)
EYE_WHITE = (250, 250, 250)
INK = (32, 26, 24)
SHIRT = (74, 108, 156)
SHIRT_DARK = (54, 82, 122)


def spiffo(canvas, x, y, s, holding=None):
    """A cartoon raccoon mascot: a nod to Spiffo, the Project Zomboid mascot.

    s is the size of the head; the body is drawn proportionally below it.
    """
    # ears, small and set to the sides
    canvas.ellipse(x + 0.16 * s, y + 0.19 * s, 0.11 * s, 0.10 * s, FUR_DARK)
    canvas.ellipse(x + 0.84 * s, y + 0.19 * s, 0.11 * s, 0.10 * s, FUR_DARK)
    canvas.ellipse(x + 0.16 * s, y + 0.19 * s, 0.06 * s, 0.05 * s, FUR)
    canvas.ellipse(x + 0.84 * s, y + 0.19 * s, 0.06 * s, 0.05 * s, FUR)
    # head
    canvas.ellipse(x + 0.50 * s, y + 0.50 * s, 0.38 * s, 0.33 * s, FUR)
    # the raccoon mask: one wide band across the eyes
    canvas.ellipse(x + 0.50 * s, y + 0.46 * s, 0.30 * s, 0.16 * s, MASK)
    # eyes
    canvas.ellipse(x + 0.36 * s, y + 0.45 * s, 0.08 * s, 0.07 * s, EYE_WHITE)
    canvas.ellipse(x + 0.64 * s, y + 0.45 * s, 0.08 * s, 0.07 * s, EYE_WHITE)
    canvas.circle(x + 0.37 * s, y + 0.46 * s, 0.045 * s, INK)
    canvas.circle(x + 0.65 * s, y + 0.46 * s, 0.045 * s, INK)
    canvas.circle(x + 0.34 * s, y + 0.42 * s, 0.02 * s, EYE_WHITE)
    canvas.circle(x + 0.62 * s, y + 0.42 * s, 0.02 * s, EYE_WHITE)
    # muzzle, pointed downwards
    canvas.ellipse(x + 0.50 * s, y + 0.68 * s, 0.16 * s, 0.13 * s, MUZZLE)
    canvas.ellipse(x + 0.50 * s, y + 0.60 * s, 0.06 * s, 0.045 * s, INK)
    canvas.line(x + 0.44 * s, y + 0.72 * s, x + 0.50 * s, y + 0.76 * s, 2, INK)
    canvas.line(x + 0.56 * s, y + 0.72 * s, x + 0.50 * s, y + 0.76 * s, 2, INK)
    # body: shoulders and a rounded torso in a blue shirt
    canvas.ellipse(x + 0.50 * s, y + 1.18 * s, 0.32 * s, 0.30 * s, SHIRT)
    canvas.ellipse(x + 0.50 * s, y + 0.96 * s, 0.24 * s, 0.10 * s, SHIRT)
    canvas.ellipse(x + 0.50 * s, y + 0.98 * s, 0.09 * s, 0.04 * s, SHIRT_DARK)
    # arms, joined to the shoulders
    canvas.ellipse(x + 0.20 * s, y + 1.06 * s, 0.10 * s, 0.08 * s, FUR)
    canvas.ellipse(x + 0.80 * s, y + 1.06 * s, 0.10 * s, 0.08 * s, FUR)
    if holding == "can":
        can(canvas, x + 0.74 * s, y + 0.84 * s, 0.15 * s, 0.20 * s, FOOD_RED)
    return x, y


# --------------------------------------------------------------------------- #
# Object illustrations
# --------------------------------------------------------------------------- #

def can(canvas, x, y, w, h, color):
    """A food can."""
    canvas.rectangle(x, y, w, h, color)
    canvas.rectangle(x, y, w, max(2, h // 8), STEEL_LIGHT)
    canvas.rectangle(x, y + h - max(2, h // 10), w, max(2, h // 10), STEEL_DARK)


def jar(canvas, x, y, w, h, color):
    """A jar or a bottle."""
    canvas.rectangle(x, y + h // 6, w, h - h // 6, color)
    canvas.rectangle(x + w // 4, y, w // 2, h // 6, STEEL_DARK)


def box(canvas, x, y, w, h, color):
    canvas.rectangle(x, y, w, h, color)
    canvas.rectangle(x, y, w, max(2, h // 8), STEEL_LIGHT)


def cooler(canvas, x, y, w, h, stocked=True, doors=True):
    """The two door display cooler: body, glass doors, shelves and handles."""
    frame_w = max(3, w // 28)
    # shadow on the floor
    canvas.rectangle(x + w // 12, y + h, w - w // 6, max(3, h // 40), SHADOW)
    # body
    canvas.rectangle(x, y, w, h, STEEL_MID)
    canvas.rectangle(x, y, w, frame_w, STEEL_LIGHT)
    canvas.rectangle(x, y + h - frame_w, w, frame_w, STEEL_DARK)
    # kick plate
    canvas.rectangle(x, y + h - h // 9, w, h // 9, STEEL_DARK)
    # interior
    interior_x = x + frame_w * 2
    interior_w = w - frame_w * 4
    interior_y = y + frame_w * 2
    interior_h = h - h // 7 - frame_w * 2
    canvas.rectangle(interior_x, interior_y, interior_w, interior_h, GLASS)

    # shelves and what is on them
    rows = 4
    shelf_h = interior_h // rows
    colours = [FOOD_RED, FOOD_GREEN, FOOD_YELLOW, FOOD_BLUE]
    for row in range(rows):
        sy = interior_y + row * shelf_h
        if row > 0:
            canvas.rectangle(interior_x, sy, interior_w, 2, STEEL_LIGHT)
        if not stocked:
            continue
        slot = interior_w // 6
        for slot_index in range(5):
            if (row + slot_index) % 3 == 0:
                continue
            ix = interior_x + 6 + slot_index * slot
            iy = sy + shelf_h - 2
            if row == 0:
                can(canvas, ix, iy - shelf_h // 2, slot - 8, shelf_h // 2 - 4,
                    colours[(row + slot_index) % len(colours)])
            elif row == 1:
                jar(canvas, ix, iy - shelf_h // 2, slot - 10, shelf_h // 2 - 4,
                    colours[(row + slot_index) % len(colours)])
            else:
                box(canvas, ix, iy - shelf_h // 3, slot - 8, shelf_h // 3 - 3,
                    colours[(row + slot_index) % len(colours)])

    if doors:
        # two glass doors with a handle each
        door_w = interior_w // 2
        for door in range(2):
            dx = interior_x + door * door_w
            canvas.rectangle(dx, interior_y, 2, interior_h, STEEL_LIGHT)
            canvas.rectangle(dx, interior_y, door_w, 3, STEEL_LIGHT)
            # reflection
            canvas.line(dx + door_w // 3, interior_y + interior_h - 12,
                        dx + door_w // 3 + 10, interior_y + 10, 2, GLASS_LIGHT)
            # handle
            hx = dx + door_w - 14
            canvas.rectangle(hx, interior_y + interior_h // 3, 4, interior_h // 3, STEEL_LIGHT)
    # centre divider
    canvas.rectangle(x + w // 2 - 2, interior_y, 4, interior_h, STEEL_LIGHT)


def sheet_metal(canvas, x, y, w, h):
    """A sheet of metal, drawn as a tilted plate."""
    for i in range(h):
        t = i / h
        canvas.rectangle(x + int(t * w * 0.18), y + i, w, 1,
                         STEEL_LIGHT if i % 4 else STEEL_MID)
    canvas.line(x, y, x + int(w * 0.18), y + h, 2, STEEL_LIGHT)


def wire_coil(canvas, x, y, w, h):
    """A coil of electric wire."""
    for i in range(3):
        canvas.circle(x + w // 6 + i * (w // 4), y + h // 2, max(3, h // 3), COPPER)
        canvas.circle(x + w // 6 + i * (w // 4), y + h // 2, max(2, h // 5), SHADOW)


def electronics_scrap(canvas, x, y, w, h):
    """A piece of electronics scrap."""
    canvas.rectangle(x, y, w, h, BOARD)
    canvas.rectangle(x + w // 4, y + h // 4, w // 3, h // 4, STEEL_DARK)
    canvas.rectangle(x + w // 2, y + h // 2, w // 4, h // 6, PLASTIC)


def screw(canvas, x, y, size):
    """A screw, seen from the top."""
    canvas.circle(x + size // 2, y + size // 2, size // 2, STEEL_LIGHT)
    canvas.line(x + size // 4, y + size // 2, x + size * 3 // 4, y + size // 2, 2, STEEL_DARK)


def hammer(canvas, x, y, w, h):
    """A hammer."""
    canvas.rectangle(x + w // 3, y, w // 3, h, WOOD)
    canvas.rectangle(x, y, w, h // 4, STEEL_DARK)
    canvas.rectangle(x + w - w // 6, y, w // 6, h // 4, STEEL_MID)


def ingredient(canvas, x, y, w, h, draw, label, count):
    """An ingredient with its label and count."""
    if draw is screw:
        screw(canvas, x + w // 2 - h // 2, y + h // 4, h // 2)
    else:
        draw(canvas, x + w // 4, y, w // 2, h)
    canvas.text_centered(x + w // 2, y + h + 14, label, 3, TEXT_BRIGHT)
    canvas.text_centered(x + w // 2, y + h + 42, count, 4, AMBER)


# --------------------------------------------------------------------------- #
# Cover (256x256)
# --------------------------------------------------------------------------- #

def build_cover(destino):
    canvas = _background(COVER, COVER)

    # title board
    _heading(canvas, "CELL FRIDGE", 3, 8)

    # the scene: the cooler and the mascot next to it
    cooler(canvas, 16, 62, 108, 122, stocked=True, doors=True)
    spiffo(canvas, 132, 96, 86, holding="can")

    # caption
    canvas.rectangle(10, 200, COVER - 20, 42, (38, 26, 18))
    canvas.rectangle(10, 200, COVER - 20, 2, BANNER_EDGE)
    canvas.text_centered(COVER // 2, 210, "MORE ROOM FOR", 2, AMBER)
    canvas.text_centered(COVER // 2, 226, "YOUR FOOD", 2, AMBER)

    write_png(canvas, destino)
    return destino


# --------------------------------------------------------------------------- #
# Gallery (1280x720)
# --------------------------------------------------------------------------- #

def _image_cooler():
    canvas = _background(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "A TWO DOOR DISPLAY COOLER", 6)

    cooler(canvas, 80, 190, 340, 400, stocked=True, doors=True)
    spiffo(canvas, 430, 330, 150, holding="can")

    # callouts
    canvas.text(660, 200, "TWO DOORS, TWO CELLS", 4, AMBER)
    canvas.text_block(660, 240,
                      "A two cell entity, the size of the shop cooler. Each cell "
                      "gets its own fridge and freezer container.", 3, TEXT_DIM, 596)
    canvas.text(660, 360, "NO EXTRA ART", 4, AMBER)
    canvas.text_block(660, 400,
                      "It reuses the vanilla refrigerator tiles, so the mod ships "
                      "no textures at all.", 3, TEXT_DIM, 596)
    canvas.text(660, 520, "COOLING INCLUDED", 4, AMBER)
    canvas.text_block(660, 560,
                      "It cools, it freezes, and the food still goes bad.",
                      3, TEXT_DIM, 596)

    _footer(canvas,
            "Craft it from sheet metal, wire, electronics scrap and screws, "
            "with MetalWelding 3.", y=650)
    return canvas


def _image_capacity():
    canvas = _background(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "HOW MUCH MORE", 6)

    # left: the vanilla shop fridge, empty
    canvas.text(64, 180, "SHOP FRIDGE", 3, TEXT_DIM)
    cooler(canvas, 76, 220, 180, 250, stocked=False, doors=True)
    canvas.text_centered(166, 490, "50 KG", 5, TEXT_DIM)
    canvas.text_centered(166, 524, "+ 20 KG FREEZER", 3, TEXT_DIM)

    canvas.text(320, 300, "→", 8, AMBER)

    # middle: the cell fridge, packed
    canvas.text(500, 180, "CELL FRIDGE", 3, AMBER)
    cooler(canvas, 516, 220, 180, 250, stocked=True, doors=True)
    canvas.text_centered(606, 490, "100 KG", 5, GREEN)
    canvas.text_centered(606, 524, "+ 100 KG FREEZER", 3, GREEN)

    # right: what that means in cans
    canvas.text(800, 180, "IN CANS OF BEANS", 3, AMBER)
    canvas.text(800, 224, "CELL FRIDGE", 3, TEXT_DIM)
    for row in range(6):
        for column in range(5):
            can(canvas, 800 + column * 26, 256 + row * 34, 18, 26,
                (FOOD_RED, FOOD_GREEN, FOOD_YELLOW, FOOD_BLUE)[(row + column) % 4])
    canvas.text(1020, 224, "SHOP FRIDGE", 3, TEXT_DIM)
    for row in range(3):
        for column in range(5):
            can(canvas, 1020 + column * 26, 256 + row * 34, 18, 26, FOOD_RED)

    _footer(canvas,
            "In B42 a container capacity is a weight in kilograms, capped at 100 kg for a "
            "placed container. Shop fridge: 50 + 20. Cell Fridge: 100 + 100, or 130 + 130 "
            "with the ORGANIZED trait.", y=610)
    return canvas


def _image_craft():
    canvas = _background(GALLERY_WIDTH, GALLERY_HEIGHT)
    _heading(canvas, "CRAFT IT YOURSELF", 6)

    # the recipe, one ingredient per column
    width = 200
    x = MARGIN
    ingredient(canvas, x, 160, width, 100, sheet_metal, "SHEET", "8")
    ingredient(canvas, x + width, 160, width, 100, wire_coil, "WIRE", "4")
    ingredient(canvas, x + width * 2, 160, width, 100, electronics_scrap, "SCRAP", "2")
    ingredient(canvas, x + width * 3, 160, width, 100, screw, "SCREWS", "4")
    ingredient(canvas, x + width * 4, 160, width, 100, hammer, "HAMMER", "1")

    # skill and category
    canvas.panel(MARGIN, 370, 560, 170, fondo=PANEL, borde=AMBER, grosor=3)
    canvas.text(MARGIN + 28, 392, "SKILL", 3, TEXT_DIM)
    canvas.text(MARGIN + 28, 420, "METALWELDING 3", 5, AMBER)
    canvas.text(MARGIN + 28, 490, "CATEGORY: FURNITURE", 3, TEXT_DIM)

    # world options
    canvas.panel(660, 370, 556, 170, fondo=PANEL, borde=PANEL_BORDER, grosor=3)
    canvas.text(688, 392, "WORLD OPTIONS > CELL FRIDGE", 3, AMBER)
    canvas.text(688, 424, "FRIDGE CAPACITY (KG)", 3, TEXT_DIM)
    canvas.rectangle(688, 456, 200, 10, PANEL_BORDER)
    canvas.rectangle(691, 459, 194, 4, GREEN)
    canvas.text(900, 452, "10 - 100", 3, GREEN)
    canvas.text(688, 488, "FREEZER CAPACITY (KG)", 3, TEXT_DIM)
    canvas.rectangle(688, 518, 200, 10, PANEL_BORDER)
    canvas.rectangle(691, 521, 194, 4, GREEN)
    canvas.text(900, 514, "5 - 100", 3, GREEN)

    _footer(canvas,
            "The capacity is set in the World Options and applied when the cooler is built. "
            "Fridges already placed are refreshed by the server.", y=580)
    return canvas


def build_gallery(destino):
    for nombre, lienzo in (("1-the-cooler", _image_cooler()),
                           ("2-how-much-more", _image_capacity()),
                           ("3-craft-it", _image_craft())):
        write_png(lienzo, os.path.join(destino, f"{nombre}.png"))
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
