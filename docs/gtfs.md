# Diseño para datos GTFS

[GTFS](https://gtfs.org/) es un [estándar abierto](https://www.interoperablemobility.org/definitions/#open_standard) de datos de transporte público.

Tiene dos componentes esenciales:

- **Schedule** (o "estático"): define nombre del operador, de las rutas, trayectorias, paradas, horarios, tarifas y más.
- **Realtime**: ofrece actualizaciones en tiempo real sobre la ubicación y ocupación del bus, tiempos de llegada a las paradas, alertas del servicio y otras informaciones.

GTFS permite la distribución de la información del servicio en múltiples aplicaciones y plataformas, como Google Maps, Moovit y aplicaciones propias y de terceros. Esta variedad de aplicaciones es conveniente para las personas usuarias, al mismo tiempo que es información consistente y actualizada.

La referencia GTFS para este sistema está disponible en [Google Spreadsheets](https://docs.google.com/spreadsheets/d/15WBqeay9u9hWd-gwjlxifsYTuaXfw5KspKKyxtZZsvw/edit?usp=sharing).

En relación con los nombres e identidad visual del servicio, es necesario configurar lo siguiente.

## Nombre de rutas

Los nombres elegidos para las dos rutas en el servicio son:

- `route_short_name`: *b***UCR** L1
- `route_short_name`: *b***UCR** L2
 
## Colores de rutas

En GTFS aplica la siguiente especificación de colores para las rutas:

| `route_id` | ... | `route_color` | `route_text_color` |
| ---------- | --- | ------------- | ------------------ |
| bUCR_L1    | ... | 008641        | FFFFFF             |
| bUCR_L2    | ... | F37021        | FFFFFF             |

!!! note "Sobre elementos de marca en GTFS"
    Estas son las únicas consideraciones de diseño de la marca dentro de GTFS. El nombre corto y los colores serán desplegados por aplicaciones como Google Maps y Moovit al mostrar los resultados en sus búsquedas y mapas.
