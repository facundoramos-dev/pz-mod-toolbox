#!/usr/bin/env python3
"""Listing artwork for the Katana Sharpening mod.

Builds the 256x256 cover (the square image on the right of the Workshop page)
and the 1280x720 gallery images (the carousel below it). Both are uploaded
from the Workshop web UI, never through the mod content.

Usage:
    python3 -m toolbox.arte.katana [mod/repo/path]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from toolbox.dibujo import (ACERO, ACERO_SOMBRA, AMBAR, BORDE, FONDO_ABAJO,
                            FONDO_ARRIBA, MADERA, PANEL, PANEL_BORDE, PIEDRA,
                            PIEDRA_CARA, ROJO, ROJO_FONDO, TEXTO_FUERTE,
                            TEXTO_SUAVE, VERDE, VERDE_FONDO, Lienzo,
                            escribir_png, marco, katana, piedra_afilar)

GALERIA_ANCHO, GALERIA_ALTO = 1280, 720
PORTADA = 256
MARGEN = 64


def _fondo(ancho, alto):
    lienzo = Lienzo(ancho, alto, FONDO_ABAJO)
    lienzo.degradado_vertical(FONDO_ARRIBA, FONDO_ABAJO)
    marco(lienzo, 4 if ancho == PORTADA else 6)
    return lienzo


def _titulo(lienzo, texto, escala=6, y=48):
    lienzo.texto(MARGEN, y, texto, escala, AMBAR)
    lienzo.rectangulo(MARGEN, y + 7 * escala + 16, 320, 4, AMBAR)


def _pie(lienzo, texto, escala=3, y=596):
    lienzo.rectangulo(MARGEN, y - 24, lienzo.ancho - 2 * MARGEN, 3, BORDE)
    lienzo.texto_multilinea(MARGEN, y, texto, escala, TEXTO_SUAVE,
                             lienzo.ancho - 2 * MARGEN)


def _etiqueta(lienzo, x, y, texto, color, fondo, escala=3):
    ancho = lienzo.ancho_texto(texto, escala) + 24
    lienzo.panel(x, y, ancho, 7 * escala + 20, fondo=fondo, borde=color, grosor=2)
    lienzo.texto(x + 12, y + 10, texto, escala, color)
    return ancho


# --------------------------------------------------------------------------- #
# Cover (256x256)
# --------------------------------------------------------------------------- #

def build_cover(destino):
    lienzo = _fondo(PORTADA, PORTADA)

    lienzo.texto_centrado_region(12, 20, "KATANA", 6, AMBAR)
    lienzo.texto_centrado_region(12, 72, "AFILADO", 3, TEXTO_SUAVE)

    # katana drawn diagonally: handle bottom left, blade towards the top right
    lienzo.linea(36, 214, 58, 198, 11, MADERA)
    lienzo.linea(56, 200, 64, 193, 13, AMBAR)
    lienzo.linea(64, 193, 224, 86, 7, ACERO_SOMBRA)
    lienzo.linea(64, 192, 223, 85, 4, ACERO)

    # whetstone
    lienzo.rectangulo(148, 196, 88, 30, PIEDRA)
    lienzo.rectangulo(148, 196, 88, 7, PIEDRA_CARA)
    lienzo.rectangulo(148, 219, 88, 7, (58, 63, 68))

    # sharpening sparks
    for (x, y, r) in ((190, 128, 3), (202, 116, 2), (178, 140, 2), (212, 108, 2)):
        lienzo.circulo(x, y, r, AMBAR)

    # sharpness gauge: dull on top, full below
    lienzo.rectangulo(16, 148, 84, 10, PANEL)
    lienzo.rectangulo(16, 148, 84, 10, PANEL_BORDE)
    lienzo.rectangulo(18, 150, 80, 6, (60, 66, 72))
    lienzo.rectangulo(16, 166, 84, 10, PANEL)
    lienzo.rectangulo(16, 166, 84, 10, PANEL_BORDE)
    lienzo.rectangulo(18, 168, 80, 6, VERDE)

    escribir_png(lienzo, destino)
    return destino


# --------------------------------------------------------------------------- #
# Gallery (1280x720)
# --------------------------------------------------------------------------- #

def _imagen_bug():
    lienzo = _fondo(GALERIA_ANCHO, GALERIA_ALTO)
    _titulo(lienzo, "POR QUE NO SE PODIA AFILAR", 6)

    # left panel: the vanilla recipe
    lienzo.panel(MARGEN, 180, 520, 380)
    lienzo.texto(MARGEN + 28, 206, "RECETA VANILLA", 4, TEXTO_FUERTE)
    lienzo.texto(MARGEN + 28, 248, "SHARPEN BLADE", 5, AMBAR)
    lienzo.texto(MARGEN + 28, 306, "PIDE UN ITEM CON EL TAG:", 3, TEXTO_SUAVE)
    _etiqueta(lienzo, MARGEN + 28, 340, "base:sharpenable", VERDE, VERDE_FONDO, 4)
    lienzo.texto(MARGEN + 28, 420, "PIEDRA DE AFILAR O LIMA", 3, TEXTO_SUAVE)
    lienzo.texto(MARGEN + 28, 470, "TAG QUE NINGUN ITEM DE LA KATANA", 3, TEXTO_SUAVE)
    lienzo.texto(MARGEN + 28, 496, "TIENE EN LA DEFINICION VANILLA", 3, TEXTO_SUAVE)

    lienzo.texto(600, 320, "→", 12, AMBAR)

    # right panel: the katana tags
    lienzo.panel(696, 180, 520, 380)
    lienzo.texto(724, 206, "LA KATANA (VANILLA)", 4, TEXTO_FUERTE)
    lienzo.texto(724, 248, "TAGS:", 5, AMBAR)
    _etiqueta(lienzo, 724, 306, "base:ignorezombiedensity", TEXTO_SUAVE, PANEL, 3)
    _etiqueta(lienzo, 724, 350, "base:hasmetal", TEXTO_SUAVE, PANEL, 3)
    _etiqueta(lienzo, 724, 394, "base:fullblade", TEXTO_SUAVE, PANEL, 3)
    lienzo.panel(724, 446, 460, 42, fondo=ROJO_FONDO, borde=ROJO, grosor=2)
    lienzo.texto(738, 458, "FALTA base:sharpenable", 3, ROJO)

    _pie(lienzo,
         "La katana es la unica hoja larga del juego sin ese tag: el machete, la espada, "
         "los cuchillos y las hachas lo tienen todas. Por eso no se podia afilar nunca.",
         y=584)
    return lienzo


def _imagen_dano():
    lienzo = _fondo(GALERIA_ANCHO, GALERIA_ALTO)
    _titulo(lienzo, "EL FILO MULTIPLICA EL DANO", 6)

    lienzo.panel(MARGEN, 180, 700, 120)
    lienzo.texto(MARGEN + 28, 206, "DANO DEL GOLPE", 4, TEXTO_FUERTE)
    lienzo.texto(MARGEN + 28, 252, "BASE X (SHARPNESS + 1) / 2", 4, AMBAR)

    ancho = 520
    lienzo.texto(MARGEN, 340, "FILO INTACTO (1.0)", 4, TEXTO_FUERTE)
    lienzo.rectangulo(MARGEN, 378, ancho, 34, PANEL)
    lienzo.rectangulo(MARGEN + 3, 381, ancho - 6, 28, VERDE)
    lienzo.texto(MARGEN + ancho + 28, 380, "100%", 5, VERDE)

    lienzo.texto(MARGEN, 452, "FILO GASTADO (0.0)", 4, TEXTO_FUERTE)
    lienzo.rectangulo(MARGEN, 490, ancho, 34, PANEL)
    lienzo.rectangulo(MARGEN + 3, 493, (ancho - 6) // 2, 28, (120, 86, 60))
    lienzo.texto(MARGEN + ancho + 28, 492, "50%", 5, (196, 140, 88))

    lienzo.panel(800, 180, 416, 380)
    lienzo.texto_centrado(1008, 214, "SIN PODER AFILARLA", 3, ROJO)
    piedra_afilar(lienzo, 836, 452, 250, 62)
    katana(lienzo, 856, 498, 1146, 292, escala=3)
    lienzo.texto_centrado(1008, 528, "EL FILO SE GASTA Y NO", 2, TEXTO_SUAVE)
    lienzo.texto_centrado(1008, 546, "SE PUEDE RECUPERAR", 2, TEXTO_SUAVE)

    _pie(lienzo,
         "El filo se gastaba con cada golpe y, como no habia forma de afilarla, la katana "
         "se quedaba pegando la mitad para siempre.", y=584)
    return lienzo


def _imagen_mod():
    lienzo = _fondo(GALERIA_ANCHO, GALERIA_ALTO)
    _titulo(lienzo, "QUE HACE EL MOD", 7)

    filas = [
        ("1", "TAG base:sharpenable EN LA KATANA",
         "La katana aparece en la receta vanilla Sharpen Blade y se le puede devolver "
         "el filo con una piedra de afilar."),
        ("2", "CONDITIONMAX 10 > 13",
         "El mismo valor que la espada y la machete: dura mas golpes entre afiladas "
         "y se rompe menos."),
        ("3", "CONDITIONLOWERCHANCEONEIN 15 > 20",
         "Cada golpe tiene menos chance de danar el arma, igual que la espada."),
    ]

    y = 170
    for numero, titulo, detalle in filas:
        lienzo.panel(MARGEN, y, GALERIA_ANCHO - 2 * MARGEN, 128)
        lienzo.circulo(MARGEN + 54, y + 64, 30, VERDE_FONDO)
        lienzo.circulo(MARGEN + 54, y + 64, 27, PANEL)
        lienzo.texto_centrado(MARGEN + 54, y + 51, numero, 6, VERDE)
        lienzo.texto(MARGEN + 120, y + 26, titulo, 4, AMBAR)
        lienzo.texto_multilinea(MARGEN + 120, y + 74, detalle, 3, TEXTO_SUAVE,
                                 GALERIA_ANCHO - 2 * MARGEN - 160)
        y += 144

    _pie(lienzo,
         "Despues: Sharpen Blade (piedra de afilar) + katana > Guardar. "
         "La katana vuelve a pegar al 100%.", y=628)
    return lienzo


def build_gallery(destino):
    for nombre, lienzo in (("1-el-bug", _imagen_bug()),
                           ("2-el-dano", _imagen_dano()),
                           ("3-que-hace", _imagen_mod())):
        escribir_png(lienzo, os.path.join(destino, f"{nombre}.png"))
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
