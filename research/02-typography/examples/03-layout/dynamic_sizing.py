#!/usr/bin/env python3
"""
Ejemplo de ajuste dinámico de tamaño de fuente según especificaciones UCR.
"""
import cairo

def calculate_optimal_font_size(text, max_width, font_face="Myriad Pro", 
                                 min_size=56, max_size=110):
    """
    Calcula el tamaño de fuente óptimo para que el texto quepa 
    en el ancho máximo disponible (especificaciones UCR: 56-110mm).
    
    Args:
        text: Texto a medir
        max_width: Ancho máximo disponible en pixeles
        font_face: "Myriad Pro" (producción) o "DejaVu Sans" (desarrollo)
        min_size: Tamaño mínimo 56mm ≈ 212px @ 96dpi
        max_size: Tamaño máximo 110mm ≈ 415px @ 96dpi
    
    Returns:
        int: Tamaño de fuente óptimo en puntos
    """
    surface = cairo.SVGSurface(None, 0, 0)
    ctx = cairo.Context(surface)
    
    # Convertir mm a puntos (aprox)
    min_size_pt = int(min_size * 2.83465)
    max_size_pt = int(max_size * 2.83465)
    
    font_size = max_size_pt
    
    while font_size >= min_size_pt:
        ctx.select_font_face(font_face, 
                             cairo.FONT_SLANT_NORMAL, 
                             cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(font_size)
        
        extents = ctx.text_extents(text)
        
        if extents.width <= max_width:
            return font_size
        
        font_size -= 5  # Reducir en incrementos de 5pt
    
    return min_size_pt

def demo_font_size_adjustment():
    """
    Demuestra ajuste de tamaño para textos de diferentes longitudes.
    También genera SVG de demostración.
    """
    import os
    import cairo
    
    texts = [
        "FING",
        "Facultad de Ingeniería",
        "Escuela de Arquitectura y Urbanismo"
    ]
    
    max_width = 600  # pixeles disponibles
    font_face = "DejaVu Sans"  # Usar fallback para demo
    
    print("=" * 70)
    print("AJUSTE DINÁMICO DE TAMAÑO DE FUENTE")
    print("=" * 70)
    print(f"\nEspecificaciones UCR: 56-110mm")
    print(f"Ancho máximo: {max_width}px")
    print(f"Fuente: {font_face}\n")
    
    for text in texts:
        size = calculate_optimal_font_size(text, max_width, font_face)
        print(f"{text:45} -> {size}pt")
    
    print("\nNotas:")
    print("  • Textos cortos usan tamaño máximo (311pt)")
    print("  • Textos largos se ajustan iterativamente")
    print("  • Nunca baja del mínimo (158pt)")
    
    print("\n" + "=" * 70)
    
    # Generar SVG de demostración
    output_path = os.path.join(os.path.dirname(__file__), 'dynamic_sizing_output.svg')
    surface = cairo.SVGSurface(output_path, 700, 600)
    ctx = cairo.Context(surface)
    
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    y_offset = 50
    for text in texts:
        size = calculate_optimal_font_size(text, max_width, font_face)
        
        # Calcular altura real del texto
        ctx.select_font_face(font_face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(size)
        extents = ctx.text_extents(text)
        box_height = extents.height + 40
        
        # Fondo azul UCR
        ctx.set_source_rgb(0, 93/255, 164/255)
        ctx.rectangle(50, y_offset, 600, box_height)
        ctx.fill()
        
        # Texto blanco centrado horizontal y verticalmente
        ctx.set_source_rgb(1, 1, 1)
        x_pos = 50 + (600 - extents.width) / 2
        y_pos = y_offset + (box_height + extents.height) / 2
        ctx.move_to(x_pos, y_pos)
        ctx.show_text(text)
        
        y_offset += box_height + 30
    
    surface.finish()
    print(f"\n✓ SVG generado: {output_path}")

if __name__ == '__main__':
    demo_font_size_adjustment()
