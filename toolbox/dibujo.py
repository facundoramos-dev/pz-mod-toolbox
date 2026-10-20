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
FONDO_ARRIBA = (38, 46, 54)
FONDO_ABAJO = (19, 23, 27)
BORDE = (63, 72, 82)
PANEL = (16, 20, 24)
PANEL_BORDE = (107, 118, 131)
TEXTO_FUERTE = (214, 222, 230)
TEXTO_SUAVE = (138, 148, 158)
AMBAR = (232, 182, 76)
VERDE = (124, 179, 66)
VERDE_FONDO = (44, 58, 47)
ROJO = (198, 92, 78)
ROJO_FONDO = (58, 33, 31)
ACERO = (206, 216, 226)
ACERO_SOMBRA = (140, 152, 165)
MADERA = (104, 68, 42)
PIEDRA = (78, 84, 90)
PIEDRA_CARA = (104, 112, 120)


class Lienzo:
    def __init__(self, ancho, alto, color=FONDO_ABAJO):
        self.ancho, self.alto = ancho, alto
        self.px = bytearray(ancho * alto * 3)
        for i in range(ancho * alto):
            self.px[i * 3:i * 3 + 3] = bytes(color)

    def rectangulo(self, x, y, ancho, alto, color):
        for py in range(max(0, int(y)), min(self.alto, int(y + alto))):
            for px in range(max(0, int(x)), min(self.ancho, int(x + ancho))):
                self.px[(py * self.ancho + px) * 3:(py * self.ancho + px) * 3 + 3] = bytes(color)

    def circulo(self, cx, cy, radio, color):
        for py in range(max(0, int(cy - radio)), min(self.alto, int(cy + radio) + 1)):
            for px in range(max(0, int(cx - radio)), min(self.ancho, int(cx + radio) + 1)):
                if (px - cx) ** 2 + (py - cy) ** 2 <= radio * radio:
                    self.px[(py * self.ancho + px) * 3:(py * self.ancho + px) * 3 + 3] = bytes(color)

    def degradado_vertical(self, arriba, abajo):
        for y in range(self.alto):
            t = y / (self.alto - 1)
            color = tuple(round(arriba[i] + (abajo[i] - arriba[i]) * t) for i in range(3))
            self.rectangulo(0, y, self.ancho, 1, color)

    def linea(self, x0, y0, x1, y1, grosor, color):
        pasos = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        for i in range(pasos + 1):
            t = i / pasos
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t
            self.circulo(int(round(x)), int(round(y)), max(1, grosor // 2), color)

    def panel(self, x, y, ancho, alto, fondo=PANEL, borde=PANEL_BORDE, grosor=3):
        self.rectangulo(x, y, ancho, alto, fondo)
        self.rectangulo(x, y, ancho, grosor, borde)
        self.rectangulo(x, y + alto - grosor, ancho, grosor, borde)
        self.rectangulo(x, y, grosor, alto, borde)
        self.rectangulo(x + ancho - grosor, y, grosor, alto, borde)

    def ancho_texto(self, texto, escala):
        if not texto:
            return 0
        return (5 * escala + escala) * len(texto) - escala

    def texto(self, x, y, texto, escala, color):
        """Left aligned text, single line."""
        cx = int(x)
        for letra in texto:
            glifo = GLIFOS.get(letra.upper(), GLIFOS[" "])
            for fila, bits in enumerate(glifo):
                for columna, bit in enumerate(bits):
                    if bit == "1":
                        self.rectangulo(cx + columna * escala,
                                        int(y) + fila * escala, escala, escala, color)
            cx += 6 * escala
        return cx

    def texto_centrado_region(self, x, y, texto, escala, color):
        """Centers the text inside the region [x, width - x].

        Shrinks the scale when the text does not fit.
        """
        paso = 5 * escala + escala
        total = paso * len(texto) - escala
        if total > self.ancho - 2 * x:
            escala = max(1, (self.ancho - 2 * x + escala) // (6 * len(texto)))
            paso = 5 * escala + escala
        cx = x + (self.ancho - 2 * x - (paso * len(texto) - escala)) // 2
        for letra in texto:
            glifo = GLIFOS.get(letra.upper(), GLIFOS[" "])
            for fila, bits in enumerate(glifo):
                for columna, bit in enumerate(bits):
                    if bit == "1":
                        self.rectangulo(cx + columna * escala,
                                        int(y) + fila * escala, escala, escala, color)
            cx += paso
        return cx

    def texto_centrado(self, cx, y, texto, escala, color):
        ancho = self.ancho_texto(texto, escala)
        return self.texto(cx - ancho // 2, y, texto, escala, color)

    def texto_multilinea(self, x, y, texto, escala, color, ancho_max=None, interlineado=None):
        """Text with explicit line breaks and word wrapping."""
        cx = int(x)
        cy = int(y)
        alto_linea = interlineado or (9 * escala)
        for parrafo in texto.split("\n"):
            if not parrafo:
                cy += alto_linea
                continue
            palabras = parrafo.split(" ")
            linea = ""
            for palabra in palabras:
                prueba = palabra if not linea else linea + " " + palabra
                if ancho_max and self.ancho_texto(prueba, escala) > ancho_max and linea:
                    cx = self.texto(x, cy, linea, escala, color)
                    cy += alto_linea
                    linea = palabra
                else:
                    linea = prueba
            if linea:
                cx = self.texto(x, cy, linea, escala, color)
                cy += alto_linea
        return cy


def escribir_png(lienzo, ruta):
    crudo = b"".join(b"\x00" + bytes(lienzo.px[y * lienzo.ancho * 3:(y + 1) * lienzo.ancho * 3])
                     for y in range(lienzo.alto))
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)

    def chunk(tipo, datos):
        return (struct.pack(">I", len(datos)) + tipo + datos
                + struct.pack(">I", zlib.crc32(tipo + datos) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", lienzo.ancho, lienzo.alto, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(crudo, 9))
           + chunk(b"IEND", b""))
    with open(ruta, "wb") as f:
        f.write(png)
    return os.path.getsize(ruta)


def marco(lienzo, grosor=4):
    """Outer frame, shared by the cover and the gallery images."""
    w, h = lienzo.ancho, lienzo.alto
    lienzo.rectangulo(grosor, grosor, w - 2 * grosor, 3, BORDE)
    lienzo.rectangulo(grosor, h - grosor - 3, w - 2 * grosor, 3, BORDE)
    lienzo.rectangulo(grosor, grosor, 3, h - 2 * grosor, BORDE)
    lienzo.rectangulo(w - grosor - 3, grosor, 3, h - 2 * grosor, BORDE)


def katana(lienzo, x0, y0, x1, y1, escala=1):
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
    lienzo.linea(x0, y0, hx, hy, 11 * escala, MADERA)
    lienzo.linea(hx, hy, gx, gy, 13 * escala, AMBAR)
    lienzo.linea(gx, gy, x1, y1, 7 * escala, ACERO_SOMBRA)
    lienzo.linea(gx + ux * 2, gy + uy * 2, x1, y1, 4 * escala, ACERO)
    return (x1, y1)


def piedra_afilar(lienzo, x, y, ancho, alto):
    lienzo.rectangulo(x, y, ancho, alto, PIEDRA)
    lienzo.rectangulo(x, y, ancho, 7, PIEDRA_CARA)
    lienzo.rectangulo(x, y + alto - 7, ancho, 7, (58, 63, 68))
