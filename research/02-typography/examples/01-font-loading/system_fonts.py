#!/usr/bin/env python3
"""
Ejemplo de carga de fuentes del sistema con pycairo.
"""
import cairo

def demo_system_font_loading():
    """
    Demuestra cómo cargar fuentes instaladas en el sistema.
    """
    import os
    output_path = os.path.join(os.path.dirname(__file__), 'system_fonts_output.svg')
    surface = cairo.SVGSurface(output_path, 700, 300)
    ctx = cairo.Context(surface)
    
    # Fondo blanco
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    # Probar Myriad Pro (si está instalada en sistema)
    try:
        ctx.select_font_face("Myriad Pro", 
                             cairo.FONT_SLANT_NORMAL, 
                             cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(48)
        
        # Fondo azul UCR
        ctx.set_source_rgb(0, 93/255, 164/255)
        ctx.rectangle(50, 50, 600, 100)
        ctx.fill()
        
        # Texto blanco centrado verticalmente
        ctx.set_source_rgb(1, 1, 1)
        extents = ctx.text_extents("Myriad Pro (sistema)")
        y_pos = 50 + (100 + extents.height) / 2
        ctx.move_to(70, y_pos)
        ctx.show_text("Myriad Pro (sistema)")
        
        print("✓ Myriad Pro cargada desde sistema")
    except Exception as e:
        print(f"✗ Myriad Pro no disponible en sistema: {e}")
        ctx.set_source_rgb(0.8, 0.8, 0.8)
        ctx.rectangle(50, 50, 600, 100)
        ctx.fill()
    
    # Alternativa: DejaVu Sans para desarrollo
    ctx.select_font_face("DejaVu Sans", 
                         cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(48)
    
    # Fondo azul UCR
    ctx.set_source_rgb(0, 93/255, 164/255)
    ctx.rectangle(50, 180, 600, 100)
    ctx.fill()
    
    # Texto blanco centrado verticalmente
    ctx.set_source_rgb(1, 1, 1)
    extents = ctx.text_extents("DejaVu Sans (fallback)")
    y_pos = 180 + (100 + extents.height) / 2
    ctx.move_to(70, y_pos)
    ctx.show_text("DejaVu Sans (fallback)")
    
    surface.finish()
    print(f"✓ Generado: {output_path}")
    print("  - Muestra carga de fuentes del sistema")
    print("  - Myriad Pro (si disponible) + DejaVu Sans (fallback)")

if __name__ == '__main__':
    demo_system_font_loading()
