# Infobús

!!! note "¿Qué es *infobús*?"
    *Infobús* es el subsistema de información para las personas usuarias del servicio de buses. Incluye pantallas, sitios web y otros componentes para el uso de los datos del servicio.



```mermaid
flowchart TD
GRT(["`**GTFS** *Realtime*`"])
GS(["`**GTFS** *Schedule*`"])
DH(("`*infobús* **servidor**`"))
D{{Otras fuentes de datos}}
P["`*infobús* **pantallas**`"]
W["`*infobús* **web**`"]
A["`*infobús* **análisis**`"]
APP["`*infobús* **app**`"]
C["`*infobús* **comunicación**`"]

GRT & GS --> DH
D --> DH
DH -->|Infobús API| APP & P & A & W & C
```

## Infobús **servidor** concentrador de datos

Este es un componente central para recolección, procesamiento y distribución de datos a todos los canales de comunicación.

## Infobús **API**

Esta es la interfaz de comunicación con todos los servicios conectados dentro del subsistema. Permite la obtención de datos procesados para usar en la aplicación particular, por ejemplo, los datos de ubicación de los buses para mostrar en las pantallas.

## Infobús **pantallas**

Estas son pantallas con informatión en tiempo real del servicio para utilizar en paradas, estaciones o en los vehículos.

## Infobús **web**

Este es un sitio centralizado de referencia de información para las personas usuarias del servicio. Contiene datos básicos como: información de la agencia, horarios, mapas, paradas, tarifas, días de operación y otros.

## Infobús **comunicación**

Esta es una estrategia de comunicación con las personas usuarias del servicio, a través de distintos canales, como redes sociales, medios impresos u otros.

## Infobús **análisis** de datos

Una plataforma para el procesamiento y análisis de datos con técnicas avanzadas y para uso de distintos actores del sistema, además de las personas usuarias, como los operadores, gestores, planificadores, reguladores, investigadores, y otros servicios interconectados.

## Infobús **app** móvil

Esta es una aplicación móvil para desplegar información a las personas usuarias sobre el servicio. Actualmente no está en desarrollo.
