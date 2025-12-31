from .core import Rotulo
from .types import SignType

__version__ = "0.1.0"

def create(type: str, **kwargs) -> Rotulo:
    """
    Helper function para crear un rótulo rápidamente.
    """
    rotulo = Rotulo()
    return rotulo.create(type, **kwargs)
