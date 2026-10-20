#!/usr/bin/env python3
"""Drawing primitives for the Steam Workshop listing images.

Pure standard library (zlib + struct), so the PNGs can be regenerated on any
machine without installing anything.

Includes a 5x7 bitmap font covering upper case letters, digits and the
punctuation used by the listing images.
"""
import os
import struct
import zlib

GLIFOS = {
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "01100", "01000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    ";": ["00000", "01100", "01100", "00000", "01100", "01100", "01000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    "%": ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    '"': ["01010", "01010", "00000", "00000", "00000", "00000", "00000"],
    "#": ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
    "=": ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    "<": ["00010", "00100", "01000", "10000", "01000", "00100", "00010"],
    ">": ["01000", "00100", "00010", "00001", "00010", "00100", "01000"],
    "|": ["00100", "00100", "00100", "00100", "00100", "00100", "00100"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    "*": ["00000", "10001", "01010", "00100", "01010", "10001", "00000"],
    "°": ["01100", "10010", "01100", "00000", "00000", "00000", "00000"],
    "×": ["00000", "10001", "01010", "00100", "01010", "10001", "00000"],
    "→": ["00000", "00100", "00010", "11111", "00010", "00100", "00000"],
}

# Palette shared by every listing image
BG_TOP = (38, 46, 54)
BG_BOTTOM = (19, 23, 27)
BORDER = (63, 72, 82)
PANEL = (16, 20, 24)
PANEL_BORDER = (107, 118, 131)
TEXT_BRIGHT = (214, 222, 230)
TEXT_DIM = (138, 148, 158)
AMBER = (232, 182, 76)
GREEN = (124, 179, 66)
GREEN_BG = (44, 58, 47)
RED = (198, 92, 78)
RED_BG = (58, 33, 31)
STEEL = (206, 216, 226)
STEEL_SHADE = (140, 152, 165)
WOOD = (104, 68, 42)
STONE = (78, 84, 90)
STONE_TOP = (104, 112, 120)


class Canvas:
    def __init__(self, width, alto, color=BG_BOTTOM):
        self.width, self.alto = width, alto
        self.px = bytearray(width * alto * 3)
        for i in range(width * alto):
            self.px[i * 3:i * 3 + 3] = bytes(color)

    def rectangle(self, x, y, width, alto, color):
        for py in range(max(0, int(y)), min(self.alto, int(y + alto))):
            for px in range(max(0, int(x)), min(self.width, int(x + width))):
                self.px[(py * self.width + px) * 3:(py * self.width + px) * 3 + 3] = bytes(color)

    def circle(self, cx, cy, radio, color):
        for py in range(max(0, int(cy - radio)), min(self.alto, int(cy + radio) + 1)):
            for px in range(max(0, int(cx - radio)), min(self.width, int(cx + radio) + 1)):
                if (px - cx) ** 2 + (py - cy) ** 2 <= radio * radio:
                    self.px[(py * self.width + px) * 3:(py * self.width + px) * 3 + 3] = bytes(color)

    def vertical_gradient(self, arriba, abajo):
        for y in range(self.alto):
            t = y / (self.alto - 1)
            color = tuple(round(arriba[i] + (abajo[i] - arriba[i]) * t) for i in range(3))
            self.rectangle(0, y, self.width, 1, color)

    def line(self, x0, y0, x1, y1, grosor, color):
        steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        for i in range(steps + 1):
            t = i / steps
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t
            self.circle(int(round(x)), int(round(y)), max(1, grosor // 2), color)

    def panel(self, x, y, width, alto, fondo=PANEL, borde=PANEL_BORDER, grosor=3):
        self.rectangle(x, y, width, alto, fondo)
        self.rectangle(x, y, width, grosor, borde)
        self.rectangle(x, y + alto - grosor, width, grosor, borde)
        self.rectangle(x, y, grosor, alto, borde)
        self.rectangle(x + width - grosor, y, grosor, alto, borde)

    def text_width(self, text, scale):
        if not text:
            return 0
        return (5 * scale + scale) * len(text) - scale

    def text(self, x, y, text, scale, color):
        """Left aligned text, single line."""
        cx = int(x)
        for letra in text:
            glifo = GLIFOS.get(letra.upper(), GLIFOS[" "])
            for fila, bits in enumerate(glifo):
                for columna, bit in enumerate(bits):
                    if bit == "1":
                        self.rectangle(cx + columna * scale,
                                        int(y) + fila * scale, scale, scale, color)
            cx += 6 * scale
        return cx

    def text_centered_in_region(self, x, y, text, scale, color):
        """Centers the text inside the region [x, width - x].

        Shrinks the scale when the text does not fit.
        """
        step = 5 * scale + scale
        total = step * len(text) - scale
        if total > self.width - 2 * x:
            scale = max(1, (self.width - 2 * x + scale) // (6 * len(text)))
            step = 5 * scale + scale
        cx = x + (self.width - 2 * x - (step * len(text) - scale)) // 2
        for letra in text:
            glifo = GLIFOS.get(letra.upper(), GLIFOS[" "])
            for fila, bits in enumerate(glifo):
                for columna, bit in enumerate(bits):
                    if bit == "1":
                        self.rectangle(cx + columna * scale,
                                        int(y) + fila * scale, scale, scale, color)
            cx += step
        return cx

    def text_centered(self, cx, y, text, scale, color):
        width = self.text_width(text, scale)
        return self.text(cx - width // 2, y, text, scale, color)

    def text_block(self, x, y, text, scale, color, ancho_max=None, interlineado=None):
        """Text with explicit line breaks and word wrapping."""
        cx = int(x)
        cy = int(y)
        alto_linea = interlineado or (9 * scale)
        for parrafo in text.split("\n"):
            if not parrafo:
                cy += alto_linea
                continue
            palabras = parrafo.split(" ")
            line = ""
            for palabra in palabras:
                prueba = palabra if not line else line + " " + palabra
                if ancho_max and self.text_width(prueba, scale) > ancho_max and line:
                    cx = self.text(x, cy, line, scale, color)
                    cy += alto_linea
                    line = palabra
                else:
                    line = prueba
            if line:
                cx = self.text(x, cy, line, scale, color)
                cy += alto_linea
        return cy


def write_png(canvas, ruta):
    crudo = b"".join(b"\x00" + bytes(canvas.px[y * canvas.width * 3:(y + 1) * canvas.width * 3])
                     for y in range(canvas.alto))
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)

    def chunk(tipo, data):
        return (struct.pack(">I", len(data)) + tipo + data
                + struct.pack(">I", zlib.crc32(tipo + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", canvas.width, canvas.alto, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(crudo, 9))
           + chunk(b"IEND", b""))
    with open(ruta, "wb") as f:
        f.write(png)
    return os.path.getsize(ruta)


def frame(canvas, grosor=4):
    """Outer frame, shared by the cover and the gallery images."""
    w, h = canvas.width, canvas.alto
    canvas.rectangle(grosor, grosor, w - 2 * grosor, 3, BORDER)
    canvas.rectangle(grosor, h - grosor - 3, w - 2 * grosor, 3, BORDER)
    canvas.rectangle(grosor, grosor, 3, h - 2 * grosor, BORDER)
    canvas.rectangle(w - grosor - 3, grosor, 3, h - 2 * grosor, BORDER)


def katana(canvas, x0, y0, x1, y1, scale=1):
    """A katana drawn diagonally: handle at the bottom left, blade towards the top.

    Lengths are proportional to the given line; the scale only drives the
    stroke width.
    """
    dx, dy = x1 - x0, y1 - y0
    largo = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / largo, dy / largo
    largo_empunadura = largo * 0.24
    largo_guarda = largo * 0.05
    hx, hy = x0 + ux * largo_empunadura, y0 + uy * largo_empunadura
    gx, gy = hx + ux * largo_guarda, hy + uy * largo_guarda
    canvas.line(x0, y0, hx, hy, 11 * scale, WOOD)
    canvas.line(hx, hy, gx, gy, 13 * scale, AMBER)
    canvas.line(gx, gy, x1, y1, 7 * scale, STEEL_SHADE)
    canvas.line(gx + ux * 2, gy + uy * 2, x1, y1, 4 * scale, STEEL)
    return (x1, y1)


def whetstone(canvas, x, y, width, alto):
    canvas.rectangle(x, y, width, alto, STONE)
    canvas.rectangle(x, y, width, 7, STONE_TOP)
    canvas.rectangle(x, y + alto - 7, width, 7, (58, 63, 68))
