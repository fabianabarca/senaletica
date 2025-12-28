"""
Ejemplo de generación de rótulo con svgwrite
Genera SVG puro sin dependencias externas
"""
import svgwrite

dwg = svgwrite.Drawing('examples/svgwrite_test.svg', size=('600px', '300px'))

# Fondo blanco
dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))

# Círculo azul UCR
circle_center = (150, 150)
circle_radius = 80
dwg.add(dwg.circle(center=circle_center, r=circle_radius, fill='#003DA5'))

# Letra "b" blanca en el círculo
dwg.add(dwg.text('b', 
                 insert=(circle_center[0], circle_center[1] + 25), 
                 text_anchor='middle',
                 font_family='Sans-serif',
                 font_size='80px',
                 font_weight='bold',
                 fill='white'))

# Texto del nombre de parada
dwg.add(dwg.text('Facultad de Ingeniería', 
                 insert=(250, 165), 
                 text_anchor='start',
                 font_family='Sans-serif',
                 font_size='32px',
                 font_weight='bold',
                 fill='#003DA5'))

dwg.save()
print("Generado: examples/svgwrite_test.svg")