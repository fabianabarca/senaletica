# Arquitectura del Paquete `rotulador`

**Relacionado con:**
- [01-python-libraries.md](../01-python-libraries/01-python-libraries.md) - Selección de pycairo (LaTeX descartado)
- [02-typography.md](../02-typography/02-typography.md) - Myriad Pro validada
- **[diagrams.md](./diagrams.md)** - Diagramas visuales de arquitectura en Mermaid

## Objetivo

Diseñar la arquitectura de un paquete Python para generación automatizada de rótulos de paradas, cumpliendo con los requisitos del issue bUCR#1.

**Stack tecnológico confirmado:**
- **pycairo (Cairo directo):** Renderizado vectorial profesional (conclusión de [01-python-libraries](../01-python-libraries/01-python-libraries.md))
  - Cairo directo es suficiente para rótulos (ver [cairo_test.py](../01-python-libraries/examples/cairo_test.py))
  - Pango descartado: presenta problemas de compatibilidad (ver [custom_font_pango.py](../02-typography/examples/01-font-loading/custom_font_pango.py))
- **Myriad Pro Bold:** Tipografía oficial UCR (disponible en [02-typography/myriad-pro/](../02-typography/myriad-pro/))
- **Performance validado:** ~100-200ms por rótulo (ejemplos ejecutables en research/)
- **Multi-formato:** SVG, PDF, PNG exports

---

## API Objetivo (del Issue)

```python
import rotulador

rotulo = rotulador.Rotulo()

parada_fing = rotulo.create(
    type="stop_back",
    stop_name="Facultad de Ingeniería",
)

parada_fing.export("parada_fing.svg")
```

---

## Principios de Diseño

1. **Simple API externa** - Fácil de usar para no-programadores
2. **Configuración por convención** - Defaults inteligentes basados en especificaciones
3. **Extensible** - Nuevos tipos de rótulos sin romper API
4. **Type-safe** - Type hints para mejor DX
5. **Testable** - Separación clara de concerns

---

## Estructura del Paquete

```
rotulador/
├── __init__.py           # API pública
├── core.py               # Clase Rotulo principal
├── types.py              # SignType enum y tipos
├── renderers/            # Backends de renderizado
│   ├── __init__.py
│   ├── base.py          # Renderer abstracto
│   └── cairo.py         # CairoRenderer (producción, única opción)
├── templates/            # Templates de diseño
│   ├── __init__.py
│   ├── base.py          # Template abstracto
│   ├── stop_back.py     # Rótulo respaldo trasero
│   └── stop_post.py     # Rótulo poste vertical
├── typography/           # Manejo de fuentes (basado en 02-typography)
│   ├── __init__.py
│   ├── loader.py        # Carga Myriad Pro .otf
│   ├── metrics.py       # Medición con pycairo (text_extents)
│   ├── adjuster.py      # Ajuste dinámico (size/multiline manual)
│   └── embedder.py      # Base64 embedding o path conversion
├── styles/               # Estilos y configuración
│   ├── __init__.py
│   ├── colors.py        # Paleta bUCR (C100 M75 Y0 K40)
│   ├── dimensions.py    # Medidas estándar (56-110mm fonts)
│   └── config.py        # Configuración global
└── utils/                # Utilidades
    ├── __init__.py
    └── validators.py    # Validación de input
```

**Nota:** Eliminado `svg.py` - según conclusiones de [01-python-libraries](../01-python-libraries/01-python-libraries.md), Cairo maneja SVG nativamente y svgwrite no ofrece ventajas para este caso de uso.

---

## Diagramas de Arquitectura

> **Diagramas completos:** [diagrams.md](./diagrams.md) | Para visualizar, copia el código en [mermaid.live](https://mermaid.live/) o utliza extensiones de VSCode.

**5 diagramas disponibles:**
1. [Diagrama de clases](./diagrams.md#1-diagrama-de-clases)
2. [Diagrama de secuencia](./diagrams.md#2-diagrama-de-secuencia)
3. [Diagrama de dependencias](./diagrams.md#3-diagrama-de-dependencias)
4. [Arquitectura del sistema](./diagrams.md#4-arquitectura-del-sistema)
5. [Flujo de datos](./diagrams.md#5-flujo-de-datos)

### Diagrama de Clases (Extracto)

```mermaid
classDiagram
    class Rotulo {
        -Renderer renderer
        -dict config
        +create(type, stop_name, **kwargs) Sign
    }
    
    class Sign {
        -bytes _data
        -SignSpec _spec
        -Renderer _renderer
        +export(path, format)
        +preview()
        +spec SignSpec
    }
    
    class SignType {
        <<enumeration>>
        STOP_BACK
        STOP_POST
        ROUTE_SYMBOL
        DIAGRAM
    }
    
    class SignSpec {
        +SignType type
        +str stop_name
        +float width
        +float height
        +float logo_size
        +float font_size
        +List~str~ text_lines
        +List~str~ route_symbols
        +str slogan
        +str background_color
        +validate() bool
    }
    
    class Renderer {
        <<abstract>>
        +render(spec)* bytes
        +export(data, path, format)*
    }
    
    class CairoRenderer {
        +render(spec) bytes
        +export(data, path, format)
        -_render_background(ctx, spec)
        -_render_logo(ctx, spec)
        -_render_text(ctx, spec)
        -_render_route_symbols(ctx, spec)
    }
    
    class Template {
        <<abstract>>
        +sign_type* SignType
        +generate_spec(stop_name, **kwargs)* SignSpec
    }
    
    class StopBackTemplate {
        +sign_type SignType
        +generate_spec(stop_name, **kwargs) SignSpec
        -_split_text(text, max_width) List~str~
        -_calculate_width(lines, font_size) float
    }
    
    class StopPostTemplate {
        +sign_type SignType
        +generate_spec(stop_name, **kwargs) SignSpec
    }
    
    class TypographyLoader {
        +load_myriad_pro() Font
        +load_system_font(name) Font
    }
    
    class TypographyMetrics {
        +measure_text(text, font, size) Extents
        +calculate_optimal_font_size(text, max_width) float
    }
    
    class TypographyAdjuster {
        +adjust_multiline(text, max_width) List~str~
        +adjust_spacing(text, target_width) float
    }
    
    class RotuladorConfig {
        +Path font_path
        +str ucr_blue
        +float font_size_min
        +float font_size_max
        +int dpi
    }
    
    Rotulo --> Renderer : uses
    Rotulo --> Sign : creates
    Sign --> SignSpec : contains
    Sign --> Renderer : uses
    SignSpec --> SignType : has
    Renderer <|-- CairoRenderer : implements
    Template <|-- StopBackTemplate : implements
    Template <|-- StopPostTemplate : implements
    Template --> SignSpec : generates
    StopBackTemplate --> TypographyMetrics : uses
    CairoRenderer --> TypographyLoader : uses
    Rotulo --> Template : uses
    Rotulo --> RotuladorConfig : uses
```

**Diagramas restantes:** Ver [diagrams.md](./diagrams.md) para secuencia, dependencias, arquitectura y flujo de datos.

---

## Diseño de Clases

### 1. API Principal

```python
# rotulador/__init__.py
from .core import Rotulo
from .types import SignType

__version__ = "0.1.0"
__all__ = ["Rotulo", "SignType"]
```

### 2. Clase Core

```python
# rotulador/core.py
from typing import Optional, Union
from pathlib import Path
from .types import SignType
from .renderers.base import Renderer
from .renderers.cairo import CairoRenderer
from .templates.base import Template
from .templates import get_template

class Rotulo:
    """
    Generador de rótulos de señalética para bUCR.
    
    Examples:
        >>> rotulo = Rotulo()
        >>> sign = rotulo.create(
        ...     type="stop_back",
        ...     stop_name="Facultad de Ingeniería"
        ... )
        >>> sign.export("fing.svg")
    """
    
    def __init__(
        self,
        renderer: Optional[Renderer] = None,
        config: Optional[dict] = None
    ):
        """
        Inicializa el generador.
        
        Args:
            renderer: Backend de renderizado (default: CairoRenderer)
            config: Configuración personalizada
        """
        self.renderer = renderer or CairoRenderer()
        self.config = config or {}
    
    def create(
        self,
        type: Union[str, SignType],
        stop_name: str,
        **kwargs
    ) -> "Sign":
        """
        Crea un rótulo según especificaciones.
        
        Args:
            type: Tipo de rótulo ("stop_back", "stop_post")
            stop_name: Nombre de la parada
            **kwargs: Parámetros adicionales (route_symbols, slogan, etc.)
        
        Returns:
            Sign: Objeto Sign listo para exportar
        """
        # Normalizar tipo
        sign_type = SignType(type) if isinstance(type, str) else type
        
        # Obtener template apropiado
        template = get_template(sign_type)
        
        # Generar especificación
        spec = template.generate_spec(
            stop_name=stop_name,
            **kwargs
        )
        
        # Renderizar
        rendered = self.renderer.render(spec)
        
        return Sign(rendered, spec, self.renderer)


class Sign:
    """
    Representa un rótulo generado.
    """
    
    def __init__(self, rendered_data, spec, renderer):
        self._data = rendered_data
        self._spec = spec
        self._renderer = renderer
    
    def export(
        self,
        path: Union[str, Path],
        format: Optional[str] = None
    ):
        """
        Exporta el rótulo a archivo.
        
        Args:
            path: Ruta de salida
            format: Formato (svg, pdf, png). Auto-detecta de extensión.
        """
        path = Path(path)
        format = format or path.suffix.lstrip('.')
        
        self._renderer.export(self._data, path, format)
    
    def preview(self):
        """Muestra preview del rótulo (si hay GUI)."""
        pass
    
    @property
    def spec(self) -> dict:
        """Retorna especificación del diseño."""
        return self._spec
```

### 3. Sistema de Tipos

```python
# rotulador/types.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

class SignType(Enum):
    """Tipos de rótulos disponibles."""
    STOP_BACK = "stop_back"      # Respaldo trasero horizontal
    STOP_POST = "stop_post"      # Poste vertical
    ROUTE_SYMBOL = "route_symbol" # Símbolo de ruta
    DIAGRAM = "diagram"          # Diagrama de rutas

@dataclass
class SignSpec:
    """Especificación completa de un rótulo."""
    type: SignType
    stop_name: str
    width: float  # mm
    height: float  # mm
    
    # Elementos visuales
    logo_size: float
    font_size: float
    text_lines: List[str]
    
    # Opcionales
    route_symbols: Optional[List[str]] = None
    slogan: Optional[str] = None
    background_color: str = "#FFFFFF"
    
    def validate(self) -> bool:
        """Valida que la especificación sea correcta."""
        # Verificar rangos según normas
        if not (56 <= self.font_size <= 110):
            raise ValueError(f"Font size {self.font_size}mm fuera de rango 56-110mm")
        return True
```

### 4. Templates

```python
# rotulador/templates/base.py
from abc import ABC, abstractmethod
from ..types import SignSpec, SignType

class Template(ABC):
    """Template abstracto para rótulos."""
    
    @property
    @abstractmethod
    def sign_type(self) -> SignType:
        """Tipo de rótulo que genera este template."""
        pass
    
    @abstractmethod
    def generate_spec(self, stop_name: str, **kwargs) -> SignSpec:
        """
        Genera especificación del rótulo.
        
        Implementa la lógica de diagramación:
        - Calcula dimensiones
        - Ajusta tamaño de fuente
        - Divide texto en líneas
        - Posiciona elementos
        """
        pass


# rotulador/templates/stop_back.py
from .base import Template
from ..types import SignSpec, SignType
from ..typography.metrics import calculate_optimal_font_size

class StopBackTemplate(Template):
    """
    Template para rótulo de respaldo trasero (horizontal).
    
    Especificaciones:
    - Ancho: Variable según nombre
    - Alto: 300mm (estándar)
    - Logo "b": 60mm diámetro
    - Texto: 1-2 líneas, centrado
    """
    
    @property
    def sign_type(self) -> SignType:
        return SignType.STOP_BACK
    
    def generate_spec(
        self,
        stop_name: str,
        route_symbols: list = None,
        slogan: str = None,
        **kwargs
    ) -> SignSpec:
        # 1. Calcular líneas de texto
        lines = self._split_text(stop_name, max_width=800)
        
        # 2. Calcular tamaño de fuente óptimo
        font_size = calculate_optimal_font_size(
            text=stop_name,
            max_width=800,
            min_size=56,
            max_size=110
        )
        
        # 3. Calcular dimensiones totales
        height = 300  # mm estándar
        width = self._calculate_width(lines, font_size)
        
        # 4. Crear especificación
        return SignSpec(
            type=self.sign_type,
            stop_name=stop_name,
            width=width,
            height=height,
            logo_size=60,
            font_size=font_size,
            text_lines=lines,
            route_symbols=route_symbols,
            slogan=slogan
        )
    
    def _split_text(self, text: str, max_width: float) -> List[str]:
        """Divide texto en líneas si es necesario."""
        # TODO: Implementar lógica de split inteligente
        if len(text) <= 30:
            return [text]
        else:
            # Split en palabras
            words = text.split()
            if len(words) <= 2:
                return [text]
            mid = len(words) // 2
            return [
                ' '.join(words[:mid]),
                ' '.join(words[mid:])
            ]
    
    def _calculate_width(self, lines: List[str], font_size: float) -> float:
        """Calcula ancho necesario basado en texto."""
        # TODO: Usar typography.metrics para cálculo preciso
        # Por ahora, estimación
        max_chars = max(len(line) for line in lines)
        return max(600, max_chars * font_size * 0.6)
```

### 5. Renderer con Cairo Directo

**Decisión técnica:** Usar Cairo directo (sin Pango) basado en:
- Ejemplos validados usan Cairo puro ([cairo_test.py](../01-python-libraries/examples/cairo_test.py))
- Pango presenta problemas de compatibilidad ([custom_font_pango.py](../02-typography/examples/01-font-loading/custom_font_pango.py))
- Cairo solo es suficiente para rótulos simples
- Multi-línea se puede hacer manualmente (ver [multiline_split.py](../02-typography/examples/03-layout/multiline_split.py))

```python
# rotulador/renderers/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from ..types import SignSpec

class Renderer(ABC):
    """Renderer abstracto (Cairo es la única implementación)."""
    
    @abstractmethod
    def render(self, spec: SignSpec):
        """
        Renderiza un rótulo según especificación.
        
        Returns:
            Datos renderizados en formato interno del renderer
        """
        pass
    
    @abstractmethod
    def export(self, data, path: Path, format: str):
        """
        Exporta datos renderizados a archivo.
        
        Args:
            data: Datos del render()
            path: Ruta de salida
            format: svg, pdf, png, etc.
        """
        pass


# rotulador/renderers/cairo.py
import cairo
from .base import Renderer
from ..types import SignSpec
from ..typography.loader import load_font

class CairoRenderer(Renderer):
    """Renderer usando pycairo (Cairo directo, sin Pango).
    
    Basado en ejemplos validados:
    - cairo_test.py: Renderizado básico funcional
    - custom_font_pango.py: Cairo directo por compatibilidad
    - multiline_split.py: Multi-línea manual
    
    Performance validado: ~100-200ms por rótulo
    """
    
    def render(self, spec: SignSpec):
        """Renderiza con Cairo."""
        # Crear surface
        surface = cairo.SVGSurface(
            None,  # Rendering a memoria
            spec.width,
            spec.height
        )
        ctx = cairo.Context(surface)
        
        # Renderizar elementos
        self._render_background(ctx, spec)
        self._render_logo(ctx, spec)
        self._render_text(ctx, spec)
        
        if spec.route_symbols:
            self._render_route_symbols(ctx, spec)
        
        return {
            'surface': surface,
            'context': ctx,
            'spec': spec
        }
    
    def export(self, data, path, format):
        """Exporta a archivo."""
        surface = data['surface']
        
        if format == 'svg':
            # SVG ya está en el surface
            surface.write_to_png(str(path))  # Temp
            # TODO: Proper SVG export
        elif format == 'png':
            # Crear surface PNG
            pass
        elif format == 'pdf':
            # Crear surface PDF
            pass
    
    def _render_background(self, ctx, spec):
        """Renderiza fondo."""
        ctx.set_source_rgb(1, 1, 1)  # Blanco
        ctx.paint()
    
    def _render_logo(self, ctx, spec):
        """Renderiza logo "b"."""
        # TODO: Dibujar círculo UCR blue con "b" blanco
        pass
    
    def _render_text(self, ctx, spec):
        """Renderiza texto de parada."""
        # TODO: Usar tipografía UCR, ajustar según spec
        pass
    
    def _render_route_symbols(self, ctx, spec):
        """Renderiza símbolos de rutas."""
        pass
```

---

## Sistema de Configuración

```python
# rotulador/styles/config.py
from dataclasses import dataclass
from pathlib import Path

@dataclass
class RotuladorConfig:
    """Configuración global del sistema.
    
    Defaults basados en:
    - Manual de Identidad Visual UCR
    - Investigación en 02-typography.md
    - Normas INTECO Ley 7600
    """
    
    # Colores bUCR
    ucr_blue: str = "#003DA5"
    ucr_yellow: str = "#FFD700"
    text_color: str = "#000000"
    background_color: str = "#FFFFFF"
    
    # Tipografía
    font_family: str = "Helvetica Neue"
    font_path: str = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    min_font_size: float = 56  # mm
    max_font_size: float = 110  # mm
    
    # Dimensiones
    logo_diameter: float = 60  # mm
    standard_height: float = 300  # mm
    margin: float = 20  # mm
    
    # Output
    default_format: str = "svg"
    dpi: int = 300  # Para raster exports


# Singleton global
_config = RotuladorConfig()

def get_config() -> RotuladorConfig:
    """Obtiene configuración global."""
    return _config

def set_config(config: RotuladorConfig):
    """Establece configuración personalizada."""
    global _config
    _config = config
```

---

## Uso Avanzado

### Ejemplo 1: Configuración Custom

```python
import rotulador
from rotulador.styles.config import RotuladorConfig, set_config
from pathlib import Path

# Configurar con Myriad Pro (fuente oficial UCR)
config = RotuladorConfig(
    font_path=Path("research/02-typography/myriad-pro/MYRIADPRO-BOLD.OTF"),
    ucr_blue="#002B5C",  # Azul UCR
    font_size_min=56,    # mm (Norma INTECO)
    font_size_max=110    # mm (Norma INTECO)
)
set_config(config)

# Usar normalmente
r = rotulador.Rotulo()
sign = r.create("stop_back", "Derecho")
sign.export("derecho.svg")
sign.export("derecho.pdf")  # Multi-formato con Cairo
```

### Ejemplo 2: Batch Generation

```python
import rotulador

paradas = [
    "Facultad de Ingeniería",
    "Ciencias Sociales",
    "Derecho",
    "Artes Plásticas",
    # ... 20+ paradas
]

r = rotulador.Rotulo()

for nombre in paradas:
    sign = r.create("stop_back", nombre)
    filename = nombre.lower().replace(' ', '_')
    sign.export(f"output/{filename}.svg")
    print(f"✓ Generado: {filename}.svg")
```

### Ejemplo 3: Con Símbolos de Rutas

```python
import rotulador

r = rotulador.Rotulo()

sign = r.create(
    type="stop_back",
    stop_name="Facultad de Ingeniería",
    route_symbols=["A", "B"],  # Rutas que paran aquí
    slogan="el b es el bus de la U"
)

sign.export("fing_completo.svg")
```

---

## Extensibilidad

### Agregar Nuevo Tipo de Rótulo

```python
# rotulador/templates/info_panel.py
from .base import Template
from ..types import SignType, SignSpec

class InfoPanelTemplate(Template):
    """Template para panel informativo general."""
    
    @property
    def sign_type(self) -> SignType:
        return SignType.INFO_PANEL
    
    def generate_spec(self, title: str, content: str, **kwargs) -> SignSpec:
        # Implementar lógica específica
        pass

# Registrar template
# rotulador/templates/__init__.py
_templates = {
    SignType.STOP_BACK: StopBackTemplate(),
    SignType.STOP_POST: StopPostTemplate(),
    SignType.INFO_PANEL: InfoPanelTemplate(),  # Nuevo
}
```

---

## Testing

```python
# tests/test_rotulo.py
import pytest
import rotulador

def test_create_basic_sign():
    r = rotulador.Rotulo()
    sign = r.create("stop_back", "Test")
    assert sign is not None
    assert sign.spec.stop_name == "Test"

def test_font_size_constraints():
    r = rotulador.Rotulo()
    sign = r.create("stop_back", "A" * 100)  # Nombre muy largo
    
    # Debe ajustar al mínimo permitido
    assert 56 <= sign.spec.font_size <= 110

def test_export_svg():
    r = rotulador.Rotulo()
    sign = r.create("stop_back", "Test")
    
    output = tmp_path / "test.svg"
    sign.export(output)
    
    assert output.exists()
    assert output.stat().st_size > 0
```

---

## Roadmap de Implementación

**Estado actual:** Investigación completada (8h), ejemplos validados
- Stack seleccionado: pycairo (Cairo directo)
- Myriad Pro Bold obtenida y probada
- 14 ejemplos ejecutables funcionando
- Performance validado: ~100-200ms/sign

### Fase 1: MVP (3-4 horas)
-  Estructura de paquete según diseño
-  API básica funcional (core.py, types.py)
-  StopBackTemplate simple
-  CairoRenderer básico (basado en examples/cairo_test.py)
-  Myriad Pro loading (basado en 02-typography/examples/)

### Fase 2: Producción (4-5 horas)
-  CairoRenderer completo (Cairo directo, sin Pango)
-  Typography system robusto (loader, metrics con Cairo, adjuster)
-  StopPostTemplate
-  Font embedding (base64 y path conversion)
-  Multi-línea automático (basado en [multiline_split.py](../02-typography/examples/03-layout/multiline_split.py))

### Fase 3: Escalabilidad (2-3 horas)
-  CLI tool
-  Batch generation optimizada
-  Template validation
-  Comprehensive tests

### Fase 4: Integración (futuro)
-  Web API (FastAPI)
-  Database integration (GTFS)
-  Admin dashboard
-  Version control de rótulos

---

---

## Contexto de Investigación Completada

**Investigación previa (8h):**
1. [01-python-libraries](../01-python-libraries/) - 5 bibliotecas evaluadas, pycairo (Cairo directo) seleccionado (LaTeX descartado)
2. [02-typography](../02-typography/) - Myriad Pro configurada, 9 ejemplos validados (Cairo directo funcional)
3. [04-reference-cases](../04-reference-cases/) - MBTA, TfL, BART analizados
4. [05-scalability](../05-scalability/) - Estrategia de fases definida
5. [06-final-specification](../06-final-specification/) - Especificación ejecutiva

**Ejemplos ejecutables validados:** 14 archivos en research/{01,02}-*/examples/

**Próximo paso:** Implementar MVP según esta arquitectura (Fase 1: 3-4h)

---

**Actualizado:** 30 de diciembre de 2025
