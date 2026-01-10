# Plan de Desarrollo Fase 2: Sistema de Señalética Profesional

**Objetivo:** Evolucionar el paquete `rotulador` de un MVP funcional a un sistema de producción capaz de generar señalética real, estandarizada y lista para impresión, cumpliendo con normativas UCR e INTECO.

---

## ⚠️ PRE-REQUISITO: Consolidación de Ramas Existentes

**Antes de iniciar Fase 2, es IMPERATIVO consolidar el contenido de las ramas `rotulos`, `gh-pages` y `prueba-jose` para evitar duplicación de esfuerzos y aprovechar especificaciones técnicas existentes.**

### Información Nueva Identificada

Tras análisis exhaustivo de las ramas existentes, se encontró contenido crítico no presente en el research actual:

#### Rama `rotulos` (Más Relevante)
- **Assets gráficos completos:** 40+ archivos SVG/PNG de logos, símbolos y plantillas (b_azul.svg, parada_vertical.svg, etc.)
- **Especificaciones técnicas detalladas:**
  - Paleta de colores oficial: Celeste UCR (#00C0F3), Azul UCR (#005DA4), Verde UCR (#6DC067)
  - Dimensiones exactas: Logo "b" 45-60cm diámetro, texto 300-400pt (10-14cm)
  - Dos tipos de rótulos: Vertical (poste) y Horizontal (respaldo)
  - Tipografía: Myriad Pro Bold, tamaños 56-110mm (INTECO compliant)
- **Referencias normativas:** PDFs oficiales (identidad_visual_ucr_3.1.pdf, norma_INTE_W5_2021.pdf)
- **Documentación técnica:** elementos.md, infraestructura.md, respaldo.md con especificaciones completas

#### Rama `gh-pages`
- Sitio web generado con MkDocs (despliegue automático)
- Documentación pública del proyecto

#### Rama `prueba-jose`
- Contenido inicial similar a `rotulos`, sin actualizaciones significativas

### Plan de Consolidación

1. **Merge de `rotulos` a `main`:**
   - Integrar assets gráficos (SVG/PNG) al directorio `docs/assets/`
   - Actualizar documentación con especificaciones técnicas de elementos.md, infraestructura.md
   - Resolver conflictos con archivos existentes (ej: colores en research/)

2. **Actualización del Research:**
   - Incorporar paleta de colores oficial y dimensiones exactas
   - Actualizar especificaciones de plantillas con medidas reales (45-60cm)
   - Integrar referencias normativas (PDFs INTECO, identidad visual)

3. **Limpieza de Ramas:**
   - Archivar `prueba-jose` (sin valor adicional)
   - Mantener `gh-pages` para despliegues futuros

### Impacto en Fase 2
Esta consolidación permitirá:
- **Precisión técnica:** Usar dimensiones y colores oficiales en lugar de aproximaciones
- **Assets listos:** SVG de plantillas para implementar templates complejos
- **Cumplimiento normativo:** Asegurar conformidad con INTECO y UCR desde el inicio

**Tiempo estimado:** 4-6 horas para merge y actualización de research.

---

## 1. Migración a Unidades Físicas (Milímetros)

El sistema actual utiliza píxeles arbitrarios. Para impresión profesional, es imperativo trabajar con dimensiones físicas reales.

### Tareas Técnicas
- [ ] **Sistema de Unidades:** Implementar conversión automática `mm -> pt` (Cairo usa puntos, 1mm ≈ 2.83pt).
- [ ] **Refactor de Dimensions:** Migrar `src/rotulador/styles/dimensions.py` para definir constantes en milímetros.
  - Ejemplo: `CANVAS_WIDTH = 700` -> `CANVAS_WIDTH_MM = 450` (o la medida real del rótulo).
- [ ] **Soporte DPI:** Permitir configurar la resolución de salida (72 dpi para web, 300 dpi para impresión).

## 2. Motor de Layout Avanzado (Grid & Typography)

Para soportar diseños complejos (como el poste vertical con horarios), necesitamos abandonar las coordenadas absolutas ("mágicas") y usar un sistema de grilla y flujo de texto.

### Tareas Técnicas
- [ ] **Clase `LayoutEngine`:**
  - Sistema de columnas y filas (Grid System).
  - Márgenes y padding configurables en mm.
- [ ] **Manejo de Texto Avanzado:**
  - **Auto-wrap:** Partir texto en múltiples líneas inteligentemente si excede el ancho.
  - **Line-height (Leading):** Control preciso del interlineado.
  - **Kerning/Tracking:** Ajuste de espacio entre letras para legibilidad (Ley 7600).
- [ ] **Alineación Vertical:** Centrado real basado en métricas de fuente (Ascender/Descender), no solo bounding box.

## 3. Integración de Datos de Rutas (`routes.md`)

La señalética real requiere información dinámica (rutas, horarios, destinos) que ya existe en `research/05-scalability/routes.md`.

### Tareas Técnicas
- [ ] **Modelos de Datos:** Crear clases `Route`, `Schedule`, `Stop` en `src/rotulador/models/`.
- [ ] **Parser de Markdown/Data:** Implementar utilidad para leer `routes.md` y estructurarlo en objetos Python.
- [ ] **Inyección de Datos:** Actualizar `SignTemplate.render()` para aceptar objetos complejos de datos, no solo strings simples.

## 4. Nuevas Plantillas (Señalética Compleja)

Implementar los tipos de rótulos necesarios para una parada completa.

### Tareas Técnicas
- [ ] **`StopPostTemplate` (Poste Vertical):**
  - Cabecera con logo bUCR.
  - Lista de rutas (L1, L2) con sus colores.
  - Tabla de horarios simplificada.
  - Iconografía (Bus, Accesibilidad).
- [ ] **`RouteMapTemplate` (Mapa Esquemático):**
  - Generación procedimental de la línea de ruta (termómetro).
  - Indicadores de "Usted está aquí".

## 5. Assets e Iconografía

- [ ] **Vectorización de Iconos:** Convertir/Obtener iconos oficiales (Bus, Silla de ruedas) a SVG paths o cargarlos dinámicamente.
- [ ] **Gestión de Assets:** Mejorar `src/rotulador/assets/` para incluir iconos además de fuentes.

---

## Roadmap de Implementación

1. **Semana 1:** Refactor a milímetros y Motor de Layout básico (Texto multilínea).
2. **Semana 2:** Modelado de datos (Rutas/Horarios) y Parser.
3. **Semana 3:** Implementación de `StopPostTemplate` (Poste vertical).
4. **Semana 4:** Refinamiento visual, iconos y validación de impresión.
