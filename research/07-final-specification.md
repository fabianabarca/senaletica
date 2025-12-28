# Especificación Final: Sistema Generador Automático de Rótulos bUCR

**Proyecto:** bUCR - Sistema de señalética del bus interno UCR  
**Issue:** #1 - Automatic sign generator  
**Investigador:** Brandon Trigueros Lara  
**Fecha:** 28 de diciembre de 2025  
**Horas invertidas:** 8h (investigación y diseño)  

---

## Resumen Ejecutivo

Este documento presenta la especificación técnica para un sistema automatizado de generación de rótulos de paradas de autobús, resultado de investigación exhaustiva sobre:

1.  Bibliotecas Python para generación gráfica
2.  Manejo de tipografías personalizadas
3.  Evaluación LaTeX vs Python
4.  Casos de referencia (MBTA, TfL, BART)
5.  Estrategias de escalabilidad
6.  Arquitectura propuesta

**Recomendación:** Implementar paquete Python `rotulador` con arquitectura modular que escala desde 20 paradas UCR hasta potencialmente miles a nivel nacional.

---

## 1. Problema a Resolver

### Situación Actual

**Manual e inescalable:**
- Diseñadores crean cada rótulo individualmente en Illustrator/Inkscape
- 20 paradas UCR: manejable
- Miles de paradas nacionales: **imposible**

### Visión

**Automatizado y escalable:**
```python
import rotulador

sign = rotulador.create("stop_back", "Facultad de Ingeniería")
sign.export("fing.svg")
```

- **1 línea** genera rótulo profesional
- Cumple especificaciones de diseño UCR
- Listo para producción (SVG/PDF/PNG)
- Escalable a nivel nacional

---

## 2. Decisiones Técnicas Clave

### 2.1 Stack Tecnológico: Python + Cairo

**Seleccionado:** `pycairo` para producción, `svgwrite` para prototipado

| Criterio | Ganador | Razón |
|----------|---------|-------|
| Formato vectorial |  SVG/PDF | Print-quality |
| Tipografía custom |  Cairo | HarfBuzz integration |
| Performance |  Cairo | Nativo, ~100-200ms/sign |
| Mantenibilidad |  Python | Stack conocido |
| Escalabilidad |  Cairo | Batch generation eficiente |

**Descartados:**
-  LaTeX/TikZ: Overkill, performance pobre, curva de aprendizaje alta
-  Pillow: Raster only, no es vectorial
-  ReportLab: Enfocado en PDF, no SVG nativo

### 2.2 Arquitectura: Modular y Extensible

```
rotulador/
├── core.py              # API principal (Rotulo, Sign)
├── types.py             # Enums y dataclasses
├── renderers/           # Backends (Cairo, SVG)
├── templates/           # Templates por tipo
├── typography/          # Font loading y medición
├── styles/              # Colores, dimensiones, config
└── utils/               # Validación, helpers
```

**Patrón de diseño:**
- Strategy Pattern para renderers (Cairo, alternativas futuras)
- Template Method para tipos de rótulos
- Factory Pattern para creación de signs
- Configuration over code

### 2.3 Escalabilidad: Fases Progresivas

| Fase | Paradas | Herramienta | Desarrollo |
|------|---------|-------------|------------|
| **1: UCR** | 20 | CLI + Git | ~40h |
| **2: Regional** | 30-200 | CLI + Config files | +20h |
| **3: Nacional** | 200+ | Django Platform + DB | +300h |

**Decisión:** Comenzar con Fase 1, arquitectura lista para Fase 3.

---

## 3. Especificación del API

### 3.1 API Básico (Requerimiento del Issue)

```python
import rotulador

rotulo = rotulador.Rotulo()

parada_fing = rotulo.create(
    type="stop_back",
    stop_name="Facultad de Ingeniería",
)

parada_fing.export("parada_fing.svg")
```

### 3.2 API Avanzado (Extensiones)

```python
# Con configuración custom
from rotulador.styles.config import RotuladorConfig

config = RotuladorConfig(
    font_path="/path/to/ucr-font.ttf",
    ucr_blue="#002B5C"
)

rotulo = rotulador.Rotulo(config=config)

# Con elementos adicionales
sign = rotulo.create(
    type="stop_back",
    stop_name="Facultad de Ingeniería",
    route_symbols=["A", "B"],
    slogan="el b es el bus de la U"
)

# Múltiples formatos
sign.export("fing.svg")
sign.export("fing.pdf")
sign.export("fing.png", dpi=300)

# Batch generation
paradas = ["FING", "Ciencias", "Derecho", ...]
for nombre in paradas:
    sign = rotulo.create("stop_back", nombre)
    sign.export(f"output/{nombre}.svg")
```

### 3.3 CLI Interface

```bash
# Instalación
pip install bucr-rotulador

# Uso básico
rotulador generate --stop "Facultad de Ingeniería" --type stop_back

# Batch desde CSV
rotulador batch --input stops.csv --output output/

# Configuración
rotulador config --font /path/to/font.ttf
rotulador config --color-blue "#002B5C"

# Preview (servidor local)
rotulador preview --serve --port 8000
```

---

## 4. Sistema de Templates

### 4.1 Tipos de Rótulos Soportados

#### Tipo 1: `stop_back` - Respaldo Trasero Horizontal

**Especificaciones:**
- Ancho: Variable (600-1200mm)
- Alto: 300mm estándar
- Logo "b": 60mm diámetro
- Texto: 1-2 líneas, centrado
- Font size: 56-110mm (según longitud nombre)

**Elementos:**
- Logo circular "b" (izquierda o centro)
- Nombre de parada (tipografía UCR)
- Símbolos de rutas (opcional, independientes)
- Slogan (opcional, inferior)

#### Tipo 2: `stop_post` - Poste Vertical

**Especificaciones:**
- Ancho: 60mm (igual que logo)
- Alto: Variable (logo + placa nombre)
- Logo "b": 60mm diámetro (superior)
- Placa nombre: 60mm ancho, 30mm o 45mm alto

**Elementos:**
- Logo circular "b" (superior)
- Placa con nombre (inferior, separada)

#### Tipo 3: `route_symbol` - Símbolo de Ruta

**Especificaciones:**
- Tamaño: Pequeño, modular
- Forma: Rectángulo con letra (A, B, C...)
- Colores: Por ruta

#### Tipo 4: `diagram` - Diagrama de Rutas

**Especificaciones:**
- Mapa simplificado de rutas
- Símbolos + conexiones
- Paradas destacadas

### 4.2 Ajuste Dinámico de Texto

**Algoritmo:**

```python
def calculate_font_size(text: str, max_width: float) -> float:
    """
    Ajusta font size para que texto quepa en espacio.
    
    Rules:
    - Máximo permitido: 110mm (norma INTECO)
    - Mínimo permitido: 56mm (legibilidad 2-5m)
    - Preferir tamaño grande (mejor legibilidad)
    """
    font_size = 110  # Empezar con máximo
    
    while font_size >= 56:
        measured_width = measure_text(text, font_size)
        
        if measured_width <= max_width:
            return font_size
        
        font_size -= 2  # Decrementar
    
    # Si no cabe, dividir en 2 líneas
    return 56  # Mínimo legal
```

**Multi-línea automático:**
- "Facultad de Ingeniería" → 1 línea (OK)
- "Escuela de Arquitectura y Urbanismo" → 2 líneas (auto-split)

---

## 5. Manejo de Tipografías

### 5.1 Fuentes UCR Oficiales

**Por investigar con diseño gráfico UCR:**
- ¿Cuál es la tipografía oficial?
- ¿Dónde obtener archivos .ttf/.otf?
- ¿Licencia permite embedding?

**Fallback (mientras):**
- Liberation Sans Bold (métrica-compatible con Helvetica)
- Open Sans (open source, alta legibilidad)
- Roboto (moderna, similar a Helvetica)

### 5.2 Font Embedding en SVG

**Estrategia 1:** Base64 embedding (archivo único)
```svg
<defs>
  <style>
    @font-face {
      font-family: 'UCRFont';
      src: url(data:font/truetype;base64,AAAAB3NzaC1yc2E...)
           format('truetype');
    }
  </style>
</defs>
```

**Estrategia 2:** Path conversion (máxima compatibilidad)
- Convertir texto a paths SVG
- No requiere fuentes instaladas
- Máxima portabilidad

### 5.3 Medición Precisa

**Herramientas:**
- `fontTools` para análisis de métricas
- `pycairo.Context.text_extents()` para medición en renderizado
- Custom adjuster para casos edge

---

## 6. Casos de Referencia y Lecciones

### 6.1 MBTA (Boston) - SignMaker

**Lecciones aplicadas:**
-  Separar design standards de implementation
-  GTFS como source of truth
-  Template-based generation
-  Version control de outputs

### 6.2 BART (San Francisco) - Standards Manual

**Lecciones aplicadas:**
-  Web-first documentation (MkDocs ya existe)
-  Asset library (SVG components)
-  Modern, git-based approach

### 6.3 TfL (London) - Johnston System

**Lecciones aplicadas:**
-  Documentación exhaustiva
-  Quality control stricto
-  Balance: no overkill para 20 paradas

### 6.4 NYC MTA - Anti-patrón

**Lecciones (qué NO hacer):**
-  Evitar producción descentralizada
-  No permitir inconsistencia visual
-  Centralizar desde el inicio

---

## 7. Plan de Implementación

### Fase 1: MVP (2-3 horas)

**Entregables:**
- [x] Estructura de paquete Python
- [ ] Clase `Rotulo` funcional
- [ ] Template `stop_back` básico
- [ ] Renderer SVG (svgwrite)
- [ ] CLI básico

**Resultado:** Generar 1 rótulo simple funcional

### Fase 2: Producción (3-4 horas)

**Entregables:**
- [ ] CairoRenderer completo
- [ ] Typography system robusto
- [ ] Template `stop_post`
- [ ] Ajuste dinámico de texto
- [ ] Font embedding

**Resultado:** Generar todos los rótulos UCR (20) con calidad profesional

### Fase 3: Pulido (2-3 horas)

**Entregables:**
- [ ] Tests comprehensivos
- [ ] Documentación (Sphinx)
- [ ] CLI completo (batch, preview)
- [ ] Ejemplos de uso
- [ ] PyPI package

**Resultado:** Paquete listo para distribución

### Total Estimado: 8-10 horas implementación

---

## 8. Integración con Ecosistema bUCR

### 8.1 GTFS Integration

```python
import gtfs_kit

# Cargar datos GTFS
feed = gtfs_kit.read_feed("data/gtfs.zip")

# Generar rótulo por cada stop
for stop in feed.stops:
    sign = rotulador.create(
        "stop_back",
        stop_name=stop.stop_name,
        stop_id=stop.stop_id
    )
    sign.export(f"output/{stop.stop_id}.svg")
```

### 8.2 Web Integration (Futuro)

```python
# Django view
from rotulador import Rotulo

def generate_sign_view(request):
    stop_name = request.POST.get('stop_name')
    
    rotulo = Rotulo()
    sign = rotulo.create("stop_back", stop_name)
    
    # Save to storage
    sign.export(f"media/signs/{stop_name}.svg")
    
    return JsonResponse({'url': f'/media/signs/{stop_name}.svg'})
```

### 8.3 MkDocs Documentation

```markdown
<!-- docs/rotulador.md -->
# Sistema de Generación de Rótulos

## Instalación

\`\`\`bash
pip install bucr-rotulador
\`\`\`

## Uso

\`\`\`python
import rotulador
sign = rotulador.create("stop_back", "FING")
sign.export("fing.svg")
\`\`\`
```

---

## 9. Validación y Quality Control

### 9.1 Automated Validation

```python
def validate_sign_spec(spec: SignSpec) -> List[str]:
    """Valida que el rótulo cumpla normas."""
    errors = []
    
    # INTECO 5.1.1.2: Tamaño de letra
    if not (56 <= spec.font_size <= 110):
        errors.append(f"Font size {spec.font_size}mm fuera de rango 56-110mm")
    
    # Contraste
    if not has_sufficient_contrast(spec.text_color, spec.background_color):
        errors.append("Contraste insuficiente (WCAG AA)")
    
    # Dimensiones logo
    if spec.logo_size != 60:
        errors.append("Logo debe ser 60mm diámetro")
    
    return errors
```

### 9.2 Visual Comparison

```bash
# Comparar con diseño manual existente
rotulador compare \
    docs/assets/logos/fing.svg \
    output/fing_generated.svg \
    --output diff.png
```

### 9.3 Approval Workflow (Fase 3)

```
Draft → Designer Review → Approved → Production → Installed
```

---

## 10. Costos y ROI

### 10.1 Inversión Inicial

| Actividad | Horas | Costo (@$25/h) |
|-----------|-------|----------------|
| Investigación (este doc) | 8h | $200 |
| Implementación MVP | 8h | $200 |
| Testing y pulido | 4h | $100 |
| Documentación | 4h | $100 |
| **Total Fase 1** | **24h** | **$600** |

### 10.2 Ahorros

**Situación actual (manual):**
- Diseñar 1 rótulo: 1-2h
- 20 rótulos UCR: 20-40h (~$500-1000)
- Re-diseño si cambian specs: otros 20-40h

**Con sistema automatizado:**
- Generar 20 rótulos: 5 minutos
- Re-generar todos: 5 minutos
- Escalar a 1000 rótulos: 30 minutos

**ROI:** Se paga en la primera iteración

### 10.3 Valor a Largo Plazo

**Escenario nacional:**
- 3000 paradas × 1h manual = 3000h ($75,000)
- Con sistema: 1h batch generation ($25)
- **Ahorro:** $74,975

---

## 11. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Fuentes UCR no disponibles | Media | Alto | Usar Liberation Sans (compatible) |
| Cairo difícil de instalar | Baja | Medio | Documentar setup, Docker image |
| Specs de diseño cambian | Alta | Medio | Templates parametrizados, fácil ajustar |
| Escala más rápido de esperado | Media | Bajo | Arquitectura ya lista para DB |
| No cumple calidad profesional | Baja | Alto | Validación exhaustiva con diseñadores |

---

## 12. Próximos Pasos

### Inmediatos (Post-investigación)

1. **Validar con supervisor TCU**
   - [ ] Presentar este documento
   - [ ] Obtener feedback
   - [ ] Confirmar si procede implementación

2. **Coordinación con diseño gráfico UCR**
   - [ ] Solicitar fuentes oficiales
   - [ ] Validar especificaciones de color
   - [ ] Confirmar dimensiones exactas

3. **Setup de desarrollo**
   - [ ] Crear repositorio `rotulador`
   - [ ] Configurar entorno Python
   - [ ] Instalar dependencias (Cairo, etc.)

### Fase Implementación (Si aprobado)

4. **MVP (Week 1)**
   - [ ] Estructura de paquete
   - [ ] Template básico
   - [ ] Primera generación exitosa

5. **Producción (Week 2)**
   - [ ] Templates completos
   - [ ] Typography system
   - [ ] 20 rótulos UCR generados

6. **Release (Week 3)**
   - [ ] Testing
   - [ ] Documentación
   - [ ] PyPI package

---

## 13. Conclusiones

###  Factibilidad: Alta

El sistema propuesto es:
- **Técnicamente viable:** Tecnologías maduras y probadas
- **Económicamente justificable:** ROI positivo desde primera iteración
- **Escalable:** De 20 a miles de paradas sin rediseño
- **Mantenible:** Python puro, stack conocido

###  Recomendación: Proceder con Implementación

**Justificaciones:**

1. **Necesidad real:** Diseño manual no escala
2. **Tecnología apropiada:** Python + Cairo es el sweet spot
3. **Casos de referencia:** MBTA, BART demuestran viabilidad
4. **Arquitectura sólida:** Diseño modular y extensible
5. **Plan claro:** Roadmap de 3 fases bien definido

###  Métricas de Éxito

**KPIs para MVP:**
-  Genera rótulo que cumple specs visuales
-  Output SVG valida correctamente
-  Font size en rango 56-110mm
-  Contraste adecuado (WCAG AA)
-  Diseñadores aprueban calidad

**KPIs para Producción:**
-  20 rótulos UCR generados correctamente
-  Tiempo de generación < 1 minuto para batch
-  Al menos 1 rótulo impreso e instalado
-  Zero defectos reportados post-instalación

---

## 14. Referencias y Recursos

### Documentación Generada (Esta Investigación)

1. [README.md](README.md) - Overview del proyecto
2. [01-python-libraries.md](01-python-libraries.md) - Comparativa de bibliotecas
3. [02-typography.md](02-typography.md) - Manejo de tipografías
4. [03-latex-evaluation.md](03-latex-evaluation.md) - LaTeX vs Python
5. [04-architecture.md](04-architecture.md) - Arquitectura propuesta
6. [05-reference-cases.md](05-reference-cases.md) - Casos MBTA, BART, TfL
7. [06-scalability.md](06-scalability.md) - Templates y escalabilidad
8. [07-final-specification.md](07-final-specification.md) - Este documento

### Referencias Externas

**Standards y Normas:**
- INTECO 5.1.1.2 - Tamaño para lectura visual
- WCAG 2.1 AA - Contraste de color
- GTFS Specification - Transit data format

**Casos de Estudio:**
- MBTA Standards & Guidelines: https://www.mbta.com/design-standards-guidelines
- BART Standards Manual: https://www.standards.bartsignage.com/
- TfL Sign Design: https://tfl.gov.uk/corporate/publications-and-reports/signs

**Herramientas Técnicas:**
- pycairo: https://pycairo.readthedocs.io/
- fontTools: https://fonttools.readthedocs.io/
- svgwrite: https://svgwrite.readthedocs.io/

---

## Apéndices

### A. Glosario

- **GTFS:** General Transit Feed Specification - formato estándar para datos de transporte
- **SVG:** Scalable Vector Graphics - formato vectorial
- **TRL:** Technology Readiness Level - nivel de madurez tecnológica
- **ROI:** Return on Investment - retorno de inversión
- **MVP:** Minimum Viable Product - producto mínimo viable
- **CLI:** Command Line Interface - interfaz de línea de comandos
- **API:** Application Programming Interface - interfaz de programación

### B. Acrónimos de Agencias

- **MBTA:** Massachusetts Bay Transportation Authority (Boston)
- **TfL:** Transport for London (Londres)
- **BART:** Bay Area Rapid Transit (San Francisco)
- **MTA:** Metropolitan Transportation Authority (New York)
- **UCR:** Universidad de Costa Rica
- **MOPT:** Ministerio de Obras Públicas y Transportes (Costa Rica)

### C. Comandos Rápidos

```bash
# Setup
git clone https://github.com/simovilab/rotulador
cd rotulador
pip install -e .

# Generar un rótulo
rotulador generate --stop "FING" --type stop_back

# Batch desde CSV
rotulador batch --input data/ucr_stops.csv

# Preview local
rotulador preview --serve

# Tests
pytest tests/

# Build package
python setup.py sdist bdist_wheel
```

---

## Metadata del Documento

**Versión:** 1.0  
**Fecha:** 28 de diciembre de 2025  
**Autor:** Brandon Trigueros Lara  
**Proyecto:** TCU-450 SIMOVI  
**Issue:** bUCR#1 - Automatic sign generator  
**Horas:** 8h (investigación y especificación)  
**Estado:**  COMPLETO - Listo para revisión  

---

**Firma:**

Brandon Trigueros Lara  
Estudiante TCU - Laboratorio SIMOVI  
Universidad de Costa Rica  
brandon.trigueros@ucr.ac.cr

---

**Próxima acción:** Presentar a supervisor para aprobación de fase de implementación.
