"""
Ejemplo de generación de rótulo con drawsvg
Genera SVG con API moderna de alto nivel
"""
import drawsvg as draw

# Crear drawing
d = draw.Drawing(600, 300, origin=(0, 0))

# Fondo blanco
d.append(draw.Rectangle(0, 0, 600, 300, fill='white'))

# Círculo azul UCR
circle_x, circle_y = 150, 150
circle_radius = 80
d.append(draw.Circle(circle_x, circle_y, circle_radius, fill='#003DA5'))

# Letra "b" blanca en el círculo
d.append(draw.Text('b', 80, circle_x, circle_y,
                   text_anchor='middle',
                   dominant_baseline='middle',
                   font_family='sans-serif',
                   font_weight='bold',
                   fill='white'))

# Texto del nombre de parada
d.append(draw.Text('Facultad de Ingeniería', 32, 250, 150,
                   text_anchor='start',
                   dominant_baseline='middle',
                   font_family='sans-serif',
                   font_weight='bold',
                   fill='#003DA5'))

# Guardar
d.save_svg('examples/drawsvg_test.svg')
print("Generado: drawsvg_test.svg")
