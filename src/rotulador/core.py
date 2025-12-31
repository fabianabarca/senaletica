from typing import Optional
from .types import SignType
from .renderers.cairo import CairoRenderer
from .templates.stop_back import StopBackTemplate

class Rotulo:
    """
    Clase principal para la generación de rótulos.
    """
    
    def __init__(self):
        self.renderer = CairoRenderer()
        self._current_sign = None
        
    def create(self, type: str | SignType, **kwargs) -> 'Rotulo':
        """
        Genera un rótulo en memoria.
        
        Args:
            type: Tipo de rótulo ("stop_back", etc)
            **kwargs: Argumentos específicos del template (ej: stop_name)
        """
        if isinstance(type, str):
            try:
                sign_type = SignType(type)
            except ValueError:
                raise ValueError(f"Tipo de rótulo inválido: {type}")
        else:
            sign_type = type
            
        if sign_type == SignType.STOP_BACK:
            template = StopBackTemplate(self.renderer)
            template.render(**kwargs)
        else:
            raise NotImplementedError(f"El tipo {sign_type} no está implementado aún.")
            
        return self
        
    def export(self, filename: str):
        """
        Guarda el rótulo generado en un archivo.
        """
        self.renderer.save(filename)
