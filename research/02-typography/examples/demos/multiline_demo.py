#!/usr/bin/env python3
"""
Ejemplo de división automática en múltiples líneas.
"""
import cairo

def split_and_render(text, max_width=600, font_size=150):
    """
    Divide texto en líneas y renderiza.
    """
    surface = cairo.SVGSurface(None, 0, 0)
    ctx = cairo.Context(surface)
    
    ctx.select_font_face("DejaVu Sans", 
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

def create_multiline_svg():
    """
    Crea SVG con texto en múltiples líneas.
    """
    import os
    
    text = "Escuela de Arquitectura y Urbanismo"
    max_width = 550  # Reducir para evitar cortes
    font_size = 80   # Tamaño más pequeño
    line_height = 100
    
    lines = split_and_render(text, max_width, font_size)
    
    total_height = len(lines) * line_height + 100
    output_path = os.path.join(os.path.dirname(__file__), 'typography_multiline.svg')
    
    surface = cairo.SVGSurface(output_path, 700, total_height)
    ctx = cairo.Context(surface)
    
    # Fondo blanco
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    # Fondo azul para texto
    ctx.set_source_rgb(0, 93/255, 164/255)
    ctx.rectangle(75, 30, max_width, len(lines) * line_height + 60)
    ctx.fill()
    
    # Renderizar cada línea
    ctx.set_source_rgb(1, 1, 1)
    ctx.select_font_face("DejaVu Sans", 
                         cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)
    
    y_offset = 100
    for line in lines:
        extents = ctx.text_extents(line)
        x_pos = 75 + (max_width - extents.width) / 2
        
        ctx.move_to(x_pos, y_offset)
        ctx.show_text(line)
        
        y_offset += line_height
    
    # Info
    ctx.set_source_rgb(0, 0, 0)
    ctx.select_font_face("DejaVu Sans", 
                         cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(14)
    ctx.move_to(50, total_height - 20)
    ctx.show_text(f"{len(lines)} líneas × {font_size}pt")
    
    surface.finish()
    print(f"Generated: {output_path} ({len(lines)} lines)")

if __name__ == '__main__':
    create_multiline_svg()
