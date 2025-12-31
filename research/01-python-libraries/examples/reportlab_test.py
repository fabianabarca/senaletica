"""
Ejemplo de generación de rótulo con ReportLab
Genera documento PDF vectorial
"""
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
import os

# Crear canvas PDF
output_pdf = os.path.join(os.path.dirname(__file__), 'reportlab_test.pdf')
c = canvas.Canvas(output_pdf, pagesize=(600, 300))

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
print(f"Generado: {output_pdf}")
