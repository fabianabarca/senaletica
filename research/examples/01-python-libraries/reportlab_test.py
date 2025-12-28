"""
Ejemplo de generación de rótulo con ReportLab
Genera documento PDF vectorial
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors

# Crear canvas PDF
c = canvas.Canvas('examples/reportlab_test.pdf', pagesize=(600, 300))

# Círculo azul UCR
circle_x, circle_y = 150, 150
circle_radius = 80
c.setFillColor(colors.HexColor('#003DA5'))
c.circle(circle_x, circle_y, circle_radius, fill=1)

# Letra "b" blanca en el círculo
c.setFillColor(colors.white)
c.setFont("Helvetica-Bold", 80)
# Aproximar centrado (ReportLab no tiene textbbox fácil)
c.drawString(circle_x - 20, circle_y - 25, "b")

# Texto del nombre de parada
c.setFillColor(colors.HexColor('#003DA5'))
c.setFont("Helvetica-Bold", 32)
c.drawString(250, 135, "Facultad de Ingeniería")

# Guardar
c.save()
print("Generado: reportlab_test.pdf")

# Convertir a PNG para visualización
try:
    from pdf2image import convert_from_path
    images = convert_from_path('examples/reportlab_test.pdf', dpi=150)
    if images:
        images[0].save('examples/reportlab_test.png')
        print("Convertido a: reportlab_test.png")
except ImportError:
    print("Instalar pdf2image para conversión: pip install pdf2image")
except Exception as e:
    print(f"No se pudo convertir a PNG: {e}")
