#!/usr/bin/env python3
"""
Ejemplo de medición precisa de texto con pycairo.
"""
import cairo

def measure_text(text, font_face, font_size):
    """
    Mide dimensiones exactas de texto en Cairo.
    """
    surface = cairo.SVGSurface(None, 0, 0)
    ctx = cairo.Context(surface)
    
    ctx.select_font_face(font_face, 
                         cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)
    
    extents = ctx.text_extents(text)
    
    return {
        'width': extents.width,
        'height': extents.height,
        'x_bearing': extents.x_bearing,
        'y_bearing': extents.y_bearing,
        'x_advance': extents.x_advance,
        'y_advance': extents.y_advance
    }

def demo_text_measurement():
    """
    Demuestra medición de texto con diferentes fuentes.
    """
    text = "Facultad de Ingeniería"
    
    print("=" * 60)
    print("MEDICIÓN DE TEXTO CON PYCAIRO")
    print("=" * 60)
    print(f"\nTexto: '{text}'")
    print(f"Tamaño: 48pt\n")
    
    # Medir con Myriad Pro (si disponible)
    try:
        metrics_myriad = measure_text(text, "Myriad Pro", 48)
        print("Myriad Pro:")
        print(f"  Ancho: {metrics_myriad['width']:.2f}px")
        print(f"  Alto: {metrics_myriad['height']:.2f}px")
        print(f"  Avance X: {metrics_myriad['x_advance']:.2f}px")
    except Exception as e:
        print(f"Myriad Pro: No disponible ({e})")
    
    # Medir con DejaVu Sans (fallback)
    metrics_dejavu = measure_text(text, "DejaVu Sans", 48)
    print("\nDejaVu Sans:")
    print(f"  Ancho: {metrics_dejavu['width']:.2f}px")
    print(f"  Alto: {metrics_dejavu['height']:.2f}px")
    print(f"  Avance X: {metrics_dejavu['x_advance']:.2f}px")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    demo_text_measurement()
