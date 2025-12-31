# Sistema de señalética de *b*UCR

> Una guía de referencia del sistema de diseño de la señalética del bus interno de la UCR

## Documentación

El archivo `SENALETICA.md` detalla el sistema de diseño (colores, tipografía, etc.) basado en la identidad visual de la UCR. 

En el directorio `/especificaciones` están las especificaciones de diseño para...

## Ejemplos

Isotipo del sistema del bus interno ("el *b*"):

Imagotipo del sistema del bus interno ("bUCR"):

Slogans:

- "el ***b*** es el bus de la U"
- "UCR con ***b*** de bus"

---

## 🛠️ Generador Automático (`rotulador`)

Este repositorio incluye el paquete Python `rotulador` para generar automáticamente los rótulos de paradas en formato vectorial (SVG/PDF).

### Instalación

```bash
pip install .
```

### Uso Básico

**Desde Python:**

```python
import rotulador

# Crear rótulo de respaldo (Stop Back)
sign = rotulador.create("stop_back", stop_name="Facultad de Ingeniería")
sign.export("fing.svg")
```

**Desde Terminal (CLI):**

```bash
rotulador stop_back "Facultad de Ingeniería" --output fing.svg
```

### Requisitos

- Python 3.10+
- libcairo2 (Sistema)
- Fuente "Myriad Pro" instalada en el sistema (para renderizado correcto)



