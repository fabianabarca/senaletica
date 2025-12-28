# Manejo de Tipografías en Python

## Objetivo

Investigar cómo usar tipografías personalizadas en Python para generar rótulos con la identidad visual de la UCR/bUCR.

## Requisitos Tipográficos

Según la documentación de bUCR y normas INTECO:

- **Tamaño de letra:** 56mm - 110mm
- **Legibilidad:** 2-5 metros de distancia
- **Fuente:** Según guía de identidad visual UCR
- **Estilo:** Bold/Regular según jerarquía
- **Ajuste dinámico:** Texto debe adaptarse al espacio disponible

---

## Fuentes de la UCR

### Tipografía Oficial UCR

**Investigar:**
- ¿Qué fuentes usa la UCR en su identidad oficial?
- ¿Están disponibles las fuentes institucionalmente?
- ¿Requieren licencia especial?

**Alternativas comunes:**
- **Helvetica Neue** (común en identidades corporativas)
- **Roboto** (open source, similar a Helvetica)
- **Open Sans** (open source, alta legibilidad)
- **Liberation Sans** (métrica-compatible con Arial/Helvetica)

---

## Formatos de Fuentes

### TrueType (.ttf)
-  Más compatible
-  Bien soportado en Python
-  Fácil de embedir

### OpenType (.otf)
-  Características tipográficas avanzadas
-  Soportado por bibliotecas modernas
-  Algunas features pueden no renderizarse en todas las bibliotecas

### Web Fonts (.woff, .woff2)
-  Para uso en SVG web
-  No directamente usables en Python
-  Requieren conversión

---

## Manejo de Fuentes por Biblioteca

### 1. Pillow (ImageFont)

```python
from PIL import ImageFont

# Cargar fuente
font = ImageFont.truetype('/path/to/font.ttf', size=48)

# Medir texto
from PIL import ImageDraw, Image

img = Image.new('RGB', (1, 1))
draw = ImageDraw.Draw(img)
bbox = draw.textbbox((0, 0), "Texto de prueba", font=font)

width = bbox[2] - bbox[0]
height = bbox[3] - bbox[1]

print(f"Ancho: {width}px, Alto: {height}px")
```

**Características:**
-  Muy preciso para medición
-  Soporte completo TrueType/OpenType
-  Ajuste de tamaño dinámico fácil
-  Solo para raster, no SVG

---

### 2. pycairo

```python
import cairo

surface = cairo.SVGSurface('test.svg', 600, 300)
ctx = cairo.Context(surface)

# Opción 1: Fuente del sistema
ctx.select_font_face("Helvetica", 
                     cairo.FONT_SLANT_NORMAL, 
                     cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(48)

# Opción 2: Fuente custom con fontconfig
# (requiere instalar fuente en el sistema)

# Medir texto
text = "Facultad de Ingeniería"
extents = ctx.text_extents(text)

width = extents.width
height = extents.height

print(f"Ancho: {width}px, Alto: {height}px")
```

**Características:**
-  Medición precisa en espacio vectorial
-  Renderizado de alta calidad
-  Fuentes custom requieren instalación en sistema
-  No soporta font embedding directo en SVG

---

### 3. svgwrite

```python
import svgwrite

dwg = svgwrite.Drawing('test.svg', size=('600px', '300px'))

# Texto con fuente
text = dwg.text("Facultad de Ingeniería",
                insert=(300, 150),
                text_anchor='middle',
                font_family='Helvetica',
                font_size='48px',
                font_weight='bold')
dwg.add(text)

# Para fuentes custom, usar @font-face
dwg.defs.add(dwg.style("""
    @font-face {
        font-family: 'UCRFont';
        src: url('fonts/ucr-font.woff2') format('woff2');
    }
"""))

dwg.save()
```

**Características:**
-  No mide texto (SVG puro)
-  Soporta @font-face para web fonts
-  Requiere cálculos externos para layout
-  Embedding de fuentes posible

---

### 4. fontTools

Biblioteca especializada en manipulación de fuentes:

```python
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

font = TTFont('/path/to/font.ttf')

# Obtener métricas de fuente
units_per_em = font['head'].unitsPerEm
ascent = font['hhea'].ascent
descent = font['hhea'].descent

# Medir ancho de texto
def measure_text(font, text, size):
    glyphs = font.getGlyphSet()
    width = 0
    for char in text:
        glyph_name = font.getBestCmap().get(ord(char))
        if glyph_name:
            width += glyphs[glyph_name].width
    
    scale = size / units_per_em
    return width * scale

text = "Facultad de Ingeniería"
width = measure_text(font, text, 48)
print(f"Ancho aproximado: {width}px")
```

**Características:**
-  Control total sobre fuentes
-  Medición precisa sin renderizado
-  Análisis de métricas avanzadas
-  API compleja
-  Ideal para combinar con svgwrite

---

## Estrategia de Ajuste Dinámico

### Problema

Diferentes nombres de paradas tienen diferentes longitudes:
- "FING" (corto)
- "Facultad de Ingeniería" (medio)
- "Escuela de Arquitectura y Urbanismo" (largo)

### Soluciones

#### 1. Ajuste de Tamaño de Fuente

```python
def calculate_font_size(text, max_width, min_size=56, max_size=110):
    """
    Calcula el tamaño de fuente óptimo para que el texto
    quepa en el ancho máximo disponible.
    """
    font_size = max_size
    
    while font_size >= min_size:
        font = ImageFont.truetype('font.ttf', size=font_size)
        bbox = measure_text(text, font)
        
        if bbox.width <= max_width:
            return font_size
        
        font_size -= 2
    
    return min_size  # Usar mínimo si no cabe
```

#### 2. Multi-línea Automático

```python
def split_text_multiline(text, max_width, font):
    """
    Divide texto en múltiples líneas si es muy largo.
    """
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if measure_text(test_line, font).width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines
```

#### 3. Tracking/Kerning Ajustable

```python
def adjust_letter_spacing(text, current_width, target_width):
    """
    Calcula letter-spacing CSS para ajustar ancho exacto.
    """
    num_gaps = len(text) - 1
    extra_space = target_width - current_width
    
    if num_gaps > 0:
        letter_spacing = extra_space / num_gaps
        return letter_spacing
    
    return 0
```

---

## Font Embedding en SVG

### Estrategia 1: Base64 Embedding

```python
import base64

def embed_font_in_svg(font_path):
    with open(font_path, 'rb') as f:
        font_data = f.read()
    
    base64_font = base64.b64encode(font_data).decode('utf-8')
    
    font_face = f"""
    @font-face {{
        font-family: 'CustomFont';
        src: url(data:font/truetype;charset=utf-8;base64,{base64_font})
             format('truetype');
    }}
    """
    
    return font_face
```

**Pros:**
-  SVG autocontenido (single file)
-  No requiere archivos externos

**Contras:**
-  Archivo SVG más grande
-  Puede tener problemas en algunos viewers

---

### Estrategia 2: Path Conversion

```python
from fontTools.pens.svgPathPen import SVGPathPen

def text_to_path(font, text, size):
    """
    Convierte texto a paths SVG (outline).
    """
    glyphs = font.getGlyphSet()
    paths = []
    
    x_offset = 0
    for char in text:
        glyph_name = font.getBestCmap().get(ord(char))
        if glyph_name:
            pen = SVGPathPen(glyphs)
            glyphs[glyph_name].draw(pen)
            path = pen.getCommands()
            paths.append(path)
            x_offset += glyphs[glyph_name].width
    
    return paths
```

**Pros:**
-  Tipografía garantizada (no requiere fuentes instaladas)
-  Máxima compatibilidad

**Contras:**
-  No editable como texto
-  Archivo más complejo
-  Búsqueda/accesibilidad afectada

---

## Recomendaciones

### Para Prototipo:
1. **Usar Pillow** para medir texto
2. **Usar fuentes del sistema** (Helvetica/Arial)
3. **Generar SVG** con svgwrite usando medidas calculadas
4. **Ajuste de tamaño** con algoritmo iterativo

### Para Producción:
1. **Obtener fuentes UCR oficiales** (verificar con diseño gráfico)
2. **pycairo + fontconfig** para renderizado profesional
3. **Font embedding** en SVG para distribución
4. **Fallback a Liberation Sans** si no hay fuentes UCR

### Sistema Híbrido (Recomendado):
1. **fontTools** para análisis de métricas
2. **svgwrite** para generación SVG
3. **Base64 embedding** para fuentes custom
4. **Cairo** para export a PDF/PNG si es necesario

---

## Próximos Pasos

1.  Analizar opciones de manejo de fuentes
2.  Contactar diseño gráfico UCR para fuentes oficiales
3.  Implementar prototipo con fuentes open source
4.  Pruebas de legibilidad (56mm-110mm a 2-5m)
5.  Validar con normas INTECO

---

**Actualizado:** 28 de diciembre de 2025
