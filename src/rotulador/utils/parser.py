"""
Parser para datos de rutas desde archivos Markdown.
"""

import re
from typing import List, Dict, Any
from datetime import time
from ..models import Route, Schedule, Stop, StopData

class RoutesParser:
    """
    Parser para extraer datos de rutas y horarios desde routes.md
    """
    
    def __init__(self, markdown_content: str):
        self.content = markdown_content
        self.routes: Dict[str, Route] = {}
        self.schedules: List[Schedule] = []
    
    def parse(self) -> Dict[str, Any]:
        """Parsea el contenido completo y retorna datos estructurados."""
        self._parse_routes()
        self._parse_schedules()
        return {
            'routes': list(self.routes.values()),
            'schedules': self.schedules
        }
    
    def _parse_routes(self):
        """Extrae información de rutas."""
        # L1
        if '### L1' in self.content:
            self.routes['L1'] = Route(
                id='L1',
                short_name='L1',
                long_name='Sin vuelta a la milla universitaria',
                color='#00C0F3',  # Celeste UCR
                text_color='#FFFFFF'
            )
        
        # L2
        if '### L2' in self.content:
            self.routes['L2'] = Route(
                id='L2',
                short_name='L2',
                long_name='Con vuelta a la milla universitaria',
                color='#6DC067',  # Verde UCR
                text_color='#FFFFFF'
            )
    
    def _parse_schedules(self):
        """Extrae horarios de las tablas."""
        # Buscar tablas con horarios
        table_pattern = r'\| Ruta \| Desde.*?\|(.*?)\|'
        tables = re.findall(table_pattern, self.content, re.DOTALL)
        
        for table in tables:
            lines = table.strip().split('\n')
            for line in lines:
                if '|' in line and 'Ruta' not in line and '---' not in line:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 3:
                        route_id = parts[0]
                        stop_name = parts[1]
                        time_str = parts[2]
                        
                        try:
                            # Parsear tiempo (formato H:MM)
                            hour, minute = map(int, time_str.split(':'))
                            arrival_time = time(hour, minute)
                            
                            schedule = Schedule(
                                route_id=route_id,
                                arrival_time=arrival_time,
                                headsign="Deportivas"  # Simplificado para MVP
                            )
                            self.schedules.append(schedule)
                        except ValueError:
                            continue  # Saltar líneas inválidas
    
    @classmethod
    def from_file(cls, filepath: str) -> 'RoutesParser':
        """Crea parser desde archivo."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return cls(content)
    
    def get_stop_data(self, stop_name: str) -> StopData:
        """Retorna StopData para una parada específica."""
        # Para MVP, crear stop dummy
        stop = Stop(
            id=stop_name.lower().replace(' ', '_'),
            name=stop_name,
            latitude=0.0,  # Dummy
            longitude=0.0   # Dummy
        )
        
        # Filtrar schedules para esta parada (simplificado)
        relevant_schedules = [s for s in self.schedules if stop_name in ['Educación', 'Artes Plásticas']]
        
        return StopData(
            stop=stop,
            routes=list(self.routes.values()),
            schedules=relevant_schedules
        )