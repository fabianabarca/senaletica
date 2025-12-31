from abc import ABC, abstractmethod
from ..renderers.base import Renderer

class SignTemplate(ABC):
    """
    Clase base para plantillas de rótulos.
    """
    
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        
    @abstractmethod
    def render(self, **kwargs):
        """Renderiza el rótulo con los datos proporcionados"""
        pass
