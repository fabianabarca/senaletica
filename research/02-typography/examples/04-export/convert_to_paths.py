#!/usr/bin/env python3
"""
Ejemplo de conversión de texto a paths SVG (outlines vectoriales).
Elimina la necesidad de fuentes, máxima compatibilidad.
"""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import svgwrite

def text_to_paths(font_path, text, font_size=48):
    """
    Convierte texto a paths SVG usando fontTools.
    
    Args:
        font_path: Ruta al archivo .ttf o .otf
        text: Texto a convertir
        font_size: Tamaño de fuente en puntos
    
    Returns:
        tuple: (lista de paths, ancho total)
    """
    font = TTFont(font_path)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    
    units_per_em = font['head'].unitsPerEm
    scale = font_size / units_per_em
    
    paths = []
    x_offset = 0
    
    for char in text:
        if char == ' ':
            # Espacio: solo avanzar
            space_width = int(units_per_em * 0.25 * scale)
            x_offset += space_width
            paths.append((None, space_width))
            continue
        
        glyph_name = cmap.get(ord(char))
        if not glyph_name:
            continue
        
        glyph = glyph_set[glyph_name]
        
        # Crear pen para SVG path
        svg_pen = SVGPathPen(glyph_set)
        
        # Aplicar transformación (escala y traslación)
        transform_pen = TransformPen(svg_pen, (scale, 0, 0, -scale, x_offset, 0))
        
        # Dibujar glyph
        glyph.draw(transform_pen)
        
        # Obtener path data
        path_data = svg_pen.getCommands()
        width = int(glyph.width * scale)
        
        paths.append((path_data, width))
        x_offset += width
    
    return paths, x_offset

def create_svg_with_paths(font_path, text, svg_path, font_size=48):
    """
    Crea SVG usando paths en vez de texto+fuente.
    """
    paths, total_width = text_to_paths(font_path, text, font_size)
    
    dwg = svgwrite.Drawing(svg_path, size=(total_width + 100, font_size + 50))
    
    # Grupo para todos los paths
    group = dwg.g(fill='#003DA5', transform=f'translate(50, {font_size + 10})')
    
    for path_data, width in paths:
        if path_data:  # Ignorar espacios (None)
            path_element = dwg.path(d=path_data)
            group.add(path_element)
    
    dwg.add(group)
    dwg.save()
    
    return total_width

def demo_path_conversion():
    """
    Demuestra conversión de texto a paths con Myriad Pro.
    """
    import os
    script_dir = os.path.dirname(__file__)
    font_path = os.path.join(script_dir, '../../myriad-pro/MYRIADPRO-BOLD.OTF')
    text = 'FING'
    svg_path = os.path.join(script_dir, 'convert_to_paths_output.svg')
    font_size = 72
    
    print("=" * 70)
    print("CONVERSIÓN DE TEXTO A PATHS SVG")
    print("=" * 70)
    print(f"\nFuente: {font_path}")
    print(f"Texto: '{text}'")
    print(f"Tamaño: {font_size}pt")
    print(f"Output: {svg_path}\n")
    
    total_width = create_svg_with_paths(font_path, text, svg_path, font_size)
    
    print("Resultados:")
    print(f"  ✓ SVG generado con paths vectoriales")
    print(f"  ✓ Ancho total: {total_width}px")
    print(f"  ✓ Cada letra convertida a outline")
    
    print("\nVentajas:")
    print("  • Tipografía 100% garantizada")
    print("  • Máxima compatibilidad con visores")
    print("  • Archivos relativamente pequeños (5-20KB)")
    print("  • Editable en Inkscape/Illustrator")
    
    print("\nDesventajas:")
    print("  • Texto no es seleccionable")
    print("  • No indexable por búsqueda")
    print("  • Problemas de accesibilidad (no screen reader)")
    
    print("\nUso recomendado:")
    print("  → Producción final de rótulos")
    print("  → Impresión profesional")
    print("  → Cuando calidad es prioritaria")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    demo_path_conversion()
