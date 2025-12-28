"""
Ejemplo de generación de rótulo con Pillow (PIL)
Genera una imagen raster PNG con círculo y texto
"""
from PIL import Image, ImageDraw, ImageFont

# Crear imagen con más ancho para el texto completo
img = Image.new('RGB', (700, 300), color='white')
draw = ImageDraw.Draw(img)

# Dibujar círculo azul UCR
circle_center = (150, 150)
circle_radius = 80
draw.ellipse([
    circle_center[0] - circle_radius,
    circle_center[1] - circle_radius,
    circle_center[0] + circle_radius,
    circle_center[1] + circle_radius
], fill='#003DA5')

# Dibujar letra "b" blanca en el círculo
try:
    font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size=80)
except:
    font_large = ImageFont.load_default()

b_text = "b"
bbox = draw.textbbox((0, 0), b_text, font=font_large)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
draw.text(
    (circle_center[0] - text_width/2, circle_center[1] - text_height/2 - 10),
    b_text,
    fill='white',
    font=font_large
)

# Texto del nombre de parada
try:
    font_text = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size=32)
except:
    font_text = ImageFont.load_default()

text = "Facultad de Ingeniería"
bbox = draw.textbbox((0, 0), text, font=font_text)
text_width = bbox[2] - bbox[0]

# Centrar texto a la derecha del círculo
x = 250
y = 135
draw.text((x, y), text, fill='#003DA5', font=font_text)

# Guardar
img.save('examples/pillow_test.png')
print("Generado: pillow_test.png")
