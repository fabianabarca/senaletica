# Sistema de Plantillas y Escalabilidad

**Relacionado con:**
- [01-python-libraries.md](../01-python-libraries/01-python-libraries.md) - Performance: ~100-200ms/sign
- [02-typography.md](../02-typography/02-typography.md) - Myriad Pro, font embedding
- [03-architecture.md](../03-architecture/03-architecture.md) - Diseño modular
- [04-reference-cases.md](../04-reference-cases/04-reference-cases.md) - Lecciones de MBTA, BART

## Objetivo

Definir estrategia para escalar el sistema de generación de rótulos desde las ~20 paradas de la UCR hasta potencialmente miles de paradas a nivel nacional.

**Con stack validado:** pycairo (Cairo directo), Myriad Pro, performance ~100-200ms/sign

---

## Contexto de Escala

### Escenario Actual: UCR (Fase 1)
- **Paradas:** ~20
- **Rutas:** 2-3
- **Frecuencia de cambios:** Baja (semestral)
- **Stakeholders:** UCR Transporte
- **Tecnología actual:** Diseño manual (Illustrator/Inkscape)

### Escenario Futuro: Nacional (Fase 3)
- **Paradas:** Miles (3000+)
- **Rutas:** Cientos
- **Frecuencia de cambios:** Alta (semanal/diaria)
- **Stakeholders:** Múltiples operadores
- **Tecnología necesaria:** Plataforma automatizada

### Pregunta Clave (del Issue)

> "¿Cuándo sería necesaria una plataforma completa para tener un control de la rotulación existente?"

**Respuesta corta:** A partir de ~100 paradas o cuando hay múltiples operadores.

---

## Sistema de Plantillas

### Filosofía de Diseño

**"Configuration over Code"**

```python
# Malo: Código hard-coded por parada
if stop_name == "FING":
    width = 600
    font_size = 72
elif stop_name == "Ciencias Sociales":
    width = 800
    font_size = 64
# ... No escala

# Bueno: Template con configuración
template = get_template("stop_back")
spec = template.generate(stop_name=any_name)  # Automático
```

---

## Niveles de Plantillas

### Nivel 1: Template de Tipo (Básico)

**Un template por tipo de rótulo:**

```python
TEMPLATES = {
    "stop_back": StopBackTemplate(),     # Respaldo horizontal
    "stop_post": StopPostTemplate(),     # Poste vertical
    "route_symbol": RouteSymbolTemplate(), # Símbolo ruta
    "diagram": RouteDiagramTemplate()     # Diagrama
}
```

**Escalabilidad:**  Suficiente para UCR (20 paradas)  
**Limitación:** Todos los rótulos del mismo tipo se ven idénticos

---

### Nivel 2: Template con Variantes (Intermedio)

**Variantes dentro de cada tipo:**

```python
class StopBackTemplate:
    VARIANTS = {
        "standard": {
            "width": "auto",
            "height": 300,
            "logo_position": "left",
            "text_lines": "auto"
        },
        "compact": {
            "width": 600,
            "height": 200,
            "logo_position": "top",
            "text_lines": 1
        },
        "large": {
            "width": 1200,
            "height": 400,
            "logo_position": "center",
            "text_lines": "auto"
        }
    }
```

**Uso:**
```python
sign = rotulo.create(
    type="stop_back",
    variant="compact",  # Nuevo parámetro
    stop_name="FING"
)
```

**Escalabilidad:**  Bueno hasta ~200 paradas  
**Ventaja:** Flexibilidad sin complejidad

---

### Nivel 3: Template Parametrizado (Avanzado)

**Configuración completa por parada:**

```yaml
# config/stops/fing.yaml
stop_id: "UCR_FING"
stop_name: "Facultad de Ingeniería"
sign_config:
  type: "stop_back"
  variant: "standard"
  custom_width: 800
  custom_font_size: 68
  logo_override: "fing_custom_logo.svg"
  routes: ["A", "B"]
  additional_info: "Horario: 6am - 10pm"
```

```python
# Cargar configuración
config = load_stop_config("fing.yaml")
sign = rotulo.create_from_config(config)
```

**Escalabilidad:**  Hasta miles de paradas  
**Complejidad:** Alta - requiere gestión de archivos

---

### Nivel 4: Database-Driven (Plataforma Completa)

**Base de datos como source of truth:**

```sql
-- Database schema
CREATE TABLE stops (
    stop_id VARCHAR PRIMARY KEY,
    stop_name VARCHAR NOT NULL,
    sign_type VARCHAR,
    sign_variant VARCHAR,
    custom_config JSONB,
    last_updated TIMESTAMP,
    approved BOOLEAN DEFAULT FALSE
);

CREATE TABLE signs (
    sign_id UUID PRIMARY KEY,
    stop_id VARCHAR REFERENCES stops(stop_id),
    version INT,
    file_path VARCHAR,
    generated_at TIMESTAMP,
    status VARCHAR  -- draft, approved, printed, installed
);
```

**API:**
```python
# Admin genera rótulo
sign = rotulador.create_from_db(stop_id="UCR_FING")

# Auto-tracking
sign.save_to_db()  # Version control automático
sign.mark_as_approved(by_user="admin@ucr.ac.cr")
sign.export_for_production()
```

**Escalabilidad:**  Ilimitada  
**Requerimiento:** Plataforma web completa

---

## Estrategia de Escalabilidad por Fase

### Fase 1: UCR Piloto (0-30 paradas)

**Herramienta:** Python CLI + pycairo

```bash
# Generar todas las paradas UCR
rotulador generate --input stops.csv --output output/

# Generar una parada específica
rotulador generate --stop "Facultad de Ingeniería" --type stop_back

# Con Myriad Pro y multi-formato
rotulador generate --stop "Derecho" --formats svg,pdf,png
```

**Storage:**
```
output/
├── fing_stop_back.svg
├── fing_stop_back.pdf
├── ciencias_sociales_stop_back.svg
├── derecho_stop_back.svg
└── ...
```

**Performance (validado):**
- Individual: ~100-200ms/sign (ver [01-python-libraries/examples/](../01-python-libraries/examples/))
- Batch 20 paradas: ~2-4 segundos total
- Batch 1000 paradas: ~2-3 minutos estimado

**Dependencias de sistema:**
```bash
# Ubuntu/Debian
sudo apt install libcairo2-dev pkg-config python3-dev

# Python
pip install pycairo fonttools
```

**Pros:**
-  Simple
-  No requiere infraestructura web
-  Git para version control
-  Performance excelente para < 100 paradas
-  Myriad Pro font embedding funcional

**Contras:**
-  No tracking de qué está instalado físicamente
-  No workflow de aprobación integrado
-  Deployment requiere instalar dependencias

**Cuándo es suficiente:** UCR solamente (20 paradas), actualizaciones semestrales

---

### Fase 2: Múltiples Operadores (30-200 paradas)

**Herramienta:** CLI + Config Files

```yaml
# config/ucr.yaml
operator: "UCR Transporte"
stops:
  - name: "FING"
    type: "stop_back"
  - name: "Ciencias"
    type: "stop_post"

# config/operator_2.yaml  
operator: "Operador Regional"
stops:
  - name: "Terminal"
    type: "stop_back"
```

```bash
# Generar por operador
rotulador batch --config config/ucr.yaml
rotulador batch --config config/operator_2.yaml
```

**Storage:** Git repository
```
signs/
├── ucr/
│   ├── fing.svg
│   └── ciencias.svg
├── operator_2/
│   └── terminal.svg
└── metadata/
    └── generation_log.json
```

**Pros:**
-  Multi-tenant básico
-  Configuración organizada
-  Git history = version control

**Contras:**
-  Aún sin tracking de estado físico
-  Aprobaciones manuales (email, etc.)

**Cuándo es suficiente:** Hasta ~5 operadores pequeños

---

### Fase 3: Sistema Nacional (200+ paradas)

**Herramienta:** Web Platform (Django)

**Arquitectura:**
```
[Django Admin Panel]
    ↓
[PostgreSQL Database]
    ├── Stops (GTFS-based)
    ├── Signs (generated, versions)
    ├── Users (operators, approvers)
    └── Production orders
    ↓
[rotulador API Service]
    ↓
[S3/Storage Backend]
    ├── SVG originals
    ├── PDF print-ready
    └── PNG previews
```

**Features necesarios:**

1. **User Management**
   - Operadores (create/edit stops)
   - Diseñadores (modify templates)
   - Aprobadores (approve for production)
   - Impresores (download print files)

2. **Workflow**
   ```
   Draft → Review → Approved → Printed → Installed
   ```

3. **GTFS Integration**
   ```python
   # Auto-import from GTFS
   gtfs_stops = load_gtfs("data/gtfs.zip")
   for stop in gtfs_stops:
       if not Sign.exists(stop_id=stop.stop_id):
           generate_sign(stop)
   ```

4. **Batch Operations**
   ```python
   # Regenerar todo cuando cambian specs
   old_stops = Sign.objects.filter(version="1.0")
   for sign in old_stops:
       regenerate_sign(sign, new_version="2.0")
   ```

5. **Reporting**
   - ¿Cuántos rótulos por operador?
   - ¿Cuáles necesitan actualización?
   - ¿Cuál es el estado de producción?

**Pros:**
-  Escalabilidad total
-  Control completo
-  Trazabilidad
-  Multi-user

**Contras:**
-  Desarrollo extenso (~200h)
-  Mantenimiento continuo
-  Infraestructura (hosting, DB)

**Cuándo es necesario:**
- Más de 200 paradas
- Más de 5 operadores
- Updates frecuentes (mensual o más)
- Presupuesto para desarrollo

---

## Decisión Framework: ¿Cuándo Escalar?

### Calculadora de Complejidad

```python
def calculate_complexity_score(
    num_stops: int,
    num_operators: int,
    update_frequency: str,  # "yearly", "monthly", "weekly", "daily"
    custom_requirements: int  # 0-10 scale
) -> int:
    """
    Calcula score de complejidad.
    
    Score < 20: CLI suficiente
    Score 20-50: Config files + Git
    Score > 50: Platform necesaria
    """
    
    freq_scores = {
        "yearly": 1,
        "monthly": 5,
        "weekly": 10,
        "daily": 20
    }
    
    score = (
        num_stops * 0.1 +
        num_operators * 5 +
        freq_scores[update_frequency] +
        custom_requirements * 2
    )
    
    return score


# Ejemplos
ucr_score = calculate_complexity_score(
    num_stops=20,
    num_operators=1,
    update_frequency="yearly",
    custom_requirements=2
)
# Score: 2 + 5 + 1 + 4 = 12 → CLI suficiente 

national_score = calculate_complexity_score(
    num_stops=2000,
    num_operators=50,
    update_frequency="monthly",
    custom_requirements=7
)
# Score: 200 + 250 + 5 + 14 = 469 → Platform necesaria 
```

---

## Recomendaciones por Escenario

### Escenario: Solo UCR (actual)

**Solución:** Python package + CLI + Git + (opcional) Docker

```bash
# Opción 1: Instalación local
pip install bucr-rotulador
rotulador init  # Setup inicial, instala Myriad Pro
rotulador generate-all --input data/stops.csv
git add output/
git commit -m "Generated signs for semester 2025-1"

# Opción 2: Con Docker (recomendado para CI/CD)
docker run -v $(pwd)/data:/data -v $(pwd)/output:/output \
  bucr/rotulador generate-all --input /data/stops.csv
```

**Performance (20 paradas UCR):**
- Local: ~2-4 segundos total
- Docker: ~4-7 segundos (incluye startup)
- Output: SVG (primary) + PDF + PNG @ 300dpi

**Inversión:** ~40-46h desarrollo
**Mantenimiento:** ~2h/semestre  
**ROI:** Alto (vs diseño manual ~2h por rótulo = 40h ahorradas por generación)

**Stack técnico confirmado:**
- pycairo 1.29.0 (Cairo directo)
- Myriad Pro Bold (94KB .otf incluida)
- fontTools para metrics
- Docker image base: python:3.12-slim (~500MB final)

---

### Escenario: UCR + 3-5 Universidades

**Solución:** Config-driven + Git + Simple web preview

```yaml
# config.yaml
organizations:
  - name: UCR
    stops_file: data/ucr_stops.csv
  - name: UNA
    stops_file: data/una_stops.csv
```

```bash
rotulador batch-generate config.yaml
rotulador preview --serve  # HTTP server para preview
```

**Inversión:** ~60h desarrollo  
**Mantenimiento:** ~4h/mes  
**ROI:** Medio-alto

---

### Escenario: Sistema Nacional (MOPT coordinado)

**Solución:** Django platform + API + Admin panel

```python
# Django models
class Stop(models.Model):
    stop_id = models.CharField(primary_key=True)
    operator = models.ForeignKey(Operator)
    sign_config = models.JSONField()
    
class Sign(models.Model):
    stop = models.ForeignKey(Stop)
    version = models.IntegerField()
    svg_file = models.FileField()
    status = models.CharField(choices=STATUS_CHOICES)
    approved_by = models.ForeignKey(User, null=True)
```

**Inversión:** ~300h desarrollo + 80h deployment  
**Mantenimiento:** ~20h/mes  
**ROI:** Alto (escala nacional justifica inversión)

---

## Template Management System

### Versionamiento de Templates

```python
# rotulador/templates/versions.py
class TemplateVersion:
    """Maneja versiones de templates."""
    
    VERSIONS = {
        "1.0": {
            "stop_back": StopBackTemplateV1,
            "release_date": "2025-01-15",
            "changes": "Initial release"
        },
        "1.1": {
            "stop_back": StopBackTemplateV1_1,
            "release_date": "2025-06-01",
            "changes": "Adjusted font sizing algorithm"
        }
    }
    
    @classmethod
    def get_template(cls, type: str, version: str = "latest"):
        """Obtiene template específico."""
        if version == "latest":
            version = max(cls.VERSIONS.keys())
        
        return cls.VERSIONS[version][type]()


# Uso
sign = rotulador.create(
    "stop_back",
    "FING",
    template_version="1.0"  # Reproducir diseño antiguo
)
```

**Beneficio:** Permite regenerar diseños históricos exactos

---

### Template Registry Pattern

```python
# rotulador/templates/__init__.py
class TemplateRegistry:
    """Registry para templates custom."""
    
    _registry = {}
    
    @classmethod
    def register(cls, sign_type: str, template_class):
        """Registra template custom."""
        cls._registry[sign_type] = template_class
    
    @classmethod
    def get(cls, sign_type: str):
        """Obtiene template."""
        if sign_type not in cls._registry:
            raise ValueError(f"Unknown sign type: {sign_type}")
        return cls._registry[sign_type]()


# Operators pueden registrar customs
class UCRCustomStopBack(StopBackTemplate):
    """Template custom UCR con logo especial."""
    pass

TemplateRegistry.register("ucr_stop_back", UCRCustomStopBack)
```

**Beneficio:** Extensibilidad sin modificar código core

---

## Estrategia de Migración

### De Manual a Automatizado

**Paso 1:** Inventario actual
```bash
# Listar todos los rótulos existentes
ls docs/assets/logos/*.svg
# → Identificar patterns
```

**Paso 2:** Extraer especificaciones
```yaml
# specs/extracted_specs.yaml
fing:
  measured_width: 850mm
  measured_height: 300mm
  font_size: 72pt
  logo_diameter: 60mm
```

**Paso 3:** Generar con sistema nuevo
```bash
rotulador generate fing --match-specs specs/extracted_specs.yaml
```

**Paso 4:** Comparar visual
```bash
rotulador compare docs/assets/logos/fing.svg output/fing.svg
# → Show diff overlay
```

**Paso 5:** Iterar hasta match 100%

**Paso 6:** Deploy nuevo sistema

---

## Conclusión

### Para bUCR Hoy (UCR solamente)

**Usar Nivel 1-2:**
- Python package con CLI
- Templates básicos + variantes
- Git para version control
- Sin plataforma web

**Justificación:**
- 20 paradas no justifican plataforma
- Updates poco frecuentes
- Single operator

### Para Futuro Nacional

**Planificar para Nivel 4:**
- Arquitectura permite crecimiento
- Database schema defined
- API-first design
- Cuando llegue a 100+ paradas, escalar

### Sweet Spot

**Comenzar simple, arquitectura preparada para escalar.**

```python
# Hoy
rotulador generate --stop "FING"

# Futuro (mismo código interno)
api.post("/signs/generate", {"stop_id": "FING"})
```

---

**Próximo paso:** Compilar documento final de especificación con todas las recomendaciones.

**Actualizado:** 30 de diciembre de 2025
