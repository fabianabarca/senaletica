#!/usr/bin/env python3
"""
Ejemplo de análisis profundo de métricas tipográficas con fontTools.
"""
from fontTools.ttLib import TTFont

def analyze_font(font_path):
    """
    Extrae métricas completas de una fuente TrueType/OpenType.
    """
    font = TTFont(font_path)
    
    # Métricas globales
    units_per_em = font['head'].unitsPerEm
    ascent = font['hhea'].ascent
    descent = font['hhea'].descent
    line_gap = font['hhea'].lineGap
    
    # Información de nombres
    name_records = font['name']
    font_family = name_records.getDebugName(1)
    font_subfamily = name_records.getDebugName(2)
    
    return {
        'family': font_family,
        'subfamily': font_subfamily,
        'units_per_em': units_per_em,
        'ascent': ascent,
        'descent': descent,
        'line_gap': line_gap,
        'line_height': ascent - descent + line_gap,
        'glyph_count': len(font.getGlyphSet())
    }

def demo_font_analysis():
    """
    Analiza Myriad Pro Bold y muestra métricas detalladas.
    """
    import os
    script_dir = os.path.dirname(__file__)
    font_path = os.path.join(script_dir, "../../myriad-pro/MYRIADPRO-BOLD.OTF")
    
    print("=" * 70)
    print("ANÁLISIS DE MÉTRICAS TIPOGRÁFICAS")
    print("=" * 70)
    print(f"\nFuente: {font_path}\n")
    
    font_info = analyze_font(font_path)
    
    print("Información:")
    print(f"  Familia: {font_info['family']}")
    print(f"  Subfamilia: {font_info['subfamily']}")
    print(f"  Glifos totales: {font_info['glyph_count']}")
    
    print("\nMétricas globales:")
    print(f"  Units per EM: {font_info['units_per_em']}")
    print(f"  Ascent: {font_info['ascent']} ({font_info['ascent']/font_info['units_per_em']*100:.1f}%)")
    print(f"  Descent: {font_info['descent']} ({font_info['descent']/font_info['units_per_em']*100:.1f}%)")
    print(f"  Line gap: {font_info['line_gap']}")
    print(f"  Line height: {font_info['line_height']}")
    
    print("\nCasos de uso:")
    print("  • Validar que se tiene la fuente correcta")
    print("  • Calcular line-height preciso para layouts")
    print("  • Analizar kerning pairs")
    print("  • Extraer glyph paths para conversión a SVG")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    demo_font_analysis()
