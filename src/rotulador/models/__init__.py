"""
Modelos de datos para el sistema de rotulación.
"""

from typing import List, Optional
from dataclasses import dataclass
from datetime import time

@dataclass
class Stop:
    """Representa una parada de bus."""
    id: str
    name: str
    latitude: float
    longitude: float
    
@dataclass
class Route:
    """Representa una ruta de bus."""
    id: str
    short_name: str  # e.g., "L1", "L2"
    long_name: str
    color: str  # Hex color
    text_color: str  # Hex color for text
    
@dataclass
class Schedule:
    """Representa un horario de llegada."""
    route_id: str
    arrival_time: time
    headsign: str  # Destination
    
@dataclass
class StopData:
    """Datos completos de una parada para generar rótulos."""
    stop: Stop
    routes: List[Route]
    schedules: List[Schedule]
    
    def get_upcoming_schedules(self, limit: int = 5) -> List[Schedule]:
        """Retorna los próximos horarios ordenados por tiempo."""
        # Para MVP, solo ordenar por arrival_time
        return sorted(self.schedules, key=lambda s: s.arrival_time)[:limit]