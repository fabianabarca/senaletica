#!/usr/bin/env python3
"""
Ejemplo de medición rápida de texto con Pillow.
"""
from PIL import ImageFont

def measure_text_pillow(text, font_path, font_size):
    """
    Mide texto usando Pillow (preciso para archivos .ttf/.otf).
    """
    font = ImageFont.truetype(font_path, size=font_size)
    bbox = font.getbbox(text)
    return {
        'width': bbox[2] - bbox[0], 
        'height': bbox[3] - bbox[1]
    }

def demo_pillow_measurement():
    """
    Demuestra medición con Pillow usando Myriad Pro.
    """
    import os
    script_dir = os.path.dirname(__file__)
    text = "Facultad de Ingeniería"
    font_path = os.path.join(script_dir, "../../myriad-pro/MYRIADPRO-BOLD.OTF")
    font_size = 48
    
    print("=" * 60)
    print("MEDICIÓN DE TEXTO CON PILLOW")
    print("=" * 60)
    print(f"\nTexto: '{text}'")
    print(f"Fuente: {font_path}")
    print(f"Tamaño: {font_size}pt\n")
    
    metrics = measure_text_pillow(text, font_path, font_size)
    
    print("Resultados:")
    print(f"  Ancho: {metrics['width']}px")
    print(f"  Alto: {metrics['height']}px")
    
    print("\nVentajas de Pillow:")
    print("  ✓ Muy preciso con archivos TrueType/OpenType")
    print("  ✓ No requiere superficie de renderizado")
    print("  ✓ Útil para pre-cálculo antes de usar Cairo")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    demo_pillow_measurement()
