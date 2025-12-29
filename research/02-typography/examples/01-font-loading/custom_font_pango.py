#!/usr/bin/env python3
"""
Ejemplo de carga de fuente custom con Cairo.
Nota: PangoCairo tiene problemas de compatibilidad entre pycairo y PyGObject.
Esta versión usa Cairo directo cargando Myriad Pro desde el sistema.
"""
import cairo
import os

def load_custom_font():
    """
    Carga Myriad Pro Bold desde el sistema usando Cairo.
    """
    script_dir = os.path.dirname(__file__)
    font_path = os.path.join(script_dir, "../../myriad-pro/MYRIADPRO-BOLD.OTF")
    output_path = os.path.join(script_dir, 'custom_font_pango_output.svg')
    
    surface = cairo.SVGSurface(output_path, 700, 300)
    ctx = cairo.Context(surface)
    
    # Fondo blanco
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    # Fondo azul UCR
    ctx.set_source_rgb(0, 93/255, 164/255)
    ctx.rectangle(50, 80, 600, 140)
    ctx.fill()
    
    # Cargar Myriad Pro desde el sistema
    # Nota: Cairo solo puede usar fuentes instaladas en el sistema
    # Para cargar .otf directamente se requiere Pango, pero tiene problemas
    # de compatibilidad entre pycairo y PyGObject en algunos entornos
    ctx.select_font_face("Myriad Pro", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(48)
    ctx.set_source_rgb(1, 1, 1)
    
    text = "Facultad de Ingeniería"
    extents = ctx.text_extents(text)
    x_pos = 50 + (600 - extents.width) / 2
    y_pos = 150 + extents.height / 2
    
    ctx.move_to(x_pos, y_pos)
    ctx.show_text(text)
    
    surface.finish()
    print(f"✓ Generado: {output_path}")
    print(f"  - Fuente Myriad Pro desde sistema (no desde {font_path})")
    print("  - Cairo directo (sin Pango por problemas de compatibilidad)")
    print("  - Para cargar .otf directamente ver embed_base64.py o convert_to_paths.py")

if __name__ == '__main__':
    load_custom_font()
