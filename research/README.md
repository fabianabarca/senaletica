# Investigación: Generador Automático de Rótulos

**Issue:** bUCR#1 - Automatic sign generator  
**Branch:** `feature/bucr-1-sign-generator-research`  
**Investigador:** Brandon Trigueros  
**Fecha:** Diciembre 2025  

## Objetivo

Investigar y proponer una arquitectura para un sistema automatizado de generación de rótulos de paradas de autobús, capaz de escalar desde las ~20 paradas de la UCR hasta miles de paradas a nivel nacional.

## Contexto

Actualmente, los rótulos de bUCR se diseñan manualmente en herramientas de diseño gráfico. Esto funciona para 20 paradas, pero no es escalable. Necesitamos un sistema que permita generar rótulos consistentes usando plantillas predefinidas.

### Tipos de Rótulos a Generar

1. **Tipo cartel** (horizontal): Para paradas con infraestructura (respaldo trasero)
2. **Tipo señal vial** (vertical): Para paradas sin infraestructura (poste)

### Especificaciones de Diseño

- **Logo "b"**: Circular, 60cm de diámetro
- **Tipografía**: Según guía de identidad visual UCR
- **Tamaño de letra**: 56mm - 110mm (legibilidad 2-5 metros)
- **Colores**: Según identidad visual bUCR
- **Formatos de salida**: SVG (preferido), PNG, PDF

## API Objetivo (Ejemplo del Issue)

```python
import rotulador

rotulo = rotulador.Rotulo()

parada_fing = rotulo.create(
    type="stop_back",
    stop_name="Facultad de Ingeniería",
)

parada_fing.export("parada_fing.svg")
```

## Preguntas de Investigación

1. ¿Cuáles bibliotecas Python son adecuadas para diagramación de rótulos?
2. ¿Cómo manejar tipografías personalizadas en Python?
3. ¿Es LaTeX/TikZ apropiado o es overkill?
4. ¿Qué arquitectura permitiría escalar a nivel nacional?
5. ¿Cuándo justifica desarrollar una plataforma completa con base de datos?

## Estructura de la Investigación

```
research/
├── README.md (este archivo)
├── 01-python-libraries.md (comparativa de bibliotecas)
├── 02-typography.md (manejo de tipografías)
├── 03-latex-evaluation.md (análisis LaTeX vs Python)
├── 04-architecture.md (propuesta de arquitectura)
├── 05-reference-cases.md (MBTA y otros casos)
├── 06-scalability.md (templates y escalabilidad)
├── 07-final-specification.md (documento final)
└── examples/ (ejemplos de código)
```

## Referencias

- **MBTA SignMaker**: [BIA Wayfinding](https://biasignmaker.com/)
- **Documentación bUCR**: `/docs/respaldo.md`, `/docs/elementos.md`
- **GTFS Spec**: Para integración con sistema de información
- **INTECO 5.1.1.2**: Norma de tamaño para lectura visual

## Cronograma (8 horas)

| Tarea | Tiempo | Estado |
|-------|--------|--------|
| Setup y estructura | 0.5h |  |
| Investigación bibliotecas Python | 1.5h |  |
| Análisis tipografías | 1h |  |
| Evaluación LaTeX | 1h |  |
| Casos de referencia | 1h |  |
| Arquitectura propuesta | 2h |  |
| Documento final | 1h |  |

---

**Próximo paso:** Investigar bibliotecas Python para generación de gráficos vectoriales.
