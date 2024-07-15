# Databús

!!! note "¿Qué es *Databús*?"
    *Databús* es el subsistema de recolección, creación y distribución de **datos** del servicio de transporte público, tanto la información "estática" de rutas, horarios, mapas y otros, como alertas y la información en tiempo real de los vehículos. 

    El conjunto de tecnologías e interfaces desarrollado permite la operación autónoma pero también en conjunto con otros proveedores y tecnologías, cumpliendo con su objetivo de interoperabilidad. *Databús* utiliza varios estándares, pero principalmente GTFS.

*Databús* tiene varios componentes, cuya relación está indicada en el siguiente esquema.

```mermaid
flowchart TD
A>Agencia]
TM{{Otros equipos de <br> telemetría y rastreo}}
APP["`*databús* **app**`"]
GTFS["`*databús* **editor**`"]
RT(("`*databús* **servidor**`"))
GRT(["`**GTFS** *Realtime*`"])
GS(["`**GTFS** *Schedule*`"])

APP -->|databús API| RT
TM --> |databús API| RT
RT --> GRT
A --> GTFS
GTFS --> RT
GTFS --> GS
```

## Componentes

Los detalles de cada componente son los siguientes.

### :material-table-cog: Databús **editor** GTFS

Este es un editor web para crear suministros (*feeds*) de datos **GTFS** *Schedule*, los cuales distribuyen la información del servicio de transporte público a todas las aplicaciones de asistencia para las personas usuarias, como las aplicaciones de planificación de viajes multimodales (por ejemplo, Google Maps o Moovit) y otros medios de difusión y análisis, como sitios web, pantallas, medios impresos, y otros.

### :material-api: Databús **API**

Esta es la interfaz que permite conectar a los equipos de telemetría y rastreo en los vehículos con el servidor en tiempo real. Es una interfaz universal que no condiciona cuáles equipos pueden enviar esta información. Está diseñado para contener una amplia variedad de tipos de datos relativos, por ejemplo, a la operación del vehículo y que es de interés para el operador del sistema, sin embargo, es posible utilizar solamente un subconjunto para construir el **GTFS** *Realtime* de los servicios de información para personas usuarias.

### :material-server: Databús **servidor** en tiempo real

Este es un servidor que recolecta, procesa y construye el suministro **GTFS** *Realtime*, que es el complemento a **GTFS** *Schedule* para el uso del servicio.

### :material-cellphone-cog: Databús **app** móvil operativa

Esta es una solución alternativa de bajo costo para un equipo de telemetría y rastreo con funcionalidad limitada, capaz de proveer los datos mínimos de **GTFS** *Realtime* y ofrecer información a las personas usuarias, aunque no tanto así a los operadores del servicio. Es utilizado por el conductor del vehículo.

## Identidad visual

Esta es la propuesta para identificar cada componente:

<div class="grid cards" markdown>

- <img src="../assets/png/databus_editor.png" width="125px" />

- <img src="../assets/png/databus_servidor.png" width="125px" />

- <img src="../assets/png/databus_app.png" width="125px" />

- <img src="../assets/png/databus_api.png" width="125px" />

</div>

**Características**

- Utiliza la tipografía Myriad Pro
- Utiliza el color Verde UCR
