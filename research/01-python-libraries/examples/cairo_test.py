"""
Ejemplo de generación de rótulo con pycairo
Genera SVG vectorial de alta calidad
"""
import cairo
import math
import os

# Crear surface SVG con más ancho para el texto completo
width, height = 700, 300
output_path = os.path.join(os.path.dirname(__file__), 'cairo_test.svg')
surface = cairo.SVGSurface(output_path, width, height)
ctx = cairo.Context(surface)

# Fondo blanco
ctx.set_source_rgb(1, 1, 1)
ctx.paint()

# Círculo azul UCR
circle_x, circle_y = 150, 150
circle_radius = 80
ctx.arc(circle_x, circle_y, circle_radius, 0, 2 * math.pi)
ctx.set_source_rgb(0, 0.24, 0.65)  # #003DA5
ctx.fill()

# Letra "b" blanca en el círculo
ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(80)
ctx.set_source_rgb(1, 1, 1)  # Blanco

# Centrar la "b"
text = "b"
extents = ctx.text_extents(text)
x = circle_x - extents.width / 2 - extents.x_bearing
y = circle_y - extents.height / 2 - extents.y_bearing
ctx.move_to(x, y)
ctx.show_text(text)

# Texto del nombre de parada
ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(32)
ctx.set_source_rgb(0, 0.24, 0.65)  # #003DA5

text = "Facultad de Ingeniería"
extents = ctx.text_extents(text)
x = 250
y = 150 + extents.height / 2
ctx.move_to(x, y)
ctx.show_text(text)

# Finalizar
surface.finish()
print(f"Generado: {output_path}")
