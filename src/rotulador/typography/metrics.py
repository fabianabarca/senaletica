"""
Utilidades para medición de texto.
"""
import cairo

class TextMetrics:
    """
    Wrapper para cairo.TextExtents con utilidades adicionales.
    """
    
    def __init__(self, ctx: cairo.Context, text: str):
        self.extents = ctx.text_extents(text)
        self.width = self.extents.width
        self.height = self.extents.height
        self.x_bearing = self.extents.x_bearing
        self.y_bearing = self.extents.y_bearing
        self.x_advance = self.extents.x_advance
        self.y_advance = self.extents.y_advance
        
    @property
    def center_offset_x(self) -> float:
        """Offset X para centrar el texto"""
        return -(self.width / 2 + self.x_bearing)
        
    @property
    def center_offset_y(self) -> float:
        """Offset Y para centrar el texto"""
        return -(self.height / 2 + self.y_bearing)
