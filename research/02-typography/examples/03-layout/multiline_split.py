#!/usr/bin/env python3
"""
Ejemplo de división automática de texto en múltiples líneas.
"""
import cairo

def split_text_multiline(text, max_width, font_face="Myriad Pro", 
                         font_size=200):
    """
    Divide texto en múltiples líneas si es muy largo,
    manteniendo palabras completas.
    
    Args:
        text: Texto a dividir
        max_width: Ancho máximo por línea
        font_face: "Myriad Pro" (producción) o "DejaVu Sans" (desarrollo)
        font_size: Tamaño de fuente en puntos
    
    Returns:
        list: Lista de strings (una por línea)
    """
    surface = cairo.SVGSurface(None, 0, 0)
    ctx = cairo.Context(surface)
    
    ctx.select_font_face(font_face, 
                         cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)
    
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        extents = ctx.text_extents(test_line)
        
        if extents.width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def demo_multiline_split():
    """
    Demuestra división automática de textos largos.
    También genera SVG de demostración.
    """
    import os
    import cairo
    
    texts = [
        "Escuela de Arquitectura y Urbanismo",
        "Facultad de Ciencias Sociales",
        "FING"
    ]
    
    max_width = 600
    font_face = "DejaVu Sans"
    
    print("=" * 70)
    print("DIVISIÓN AUTOMÁTICA EN MÚLTIPLES LÍNEAS")
    print("=" * 70)
    print(f"\nAncho máximo: {max_width}px")
    print(f"Fuente: {font_face}\n")
    
    for text in texts:
        lines = split_text_multiline(text, max_width, font_face)
        print(f"Original: {text}")
        print(f"Líneas: {len(lines)}")
        for i, line in enumerate(lines, 1):
            print(f"  Línea {i}: {line}")
        print()
    
    print("Ventajas:")
    print("  • Mantiene tamaño de fuente legible")
    print("  • Respeta palabras completas (no parte palabras)")
    print("  • Centrado por línea para mejor estética")
    
    print("\n" + "=" * 70)
    
    # Generar SVG de demostración
    output_path = os.path.join(os.path.dirname(__file__), 'multiline_split_output.svg')
    surface = cairo.SVGSurface(output_path, 700, 600)
    ctx = cairo.Context(surface)
    
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    y_offset = 50
    font_size = 60
    
    for text in texts:
        lines = split_text_multiline(text, max_width, font_face, font_size)
        
        # Calcular altura total
        line_height = font_size + 10
        total_height = len(lines) * line_height + 20
        
        # Fondo azul UCR
        ctx.set_source_rgb(0, 93/255, 164/255)
        ctx.rectangle(50, y_offset, 600, total_height)
        ctx.fill()
        
        # Renderizar cada línea
        ctx.select_font_face(font_face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(font_size)
        ctx.set_source_rgb(1, 1, 1)
        
        line_y = y_offset + font_size + 10
        for line in lines:
            extents = ctx.text_extents(line)
            x_pos = 50 + (600 - extents.width) / 2
            ctx.move_to(x_pos, line_y)
            ctx.show_text(line)
            line_y += line_height
        
        y_offset += total_height + 30
    
    surface.finish()
    print(f"\n✓ SVG generado: {output_path}")

if __name__ == '__main__':
    demo_multiline_split()
