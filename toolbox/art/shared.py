#!/usr/bin/env python3
"""Shared artwork pieces: the mascot, the poster look and small objects.

The mascot is a cartoon raccoon, a nod to Spiffo, the Project Zomboid mascot.
The poster look is the warm wooden style the mod banners use in game: a wooden
wall, a title board and a caption bar.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from toolbox.drawing import AMBER, BORDER, TEXT_DIM, Canvas, frame

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
    canvas.rectangle(MARGIN, y, width, height, (86, 60, 38))
    canvas.rectangle(MARGIN, y, width, 4, BANNER_EDGE)
    canvas.rectangle(MARGIN, y + height - 4, width, 4, BANNER_EDGE)
    canvas.rectangle(MARGIN, y, 4, height, BANNER_EDGE)
    canvas.rectangle(MARGIN + width - 4, y, 4, height, BANNER_EDGE)
    canvas.text_centered(MARGIN + width // 2, y + 13, text, scale, AMBER)


def _footer(canvas, text, scale=3, y=596):
    canvas.rectangle(MARGIN, y - 24, canvas.width - 2 * MARGIN, 3, BORDER)
    canvas.text_block(MARGIN, y, text, scale, TEXT_DIM, canvas.width - 2 * MARGIN)



# poster colours
WOOD_LIGHT = (108, 78, 50)
WOOD_DARK = (62, 44, 30)
WOOD_LINE = (48, 33, 22)
BANNER_WOOD = (86, 60, 38)
BANNER_EDGE = (146, 106, 62)

# mascot colours
STONE = (96, 104, 112)
STONE_TOP = (128, 138, 148)
FUR = (214, 150, 92)
FUR_DARK = (176, 112, 62)
MASK = (58, 46, 42)
MUZZLE = (240, 224, 200)
EYE_WHITE = (250, 250, 250)
INK = (32, 26, 24)
SHIRT = (74, 108, 156)
SHIRT_DARK = (54, 82, 122)


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
    elif holding == "stone":
        canvas.rectangle(x + 0.68 * s, y + 0.86 * s, 0.26 * s, 0.12 * s, STONE)
        canvas.rectangle(x + 0.68 * s, y + 0.86 * s, 0.26 * s, 0.04 * s, STONE_TOP)
    return x, y


# --------------------------------------------------------------------------- #
# Object illustrations
# --------------------------------------------------------------------------- #

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



def caption(canvas, text, scale=2, y=200, height=42):
    """The caption bar at the bottom of a poster.

    The text can be a single line or a list of lines.
    """
    width = canvas.width - 20
    canvas.rectangle(10, y, width, height, (38, 26, 18))
    canvas.rectangle(10, y, width, 2, BANNER_EDGE)
    lineas = [text] if isinstance(text, str) else list(text)
    alto = 7 * scale + 6
    inicio = y + max(0, (height - len(lineas) * alto) // 2)
    for i, linea in enumerate(lineas):
        canvas.text_centered(canvas.width // 2, inicio + i * alto, linea, scale, AMBER)

def background(canvas, width, height):
    """A warm wooden wall, the way the shop interiors look in game."""
    canvas.vertical_gradient(WOOD_LIGHT, WOOD_DARK)
    plank = 26 if width <= 256 else 40
    for y in range(0, height, plank):
        canvas.rectangle(0, y, width, 2, WOOD_LINE)
        canvas.rectangle(0, y + 2, width, 1, (78, 56, 38))
    frame(canvas, 4 if width <= 256 else 6)
    return canvas


def heading(canvas, text, scale=6, y=48, margin=64):
    """A wooden sign board with the title, like the mod banners in game."""
    height = 7 * scale + 26
    width = canvas.width - 2 * margin
    canvas.rectangle(margin, y, width, height, BANNER_WOOD)
    canvas.rectangle(margin, y, width, 4, BANNER_EDGE)
    canvas.rectangle(margin, y + height - 4, width, 4, BANNER_EDGE)
    canvas.rectangle(margin, y, 4, height, BANNER_EDGE)
    canvas.rectangle(margin + width - 4, y, 4, height, BANNER_EDGE)
    canvas.text_centered(margin + width // 2, y + 13, text, scale, AMBER)


def footer(canvas, text, scale=3, y=596, margin=64):
    canvas.rectangle(margin, y - 24, canvas.width - 2 * margin, 3, BORDER)
    canvas.text_block(margin, y, text, scale, TEXT_DIM, canvas.width - 2 * margin)
