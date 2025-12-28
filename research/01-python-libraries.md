# Bibliotecas Python para Generación de Rótulos

## Objetivo

Identificar y comparar bibliotecas Python capaces de generar rótulos vectoriales con tipografía personalizada, cumpliendo con las especificaciones de diseño de bUCR.

## Requisitos del Sistema

1. **Generación de gráficos vectoriales** (SVG preferiblemente)
2. **Soporte para tipografías personalizadas** (fuentes UCR)
3. **Medición y ajuste de texto** dinámico
4. **Manejo de formas geométricas** (círculos, rectángulos, líneas)
5. **Control preciso de posicionamiento** (diseño profesional)
6. **Exportación a múltiples formatos** (SVG, PNG, PDF)

---

## Bibliotecas Candidatas

### 1. svgwrite

**Descripción:** Biblioteca pura Python para crear documentos SVG programáticamente.

**Pros:**
-  SVG nativo (formato ideal para señalética)
-  Control preciso de elementos SVG
-  Soporte para fuentes web y font-family
-  Lightweight, sin dependencias pesadas
-  Documentación clara

**Contras:**
-  No renderiza, solo crea SVG (necesita viewer externo)
-  Medición de texto limitada (requiere cálculos manuales)
-  No font embedding automático

**Caso de uso ideal:** Generación de SVG con especificaciones exactas conocidas de antemano.

**Ejemplo básico:**
```python
import svgwrite

dwg = svgwrite.Drawing('rotulo.svg', size=('600px', '300px'))
dwg.add(dwg.circle(center=(300, 150), r=100, fill='#003DA5'))
dwg.add(dwg.text('Facultad de Ingeniería', 
                 insert=(300, 150), 
                 text_anchor='middle',
                 font_family='Arial',
                 font_size='24px'))
dwg.save()
```

**Veredicto:**  Excelente para SVG puro, pero requiere trabajo manual para tipografía.

---

### 2. Pillow (PIL)

**Descripción:** Biblioteca de procesamiento de imágenes raster más popular de Python.

**Pros:**
-  Muy madura y estable
-  Excelente soporte para fuentes TrueType/OpenType
-  Medición precisa de texto con `textbbox()`
-  Amplia comunidad y documentación
-  Fácil ajuste dinámico de texto

**Contras:**
-  Genera imágenes raster (PNG/JPEG), no vectoriales
-  Pérdida de calidad al escalar
-  Archivos más pesados que SVG
-  No ideal para impresión profesional

**Caso de uso ideal:** Prototipos rápidos, previews, rótulos digitales.

**Ejemplo básico:**
```python
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (600, 300), color='white')
draw = ImageDraw.Draw(img)

font = ImageFont.truetype('/path/to/font.ttf', size=48)
text = "Facultad de Ingeniería"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]

# Centrar texto
x = (600 - text_width) / 2
draw.text((x, 150), text, fill='#003DA5', font=font)

img.save('rotulo.png')
```

**Veredicto:**  Bueno para prototipado, no para producción de señalética.

---

### 3. CairoSVG + pycairo

**Descripción:** Cairo es una biblioteca de gráficos 2D con bindings Python. CairoSVG permite conversión entre formatos.

**Pros:**
-  Gráficos vectoriales de alta calidad
-  Excelente renderizado de fuentes
-  Exportación a SVG, PNG, PDF
-  Usado en producción (industria)
-  Control preciso de typography

**Contras:**
-  Dependencias del sistema (libcairo)
-  Curva de aprendizaje más alta
-  API más compleja que svgwrite
-  Setup más complicado

**Caso de uso ideal:** Generación profesional multi-formato con renderizado preciso.

**Ejemplo básico:**
```python
import cairo

surface = cairo.SVGSurface('rotulo.svg', 600, 300)
ctx = cairo.Context(surface)

# Fondo
ctx.set_source_rgb(1, 1, 1)
ctx.paint()

# Círculo
ctx.arc(300, 150, 100, 0, 2 * 3.14159)
ctx.set_source_rgb(0, 0.24, 0.65)  # #003DA5
ctx.fill()

# Texto
ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(24)
ctx.set_source_rgb(0, 0, 0)
ctx.move_to(250, 250)
ctx.show_text("Facultad de Ingeniería")

surface.finish()
```

**Veredicto:**  Mejor opción para producción profesional, a pesar de complejidad.

---

### 4. ReportLab

**Descripción:** Biblioteca comercial/open source para generación de PDF con capacidades de diagramación.

**Pros:**
-  Diseñada para documentos de producción
-  Excelente manejo de tipografía
-  Soporte para gráficos vectoriales en PDF
-  Herramientas de layout avanzadas
-  Usado en industria (facturas, reportes)

**Contras:**
-  Enfocado en PDF, no SVG
-  Licencia comercial para algunas features
-  Overhead para proyecto simple de señalética
-  Conversión PDF→SVG requiere herramientas adicionales

**Caso de uso ideal:** Documentos complejos, reportes, sistemas de impresión masiva.

**Ejemplo básico:**
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

c = canvas.Canvas('rotulo.pdf', pagesize=letter)

# Círculo
c.setFillColorRGB(0, 0.24, 0.65)
c.circle(15*cm, 20*cm, 3*cm, fill=1)

# Texto
c.setFont("Helvetica-Bold", 24)
c.drawCentredString(15*cm, 10*cm, "Facultad de Ingeniería")

c.save()
```

**Veredicto:**  Excelente para PDF, pero no es la mejor opción para SVG.

---

### 5. drawsvg

**Descripción:** Biblioteca moderna para crear dibujos SVG con API de alto nivel.

**Pros:**
-  API más intuitiva que svgwrite
-  Soporte para animaciones SVG
-  Renderizado en Jupyter notebooks
-  Moderna y activamente mantenida

**Contras:**
-  Comunidad más pequeña
-  Documentación menos extensa
-  Menos maduro que svgwrite

**Caso de uso ideal:** Visualizaciones interactivas, proyectos modernos.

**Ejemplo básico:**
```python
import drawsvg as draw

d = draw.Drawing(600, 300)
d.append(draw.Circle(300, 150, 100, fill='#003DA5'))
d.append(draw.Text('Facultad de Ingeniería', 24, 300, 250, 
                   text_anchor='middle', font_family='Arial'))
d.save_svg('rotulo.svg')
```

**Veredicto:**  Buena alternativa moderna a svgwrite.

---

## Comparativa Resumida

| Característica | svgwrite | Pillow | Cairo | ReportLab | drawsvg |
|----------------|----------|--------|-------|-----------|---------|
| **Formato nativo** | SVG | PNG | SVG/PDF/PNG | PDF | SVG |
| **Vectorial** |  |  |  |  |  |
| **Tipografía custom** |  |  |  |  |  |
| **Medición texto** |  |  |  |  |  |
| **Facilidad de uso** |  |  |  |  |  |
| **Dependencias** | Ninguna | Ninguna | libcairo | Ninguna | Ninguna |
| **Producción** |  |  |  |  |  |
| **Curva aprendizaje** | Baja | Baja | Alta | Media | Baja |

---

## Recomendación Preliminar

### Para Prototipo Rápido (MVP):
**Pillow + svgwrite**
- Usar Pillow para calcular dimensiones de texto
- Usar svgwrite para generar SVG final con medidas calculadas
- Rápido de implementar, sin dependencias del sistema

### Para Producción (Sistema Completo):
**pycairo**
- Calidad profesional
- Multi-formato (SVG/PDF/PNG)
- Manejo robusto de tipografía
- Vale la pena la curva de aprendizaje

### Alternativa Intermedia:
**drawsvg + font metrics manual**
- API moderna y limpia
- Pure Python
- Calcular métricas con fontTools si es necesario

---

## Próximos Pasos

1.  Identificar bibliotecas candidatas
2.  Crear ejemplos funcionales de cada biblioteca
3.  Probar con tipografías UCR reales
4.  Medir performance y calidad de output
5.  Selección final basada en pruebas

---

**Actualizado:** 28 de diciembre de 2025
