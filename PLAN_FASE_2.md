# Plan de Desarrollo Fase 2: Sistema de Señalética Profesional

**Objetivo:** Evolucionar el paquete `rotulador` de un MVP funcional a un sistema de producción capaz de generar señalética real, estandarizada y lista para impresión, cumpliendo con normativas UCR e INTECO.

---

## ⚠️ PRE-REQUISITO: Integración de Assets Existentes (Actualizado)

**Tras verificación, se confirma que la rama `main` YA contiene los assets históricos de la rama `rotulos` en `docs/assets/` y `docs/elementos.md`. No es necesario un merge de ramas, sino la correcta utilización de estos recursos.**

### Recursos Disponibles en `main`
- **Assets Gráficos (`docs/assets/`):**
  - SVGs críticos: `b_azul.svg`, `parada.svg`, `slogan.svg`, grillas de rótulos.
  - PDFs normativos: `identidad_visual_ucr_3.1.pdf`, `norma_INTE_W5_2021.pdf`.
- **Especificaciones (`docs/elementos.md`):**
  - Paleta oficial (Celeste #00C0F3, etc.) y tipografía Myriad Pro.

### Tarea de Consolidación (Refinado)

En lugar de un merge masivo, la tarea será **refactorizar el código para usar estos assets oficiales** en lugar de aproximaciones.

1. **Limpieza y Organización:**
   - Verificar si `research/` tiene duplicados y eliminarlos en favor de `docs/`.
   - Mover scripts de MVP a usar paths relativos a `docs/assets/` si es necesario o copiar los oficiales a la estructura del paquete.

2. **Actualización de Referencias:**
   - Asegurar que `CairoRenderer` apunte a los SVGs oficiales de `docs/assets/svg/` para logos y símbolos.

**Estado:** `rotulos` es ancestro de `main`. El contenido ya existe. Proceder directo a Fase 2 integrando estos recursos.

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
