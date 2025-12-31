from abc import ABC, abstractmethod
from typing import Any

class Renderer(ABC):
    """
    Clase base abstracta para renderizadores.
    """
    
    @abstractmethod
    def setup(self, width: int, height: int):
        """Inicializa el canvas"""
        pass
        
    @abstractmethod
    def draw_circle(self, x: float, y: float, radius: float, color: tuple):
        """Dibuja un círculo"""
        pass
        
    @abstractmethod
    def draw_text(self, text: str, x: float, y: float, font_size: float, 
                  color: tuple, font_family: str = "Myriad Pro", align: str = "left"):
        """Dibuja texto"""
        pass
        
    @abstractmethod
    def save(self, filename: str):
        """Guarda el resultado en un archivo"""
        pass
