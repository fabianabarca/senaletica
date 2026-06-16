#!/usr/bin/env python3
"""
Ejemplo de cálculo de letter-spacing para ajuste tipográfico preciso.
"""

def calculate_letter_spacing(text, current_width, target_width):
    """
    Calcula letter-spacing necesario para ajustar texto
    a un ancho objetivo exacto.
    
    Args:
        text: Texto a ajustar
        current_width: Ancho actual del texto
        target_width: Ancho deseado
    
    Returns:
        float: Letter-spacing en pixeles (puede ser negativo)
    """
    num_gaps = len(text) - 1  # Espacios entre letras
    
    if num_gaps == 0:
        return 0.0
    
    extra_space = target_width - current_width
    letter_spacing = extra_space / num_gaps
    
    return letter_spacing

def demo_letter_spacing():
    """
    Demuestra cálculo de letter-spacing para diferentes escenarios.
    """
    examples = [
        {
            'text': 'FACULTAD',
            'current_width': 450,
            'target_width': 600,
            'description': 'Expandir texto corto'
        },
        {
            'text': 'INGENIERÍA',
            'current_width': 620,
            'target_width': 600,
            'description': 'Comprimir texto largo'
        },
        {
            'text': 'UCR',
            'current_width': 200,
            'target_width': 600,
            'description': 'Sigla muy corta'
        }
    ]
    
    print("=" * 70)
    print("CÁLCULO DE LETTER-SPACING")
    print("=" * 70)
    print("\nUsado en señalética profesional para ajuste tipográfico preciso.\n")
    
    for ex in examples:
        spacing = calculate_letter_spacing(
            ex['text'], 
            ex['current_width'], 
            ex['target_width']
        )
        
        print(f"Caso: {ex['description']}")
        print(f"  Texto: {ex['text']}")
        print(f"  Ancho actual: {ex['current_width']}px")
        print(f"  Ancho objetivo: {ex['target_width']}px")
        print(f"  Letter-spacing: {spacing:+.2f}px")
        print()
    
    print("Implementación en pycairo:")
    print("  1. Renderizar cada letra individualmente con offsets calculados")
    print("  2. Usar Pango con atributo 'letter-spacing'")
    print("  3. Convertir a SVG y aplicar 'letter-spacing' CSS")
    
    print("\n" + "=" * 70)
    
    # Generar SVG de demostración
    import os
    import cairo
    
    output_path = os.path.join(os.path.dirname(__file__), 'letter_spacing_output.svg')
    surface = cairo.SVGSurface(output_path, 700, 450)
    ctx = cairo.Context(surface)
    
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    # Visualizar los 3 casos
    y_offset = 80
    font_size = 48
    
    for ex in examples:
        spacing = calculate_letter_spacing(ex['text'], ex['current_width'], ex['target_width'])
        
        # Título
        ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(16)
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(50, y_offset - 20)
        ctx.show_text(ex['description'])
        
        # Fondo azul UCR
        ctx.set_source_rgb(0, 93/255, 164/255)
        ctx.rectangle(50, y_offset, 600, 80)
        ctx.fill()
        
        # Texto con letter-spacing simulado (renderizado manual)
        ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(font_size)
        ctx.set_source_rgb(1, 1, 1)
        
        # Calcular posición inicial para centrar
        total_width = ex['target_width']
        x_start = 50 + (600 - total_width) / 2
        x_pos = x_start
        
        # Renderizar cada letra con spacing
        for i, char in enumerate(ex['text']):
            ctx.move_to(x_pos, y_offset + 50)
            ctx.show_text(char)
            char_width = ctx.text_extents(char).width
            x_pos += char_width
            if i < len(ex['text']) - 1:
                x_pos += spacing
        
        # Info de spacing
        ctx.set_font_size(14)
        ctx.move_to(55, y_offset + 70)
        ctx.show_text(f"Spacing: {spacing:+.1f}px")
        
        y_offset += 130
    
    surface.finish()
    print(f"\n✓ SVG generado: {output_path}")

if __name__ == '__main__':
    demo_letter_spacing()
