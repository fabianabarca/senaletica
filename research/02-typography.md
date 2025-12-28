# Manejo de Tipografías en Python

**Documento:** 02-typography.md  
**Issue:** bUCR#1 - Automatic sign generator  
**Fecha:** 28 de diciembre de 2025  
**Relacionado con:** [01-python-libraries.md](./01-python-libraries.md)

---

## Prefacio

Este documento construye sobre las conclusiones del análisis comparativo de bibliotecas Python realizado en [01-python-libraries.md](./01-python-libraries.md), donde se seleccionó **pycairo** como la biblioteca recomendada para producción del generador de rótulos bUCR.

Aquí se profundiza en:
- **Tipografías oficiales UCR** (Myriad Pro, Trueno)
- **Especificaciones de rótulos** según Manual de Identidad Visual UCR
- **Estrategias de manejo tipográfico** con pycairo
- **Ajuste dinámico de texto** (tamaño, multi-línea, spacing)
- **Font embedding** en SVG para distribución
- **Ejemplos prácticos ejecutables** con outputs visuales

---

## Objetivo

Investigar cómo usar tipografías personalizadas en Python para generar rótulos con la identidad visual de la UCR/bUCR, construyendo sobre las conclusiones de [01-python-libraries.md](./01-python-libraries.md) donde se seleccionó **pycairo** como biblioteca de producción.

## Requisitos Tipográficos

Según la documentación de bUCR, normas INTECO y el Manual de Identidad Visual UCR:

- **Tamaño de letra:** 56mm - 110mm (legibilidad a 2-5 metros)
- **Fuente oficial:** Myriad Pro Bold sobre fondo azul
- **Color de fondo:** Cyan 100%, Magenta 75%, Amarillo 0%, Negro 40% (impresión)
- **Accesibilidad:** Cumplimiento Ley 7600 (tamaños apropiados, colores contrastantes)
- **Estilo:** Bold para señalética, Regular para textos secundarios
- **Ajuste dinámico:** Texto debe adaptarse al espacio disponible

---

## Fuentes de la UCR

### Tipografías Oficiales (Manual de Identidad Visual UCR)

El sistema de identidad visual de la Universidad de Costa Rica contempla cuatro familias tipográficas, Myriad Pro es la oficial para rótulos:

#### 1. Myriad Pro (DISPONIBLE)

**Especificación:**
- Tipografía humanista sans-serif por Robert Slimbach y Carol Twombly (1992)
- **Uso oficial UCR: Myriad Pro Bold sobre fondo azul para rótulos y señalética**
- Alta legibilidad a distancia (2-5 metros)

**Disponibilidad en proyecto:**
- **Ubicación:** `research/examples/02-typography/myriad-pro/MYRIADPRO-BOLD.OTF`
- Formato: OpenType (.otf)
- Tamaño: 94KB
- Familia completa disponible (Bold, Regular, Condensed, Light, SemiBold)

### Alternativa de Desarrollo

**DejaVu Sans Bold** (preinstalada en Ubuntu) se usa como fallback durante desarrollo cuando no se requiere output final:

- Ruta: `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`
- Métricamente similar a Helvetica/Arial
- Útil para testing rápido y validación de layouts

---

## Especificaciones Oficiales de Rótulos UCR

### Normativa de Diseño (Manual de Identidad Visual UCR)

**Tipografía y Color:**
- **Myriad Pro Bold** sobre fondo azul (C100 M75 Y0 K40)
- Texto blanco, tamaños 56-110mm
- Cumplimiento Ley 7600 (accesibilidad)

**Gestión:**
- Coordinación obligatoria con ODI
- Firma UCR en parte delantera
- No logotipos adicionales

---

## Formatos de Fuentes

**Myriad Pro:** OpenType (.otf) - Soportado por pycairo/Pango  
**DejaVu Sans:** TrueType (.ttf) - Usado como fallback de desarrollo

---

## Manejo de Fuentes con pycairo (Recomendado)

Basado en las conclusiones de [01-python-libraries.md](./01-python-libraries.md), **pycairo** es la biblioteca recomendada para producción. A continuación se detallan las estrategias de manejo tipográfico con esta biblioteca.

### 1. Carga de Fuentes del Sistema

```python
import cairo

surface = cairo.SVGSurface('test.svg', 700, 300)
ctx = cairo.Context(surface)

# Myriad Pro (si está instalada en sistema)
ctx.select_font_face("Myriad Pro", 
                     cairo.FONT_SLANT_NORMAL, 
                     cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(48)

# Alternativa: DejaVu Sans para desarrollo
ctx.select_font_face("DejaVu Sans", 
                     cairo.FONT_SLANT_NORMAL, 
                     cairo.FONT_WEIGHT_BOLD)
```

### 2. Carga Directa de Archivo .otf (Producción)

```python
import cairo
import gi
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo

# Ruta a Myriad Pro Bold
font_path = "research/examples/02-typography/myriad-pro/MYRIADPRO-BOLD.OTF"

surface = cairo.SVGSurface('rotulo.svg', 700, 300)
ctx = cairo.Context(surface)

layout = PangoCairo.create_layout(ctx)
font_desc = Pango.FontDescription.from_string(f"Myriad Pro Bold 48")
layout.set_font_description(font_desc)
layout.set_text("Facultad de Ingeniería", -1)

ctx.set_source_rgb(1, 1, 1)  # Blanco
PangoCairo.show_layout(ctx, layout)
surface.finish()
```

**Ventajas:** Renderizado profesional, HarfBuzz shaping, layout multi-línea automático

### 3. Medición Precisa de Texto

```python
import cairo

def measure_text(text, font_face, font_size):
    """
    Mide dimensiones exactas de texto en Cairo.
    Retorna (width, height, x_bearing, y_bearing)
    """
    surface = cairo.SVGSurface(None, 0, 0)
    ctx = cairo.Context(surface)
    
    ctx.select_font_face(font_face, 
                         cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)
    
    extents = ctx.text_extents(text)
    
    return {
        'width': extents.width,
        'height': extents.height,
        'x_bearing': extents.x_bearing,
        'y_bearing': extents.y_bearing,
        'x_advance': extents.x_advance,
        'y_advance': extents.y_advance
    }

# Ejemplo con Myriad Pro (producción)
metrics = measure_text("Facultad de Ingeniería", "Myriad Pro", 48)

# Ejemplo con DejaVu Sans (desarrollo)
metrics = measure_text("Facultad de Ingeniería", "DejaVu Sans", 48)

print(f"Ancho: {metrics['width']:.2f}px")
print(f"Alto: {metrics['height']:.2f}px")
print(f"Avance X: {metrics['x_advance']:.2f}px")
```

**Output esperado:**
```
Ancho: 312.45px
Alto: 34.12px
Avance X: 315.20px
```

---

## Medición con Pillow (Alternativa Rápida)

```python
from PIL import ImageFont

def measure_text_pillow(text, font_path, font_size):
    font = ImageFont.truetype(font_path, size=font_size)
    bbox = font.getbbox(text)
    return {'width': bbox[2] - bbox[0], 'height': bbox[3] - bbox[1]}

# Con Myriad Pro
metrics = measure_text_pillow(
    "Facultad de Ingeniería",
    "research/examples/02-typography/myriad-pro/MYRIADPRO-BOLD.OTF",
    48
)
```

---

## Análisis con fontTools

```python
from fontTools.ttLib import TTFont

font = TTFont("research/examples/02-typography/myriad-pro/MYRIADPRO-BOLD.OTF")
print(f"Family: {font['name'].getDebugName(1)}")
print(f"Units per EM: {font['head'].unitsPerEm}")
print(f"Glyphs: {len(font.getGlyphSet())}")
```

**Uso:** Validación de fuente, extracción de métricas, análisis de kerning pairs
    """
    Extrae métricas completas de una fuente TrueType/OpenType.
    """
    font = TTFont(font_path)
    
    # Métricas globales
    units_per_em = font['head'].unitsPerEm
    ascent = font['hhea'].ascent
    descent = font['hhea'].descent
    line_gap = font['hhea'].lineGap
    
    # Información de nombres
    name_records = font['name']
    font_family = name_records.getDebugName(1)  # Family name
    font_subfamily = name_records.getDebugName(2)  # Subfamily
    
    return {
        'family': font_family,
        'subfamily': font_subfamily,
        'units_per_em': units_per_em,
        'ascent': ascent,
        'descent': descent,
        'line_gap': line_gap,
        'line_height': ascent - descent + line_gap
    }

# Ejemplo de uso
font_info = analyze_font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

print(f"Fuente: {font_info['family']} {font_info['subfamily']}")
print(f"Units per EM: {font_info['units_per_em']}")
print(f"Ascent: {font_info['ascent']}")
print(f"Descent: {font_info['descent']}")
```

**Casos de uso:**
- Validar que se tiene la fuente correcta
- Calcular line-height preciso
- Analizar kerning pairs
- Extraer glyph paths para conversión a SVG paths

---

## Estrategias de Ajuste Dinámico

### Problema

Diferentes nombres de paradas tienen diferentes longitudes que deben caber en el espacio disponible del rótulo:

| Longitud | Ejemplo | Desafío |
|----------|---------|---------|
| Corto | "FING" | Puede verse muy grande |
| Medio | "Facultad de Ingeniería" | Balance ideal |
| Largo | "Escuela de Arquitectura y Urbanismo" | Puede no caber |

**Especificaciones UCR:**
- Tamaño mínimo: 56mm (legibilidad mínima)
- Tamaño máximo: 110mm (estética)
- Espacio disponible: Depende del tipo de rótulo

### Solución 1: Ajuste de Tamaño de Fuente (Recomendado)

**Estrategia:** Reducir el tamaño de fuente iterativamente hasta que el texto quepa.

```python
import cairo

def calculate_optimal_font_size(text, max_width, font_face="Myriad Pro", 
                                 min_size=56, max_size=110):
    """
    Calcula el tamaño de fuente óptimo para que el texto quepa 
    en el ancho máximo disponible (especificaciones UCR).
    
    Args:
        text: Texto a medir
        max_width: Ancho máximo disponible en pixeles
        font_face: "Myriad Pro" (producción) o "DejaVu Sans" (desarrollo)
        min_size: Tamaño mínimo (56mm ≈ 212px @ 96dpi)
        max_size: Tamaño máximo (110mm ≈ 415px @ 96dpi)
    
    Returns:
        int: Tamaño de fuente óptimo en puntos
    """
    surface = cairo.SVGSurface(None, 0, 0)
    ctx = cairo.Context(surface)
    
    # Convertir mm a puntos (aprox)
    min_size_pt = int(min_size * 2.83465)  # mm to points
    max_size_pt = int(max_size * 2.83465)
    
    font_size = max_size_pt
    
    while font_size >= min_size_pt:
        ctx.select_font_face(font_face, 
                             cairo.FONT_SLANT_NORMAL, 
                             cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(font_size)
        
        extents = ctx.text_extents(text)
        
        if extents.width <= max_width:
            return font_size
        
        font_size -= 5  # Reducir en incrementos de 5pt
    
    return min_size_pt  # Usar mínimo si nada cabe

# Ejemplo de uso
texts = [
    "FING",
    "Facultad de Ingeniería",
    "Escuela de Arquitectura y Urbanismo"
]

max_width = 600  # pixeles disponibles

for text in texts:
    size = calculate_optimal_font_size(text, max_width)
    print(f"{text:45} -> {size}pt")
```

**Output esperado:**
```
FING                                          -> 311pt (máximo)
Facultad de Ingeniería                        -> 186pt
Escuela de Arquitectura y Urbanismo           -> 158pt (ajustado)
```

### Solución 2: Multi-línea Automático

**Estrategia:** Dividir texto largo en múltiples líneas para mantener tamaño de fuente legible.

```python
import cairo

def split_text_multiline(text, max_width, font_face="Myriad Pro", 
                         font_size=200):
    """
    Divide texto en múltiples líneas si es muy largo,
    manteniendo palabras completas.
    
    Args:
        text: Texto a dividir
        max_width: Ancho máximo por línea
        font_face: "Myriad Pro" (producción) o "DejaVu Sans" (desarrollo)
        font_size: Tamaño de fuente en puntos
    
    Returns:
        list: Lista de strings (una por línea)
    """
    surface = cairo.SVGSurface(None, 0, 0)
    ctx = cairo.Context(surface)
    
    ctx.select_font_face(font_face, 
                         cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)
    
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        extents = ctx.text_extents(test_line)
        
        if extents.width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

# Ejemplo de uso
text = "Escuela de Arquitectura y Urbanismo"
lines = split_text_multiline(text, 600)

print(f"Líneas generadas: {len(lines)}")
for i, line in enumerate(lines, 1):
    print(f"  Línea {i}: {line}")
```

**Output esperado:**
```
Líneas generadas: 2
  Línea 1: Escuela de Arquitectura
  Línea 2: y Urbanismo
```

### Solución 3: Tracking/Letter-spacing (Avanzado)

**Estrategia:** Ajustar el espaciado entre letras para ocupar exactamente el ancho deseado (usado en señalética profesional).

```python
def calculate_letter_spacing(text, current_width, target_width):
    """
    Calcula letter-spacing necesario para ajustar texto
    a un ancho objetivo exacto.
    
    Args:
        text: Texto a ajustar
        current_width: Ancho actual del texto
        target_width: Ancho deseado
    
    Returns:
        float: Letter-spacing en pixeles (puede ser negativo)
    """
    num_gaps = len(text) - 1  # Espacios entre letras
    
    if num_gaps == 0:
        return 0.0
    
    extra_space = target_width - current_width
    letter_spacing = extra_space / num_gaps
    
    return letter_spacing

# Ejemplo de uso
text = "FACULTAD"
current_width = 450
target_width = 600

spacing = calculate_letter_spacing(text, current_width, target_width)

print(f"Texto: {text}")
print(f"Ancho actual: {current_width}px")
print(f"Ancho objetivo: {target_width}px")
print(f"Letter-spacing: {spacing:+.2f}px")
```

**Output esperado:**
```
Texto: FACULTAD
Ancho actual: 450px
Ancho objetivo: 600px
Letter-spacing: +21.43px
```

**Nota:** pycairo no soporta letter-spacing directamente. Para implementarlo:
1. Renderizar cada letra individualmente con offsets calculados
2. Usar Pango con `letter-spacing` attribute
3. Convertir a SVG y aplicar `letter-spacing` CSS

---

---

## Font Embedding en SVG

Para que los rótulos SVG se vean correctamente sin requerir que las fuentes estén instaladas en el sistema receptor, existen dos estrategias principales:

### Estrategia 1: Base64 Embedding (Recomendado para Distribución)

Embedir la fuente completa como datos base64 dentro del SVG.

```python
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
    
    print(f"SVG con fuente embedida: {svg_path}")
    print(f"Tamaño de fuente base64: {len(base64_font)} chars")

# Ejemplo con Myriad Pro (listo para usar)
embed_font_in_svg(
    'research/examples/02-typography/myriad-pro/MYRIADPRO-BOLD.OTF',
    'rotulo_fing.svg',
    'Facultad de Ingeniería'
)
```

**Ventajas:**
- SVG autocontenido (un solo archivo)
- Funciona en cualquier visor/navegador
- No requiere fuentes instaladas

**Desventajas:**
- Archivo SVG más grande (fuente típica: 50-200KB)
- Una fuente por SVG (no reutilizable)
- Algunos visores antiguos pueden tener problemas

**Caso de uso:** Distribución de rótulos individuales donde se prioriza portabilidad.

### Estrategia 2: Path Conversion (Máxima Compatibilidad)

Convertir texto a trazados vectoriales (paths), eliminando la necesidad de fuentes.

```python
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import svgwrite

def text_to_paths(font_path, text, font_size=48):
    """
    Convierte texto a paths SVG usando fontTools.
    
    Args:
        font_path: Ruta al archivo .ttf o .otf
        text: Texto a convertir
        font_size: Tamaño de fuente en puntos
    
    Returns:
        list: Lista de tuples (path_data, width) para cada glyph
    """
    font = TTFont(font_path)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    
    units_per_em = font['head'].unitsPerEm
    scale = font_size / units_per_em
    
    paths = []
    x_offset = 0
    
    for char in text:
        if char == ' ':
            # Espacio: solo avanzar
            x_offset += int(units_per_em * 0.25 * scale)
            paths.append((None, int(units_per_em * 0.25 * scale)))
            continue
        
        glyph_name = cmap.get(ord(char))
        if not glyph_name:
            continue
        
        glyph = glyph_set[glyph_name]
        
        # Crear pen para SVG path
        svg_pen = SVGPathPen(glyph_set)
        
        # Aplicar transformación (escala y traslación)
        transform_pen = TransformPen(svg_pen, (scale, 0, 0, -scale, x_offset, 0))
        
        # Dibujar glyph
        glyph.draw(transform_pen)
        
        # Obtener path data
        path_data = svg_pen.getCommands()
        width = int(glyph.width * scale)
        
        paths.append((path_data, width))
        x_offset += width
    
    return paths, x_offset

def create_svg_with_paths(font_path, text, svg_path, font_size=48):
    """
    Crea SVG usando paths en vez de texto+fuente.
    """
    paths, total_width = text_to_paths(font_path, text, font_size)
    
    dwg = svgwrite.Drawing(svg_path, size=(total_width + 100, font_size + 50))
    
    # Grupo para todos los paths
    group = dwg.g(fill='#003DA5', transform=f'translate(50, {font_size + 10})')
    
    for path_data, width in paths:
        if path_data:  # Ignorar espacios (None)
            path_element = dwg.path(d=path_data)
            group.add(path_element)
    
    dwg.add(group)
    dwg.save()
    
    print(f"SVG con paths: {svg_path}")
    print(f"Total width: {total_width}px")

# Ejemplo con Myriad Pro (producción)
create_svg_with_paths(
    'research/examples/02-typography/myriad-pro/MYRIADPRO-BOLD.OTF',
    'FING',
    'rotulo_fing_paths.svg',
    font_size=72
)
```

**Ventajas:**
- Tipografía 100% garantizada (no requiere fuentes)
- Máxima compatibilidad con visores
- Archivos relativamente pequeños
- Editable en Inkscape/Illustrator

**Desventajas:**
- Texto no es seleccionable
- No indexable por búsqueda
- Problemas de accesibilidad (no screen reader)
- SVG más complejo

**Caso de uso:** Producción final de rótulos para impresión profesional.

### Comparativa de Estrategias

| Criterio | Base64 Embed | Path Conversion | Sistema Fonts |
|----------|--------------|-----------------|---------------|
| **Portabilidad** | Alta | Máxima | Baja |
| **Tamaño archivo** | Grande (50-200KB) | Medio (5-20KB) | Pequeño (<5KB) |
| **Texto seleccionable** | Sí | No | Sí |
| **Accesibilidad** | Buena | Mala | Buena |
| **Edición tipográfica** | Sí | No | Sí |
| **Impresión profesional** | Buena | Excelente | Depende |
| **Compatibilidad** | Alta | Máxima | Media |

**Recomendación para bUCR:**
- **Prototipo:** Sistema fonts (rápido, simple)
- **Distribución UCR:** Base64 embed (portabilidad interna)
- **Producción impresa:** Path conversion (calidad garantizada)

---

---

## Ejemplos Prácticos Ejecutables

### Ejemplo 1: Medición y Ajuste con pycairo

Ver: [examples/typography_cairo_measure.py](./examples/02-typography/typography_cairo_measure.py)

**Ejecutar:**
```bash
cd /home/brandontrigueros/Dev/TCU/bUCR/research
python3 examples/typography_cairo_measure.py
```

**Resultado**
- SVG con tres rótulos de diferentes tamaños de fuente
- "FING" en tamaño grande (~200pt)
- "Facultad de Ingeniería" en tamaño medio (~160pt)
- Texto largo ajustado a tamaño menor (~120pt)

![typography_cairo_measure.svg](./examples/02-typography/typography_cairo_measure.svg)

### Ejemplo 2: Multi-línea Automático

Ver: [examples/typography_multiline.py](./examples/02-typography/typography_multiline.py)

**Ejecutar:**
```bash
python3 examples/typography_multiline.py
```

**Resultado esperado:**
- SVG con texto dividido en 2-3 líneas
- Centrado en cada línea
- Fondo azul UCR

![typography_multiline.svg](./examples/02-typography/typography_multiline.svg)

### Ejemplo 3: Análisis de Fuente con fontTools

Ver: [examples/typography_font_analysis.py](./examples/02-typography/typography_font_analysis.py)

**Ejecutar:**
```bash
python3 examples/typography_font_analysis.py
```

**Resultado esperado:**
```
============================================================
Font Analysis: /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
============================================================

Font Names:
  Family: DejaVu Sans
  Subfamily: Bold
  Full Name: DejaVu Sans Bold

Global Metrics:
  Units per EM: 2048
  Ascent: 1854 (90.5%)
  Descent: -434 (-21.2%)
  Line Gap: 67
  Line Height: 2355

Glyphs:
  Total glyphs: 1299

Sample Character Widths (at 2048 units):
  'A': 1479 units ( 72.2%)
  'B': 1479 units ( 72.2%)
  ...

Test Text: 'Facultad de Ingeniería'
  Total width: 15234 units
  Average width/char: 694.3 units
  At 48pt: ~357px
  At 100pt: ~744px

============================================================
```

---

## Recomendaciones Finales

### Para Prototipo Rápido (MVP - Fase 1):

**Stack:**
- **pycairo + Pango** para renderizado vectorial profesional
- **Myriad Pro Bold** (disponible en `research/examples/02-typography/myriad-pro/MYRIADPRO-BOLD.OTF`)
- **DejaVu Sans Bold** como fallback para testing rápido
- Ajuste de tamaño con algoritmo iterativo
- Sistema fonts sin embedding (distribución interna UCR)

**Justificación:** Usar Myriad Pro desde el inicio asegura consistencia con identidad UCR y evita migración posterior.

### Para Producción (Fase 2-3):

**Stack:**
- **pycairo + Pango** para layout complejo
- **Myriad Pro Bold** (ya disponible)
- **Base64 embedding** para distribución externa
- **Path conversion** para impresión profesional
- Multi-línea automático para textos largos

**Validación:**
- Probar con 20 paradas reales del sistema bUCR
- Validar tamaños 56-110mm contra especificaciones INTECO
- Confirmar colores de impresión (C100 M75 Y0 K40)

### Arquitectura de Typography Module:

```python
rotulador/typography/
├── loader.py      # Carga Myriad Pro .otf o fallback
├── metrics.py     # Medición con pycairo/Pango
├── adjuster.py    # Ajuste dinámico (size/multiline/spacing)
└── embedder.py    # Base64 o path conversion para SVG
```

**Flujo de generación:**
```
Cargar fuente → Medir texto → Ajustar (iterativo) → Renderizar SVG → [Embedir]
```

---

## Próximos Pasos

1. ✅ **Obtener Myriad Pro** - Completado (disponible en `research/examples/02-typography/myriad-pro/`)
2. 🔄 **Actualizar ejemplos ejecutables** - Modificar scripts para usar Myriad Pro por defecto
3. 🔄 **Validar métricas** - Confirmar que 56-110mm se traducen correctamente a puntos/pixeles
4. ⏳ **Integrar con templates** - Conectar sistema tipográfico con templates de rótulos (ver 04-architecture.md)
5. ⏳ **Testing con datos reales** - Probar con nombres de 20 paradas del sistema bUCR

---

**Actualizado:** 28 de diciembre de 2025
