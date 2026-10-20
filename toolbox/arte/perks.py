#!/usr/bin/env python3
"""Listing artwork for the Perk Descriptions mod.

Builds the 256x256 cover (the square image on the right of the Workshop page)
and the 1280x720 gallery images (the carousel below it). Both are uploaded
from the Workshop web UI, never through the mod content.

Usage:
    python3 -m toolbox.arte.perks [mod/repo/path]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from toolbox.dibujo import (AMBAR, BORDE, FONDO_ABAJO, FONDO_ARRIBA, PANEL,
                            PANEL_BORDE, ROJO, ROJO_FONDO, TEXTO_FUERTE,
                            TEXTO_SUAVE, VERDE, VERDE_FONDO, Lienzo,
                            escribir_png, marco)

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


def _tooltip(lienzo, x, y, ancho, alto, nombre, lineas, color, fondo=PANEL):
    """Mockup of a skill tooltip."""
    lienzo.panel(x, y, ancho, alto, fondo=fondo, borde=color, grosor=3)
    lienzo.texto(x + 24, y + 22, nombre, 5, TEXTO_FUERTE)
    lienzo.rectangulo(x + 24, y + 72, ancho - 48, 3, color)
    for i, linea in enumerate(lineas):
        lienzo.texto(x + 24, y + 92 + i * 34, linea, 3, color)
    return y + alto


# --------------------------------------------------------------------------- #
# Cover (256x256)
# --------------------------------------------------------------------------- #

def build_cover(destino):
    lienzo = _fondo(PORTADA, PORTADA)

    lienzo.texto_centrado_region(12, 22, "PERKS", 7, AMBAR)
    lienzo.texto_centrado_region(12, 86, "DESCRIPCIONES", 3, TEXTO_SUAVE)

    # mockup of the tooltip the mod fixes
    lienzo.rectangulo(26, 122, 204, 72, PANEL)
    lienzo.rectangulo(26, 122, 204, 3, PANEL_BORDE)
    lienzo.rectangulo(26, 191, 204, 3, PANEL_BORDE)
    lienzo.rectangulo(26, 122, 3, 72, PANEL_BORDE)
    lienzo.rectangulo(227, 122, 3, 72, PANEL_BORDE)
    lienzo.rectangulo(40, 136, 108, 7, TEXTO_FUERTE)
    lienzo.rectangulo(40, 152, 176, 5, TEXTO_SUAVE)
    lienzo.rectangulo(40, 162, 148, 5, TEXTO_SUAVE)
    lienzo.rectangulo(40, 178, 176, 8, VERDE_FONDO)
    lienzo.rectangulo(40, 178, 118, 8, VERDE)

    escribir_png(lienzo, destino)
    return destino


# --------------------------------------------------------------------------- #
# Gallery (1280x720)
# --------------------------------------------------------------------------- #

def _imagen_bug():
    lienzo = _fondo(GALERIA_ANCHO, GALERIA_ALTO)
    _titulo(lienzo, "EL BUG DEL JUEGO BASE", 6)

    lienzo.texto(MARGEN, 180, "SIN EL MOD", 4, ROJO)
    _tooltip(lienzo, MARGEN, 220, 520, 280, "HACHA",
             ["IGUI_perks_Carpinteria", "_Description"], ROJO, ROJO_FONDO)
    lienzo.texto(MARGEN + 24, 420, "SE VE LA CLAVE CRUDA", 3, ROJO)
    lienzo.texto(MARGEN + 24, 450, "EN VEZ DE LA DESCRIPCION", 3, ROJO)

    lienzo.texto(696, 180, "CON EL MOD", 4, VERDE)
    _tooltip(lienzo, 696, 220, 520, 280, "HACHA",
             ["PUEDES USAR EL HACHA PARA", "TALAR ARBOLES Y SACAR",
              "MADERA DE FORMA MAS", "EFICIENTE."], VERDE, VERDE_FONDO)

    _pie(lienzo,
         "El motor arma la clave del tooltip concatenando el nombre TRADUCIDO de la "
         "habilidad, pero el juego solo trae las descripciones bajo el nombre EN "
         "INGLES. En cualquier otro idioma la clave no existe y se muestra el texto "
         "crudo.", y=560)
    return lienzo


def _imagen_como():
    lienzo = _fondo(GALERIA_ANCHO, GALERIA_ALTO)
    _titulo(lienzo, "COMO LO ARREGLA", 6)

    ancho = 360
    pasos = [
        ("1", "NOMBRE TRADUCIDO",
         "El motor pide la clave con el nombre.",
         ["IGUI_perks_Carpinteria", "_Description"]),
        ("2", "TRADUCE AL INGLES",
         "El mod traduce ese nombre al ingles.",
         ["Perks.Carpentry", "-> Carpentry"]),
        ("3", "CLAVE CORRECTA",
         "Esa clave si existe, y ya traducida.",
         ["IGUI_perks_Carpentry", "_Description"]),
    ]

    x = MARGEN
    for i, (numero, nombre, detalle, claves) in enumerate(pasos):
        lienzo.panel(x, 190, ancho, 330)
        lienzo.circulo(x + 44, 240, 26, VERDE_FONDO)
        lienzo.circulo(x + 44, 240, 23, PANEL)
        lienzo.texto_centrado(x + 44, 229, numero, 5, VERDE)
        lienzo.texto(x + 24, 290, nombre, 3, AMBAR)
        lienzo.texto_multilinea(x + 24, 330, detalle, 3, TEXTO_SUAVE, ancho - 48)
        for j, clave in enumerate(claves):
            lienzo.texto(x + 24, 448 + j * 30, clave, 2, VERDE)
        if i < 2:
            lienzo.texto(x + ancho + 6, 330, "→", 4, AMBAR)
        x += ancho + 36

    _pie(lienzo,
         "Un solo archivo, sin copiar ninguna traduccion: el texto que se ve es el del "
         "propio juego, asi que si The Indie Stone mejora una descripcion, se ve la "
         "mejora.", y=570)
    return lienzo


def _imagen_cobertura():
    lienzo = _fondo(GALERIA_ANCHO, GALERIA_ALTO)
    _titulo(lienzo, "QUE ABARCA", 7)

    datos = [
        ("35", ["HABILIDADES", "VANILLA"],
         ["Hacha, Carpinteria,", "Cocina, Sigilo,", "Medicina y mas."]),
        ("28", ["IDIOMAS DEL", "JUEGO"],
         ["Un solo archivo.", "La clave correcta", "se resuelve en", "tiempo real."]),
        ("1", ["ARCHIVO"],
         ["Pisa el tooltip", "del juego y nada", "mas: se puede", "quitar en caliente."]),
    ]

    x = MARGEN
    ancho = 360
    for numero, nombre, detalle in datos:
        lienzo.panel(x, 190, ancho, 340)
        lienzo.texto_centrado(x + ancho // 2, 212, numero, 10, AMBAR)
        for j, linea in enumerate(nombre):
            lienzo.texto_centrado(x + ancho // 2, 300 + j * 28, linea, 3, TEXTO_FUERTE)
        lienzo.rectangulo(x + 40, 366, ancho - 80, 3, BORDE)
        for j, linea in enumerate(detalle):
            lienzo.texto(x + 30, 388 + j * 30, linea, 3, TEXTO_SUAVE)
        x += ancho + 36

    _pie(lienzo,
         "Las habilidades que agreguen otros mods mantienen su comportamiento original, "
         "y el mod se puede quitar en cualquier momento sin dejar rastro en la partida.",
         y=570)
    return lienzo


def build_gallery(destino):
    for nombre, lienzo in (("1-el-bug", _imagen_bug()),
                           ("2-como-funciona", _imagen_como()),
                           ("3-cobertura", _imagen_cobertura())):
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
