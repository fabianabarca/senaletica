# Diagramas de Arquitectura - Rotulador

Este archivo contiene los diagramas en formato Mermaid para generar imágenes.

## Instrucciones de Generación

Puedes generar las imágenes de estos diagramas usando:
- **Mermaid Live Editor:** https://mermaid.live/
- **CLI:** `mmdc -i diagrams.md -o diagrams.png`
- **VS Code:** Extensión "Markdown Preview Mermaid Support"

---

## 1. Diagrama de Clases Completo

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

---

## 2. Diagrama de Secuencia - Flujo de Generación

```mermaid
sequenceDiagram
    participant User
    participant Rotulo
    participant Template
    participant Renderer
    participant Sign
    
    User->>Rotulo: create("stop_back", "FING")
    Rotulo->>Template: get_template(STOP_BACK)
    Template-->>Rotulo: StopBackTemplate
    Rotulo->>Template: generate_spec("FING")
    
    Note over Template: - Calcula dimensiones<br/>- Ajusta font size<br/>- Split multi-línea
    
    Template-->>Rotulo: SignSpec
    Rotulo->>Renderer: render(SignSpec)
    
    Note over Renderer: Cairo:<br/>- Crea surface<br/>- Dibuja elementos<br/>- Aplica tipografía
    
    Renderer-->>Rotulo: rendered_data (bytes)
    Rotulo->>Sign: Sign(data, spec, renderer)
    Sign-->>User: Sign instance
    
    User->>Sign: export("fing.svg")
    Sign->>Renderer: export(data, path, "svg")
    Renderer-->>Sign: Done
    Sign-->>User: File saved
```

---

## 3. Diagrama de Dependencias del Paquete

```mermaid
graph TB
    subgraph "Core Package"
        A[rotulador/__init__.py]
        B[core.py]
        C[types.py]
    end
    
    subgraph "Rendering"
        D[renderers/cairo.py]
        D1[pycairo library]
    end
    
    subgraph "Templates"
        E[templates/stop_back.py]
        F[templates/stop_post.py]
    end
    
    subgraph "Typography"
        G[typography/loader.py]
        H[typography/metrics.py]
        I[typography/adjuster.py]
        J[typography/embedder.py]
        J1[fontTools library]
    end
    
    subgraph "Configuration"
        K[styles/config.py]
        L[styles/colors.py]
        M[styles/dimensions.py]
    end
    
    subgraph "External Resources"
        N[Myriad Pro .otf files]
    end
    
    A --> B
    A --> C
    B --> D
    B --> E
    B --> F
    D --> D1
    D --> G
    D --> H
    E --> H
    E --> I
    F --> H
    G --> N
    G --> J1
    J --> J1
    B --> K
    K --> L
    K --> M
    
    style D1 fill:#f9f,stroke:#333,stroke-width:2px
    style J1 fill:#f9f,stroke:#333,stroke-width:2px
    style N fill:#bbf,stroke:#333,stroke-width:2px
```

---

## 4. Arquitectura del Sistema Completo

```mermaid
graph LR
    subgraph "User Interface"
        CLI[CLI Tool]
        API[Python API]
    end
    
    subgraph "Core Logic"
        ROT[Rotulo Class]
        SIGN[Sign Class]
    end
    
    subgraph "Processing"
        TEMP[Templates]
        REND[CairoRenderer]
        TYPO[Typography]
    end
    
    subgraph "Data"
        GTFS[GTFS Data]
        CONF[Configuration]
        FONTS[Myriad Pro]
    end
    
    subgraph "Output"
        SVG[SVG Files]
        PDF[PDF Files]
        PNG[PNG Files]
    end
    
    CLI --> ROT
    API --> ROT
    ROT --> TEMP
    ROT --> REND
    TEMP --> TYPO
    REND --> TYPO
    GTFS --> ROT
    CONF --> ROT
    FONTS --> TYPO
    ROT --> SIGN
    SIGN --> SVG
    SIGN --> PDF
    SIGN --> PNG
    
    style CLI fill:#e1f5ff
    style API fill:#e1f5ff
    style SVG fill:#c8e6c9
    style PDF fill:#c8e6c9
    style PNG fill:#c8e6c9
```

---

## 5. Flujo de Datos Simplificado

```mermaid
flowchart TD
    START([Usuario]) --> INPUT[Input: Nombre parada + Tipo]
    INPUT --> VALIDATE{Validar Input}
    VALIDATE -->|Inválido| ERROR[Error]
    VALIDATE -->|Válido| TEMPLATE[Seleccionar Template]
    
    TEMPLATE --> CALC[Calcular Dimensiones]
    CALC --> FONT[Ajustar Font Size]
    FONT --> MULTI{¿Necesita<br/>multi-línea?}
    
    MULTI -->|Sí| SPLIT[Split Texto]
    MULTI -->|No| SPEC[Crear SignSpec]
    SPLIT --> SPEC
    
    SPEC --> RENDER[Renderizar con Cairo]
    RENDER --> DRAW1[Dibujar Fondo]
    DRAW1 --> DRAW2[Dibujar Logo]
    DRAW2 --> DRAW3[Dibujar Texto]
    DRAW3 --> DRAW4[Elementos Opcionales]
    
    DRAW4 --> FORMAT{Formato<br/>Export}
    FORMAT -->|SVG| SVG[Guardar SVG]
    FORMAT -->|PDF| PDF[Guardar PDF]
    FORMAT -->|PNG| PNG[Guardar PNG]
    
    SVG --> END([Archivo Generado])
    PDF --> END
    PNG --> END
    ERROR --> END
    
    style START fill:#e3f2fd
    style END fill:#c8e6c9
    style ERROR fill:#ffcdd2
    style RENDER fill:#fff9c4
```

---

## Notas de Implementación

### Colores en Diagramas
- 🟪 Dependencias externas (bibliotecas)
- 🟦 Recursos externos (fuentes)
- ⬜ Módulos internos
- 🟩 Outputs/resultados
- 🟨 Procesamiento crítico

### Generación de Imágenes

**Opción 1: Mermaid Live Editor**
1. Copiar código del diagrama
2. Ir a https://mermaid.live/
3. Pegar y exportar como PNG/SVG

**Opción 2: CLI (si tienes mermaid-cli)**
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagrams.md -o class-diagram.png -t dark
```

**Opción 3: VS Code**
1. Instalar extensión "Markdown Preview Mermaid Support"
2. Abrir este archivo
3. Vista previa (Ctrl+Shift+V)
4. Click derecho → "Copy Mermaid as PNG"

---

**Actualizado:** 30 de diciembre de 2025
