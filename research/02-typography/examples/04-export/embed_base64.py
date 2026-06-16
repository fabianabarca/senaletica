#!/usr/bin/env python3
"""
Ejemplo de embedding de fuente en SVG usando base64.
Permite distribuir SVGs autocontenidos sin dependencia de fuentes instaladas.
"""
import base64
import svgwrite

def embed_font_in_svg(font_path, svg_path, text):
    """
    Crea SVG con fuente embedida en base64.
    
    Args:
        font_path: Ruta al archivo .ttf o .otf
        svg_path: Ruta del SVG a crear
        text: Texto a renderizar
    """
    # Leer fuente y convertir a base64
    with open(font_path, 'rb') as f:
        font_data = f.read()
    
    base64_font = base64.b64encode(font_data).decode('utf-8')
    
    # Determinar formato de fuente
    font_format = 'truetype' if font_path.endswith('.ttf') else 'opentype'
    
    # Crear SVG con @font-face
    dwg = svgwrite.Drawing(svg_path, size=('800px', '400px'))
    
    # Agregar definición de fuente
    font_face_css = f"""
    @font-face {{
        font-family: 'EmbeddedFont';
        src: url(data:font/{font_format};charset=utf-8;base64,{base64_font})
             format('{font_format}');
        font-weight: bold;
    }}
    """
    
    dwg.defs.add(dwg.style(font_face_css))
    
    # Agregar texto usando la fuente embedida
    text_element = dwg.text(
        text,
        insert=(400, 200),
        text_anchor='middle',
        font_family='EmbeddedFont',
        font_size='48px',
        font_weight='bold',
        fill='#003DA5'  # Azul UCR
    )
    dwg.add(text_element)
    
    dwg.save()
    
    return len(base64_font)

def demo_base64_embedding():
    """
    Demuestra embedding de Myriad Pro en SVG.
    """
    import os
    script_dir = os.path.dirname(__file__)
    font_path = os.path.join(script_dir, '../../myriad-pro/MYRIADPRO-BOLD.OTF')
    svg_path = os.path.join(script_dir, 'embed_base64_output.svg')
    text = 'Facultad de Ingeniería'
    
    print("=" * 70)
    print("FONT EMBEDDING CON BASE64")
    print("=" * 70)
    print(f"\nFuente: {font_path}")
    print(f"Texto: '{text}'")
    print(f"Output: {svg_path}\n")
    
    base64_size = embed_font_in_svg(font_path, svg_path, text)
    
    print("Resultados:")
    print(f"  ✓ SVG generado con fuente embedida")
    print(f"  ✓ Tamaño base64: {base64_size} caracteres")
    print(f"  ✓ Tamaño fuente original: ~94KB")
    
    print("\nVentajas:")
    print("  • SVG autocontenido (un solo archivo)")
    print("  • Funciona sin fuentes instaladas")
    print("  • Compatible con cualquier visor/navegador")
    
    print("\nDesventajas:")
    print("  • Archivo SVG más grande (50-200KB)")
    print("  • Una fuente por SVG")
    
    print("\nUso recomendado:")
    print("  → Distribución de rótulos individuales")
    print("  → Cuando portabilidad es prioridad")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    demo_base64_embedding()
