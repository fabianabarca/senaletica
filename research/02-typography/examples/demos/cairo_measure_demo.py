#!/usr/bin/env python3
"""
Ejemplo de medición y ajuste de texto con pycairo.
Genera SVG con tres tamaños diferentes según longitud de texto.
"""
import cairo

def measure_and_fit_text(text, max_width=600, font_face="DejaVu Sans"):
    """
    Mide texto y ajusta tamaño de fuente para que quepa en max_width.
    """
    surface = cairo.SVGSurface(None, 0, 0)
    ctx = cairo.Context(surface)
    
    # Probar tamaños de fuente de 200pt a 100pt
    for font_size in range(200, 99, -10):
        ctx.select_font_face(font_face, 
                             cairo.FONT_SLANT_NORMAL, 
                             cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(font_size)
        
        extents = ctx.text_extents(text)
        
        if extents.width <= max_width:
            return font_size, extents.width, extents.height
    
    return 100, extents.width, extents.height

def create_test_svg():
    """
    Crea SVG con tres ejemplos de texto ajustado.
    """
    import os
    
    texts = [
        "FING",
        "Facultad de Ingeniería",
        "Escuela de Arquitectura y Urbanismo"
    ]
    
    max_width = 600
    height = 400
    
    output_path = os.path.join(os.path.dirname(__file__), 'typography_cairo_measure.svg')
    surface = cairo.SVGSurface(output_path, 700, height)
    ctx = cairo.Context(surface)
    
    # Fondo blanco
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    # Renderizar cada texto
    y_offset = 50
    
    for text in texts:
        font_size, width, height_text = measure_and_fit_text(text, max_width)
        
        # Configurar fuente para medir correctamente
        ctx.select_font_face("DejaVu Sans", 
                             cairo.FONT_SLANT_NORMAL, 
                             cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(font_size)
        extents = ctx.text_extents(text)
        box_height = extents.height + 40
        
        # Dibujar fondo azul UCR
        ctx.set_source_rgb(0, 93/255, 164/255)  # #005DA4
        ctx.rectangle(50, y_offset, max_width, box_height)
        ctx.fill()
        
        # Dibujar texto blanco centrado horizontal y verticalmente
        ctx.set_source_rgb(1, 1, 1)
        x_pos = 50 + (max_width - extents.width) / 2
        # Usar misma fórmula que multiline_demo.py para centrado vertical
        y_pos = y_offset + (box_height + extents.height) / 2
        
        ctx.move_to(x_pos, y_pos)
        ctx.show_text(text)
        
        y_offset += box_height + 20
    
    surface.finish()
    print(f"Generated: {output_path}")

if __name__ == '__main__':
    create_test_svg()

