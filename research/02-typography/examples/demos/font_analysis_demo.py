#!/usr/bin/env python3
"""
Análisis de métricas de fuente usando fontTools.
"""
from fontTools.ttLib import TTFont
import sys

def analyze_font(font_path):
    """
    Analiza y muestra métricas de una fuente TrueType/OpenType.
    """
    try:
        font = TTFont(font_path)
    except Exception as e:
        print(f"Error loading font: {e}")
        return
    
    # Información básica
    print("=" * 60)
    print(f"Font Analysis: {font_path}")
    print("=" * 60)
    
    # Nombres
    name_table = font['name']
    font_family = name_table.getDebugName(1)
    font_subfamily = name_table.getDebugName(2)
    full_name = name_table.getDebugName(4)
    
    print(f"\nFont Names:")
    print(f"  Family: {font_family}")
    print(f"  Subfamily: {font_subfamily}")
    print(f"  Full Name: {full_name}")
    
    # Métricas globales
    units_per_em = font['head'].unitsPerEm
    ascent = font['hhea'].ascent
    descent = font['hhea'].descent
    line_gap = font['hhea'].lineGap
    
    print(f"\nGlobal Metrics:")
    print(f"  Units per EM: {units_per_em}")
    print(f"  Ascent: {ascent} ({ascent/units_per_em*100:.1f}%)")
    print(f"  Descent: {descent} ({descent/units_per_em*100:.1f}%)")
    print(f"  Line Gap: {line_gap}")
    print(f"  Line Height: {ascent - descent + line_gap}")
    
    # Glifos
    glyph_set = font.getGlyphSet()
    num_glyphs = len(glyph_set.keys())
    
    print(f"\nGlyphs:")
    print(f"  Total glyphs: {num_glyphs}")
    
    # Medir algunos caracteres comunes
    cmap = font.getBestCmap()
    test_chars = "ABCEFIMabcefim"
    
    print(f"\nSample Character Widths (at {units_per_em} units):")
    for char in test_chars:
        if ord(char) in cmap:
            glyph_name = cmap[ord(char)]
            glyph = glyph_set[glyph_name]
            width = glyph.width
            width_pct = width / units_per_em * 100
            print(f"  '{char}': {width:4d} units ({width_pct:5.1f}%)")
    
    # Calcular ancho promedio para texto de prueba
    test_text = "Facultad de Ingeniería"
    total_width = 0
    for char in test_text:
        if ord(char) in cmap:
            glyph_name = cmap[ord(char)]
            total_width += glyph_set[glyph_name].width
    
    avg_width = total_width / len(test_text)
    
    print(f"\nTest Text: '{test_text}'")
    print(f"  Total width: {total_width} units")
    print(f"  Average width/char: {avg_width:.1f} units")
    print(f"  At 48pt: ~{total_width * 48 / units_per_em:.0f}px")
    print(f"  At 100pt: ~{total_width * 100 / units_per_em:.0f}px")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    # Usar DejaVu Sans Bold como ejemplo (disponible en Ubuntu)
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    
    if len(sys.argv) > 1:
        font_path = sys.argv[1]
    
    analyze_font(font_path)
